#!/usr/bin/env python3
"""Compatibility command for old local Codex environment sync."""

from __future__ import annotations

import argparse
from pathlib import Path

from skill_sync_common import copy_skill, repo_root
from sync_env_codex import sync_codex_hooks


LEGACY_CODEX_SKILLS = ("task-router-flow", "sow-delegate-flow", "telemetry-flow", "playwright-flow")


def sync_codex(dry_run: bool) -> list[str]:
    actions = sync_codex_hooks(dry_run)
    dest_root = Path.home() / ".codex" / "skills"
    root = repo_root()
    for skill_name in LEGACY_CODEX_SKILLS:
        result = copy_skill(
            skill_name,
            root / "skills" / skill_name,
            dest_root,
            overwrite=True,
            dry_run=dry_run,
        )
        actions.append(result.format())
    return actions


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", choices=["codex"], default="codex")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    actions = sync_codex(args.dry_run)
    for action in actions:
        print(action)
    print(f"done: {args.target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
