from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
REFERENCE_ENVS_ROOT = REPO_ROOT / "references" / "SkillOpt" / "skillopt" / "envs"
SPLIT_NAMES = ("train", "val", "test")


def get_initial_skill_path(name: str) -> Path:
    return REFERENCE_ENVS_ROOT / name / "skills" / "initial.md"


def load_initial_skill_text(name: str) -> str:
    return get_initial_skill_path(name).read_text(encoding="utf-8")


def is_split_dir(path: Path) -> bool:
    return path.is_dir() and all((path / split).is_dir() for split in SPLIT_NAMES)
