from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from darwinSkill.src.storage import load_run_state


@dataclass(slots=True, frozen=True)
class StepInspection:
    step: int
    directory: Path
    record_path: Path | None = None
    candidate_skill_path: Path | None = None


@dataclass(slots=True, frozen=True)
class EpochInspection:
    category: str
    epoch: int
    directory: Path
    files: list[Path] = field(default_factory=list)


@dataclass(slots=True, frozen=True)
class RunInspection:
    output_dir: Path
    summary: dict[str, Any]
    run_state: dict[str, Any]
    history: list[dict[str, Any]]
    evaluations: list[dict[str, Any]]
    final_skill: str
    best_skill: str
    steps: list[StepInspection] = field(default_factory=list)
    epochs: dict[str, list[EpochInspection]] = field(default_factory=dict)


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _list_steps(output_dir: Path) -> list[StepInspection]:
    steps_dir = output_dir / "steps"
    if not steps_dir.exists():
        return []
    results: list[StepInspection] = []
    for child in sorted(steps_dir.iterdir()):
        if not child.is_dir() or not child.name.startswith("step_"):
            continue
        try:
            step = int(child.name.split("_", 1)[1])
        except ValueError:
            continue
        record_path = child / "step_record.json"
        candidate_skill_path = child / "candidate_skill.txt"
        results.append(
            StepInspection(
                step=step,
                directory=child,
                record_path=record_path if record_path.exists() else None,
                candidate_skill_path=candidate_skill_path if candidate_skill_path.exists() else None,
            )
        )
    return results


def _list_epoch_category(output_dir: Path, category: str) -> list[EpochInspection]:
    category_dir = output_dir / category
    if not category_dir.exists():
        return []
    results: list[EpochInspection] = []
    for child in sorted(category_dir.iterdir()):
        if not child.is_dir() or not child.name.startswith("epoch_"):
            continue
        try:
            epoch = int(child.name.split("_", 1)[1])
        except ValueError:
            continue
        files = sorted(item for item in child.iterdir() if item.is_file())
        results.append(EpochInspection(category=category, epoch=epoch, directory=child, files=files))
    return results


def inspect_run(output_dir: Path | str) -> RunInspection:
    run_dir = Path(output_dir)
    summary = _read_json(run_dir / "summary.json")
    run_state = _read_json(run_dir / "run_state.json")
    history = _read_json(run_dir / "history.json")
    evaluations = _read_json(run_dir / "evaluations.json")
    final_skill = (run_dir / "final_skill.txt").read_text(encoding="utf-8")
    best_skill = (run_dir / "best_skill.md").read_text(encoding="utf-8")
    return RunInspection(
        output_dir=run_dir,
        summary=summary,
        run_state=run_state,
        history=history,
        evaluations=evaluations,
        final_skill=final_skill,
        best_skill=best_skill,
        steps=_list_steps(run_dir),
        epochs={
            "slow_update": _list_epoch_category(run_dir, "slow_update"),
            "meta_skill": _list_epoch_category(run_dir, "meta_skill"),
        },
    )


def load_step_record(output_dir: Path | str, step: int) -> dict[str, Any]:
    return _read_json(Path(output_dir) / "steps" / f"step_{step:04d}" / "step_record.json")


def summarize_run(output_dir: Path | str) -> dict[str, Any]:
    inspection = inspect_run(output_dir)
    run_state = load_run_state(Path(output_dir) / "run_state.json")
    return {
        "run_id": inspection.summary.get("run_id", ""),
        "run_name": inspection.summary.get("run_name", ""),
        "run_kind": inspection.summary.get("run_kind", ""),
        "sample_count": inspection.summary.get("sample_count", 0),
        "mean_score": inspection.summary.get("mean_score", 0.0),
        "pass_rate": inspection.summary.get("pass_rate", 0.0),
        "current_step": run_state.current_step,
        "best_step": run_state.best_step,
        "last_action": run_state.last_action,
        "step_count": len(inspection.steps),
        "slow_update_epochs": len(inspection.epochs.get("slow_update", [])),
        "meta_skill_epochs": len(inspection.epochs.get("meta_skill", [])),
    }
