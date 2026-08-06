#!/usr/bin/env python3
"""Audit the Git publication surface without echoing matched private values."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


DEFAULT_POLICY = Path("governance/publication-privacy-policy.json")
MAX_REPORTED_FINDINGS = 100


@dataclass(frozen=True, order=True)
class Finding:
    scope: str
    category: str
    location: str


@dataclass(frozen=True)
class IdentityRule:
    name: str
    email_pattern: re.Pattern[str]


@dataclass(frozen=True)
class Policy:
    identities: tuple[IdentityRule, ...]
    approved_binary_sha256: frozenset[str]


TEXT_PATTERNS = (
    (
        "absolute-windows-path",
        re.compile(r"(?<![A-Za-z0-9])[A-Za-z]:[\\/](?![\\/])"),
    ),
    (
        "personal-posix-home-path",
        re.compile(r"(?<![A-Za-z0-9])/(?:home|Users)/[^/\s]+(?:/|\b)"),
    ),
    (
        "wsl-mounted-drive-path",
        re.compile(r"(?<![A-Za-z0-9])/mnt/[a-z]/", re.IGNORECASE),
    ),
    (
        "unc-or-device-path",
        re.compile(r"\\\\(?:\?\\)?[A-Za-z0-9._$-]+\\[A-Za-z0-9._$-]+"),
    ),
    (
        "private-ipv4-address",
        re.compile(
            r"(?<!\d)(?:"
            r"10(?:\.\d{1,3}){3}|"
            r"192\.168(?:\.\d{1,3}){2}|"
            r"172\.(?:1[6-9]|2\d|3[01])(?:\.\d{1,3}){2}"
            r")(?!\d)"
        ),
    ),
    (
        "mac-address",
        re.compile(r"(?<![0-9A-F])(?:[0-9A-F]{2}[:-]){5}[0-9A-F]{2}(?![0-9A-F])", re.IGNORECASE),
    ),
    (
        "windows-user-sid",
        re.compile(r"\bS-1-5-21-(?:\d+-){2}\d+\b", re.IGNORECASE),
    ),
    (
        "machine-or-volume-identifier",
        re.compile(
            r"(?:MachineGuid\s*[:=]|Volume\{[0-9A-F-]{32,}\}|PhysicalDrive\d+)",
            re.IGNORECASE,
        ),
    ),
    (
        "local-codex-artifact-path",
        re.compile(r"\.codex[\\/](?:attachments|sessions|worktrees|memories|visualizations)[\\/]", re.IGNORECASE),
    ),
    (
        "phone-number",
        re.compile(r"(?<!\d)(?:\+?\d{1,3}[ .-]?)?\(?\d{3}\)?[ .-]\d{3}[ .-]\d{4}(?!\d)"),
    ),
    (
        "github-token",
        re.compile(r"\bgh[opurs]_[A-Za-z0-9_]{16,}"),
    ),
    (
        "openai-token",
        re.compile(r"\bsk-[A-Za-z0-9_-]{16,}"),
    ),
    (
        "aws-access-key",
        re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    ),
    (
        "private-key-material",
        re.compile(r"BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY"),
    ),
)

EMAIL_PATTERN = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
RESERVED_EMAIL_DOMAINS = {"example.com", "example.net", "example.org"}
RESERVED_EMAIL_SUFFIXES = (".example", ".invalid", ".test")


def run_git(root: Path, *args: str, input_data: bytes | None = None) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", *args],
        cwd=root,
        input=input_data,
        capture_output=True,
        check=False,
    )


def read_blob_data(root: Path, object_ids: set[str]) -> dict[str, bytes]:
    if not object_ids:
        return {}
    ordered_ids = sorted(object_ids)
    payload = ("\n".join(ordered_ids) + "\n").encode("ascii")
    completed = run_git(root, "cat-file", "--batch", input_data=payload)
    if completed.returncode != 0:
        raise RuntimeError("git cat-file --batch failed")

    output = completed.stdout
    offset = 0
    blobs: dict[str, bytes] = {}
    for requested_id in ordered_ids:
        header_end = output.find(b"\n", offset)
        if header_end < 0:
            raise RuntimeError("unexpected Git batch output")
        header = output[offset:header_end].decode("ascii")
        parts = header.split(" ")
        if len(parts) != 3 or parts[1] != "blob":
            raise RuntimeError("publication candidate is not a Git blob")
        returned_id, _, raw_size = parts
        try:
            size = int(raw_size)
        except ValueError as error:
            raise RuntimeError("unexpected Git blob size") from error
        data_start = header_end + 1
        data_end = data_start + size
        if data_end >= len(output) or output[data_end : data_end + 1] != b"\n":
            raise RuntimeError("truncated Git batch output")
        blobs[requested_id] = output[data_start:data_end]
        if returned_id != requested_id:
            blobs[returned_id] = blobs[requested_id]
        offset = data_end + 1
    return blobs


def load_policy(path: Path) -> Policy:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if raw.get("format_version") != 1:
        raise ValueError("publication privacy policy format_version must be 1")

    identities: list[IdentityRule] = []
    for item in raw.get("approved_git_identities", []):
        name = item.get("name")
        email_regex = item.get("email_regex")
        if not isinstance(name, str) or not name or not isinstance(email_regex, str) or not email_regex:
            raise ValueError("each approved Git identity requires name and email_regex")
        identities.append(IdentityRule(name=name, email_pattern=re.compile(email_regex, re.IGNORECASE)))

    approved_binary: set[str] = set()
    for item in raw.get("approved_binary_blobs", []):
        digest = item.get("sha256") if isinstance(item, dict) else None
        reason = item.get("reason") if isinstance(item, dict) else None
        if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-fA-F]{64}", digest):
            raise ValueError("each approved binary blob requires a SHA-256 digest")
        if not isinstance(reason, str) or not reason.strip():
            raise ValueError("each approved binary blob requires a review reason")
        approved_binary.add(digest.lower())

    if not identities:
        raise ValueError("at least one approved public Git identity is required")
    return Policy(tuple(identities), frozenset(approved_binary))


def approved_identity(policy: Policy, name: str, email: str) -> bool:
    return any(rule.name == name and rule.email_pattern.fullmatch(email) for rule in policy.identities)


def approved_content_email(policy: Policy, email: str) -> bool:
    domain = email.rsplit("@", 1)[-1].lower()
    if (
        domain in RESERVED_EMAIL_DOMAINS
        or domain == "localhost"
        or domain.endswith(RESERVED_EMAIL_SUFFIXES)
        or domain == "users.noreply.github.com"
    ):
        return True
    return any(rule.email_pattern.fullmatch(email) for rule in policy.identities)


def looks_binary(data: bytes) -> bool:
    if b"\x00" in data[:8192]:
        return True
    try:
        data.decode("utf-8")
    except UnicodeDecodeError:
        return True
    return False


def scan_text(text: str, scope: str, location: str, policy: Policy) -> set[Finding]:
    findings: set[Finding] = set()
    for line_number, line in enumerate(text.splitlines(), start=1):
        line_location = f"{location}:{line_number}"
        for category, pattern in TEXT_PATTERNS:
            if pattern.search(line):
                findings.add(Finding(scope, category, line_location))
        for match in EMAIL_PATTERN.finditer(line):
            if not approved_content_email(policy, match.group(0)):
                findings.add(Finding(scope, "unapproved-email-address", line_location))
    return findings


def safe_path_label(relative: str, policy: Policy) -> str:
    path_findings = scan_text(relative, "path", "<redacted-path>", policy)
    has_control_character = any(ord(character) < 32 or ord(character) == 127 for character in relative)
    if path_findings or has_control_character:
        digest = hashlib.sha256(relative.encode("utf-8", errors="surrogateescape")).hexdigest()[:12]
        return f"path-sha256:{digest}"
    return relative


def scan_path(relative: str, scope: str, policy: Policy) -> tuple[set[Finding], str]:
    safe_label = safe_path_label(relative, policy)
    findings = {
        Finding(scope, finding.category, safe_label)
        for finding in scan_text(relative, scope, safe_label, policy)
    }
    return findings, safe_label


def scan_bytes(data: bytes, scope: str, location: str, policy: Policy) -> set[Finding]:
    if looks_binary(data):
        digest = hashlib.sha256(data).hexdigest()
        if digest not in policy.approved_binary_sha256:
            return {Finding(scope, "unreviewed-binary-metadata", location)}
        return set()
    return scan_text(data.decode("utf-8"), scope, location, policy)


def publication_candidate_paths(root: Path) -> tuple[list[str], dict[str, str]]:
    tracked = run_git(root, "ls-files", "--stage", "-z")
    untracked = run_git(root, "ls-files", "--others", "--exclude-standard", "-z")
    if tracked.returncode != 0 or untracked.returncode != 0:
        raise RuntimeError("git ls-files failed")
    tracked_paths: dict[str, str] = {}
    for item in tracked.stdout.split(b"\0"):
        if not item:
            continue
        metadata, separator, raw_path = item.partition(b"\t")
        metadata_parts = metadata.split(b" ")
        if not separator or len(metadata_parts) != 3 or metadata_parts[2] != b"0":
            raise RuntimeError("Git index has an unresolved or unexpected entry")
        relative = raw_path.decode("utf-8", errors="surrogateescape")
        tracked_paths[relative] = metadata_parts[1].decode("ascii")
    untracked_paths = {
        item.decode("utf-8", errors="surrogateescape")
        for item in untracked.stdout.split(b"\0")
        if item
    }
    return sorted(set(tracked_paths) | untracked_paths), tracked_paths


def scan_current_surface(root: Path, policy: Policy) -> tuple[set[Finding], int]:
    findings: set[Finding] = set()
    paths, tracked = publication_candidate_paths(root)
    index_blobs = read_blob_data(root, set(tracked.values()))
    for relative in paths:
        path_scope = "index-path" if relative in tracked else "untracked-path"
        path_findings, safe_relative = scan_path(relative, path_scope, policy)
        findings.update(path_findings)

        staged_data = index_blobs.get(tracked[relative]) if relative in tracked else None
        if staged_data is not None:
            findings.update(scan_bytes(staged_data, "index-content", safe_relative, policy))

        working_path = root / relative
        if working_path.is_file():
            working_data = working_path.read_bytes()
            if staged_data is None or working_data != staged_data:
                content_scope = "working-tree-content" if relative in tracked else "untracked-content"
                findings.update(scan_bytes(working_data, content_scope, safe_relative, policy))
    return findings, len(paths)


def commit_ids(root: Path) -> list[str]:
    completed = run_git(root, "rev-list", "--all")
    if completed.returncode != 0:
        raise RuntimeError("git rev-list failed")
    return [line for line in completed.stdout.decode("ascii").splitlines() if line]


def scan_commit_metadata(root: Path, commits: list[str], policy: Policy) -> set[Finding]:
    findings: set[Finding] = set()
    for commit in commits:
        completed = run_git(root, "show", "-s", "--format=%an%x00%ae%x00%cn%x00%ce%x00%B", commit)
        if completed.returncode != 0:
            raise RuntimeError("git show failed for commit metadata")
        parts = completed.stdout.decode("utf-8", errors="replace").split("\0", 4)
        if len(parts) != 5:
            raise RuntimeError("unexpected Git metadata format")
        author_name, author_email, committer_name, committer_email, message = parts
        short = commit[:12]
        if not approved_identity(policy, author_name, author_email):
            findings.add(Finding("git-metadata", "unapproved-author-identity", f"commit:{short}:author"))
        if not approved_identity(policy, committer_name, committer_email):
            findings.add(Finding("git-metadata", "unapproved-committer-identity", f"commit:{short}:committer"))
        findings.update(scan_text(message, "git-message", f"commit:{short}:message", policy))
    return findings


def history_objects(root: Path) -> dict[str, str]:
    completed = run_git(root, "rev-list", "--objects", "--all")
    if completed.returncode != 0:
        raise RuntimeError("git rev-list --objects failed")
    objects: dict[str, str] = {}
    for line in completed.stdout.decode("utf-8", errors="surrogateescape").splitlines():
        object_id, separator, relative = line.partition(" ")
        objects.setdefault(object_id, relative if separator else "<unmapped>")
    return objects


def blob_ids(root: Path, objects: dict[str, str]) -> list[str]:
    if not objects:
        return []
    payload = ("\n".join(objects) + "\n").encode("ascii")
    completed = run_git(root, "cat-file", "--batch-check=%(objectname) %(objecttype)", input_data=payload)
    if completed.returncode != 0:
        raise RuntimeError("git cat-file --batch-check failed")
    blobs: list[str] = []
    for line in completed.stdout.decode("ascii").splitlines():
        object_id, object_type = line.split(" ", 1)
        if object_type == "blob":
            blobs.append(object_id)
    return blobs


def scan_history(root: Path, policy: Policy) -> tuple[set[Finding], int, int]:
    commits = commit_ids(root)
    findings = scan_commit_metadata(root, commits, policy)
    objects = history_objects(root)
    blobs = blob_ids(root, objects)
    blob_data = read_blob_data(root, set(blobs))
    for object_id in blobs:
        relative = objects.get(object_id, "<unmapped>")
        short = object_id[:12]
        path_findings, safe_relative = scan_path(relative, "history-path", policy)
        findings.update(
            Finding(finding.scope, finding.category, f"blob:{short}:{finding.location}")
            for finding in path_findings
        )
        findings.update(
            scan_bytes(blob_data[object_id], "history-content", f"blob:{short}:{safe_relative}", policy)
        )
    return findings, len(commits), len(blobs)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--policy", type=Path, default=DEFAULT_POLICY)
    parser.add_argument(
        "--history",
        action="store_true",
        help="scan all reachable commits and blobs; required before the first public push",
    )
    args = parser.parse_args()

    root = args.root.resolve()
    policy_path = args.policy if args.policy.is_absolute() else root / args.policy
    inside = run_git(root, "rev-parse", "--is-inside-work-tree")
    if inside.returncode != 0 or inside.stdout.strip() != b"true":
        print("UNAVAILABLE publication-privacy: target is not a Git worktree")
        return 2

    try:
        policy = load_policy(policy_path)
        findings, tracked_count = scan_current_surface(root, policy)
        commit_count = 0
        blob_count = 0
        if args.history:
            history_findings, commit_count, blob_count = scan_history(root, policy)
            findings.update(history_findings)
    except (OSError, ValueError, json.JSONDecodeError, re.error, RuntimeError) as error:
        print(f"UNAVAILABLE publication-privacy: {error.__class__.__name__}")
        return 2

    if findings:
        ordered = sorted(findings)
        print(f"FAIL        publication-privacy: {len(ordered)} finding(s); matched values are redacted")
        for finding in ordered[:MAX_REPORTED_FINDINGS]:
            print(f"FINDING     {finding.scope} {finding.category} {finding.location}")
        if len(ordered) > MAX_REPORTED_FINDINGS:
            print(f"FINDING     {len(ordered) - MAX_REPORTED_FINDINGS} additional finding(s) omitted")
        return 1

    print(f"PASS        publication-privacy-current: {tracked_count} tracked or untracked candidate paths scanned")
    if args.history:
        print(f"PASS        publication-privacy-history: {commit_count} commits and {blob_count} unique blobs scanned")
    else:
        print("SKIP        publication-privacy-history: run with --history before the first public push")
    print("LIMIT       contextual identity and approved binary metadata still require human review")
    return 0


if __name__ == "__main__":
    sys.exit(main())
