from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCANNER = ROOT / "scripts" / "audit_publication_privacy.py"


class PublicationPrivacyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp.name)
        self._git("init", "-b", "main")
        self._git("config", "user.name", "PublicAlias")
        self._git("config", "user.email", "1+PublicAlias@users.noreply.github.com")
        policy_dir = self.repo / "governance"
        policy_dir.mkdir()
        policy = {
            "format_version": 1,
            "approved_git_identities": [
                {
                    "name": "PublicAlias",
                    "email_regex": r"^[0-9]+\+PublicAlias@users\.noreply\.github\.com$",
                    "reason": "Synthetic public test identity",
                }
            ],
            "approved_binary_blobs": [],
        }
        (policy_dir / "publication-privacy-policy.json").write_text(
            json.dumps(policy, indent=2) + "\n",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _git(self, *args: str) -> subprocess.CompletedProcess[str]:
        completed = subprocess.run(
            ["git", *args],
            cwd=self.repo,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )
        if completed.returncode != 0:
            self.fail(completed.stderr or completed.stdout)
        return completed

    def _commit(self, message: str) -> None:
        self._git("add", "-A")
        self._git("commit", "-m", message)

    def _scan(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-X", "utf8", str(SCANNER), "--root", str(self.repo), *args],
            cwd=self.repo,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )

    def test_safe_repository_passes_current_and_history_scans(self) -> None:
        (self.repo / "README.md").write_text("# Public example\n", encoding="utf-8")
        self._commit("docs: add public example")

        current = self._scan()
        history = self._scan("--history")

        self.assertEqual(0, current.returncode, current.stdout + current.stderr)
        self.assertIn("PASS        publication-privacy-current", current.stdout)
        self.assertIn("SKIP        publication-privacy-history", current.stdout)
        self.assertEqual(0, history.returncode, history.stdout + history.stderr)
        self.assertIn("PASS        publication-privacy-history", history.stdout)

    def test_current_scan_redacts_a_sensitive_local_path(self) -> None:
        private_segment = "private" + "-owner"
        local_path = "G" + ":/" + private_segment + "/work/repository"
        (self.repo / "note.txt").write_text(f"workspace: {local_path}\n", encoding="utf-8")
        self._git("add", "note.txt")

        completed = self._scan()

        self.assertEqual(1, completed.returncode)
        self.assertIn("absolute-windows-path", completed.stdout)
        self.assertIn("note.txt", completed.stdout)
        self.assertNotIn(private_segment, completed.stdout)
        self.assertNotIn(local_path, completed.stdout)

    def test_current_scan_redacts_a_sensitive_repository_path(self) -> None:
        private_mail = "person" + "@" + "personalmail.ca"
        private_directory = self.repo / private_mail
        private_directory.mkdir()
        note = private_directory / "note.txt"
        note.write_text("public-looking content\n", encoding="utf-8")

        completed = self._scan()

        self.assertEqual(1, completed.returncode)
        self.assertIn("unapproved-email-address", completed.stdout)
        self.assertIn("path-sha256:", completed.stdout)
        self.assertNotIn(private_mail, completed.stdout)

    def test_history_scan_finds_removed_sensitive_content(self) -> None:
        private_segment = "private" + "-owner"
        old_path = "G" + ":/" + private_segment + "/work/repository"
        note = self.repo / "note.txt"
        note.write_text(f"workspace: {old_path}\n", encoding="utf-8")
        self._commit("docs: add local note")
        note.write_text("workspace: repository root\n", encoding="utf-8")
        self._commit("docs: remove local path")

        current = self._scan()
        history = self._scan("--history")

        self.assertEqual(0, current.returncode, current.stdout + current.stderr)
        self.assertEqual(1, history.returncode)
        self.assertIn("history-content", history.stdout)
        self.assertIn("absolute-windows-path", history.stdout)
        self.assertNotIn(private_segment, history.stdout)
        self.assertNotIn(old_path, history.stdout)

    def test_history_scan_redacts_an_unapproved_git_identity(self) -> None:
        private_mail = "person" + "@" + "personalmail.ca"
        self._git("config", "user.email", private_mail)
        (self.repo / "README.md").write_text("# Public example\n", encoding="utf-8")
        self._commit("docs: add example")

        completed = self._scan("--history")

        self.assertEqual(1, completed.returncode)
        self.assertIn("unapproved-author-identity", completed.stdout)
        self.assertIn("unapproved-committer-identity", completed.stdout)
        self.assertNotIn(private_mail, completed.stdout)

    def test_unreviewed_binary_blob_fails(self) -> None:
        binary = b"synthetic\x00metadata"
        self.assertEqual(64, len(hashlib.sha256(binary).hexdigest()))
        (self.repo / "asset.bin").write_bytes(binary)
        self._git("add", "asset.bin")

        completed = self._scan()

        self.assertEqual(1, completed.returncode)
        self.assertIn("unreviewed-binary-metadata", completed.stdout)
        self.assertIn("asset.bin", completed.stdout)


if __name__ == "__main__":
    unittest.main()
