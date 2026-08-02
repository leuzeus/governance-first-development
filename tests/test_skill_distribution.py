from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "audit-project-governance"
PACKAGE_TOOL = ROOT / "tools" / "package_skill.py"
SYNC_TOOL = ROOT / "tools" / "sync_skill.py"


class SkillDistributionTests(unittest.TestCase):
    @classmethod
    def _manifest(cls) -> dict:
        return json.loads((SKILL / "PACKAGE_MANIFEST.json").read_text(encoding="utf-8"))

    def test_package_is_deterministic_and_contains_only_manifest_files(self) -> None:
        manifest = self._manifest()
        with tempfile.TemporaryDirectory() as directory:
            first = Path(directory) / "first.zip"
            second = Path(directory) / "second.zip"
            for output in (first, second):
                completed = subprocess.run(
                    [sys.executable, "-X", "utf8", str(PACKAGE_TOOL), "--output", str(output)],
                    cwd=ROOT,
                    check=False,
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                )
                self.assertEqual(0, completed.returncode, completed.stderr)
            self.assertEqual(first.read_bytes(), second.read_bytes())
            expected = [f"{manifest['archive_root']}/{name}" for name in manifest["files"]]
            with zipfile.ZipFile(first) as archive:
                self.assertEqual(expected, archive.namelist())

    def test_sync_is_dry_run_by_default_and_requires_exact_approval(self) -> None:
        manifest = self._manifest()
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "target"
            target.mkdir()
            marker = target / "SKILL.md"
            marker.write_text("old\n", encoding="utf-8")
            command = [
                sys.executable,
                "-X",
                "utf8",
                str(SYNC_TOOL),
                "--target",
                str(target),
            ]
            dry_run = subprocess.run(command, cwd=ROOT, check=False, capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(1, dry_run.returncode)
            self.assertEqual("old\n", marker.read_text(encoding="utf-8"))
            rejected = subprocess.run(command + ["--apply"], cwd=ROOT, check=False, capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(2, rejected.returncode)
            self.assertEqual("old\n", marker.read_text(encoding="utf-8"))
            approval = f"sync {manifest['name']} {manifest['version']}"
            applied = subprocess.run(
                command + ["--apply", "--approve", approval],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertEqual(0, applied.returncode, applied.stderr)
            for relative in manifest["files"]:
                self.assertEqual((SKILL / relative).read_bytes(), (target / relative).read_bytes())


if __name__ == "__main__":
    unittest.main()
