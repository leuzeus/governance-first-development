from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

from scripts.validate_repository import check_skill_manifest_for

ROOT = Path(__file__).resolve().parents[1]
SKILLS = (
    ROOT / "skills" / "audit-project-governance",
    ROOT / "skills" / "audit-session-progress",
)
PACKAGE_TOOL = ROOT / "tools" / "package_skill.py"
SYNC_TOOL = ROOT / "tools" / "sync_skill.py"


class SkillDistributionTests(unittest.TestCase):
    def test_package_is_deterministic_and_contains_only_manifest_files(self) -> None:
        for skill in SKILLS:
            with self.subTest(skill=skill.name), tempfile.TemporaryDirectory() as directory:
                manifest = json.loads((skill / "PACKAGE_MANIFEST.json").read_text(encoding="utf-8"))
                first, second = Path(directory) / "first.zip", Path(directory) / "second.zip"
                for output in (first, second):
                    completed = subprocess.run(
                        [sys.executable, "-X", "utf8", str(PACKAGE_TOOL), "--skill-dir", str(skill), "--output", str(output)],
                        cwd=ROOT, check=False, capture_output=True, text=True, encoding="utf-8",
                    )
                    self.assertEqual(0, completed.returncode, completed.stderr)
                self.assertEqual(first.read_bytes(), second.read_bytes())
                expected = [f"{manifest['archive_root']}/{name}" for name in manifest["files"]]
                with zipfile.ZipFile(first) as archive:
                    self.assertEqual(expected, archive.namelist())
                    for name in manifest["files"]:
                        self.assertEqual((skill / name).read_bytes(), archive.read(f"{manifest['archive_root']}/{name}"))

    def test_sync_is_dry_run_by_default_and_requires_exact_approval(self) -> None:
        for skill in SKILLS:
            with self.subTest(skill=skill.name), tempfile.TemporaryDirectory() as directory:
                manifest = json.loads((skill / "PACKAGE_MANIFEST.json").read_text(encoding="utf-8"))
                target = Path(directory) / "target"
                target.mkdir()
                marker = target / "SKILL.md"
                marker.write_text("old\n", encoding="utf-8")
                unrelated = target / "local-customization.txt"
                unrelated.write_bytes(b"preserve me\n")
                command = [sys.executable, "-X", "utf8", str(SYNC_TOOL), "--source", str(skill), "--target", str(target)]
                for suffix, expected_code in [([], 1), (["--apply"], 2), (["--apply", "--approve", "wrong approval"], 2)]:
                    completed = subprocess.run(command + suffix, cwd=ROOT, check=False, capture_output=True, text=True, encoding="utf-8")
                    self.assertEqual(expected_code, completed.returncode, completed.stderr)
                    self.assertEqual("old\n", marker.read_text(encoding="utf-8"))
                    self.assertEqual(["SKILL.md", "local-customization.txt"], sorted(path.name for path in target.iterdir()))
                approval = f"sync {manifest['name']} {manifest['version']}"
                applied = subprocess.run(command + ["--apply", "--approve", approval], cwd=ROOT, check=False, capture_output=True, text=True, encoding="utf-8")
                self.assertEqual(0, applied.returncode, applied.stderr)
                for relative in manifest["files"]:
                    self.assertEqual((skill / relative).read_bytes(), (target / relative).read_bytes())
                self.assertEqual(b"preserve me\n", unrelated.read_bytes())

    def test_manifest_version_mismatch_is_rejected_for_each_skill(self) -> None:
        for skill in SKILLS:
            with self.subTest(skill=skill.name), tempfile.TemporaryDirectory() as directory:
                copied = Path(directory) / skill.name
                shutil.copytree(skill, copied)
                (copied / "VERSION").write_text("mismatched-version\n", encoding="utf-8")
                result = check_skill_manifest_for(copied)
                self.assertEqual("FAIL", result.status)
                self.assertIn("manifest and VERSION disagree", result.detail)

    def test_required_runtime_reference_cannot_be_omitted_from_manifest(self) -> None:
        required = {"audit-project-governance": "references/attempt-outcome-integrity.md", "audit-session-progress": "references/diagnostic.md"}
        for skill in SKILLS:
            with self.subTest(skill=skill.name), tempfile.TemporaryDirectory() as directory:
                copied = Path(directory) / skill.name
                shutil.copytree(skill, copied)
                path = copied / "PACKAGE_MANIFEST.json"
                manifest = json.loads(path.read_text(encoding="utf-8"))
                manifest["files"].remove(required[skill.name])
                path.write_text(json.dumps(manifest), encoding="utf-8")
                result = check_skill_manifest_for(copied)
                self.assertEqual("FAIL", result.status)
                self.assertIn("required runtime or provenance file absent", result.detail)


if __name__ == "__main__":
    unittest.main()
