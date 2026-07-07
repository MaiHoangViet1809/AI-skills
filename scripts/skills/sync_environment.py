#!/usr/bin/env python3
"""Compatibility command for old local Codex skill sync."""

from __future__ import annotations

import argparse
from pathlib import Path

from skill_sync_common import sync_selected_skills


def sync_codex(dry_run: bool) -> list[str]:
    results = sync_selected_skills(
        dest_root=Path.home() / ".codex" / "skills",
        skill=None,
        install_all=True,
        overwrite=True,
        dry_run=dry_run,
    )
    return [result.format() for result in results]


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
