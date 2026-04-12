#!/usr/bin/env python3
"""Install repo skills into ~/.codex/skills."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def source_root() -> Path:
    return repo_root() / "skills"


def default_target_root() -> Path:
    return Path.home() / ".codex" / "skills"


def discover_skills(root: Path) -> dict[str, Path]:
    skills: dict[str, Path] = {}
    for path in sorted(root.iterdir()):
        if not path.is_dir():
            continue
        if (path / "SKILL.md").exists():
            skills[path.name] = path
    return skills


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill", help="install one skill by directory name")
    parser.add_argument("--all", action="store_true", help="install all repo skills")
    parser.add_argument("--target-root", default=str(default_target_root()))
    parser.add_argument("--overwrite", action="store_true", help="replace existing target skill directory")
    parser.add_argument("--dry-run", action="store_true", help="show planned actions without copying")
    return parser.parse_args()


def select_skills(all_skills: dict[str, Path], one_skill: str | None, install_all: bool) -> dict[str, Path]:
    if install_all:
        return all_skills
    if one_skill:
        if one_skill not in all_skills:
            available = ", ".join(sorted(all_skills))
            raise SystemExit(f"skill '{one_skill}' not found. available: {available}")
        return {one_skill: all_skills[one_skill]}
    raise SystemExit("choose either --all or --skill <name>")


def copy_skill(name: str, src: Path, dest_root: Path, overwrite: bool, dry_run: bool) -> str:
    dest = dest_root / name
    action = "install"
    if dest.exists():
        if not overwrite:
            return f"skip  {name} -> {dest} (exists, use --overwrite)"
        action = "replace"
        if dry_run:
            return f"{action} {name} -> {dest}"
        shutil.rmtree(dest)
    else:
        if dry_run:
            return f"{action} {name} -> {dest}"

    if not dry_run:
        shutil.copytree(src, dest, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"))
    return f"{action} {name} -> {dest}"


def main() -> int:
    args = parse_args()
    src_root = source_root()
    dest_root = Path(args.target_root).expanduser().resolve()
    skills = discover_skills(src_root)
    selected = select_skills(skills, args.skill, args.all)

    if not args.dry_run:
        dest_root.mkdir(parents=True, exist_ok=True)

    for name, src in selected.items():
        print(copy_skill(name, src, dest_root, args.overwrite, args.dry_run))

    print(f"done: {len(selected)} skill(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
