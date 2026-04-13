#!/usr/bin/env python3
"""Sync repo-owned rules and selected skills into local environments."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def codex_root() -> Path:
    return Path.home() / ".codex"


def copy_tree(src: Path, dest: Path) -> None:
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(src, dest, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"))


def sync_codex(dry_run: bool) -> list[str]:
    root = repo_root()
    target_root = codex_root()
    actions: list[str] = []

    rule_src = root / "rules" / "brief-execution.md"
    rule_dest = target_root / "rules" / "brief-execution.md"
    actions.append(f"rule  {rule_src} -> {rule_dest}")

    for skill_name in ("task-router-flow", "sow-delegate-flow"):
        skill_src = root / "skills" / skill_name
        skill_dest = target_root / "skills" / skill_name
        actions.append(f"skill {skill_src} -> {skill_dest}")

    if dry_run:
        return actions

    rule_dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(rule_src, rule_dest)

    for skill_name in ("task-router-flow", "sow-delegate-flow"):
        copy_tree(root / "skills" / skill_name, target_root / "skills" / skill_name)

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
