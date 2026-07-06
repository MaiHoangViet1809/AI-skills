#!/usr/bin/env python3
"""Sync AISkills skills into Codex-specific destinations."""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path

from skill_sync_common import (
    IGNORE_PATTERNS,
    normalized_path,
    print_skill_results,
    repo_root,
    sync_selected_skills,
)


def codex_root() -> Path:
    return Path.home() / ".codex"


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


def copy_file_action(src: Path, dest: Path, dry_run: bool) -> str:
    if not dry_run:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
    return f"file    {src} -> {dest}"


def copy_tree_action(src: Path, dest: Path, dry_run: bool) -> str:
    if not dry_run:
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(src, dest, ignore=IGNORE_PATTERNS)
    return f"tree    {src} -> {dest}"


def ensure_codex_hooks_enabled(config_path: Path, dry_run: bool) -> str:
    if dry_run:
        return f"config  enable codex_hooks -> {config_path}"

    config_text = config_path.read_text(encoding="utf-8") if config_path.exists() else ""
    if "[features]" not in config_text:
        config_text = config_text.rstrip() + "\n\n[features]\n"
    if re.search(r"(?m)^codex_hooks\s*=\s*true\s*$", config_text) is None:
        if re.search(r"(?m)^\[features\]\s*$", config_text):
            config_text = re.sub(
                r"(?m)^\[features\]\s*$",
                "[features]\ncodex_hooks = true",
                config_text,
                count=1,
            )
        else:
            config_text = config_text.rstrip() + "\n\n[features]\ncodex_hooks = true\n"
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text(config_text.rstrip() + "\n", encoding="utf-8")
    return f"config  enable codex_hooks -> {config_path}"


def sync_codex_hooks(dry_run: bool) -> list[str]:
    root = repo_root()
    target_root = codex_root()
    actions = [
        copy_file_action(root / "rules" / "brief-execution.md", target_root / "rules" / "brief-execution.md", dry_run),
        copy_file_action(root / ".codex" / "hooks.json.template", target_root / "hooks.json", dry_run),
        copy_file_action(
            root / "scripts" / "telemetry" / "codex_hook_bridge.py",
            target_root / "hooks" / "codex_hook_bridge.py",
            dry_run,
        ),
        copy_tree_action(root / "aiskills_common", target_root / "lib" / "aiskills_common", dry_run),
        ensure_codex_hooks_enabled(target_root / "config.toml", dry_run),
    ]
    return actions


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scope", choices=["repo", "user", "legacy-user"])
    parser.add_argument("--profile", choices=["skills", "codex-hooks"], default="skills")
    parser.add_argument("--target-project", help="project root for repo-scoped skill installs")
    parser.add_argument("--target-root", help="explicit destination skills root override")
    parser.add_argument("--skill", help="sync one skill by directory name")
    parser.add_argument("--all", action="store_true", help="sync all repo skills")
    parser.add_argument("--overwrite", action="store_true", help="replace existing target skill directory")
    parser.add_argument("--dry-run", action="store_true", help="show planned actions without copying")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.profile == "codex-hooks":
        for action in sync_codex_hooks(args.dry_run):
            print(action)
        print("done: codex-hooks")
        return 0

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
