from __future__ import annotations

import csv
import json
import re
import string
from collections import Counter
from pathlib import Path
from typing import Any

from darwinSkill.src.contracts import MetricResult, SkillEvaluator, SkillSample
from darwinSkill.src.reference_assets import is_split_dir


def _parse_list_field(value: str | list[str] | None) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    text = str(value).strip()
    if not text:
        return []
    try:
        loaded = json.loads(text)
    except json.JSONDecodeError:
        loaded = None
    if isinstance(loaded, list):
        return [str(item).strip() for item in loaded if str(item).strip()]
    if "\n" in text:
        return [part.strip() for part in text.splitlines() if part.strip()]
    if "," in text and not text.lower().endswith(".txt"):
        return [part.strip() for part in text.split(",") if part.strip()]
    return [text]


def normalize_officeqa_record(record: dict[str, Any]) -> dict[str, Any]:
    item_id = str(record.get("uid") or record.get("id") or "").strip()
    question = str(record.get("question") or "").strip()
    ground_truth = str(record.get("ground_truth") or record.get("answer") or "").strip()
    task_type = str(record.get("category") or record.get("difficulty") or "officeqa").strip() or "officeqa"
    source_files = _parse_list_field(record.get("source_files"))
    source_docs = _parse_list_field(record.get("source_docs"))
    split = str(record.get("split") or "").strip()
    return {
        "id": item_id,
        "uid": item_id,
        "question": question,
        "ground_truth": ground_truth,
        "answer": ground_truth,
        "answers": [ground_truth] if ground_truth else [],
        "task_type": task_type,
        "category": task_type,
        "source_files": source_files,
        "source_docs": source_docs,
        "split": split,
        **{
            key: value
            for key, value in record.items()
            if key not in {"uid", "id", "question", "ground_truth", "answer", "category", "difficulty", "source_files", "source_docs", "split"}
        },
    }


def _load_json_records(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError(f"Expected JSON array in {path}")
    return [dict(item) for item in data]


def load_officeqa_records(path: Path | str) -> list[dict[str, Any]]:
    data_path = Path(path)
    if data_path.is_file():
        if data_path.suffix.lower() == ".csv":
            with data_path.open(encoding="utf-8", newline="") as handle:
                return [normalize_officeqa_record(row) for row in csv.DictReader(handle)]
        if data_path.suffix.lower() == ".json":
            return [normalize_officeqa_record(row) for row in _load_json_records(data_path)]
        raise ValueError(f"Unsupported OfficeQA file format: {data_path}")
    csv_files = sorted(data_path.glob("*.csv"))
    if csv_files:
        with csv_files[0].open(encoding="utf-8", newline="") as handle:
            return [normalize_officeqa_record(row) for row in csv.DictReader(handle)]
    json_files = sorted(data_path.glob("*.json"))
    if json_files:
        return [normalize_officeqa_record(row) for row in _load_json_records(json_files[0])]
    raise FileNotFoundError(f"No CSV or JSON OfficeQA records found under {data_path}")


def load_officeqa_dataset(path: Path | str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    root = Path(path)
    if is_split_dir(root):
        train_records = load_officeqa_records(root / "train")
        eval_records = load_officeqa_records(root / "val")
        if not eval_records:
            eval_records = load_officeqa_records(root / "test")
        return train_records, eval_records or list(train_records)
    records = load_officeqa_records(root)
    return records, list(records)


def build_officeqa_samples(records: list[dict[str, Any]]) -> list[SkillSample]:
    return [
        SkillSample(
            prompt=str(record.get("question", "")),
            expected_answer=str(record.get("ground_truth") or record.get("answer") or ""),
            metadata=dict(normalize_officeqa_record(record)),
        )
        for record in records
    ]


NUMERIC_CHARS = set("0123456789.-")


def normalize_answer(text: str) -> str:
    lowered = text.lower().strip().replace(",", "")
    lowered = "".join(char for char in lowered if char not in string.punctuation or char in NUMERIC_CHARS or char == "%")
    lowered = re.sub(r"\b(million|millions|billion|billions|dollars|dollar|nominal)\b", " ", lowered)
    return " ".join(lowered.split())


def extract_answer(text: str) -> str:
    matches = re.findall(r"<answer>(.*?)</answer>", text, re.DOTALL | re.IGNORECASE)
    if matches:
        return matches[-1].strip()
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return lines[-1] if lines else text.strip()


class OfficeQAEvaluator(SkillEvaluator):
    def evaluate(self, prediction: str, sample: SkillSample) -> MetricResult:
        predicted_answer = extract_answer(prediction)
        gold_answer = str(sample.metadata.get("ground_truth") or sample.expected_answer)
        normalized_prediction = normalize_answer(predicted_answer)
        normalized_gold = normalize_answer(gold_answer)
        em = 1.0 if normalized_prediction == normalized_gold else 0.0
        prediction_tokens = normalized_prediction.split()
        gold_tokens = normalized_gold.split()
        if not prediction_tokens or not gold_tokens:
            f1 = 1.0 if prediction_tokens == gold_tokens else 0.0
        else:
            common = Counter(prediction_tokens) & Counter(gold_tokens)
            overlap = sum(common.values())
            if overlap == 0:
                f1 = 0.0
            else:
                precision = overlap / len(prediction_tokens)
                recall = overlap / len(gold_tokens)
                f1 = 2 * precision * recall / (precision + recall)
        return MetricResult(
            score=f1,
            passed=bool(em),
            details={
                "predicted_answer": predicted_answer,
                "gold_answer": gold_answer,
                "em": em,
                "f1": f1,
            },
        )
