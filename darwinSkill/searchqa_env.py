from __future__ import annotations

import json
import re
import string
from collections import Counter
from pathlib import Path
from typing import Any

from darwinSkill.contracts import MetricResult, SkillEvaluator, SkillSample
from darwinSkill.reference_assets import is_split_dir


def _load_json_or_jsonl(path: Path) -> list[dict[str, Any]]:
    content = path.read_text(encoding="utf-8").strip()
    if not content:
        return []
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        parsed = None
    if isinstance(parsed, list):
        return [dict(item) for item in parsed]
    if isinstance(parsed, dict):
        nested = parsed.get("data")
        if isinstance(nested, list):
            return [dict(item) for item in nested]
        return [dict(item) for item in parsed.values() if isinstance(item, dict)]
    return [json.loads(line) for line in content.splitlines() if line.strip()]


def _resolve_data_file(path: Path) -> Path:
    if path.is_file():
        return path
    candidates = sorted(path.glob("*.json")) + sorted(path.glob("*.jsonl"))
    if len(candidates) != 1:
        raise ValueError(f"SearchQA expects exactly one JSON/JSONL file under {path}")
    return candidates[0]


def normalize_searchqa_record(record: dict[str, Any]) -> dict[str, Any]:
    answers = record.get("answers")
    if not isinstance(answers, list):
        single = record.get("answer")
        answers = [single] if single not in {None, ""} else []
    normalized_answers = [str(item).strip() for item in answers if str(item).strip()]
    return {
        "id": str(record.get("id", "")).strip(),
        "question": str(record.get("question", "")).strip(),
        "context": str(record.get("context", "")),
        "answers": normalized_answers,
        "answer": normalized_answers[0] if normalized_answers else "",
        "task_type": str(record.get("task_type", "qa")).strip() or "qa",
        **{key: value for key, value in record.items() if key not in {"id", "question", "context", "answers", "answer"}},
    }


def load_searchqa_records(path: Path | str) -> list[dict[str, Any]]:
    data_path = Path(path)
    resolved = _resolve_data_file(data_path)
    return [normalize_searchqa_record(item) for item in _load_json_or_jsonl(resolved)]


def load_searchqa_dataset(path: Path | str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    root = Path(path)
    if is_split_dir(root):
        train_records = load_searchqa_records(root / "train")
        eval_records = load_searchqa_records(root / "val")
        if not eval_records:
            eval_records = load_searchqa_records(root / "test")
        return train_records, eval_records or list(train_records)
    records = load_searchqa_records(root)
    return records, list(records)


def build_searchqa_samples(records: list[dict[str, Any]]) -> list[SkillSample]:
    return [
        SkillSample(
            prompt=str(record.get("question", "")),
            expected_answer=str((record.get("answers") or [record.get("answer", "")])[0] or ""),
            metadata=dict(normalize_searchqa_record(record)),
        )
        for record in records
    ]


def normalize_answer(text: str) -> str:
    lowered = text.lower()
    lowered = "".join(char for char in lowered if char not in string.punctuation)
    lowered = re.sub(r"\b(a|an|the)\b", " ", lowered)
    return " ".join(lowered.split()).strip()


def extract_answer(text: str) -> str:
    matches = re.findall(r"<answer>(.*?)</answer>", text, re.DOTALL | re.IGNORECASE)
    if matches:
        return matches[-1].strip()
    lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
    return lines[-1] if lines else text.strip()


def exact_match(prediction: str, gold_answers: list[str]) -> float:
    normalized_prediction = normalize_answer(prediction)
    return 1.0 if any(normalize_answer(answer) == normalized_prediction for answer in gold_answers) else 0.0


def f1_score(prediction: str, gold_answers: list[str]) -> float:
    prediction_tokens = normalize_answer(prediction).split()
    if not prediction_tokens:
        return 1.0 if any(not normalize_answer(answer).split() for answer in gold_answers) else 0.0
    best = 0.0
    for gold in gold_answers:
        gold_tokens = normalize_answer(gold).split()
        if not gold_tokens:
            continue
        common = Counter(prediction_tokens) & Counter(gold_tokens)
        overlap = sum(common.values())
        if overlap == 0:
            continue
        precision = overlap / len(prediction_tokens)
        recall = overlap / len(gold_tokens)
        best = max(best, 2 * precision * recall / (precision + recall))
    return best


def substring_match(prediction: str, gold_answers: list[str]) -> float:
    normalized_prediction = normalize_answer(prediction)
    for gold in gold_answers:
        normalized_gold = normalize_answer(gold)
        if normalized_gold in normalized_prediction or normalized_prediction in normalized_gold:
            return 1.0
    return 0.0


class SearchQAEvaluator(SkillEvaluator):
    def evaluate(self, prediction: str, sample: SkillSample) -> MetricResult:
        predicted_answer = extract_answer(prediction)
        gold_answers = list(sample.metadata.get("answers") or [sample.expected_answer])
        em = exact_match(predicted_answer, gold_answers)
        f1 = f1_score(predicted_answer, gold_answers)
        sub_em = substring_match(predicted_answer, gold_answers)
        return MetricResult(
            score=f1,
            passed=bool(em),
            details={
                "predicted_answer": predicted_answer,
                "gold_answers": gold_answers,
                "em": em,
                "f1": f1,
                "sub_em": sub_em,
            },
        )
