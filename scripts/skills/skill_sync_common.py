"""Shared helpers for AISkills skill synchronization scripts."""

from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path


IGNORE_PATTERNS = shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store")


@dataclass(frozen=True)
class SkillCopyResult:
    action: str
    name: str
    destination: Path
    copied: bool

    def format(self) -> str:
        return f"{self.action:<7} {self.name} -> {self.destination}"


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def source_root() -> Path:
    return repo_root() / "skills"


def normalized_path(raw_path: str | Path) -> Path:
    return Path(raw_path).expanduser().resolve()


def discover_skills(root: Path | None = None) -> dict[str, Path]:
    skill_root = root or source_root()
    skills: dict[str, Path] = {}
    for path in sorted(skill_root.iterdir()):
        if path.is_dir() and (path / "SKILL.md").exists():
            skills[path.name] = path
    return skills


def select_skills(all_skills: dict[str, Path], one_skill: str | None, install_all: bool) -> dict[str, Path]:
    if install_all and one_skill:
        raise SystemExit("choose either --all or --skill <name>, not both")
    if install_all:
        return all_skills
    if one_skill:
        if one_skill not in all_skills:
            available = ", ".join(sorted(all_skills))
            raise SystemExit(f"skill '{one_skill}' not found. available: {available}")
        return {one_skill: all_skills[one_skill]}
    raise SystemExit("choose either --all or --skill <name>")


def copy_skill(name: str, src: Path, dest_root: Path, overwrite: bool, dry_run: bool) -> SkillCopyResult:
    dest = dest_root / name
    if dest.exists():
        if not overwrite:
            return SkillCopyResult("skip", name, dest, copied=False)
        if not dry_run:
            shutil.rmtree(dest)
        action = "replace"
    else:
        action = "install"

    if not dry_run:
        dest_root.mkdir(parents=True, exist_ok=True)
        shutil.copytree(src, dest, ignore=IGNORE_PATTERNS)

    return SkillCopyResult(action, name, dest, copied=not dry_run)


def sync_selected_skills(
    *,
    dest_root: Path,
    skill: str | None,
    install_all: bool,
    overwrite: bool,
    dry_run: bool,
) -> list[SkillCopyResult]:
    skills = discover_skills()
    selected = select_skills(skills, skill, install_all)
    return [
        copy_skill(name, src, dest_root, overwrite=overwrite, dry_run=dry_run)
        for name, src in selected.items()
    ]


def print_skill_results(results: list[SkillCopyResult]) -> None:
    for result in results:
        print(result.format())
    print(f"done: {len(results)} skill(s)")
