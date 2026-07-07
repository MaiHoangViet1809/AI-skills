#!/usr/bin/env python3
"""Sync AISkills skills into Codex-specific destinations."""

from __future__ import annotations

import argparse
from pathlib import Path

from skill_sync_common import (
    normalized_path,
    print_skill_results,
    sync_selected_skills,
)


def codex_skill_root(scope: str | None, target_project: str | None, target_root: str | None) -> Path:
    if target_root:
        return normalized_path(target_root)
    if scope == "repo":
        if not target_project:
            raise SystemExit("--scope repo requires --target-project unless --target-root is supplied")
        return normalized_path(target_project) / ".agents" / "skills"
    if scope == "user":
        return Path.home() / ".agents" / "skills"
    if scope == "legacy-user":
        return Path.home() / ".codex" / "skills"
    raise SystemExit("--profile skills requires --scope repo|user|legacy-user")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scope", choices=["repo", "user", "legacy-user"])
    parser.add_argument("--profile", choices=["skills"], default="skills")
    parser.add_argument("--target-project", help="project root for repo-scoped skill installs")
    parser.add_argument("--target-root", help="explicit destination skills root override")
    parser.add_argument("--skill", help="sync one skill by directory name")
    parser.add_argument("--all", action="store_true", help="sync all repo skills")
    parser.add_argument("--overwrite", action="store_true", help="replace existing target skill directory")
    parser.add_argument("--dry-run", action="store_true", help="show planned actions without copying")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    dest_root = codex_skill_root(args.scope, args.target_project, args.target_root)
    results = sync_selected_skills(
        dest_root=dest_root,
        skill=args.skill,
        install_all=args.all,
        overwrite=args.overwrite,
        dry_run=args.dry_run,
    )
    print_skill_results(results)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
