#!/usr/bin/env python3
"""Sync AISkills skills into an explicit custom destination."""

from __future__ import annotations

import argparse

from skill_sync_common import normalized_path, print_skill_results, sync_selected_skills


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target-root", required=True, help="explicit destination skills root")
    parser.add_argument("--skill", help="sync one skill by directory name")
    parser.add_argument("--all", action="store_true", help="sync all repo skills")
    parser.add_argument("--overwrite", action="store_true", help="replace existing target skill directory")
    parser.add_argument("--dry-run", action="store_true", help="show planned actions without copying")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    results = sync_selected_skills(
        dest_root=normalized_path(args.target_root),
        skill=args.skill,
        install_all=args.all,
        overwrite=args.overwrite,
        dry_run=args.dry_run,
    )
    print_skill_results(results)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
