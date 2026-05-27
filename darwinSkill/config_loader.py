from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from darwinSkill.contracts import SkillSample, TrainingConfig


def _merge_dicts(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _merge_dicts(merged[key], value)
        else:
            merged[key] = value
    return merged


def _load_yaml(path: Path, visited: set[Path] | None = None) -> dict[str, Any]:
    visited = visited or set()
    resolved = path.resolve()
    if resolved in visited:
        raise ValueError(f"Cyclic config inheritance detected at {path}.")
    visited.add(resolved)
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    base_ref = payload.pop("_base_", None)
    if not base_ref:
        return payload
    if isinstance(base_ref, str):
        base_paths = [base_ref]
    else:
        base_paths = list(base_ref)
    merged: dict[str, Any] = {}
    for base_path in base_paths:
        merged = _merge_dicts(
            merged,
            _load_yaml((path.parent / base_path).resolve(), visited),
        )
    return _merge_dicts(merged, payload)


def load_config(path: Path | str) -> dict[str, Any]:
    config_path = Path(path)
    if config_path.suffix in {".yaml", ".yml"}:
        return _load_yaml(config_path)
    if config_path.suffix == ".json":
        return json.loads(config_path.read_text(encoding="utf-8"))
    raise ValueError(f"Unsupported config format for {config_path}.")


def build_training_config(payload: dict[str, Any]) -> TrainingConfig:
    train = dict(payload.get("train", {}))
    env = dict(payload.get("env", {}))
    output_root = env.get("out_root", train.get("output_root", "outputs/darwinSkill"))
    return TrainingConfig(
        num_epochs=int(train.get("num_epochs", 1)),
        batch_size=int(train.get("batch_size", 4)),
        edit_budget=int(payload.get("optimizer", {}).get("learning_rate", train.get("edit_budget", 4))),
        initial_skill=str(train.get("initial_skill", train.get("skill_init", ""))),
        output_root=output_root,
        run_name=str(train.get("run_name", payload.get("run_name", "train"))),
        use_slow_update=bool(payload.get("optimizer", {}).get("use_slow_update", True)),
        use_meta_skill=bool(payload.get("optimizer", {}).get("use_meta_skill", True)),
    )


def build_samples(records: list[dict[str, Any]]) -> list[SkillSample]:
    return [
        SkillSample(
            prompt=str(record["prompt"]),
            expected_answer=str(record["expected_answer"]),
            metadata=dict(record.get("metadata", {})),
        )
        for record in records
    ]

