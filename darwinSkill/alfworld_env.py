from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from darwinSkill.contracts import MetricResult, SkillEvaluator, SkillSample
from darwinSkill.reference_assets import is_split_dir


def _load_items(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError(f"Expected JSON array in {path}")
    return [dict(item) for item in payload]


def _resolve_data_file(path: Path) -> Path:
    if path.is_file():
        return path
    candidates = sorted(path.glob("*.json"))
    if len(candidates) != 1:
        raise ValueError(f"ALFWorld expects exactly one JSON file under {path}")
    return candidates[0]


def _infer_eval_dataset(gamefile: str) -> str:
    if "/valid_seen/" in gamefile:
        return "eval_in_distribution"
    if "/valid_unseen/" in gamefile:
        return "eval_out_of_distribution"
    return "train"


def normalize_alfworld_record(record: dict[str, Any]) -> dict[str, Any]:
    gamefile = str(record.get("gamefile") or "").strip()
    task_description = str(record.get("task_description") or record.get("task_desc") or record.get("goal") or "").strip()
    task_type = str(record.get("task_type") or record.get("instruction_type") or "").strip() or "alfworld"
    result_id = str(record.get("id") or record.get("result_id") or gamefile or "env").strip()
    eval_dataset = str(record.get("eval_dataset") or _infer_eval_dataset(gamefile))
    return {
        "id": result_id,
        "gamefile": gamefile,
        "task_description": task_description or gamefile,
        "task_type": task_type,
        "instruction_type": task_type,
        "eval_dataset": eval_dataset,
        "expected_outcome": str(record.get("expected_outcome") or "success"),
        **{
            key: value
            for key, value in record.items()
            if key not in {"id", "result_id", "gamefile", "task_description", "task_desc", "goal", "task_type", "instruction_type", "eval_dataset", "expected_outcome"}
        },
    }


def load_alfworld_records(path: Path | str) -> list[dict[str, Any]]:
    data_path = Path(path)
    resolved = _resolve_data_file(data_path)
    return [normalize_alfworld_record(item) for item in _load_items(resolved)]


def load_alfworld_dataset(path: Path | str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    root = Path(path)
    if is_split_dir(root):
        train_records = load_alfworld_records(root / "train")
        eval_records = load_alfworld_records(root / "val")
        if not eval_records:
            eval_records = load_alfworld_records(root / "test")
        return train_records, eval_records or list(train_records)
    records = load_alfworld_records(root)
    return records, list(records)


def build_alfworld_samples(records: list[dict[str, Any]]) -> list[SkillSample]:
    return [
        SkillSample(
            prompt=str(normalize_alfworld_record(record).get("task_description", "")),
            expected_answer="success",
            metadata=normalize_alfworld_record(record),
        )
        for record in records
    ]


def extract_answer(text: str) -> str:
    matches = re.findall(r"<answer>(.*?)</answer>", text, re.DOTALL | re.IGNORECASE)
    if matches:
        return matches[-1].strip()
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return lines[-1] if lines else text.strip()


def parse_success(prediction: str) -> bool:
    answer = extract_answer(prediction).strip().lower()
    if answer in {"success", "completed", "complete", "done", "won", "pass", "1", "true", "yes"}:
        return True
    if answer in {"fail", "failed", "timeout", "0", "false", "no"}:
        return False
    if "success" in answer or "completed" in answer:
        return True
    return False


class ALFWorldEvaluator(SkillEvaluator):
    def evaluate(self, prediction: str, sample: SkillSample) -> MetricResult:
        won = parse_success(prediction)
        task_type = str(sample.metadata.get("task_type") or "alfworld")
        gamefile = str(sample.metadata.get("gamefile") or "")
        task_description = str(sample.metadata.get("task_description") or sample.prompt)
        return MetricResult(
            score=1.0 if won else 0.0,
            passed=won,
            details={
                "hard": 1 if won else 0,
                "soft": 1.0 if won else 0.0,
                "task_type": task_type,
                "gamefile": gamefile,
                "task_description": task_description,
                "predicted_answer": extract_answer(prediction),
            },
        )
