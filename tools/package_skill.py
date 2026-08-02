#!/usr/bin/env python3
"""Create a deterministic, self-describing skill archive."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import zipfile
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SKILL = ROOT / "skills" / "audit-project-governance"
FIXED_TIMESTAMP = (1980, 1, 1, 0, 0, 0)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def load_manifest(skill_dir: Path) -> dict:
    path = skill_dir / "PACKAGE_MANIFEST.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    required = {"format_version", "name", "version", "archive_root", "files"}
    missing = required - manifest.keys()
    if missing:
        raise ValueError(f"manifest missing: {', '.join(sorted(missing))}")
    if manifest["format_version"] != 1:
        raise ValueError("unsupported package manifest format")
    files = manifest["files"]
    if not isinstance(files, list) or not files or files != sorted(set(files)):
        raise ValueError("manifest files must be a non-empty sorted unique list")
    for relative in files:
        posix = PurePosixPath(relative)
        if posix.is_absolute() or ".." in posix.parts or str(posix) != relative:
            raise ValueError(f"unsafe manifest path: {relative}")
        if not (skill_dir / Path(*posix.parts)).is_file():
            raise ValueError(f"manifest file unavailable: {relative}")
    return manifest


def build_archive(skill_dir: Path, output: Path) -> tuple[dict, str]:
    manifest = load_manifest(skill_dir)
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_STORED) as archive:
        for relative in manifest["files"]:
            source = skill_dir / Path(*PurePosixPath(relative).parts)
            archive_name = f"{manifest['archive_root']}/{relative}"
            info = zipfile.ZipInfo(archive_name, FIXED_TIMESTAMP)
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_STORED
            archive.writestr(info, source.read_bytes())
    return manifest, sha256(output)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill-dir", type=Path, default=DEFAULT_SKILL)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)

    skill_dir = args.skill_dir.resolve()
    try:
        manifest = load_manifest(skill_dir)
        output = (
            args.output
            or ROOT / "dist" / f"{manifest['name']}-{manifest['version']}.zip"
        ).resolve()
        manifest, digest = build_archive(skill_dir, output)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"FAIL package-skill: {error}", file=sys.stderr)
        return 1

    print(f"PASS package-skill: {output}")
    print(f"VERSION {manifest['version']}")
    print(f"FILES {len(manifest['files'])}")
    print(f"SHA256 {digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
