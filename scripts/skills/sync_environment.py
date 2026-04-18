#!/usr/bin/env python3
"""Sync repo-owned rules and selected skills into local environments."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path
import re


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

    hooks_template = root / ".codex" / "hooks.json.template"
    hooks_dest = target_root / "hooks.json"
    actions.append(f"hooks {hooks_template} -> {hooks_dest}")
    bridge_src = root / "scripts" / "telemetry" / "codex_hook_bridge.py"
    bridge_dest = target_root / "hooks" / "codex_hook_bridge.py"
    actions.append(f"hook  {bridge_src} -> {bridge_dest}")
    common_src = root / "aiskills_common"
    common_dest = target_root / "lib" / "aiskills_common"
    actions.append(f"lib   {common_src} -> {common_dest}")

    for skill_name in ("task-router-flow", "sow-delegate-flow", "telemetry-flow"):
        skill_src = root / "skills" / skill_name
        skill_dest = target_root / "skills" / skill_name
        actions.append(f"skill {skill_src} -> {skill_dest}")

    if dry_run:
        return actions

    rule_dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(rule_src, rule_dest)

    hooks_dest.parent.mkdir(parents=True, exist_ok=True)
    hooks_text = hooks_template.read_text(encoding="utf-8")
    hooks_dest.write_text(hooks_text, encoding="utf-8")
    bridge_dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(bridge_src, bridge_dest)
    copy_tree(common_src, common_dest)

    for skill_name in ("task-router-flow", "sow-delegate-flow", "telemetry-flow"):
        copy_tree(root / "skills" / skill_name, target_root / "skills" / skill_name)

    config_path = target_root / "config.toml"
    config_text = config_path.read_text(encoding="utf-8") if config_path.exists() else ""
    if "[features]" not in config_text:
        config_text = config_text.rstrip() + "\n\n[features]\n"
    if re.search(r"(?m)^codex_hooks\s*=\s*true\s*$", config_text) is None:
        if re.search(r"(?m)^\[features\]\s*$", config_text):
            config_text = re.sub(r"(?m)^\[features\]\s*$", "[features]\ncodex_hooks = true", config_text, count=1)
        else:
            config_text = config_text.rstrip() + "\n\n[features]\ncodex_hooks = true\n"
        config_path.write_text(config_text.rstrip() + "\n", encoding="utf-8")

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
