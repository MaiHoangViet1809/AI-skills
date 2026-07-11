#!/usr/bin/env python3
"""Compare one canonical AISkills skill with one installed copy."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from skill_sync_common import IGNORE_PATTERNS, discover_skills, normalized_path


def visible_files(root: Path) -> dict[Path, Path]:
    files: dict[Path, Path] = {}
    if not root.is_dir():
        return files

    for directory, dirnames, filenames in os.walk(root):
        current = Path(directory)
        ignored = set(IGNORE_PATTERNS(str(current), [*dirnames, *filenames]))
        dirnames[:] = sorted(name for name in dirnames if name not in ignored)
        for filename in sorted(filenames):
            if filename in ignored:
                continue
            path = current / filename
            files[path.relative_to(root)] = path
    return files


def compare_skill(source: Path, destination: Path) -> dict[str, list[Path]]:
    source_files = visible_files(source)
    destination_files = visible_files(destination)
    source_paths = set(source_files)
    destination_paths = set(destination_files)

    return {
        "missing": sorted(source_paths - destination_paths),
        "extra": sorted(destination_paths - source_paths),
        "changed": sorted(
            path
            for path in source_paths & destination_paths
            if source_files[path].read_bytes() != destination_files[path].read_bytes()
        ),
    }


def print_mismatches(mismatches: dict[str, list[Path]]) -> None:
    for bucket in ("missing", "extra", "changed"):
        paths = mismatches[bucket]
        if not paths:
            continue
        print(f"{bucket}:")
        for path in paths:
            print(f"  {path.as_posix()}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill", required=True, help="canonical skill directory name")
    parser.add_argument("--target-root", required=True, help="installed skills root containing the skill")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    skills = discover_skills()
    if args.skill not in skills:
        available = ", ".join(sorted(skills))
        raise SystemExit(f"skill '{args.skill}' not found. available: {available}")

    destination = normalized_path(args.target_root) / args.skill
    mismatches = compare_skill(skills[args.skill], destination)
    if any(mismatches.values()):
        print_mismatches(mismatches)
        print(f"parity: fail {args.skill} -> {destination}")
        return 1

    print(f"parity: ok {args.skill} -> {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
