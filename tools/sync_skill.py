#!/usr/bin/env python3
"""Compare or explicitly copy canonical skill package files to a target."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import dataclass
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT / "skills" / "audit-project-governance"


@dataclass(frozen=True)
class Difference:
    state: str
    relative: str
    source_hash: str
    target_hash: str | None


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def load_manifest(source: Path) -> dict:
    manifest = json.loads((source / "PACKAGE_MANIFEST.json").read_text(encoding="utf-8"))
    files = manifest.get("files")
    if not isinstance(files, list) or not files or files != sorted(set(files)):
        raise ValueError("manifest files must be a non-empty sorted unique list")
    for relative in files:
        posix = PurePosixPath(relative)
        if posix.is_absolute() or ".." in posix.parts or str(posix) != relative:
            raise ValueError(f"unsafe manifest path: {relative}")
        if not (source / Path(*posix.parts)).is_file():
            raise ValueError(f"source file unavailable: {relative}")
    return manifest


def compare(source: Path, target: Path, files: list[str]) -> list[Difference]:
    differences: list[Difference] = []
    for relative in files:
        parts = Path(*PurePosixPath(relative).parts)
        source_data = (source / parts).read_bytes()
        destination = target / parts
        if not destination.is_file():
            differences.append(Difference("missing", relative, digest(source_data), None))
            continue
        target_data = destination.read_bytes()
        if target_data != source_data:
            differences.append(
                Difference("changed", relative, digest(source_data), digest(target_data))
            )
    return differences


def apply_files(source: Path, target: Path, differences: list[Difference]) -> None:
    for item in differences:
        parts = Path(*PurePosixPath(item.relative).parts)
        destination = target / parts
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes((source / parts).read_bytes())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--target", type=Path, required=True)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--approve", default="")
    args = parser.parse_args(argv)

    source = args.source.resolve()
    target = args.target.resolve()
    if source == target:
        print("FAIL sync-skill: source and target are identical", file=sys.stderr)
        return 2
    try:
        manifest = load_manifest(source)
        differences = compare(source, target, manifest["files"])
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"FAIL sync-skill: {error}", file=sys.stderr)
        return 2

    for item in differences:
        target_hash = item.target_hash or "UNAVAILABLE"
        print(
            f"{item.state.upper():8} {item.relative} "
            f"source={item.source_hash} target={target_hash}"
        )

    if not differences:
        print(f"PASS sync-skill: target matches {manifest['name']} {manifest['version']}")
        return 0

    if not args.apply:
        print(f"PLAN {len(differences)} file(s) would be copied; no files were changed")
        return 1

    approval = f"sync {manifest['name']} {manifest['version']}"
    if args.approve != approval:
        print(
            f"FAIL sync-skill: --apply requires --approve \"{approval}\"",
            file=sys.stderr,
        )
        return 2

    try:
        apply_files(source, target, differences)
    except OSError as error:
        print(f"FAIL sync-skill: {error}", file=sys.stderr)
        return 2
    remaining = compare(source, target, manifest["files"])
    if remaining:
        print("FAIL sync-skill: target still differs after copy", file=sys.stderr)
        return 2
    print(f"PASS sync-skill: copied {len(differences)} file(s); unrelated target files were preserved")
    return 0


if __name__ == "__main__":
    sys.exit(main())
