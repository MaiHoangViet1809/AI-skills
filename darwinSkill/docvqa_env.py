from __future__ import annotations

import ast
import csv
import json
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from darwinSkill.contracts import MetricResult, SkillEvaluator, SkillSample
from darwinSkill.reference_assets import is_split_dir


def _parse_answers(raw: Any) -> list[str]:
    if raw is None:
        return [""]
    if isinstance(raw, str):
        text = raw.strip()
        if not text:
            return [""]
        parsed = None
        if text[0] in "[{":
            try:
                parsed = json.loads(text)
            except json.JSONDecodeError:
                try:
                    parsed = ast.literal_eval(text)
                except (ValueError, SyntaxError):
                    parsed = None
        if parsed is None:
            return [text]
        return _parse_answers(parsed)
    if isinstance(raw, dict):
        for key in ("answers", "ground_truth", "answer"):
            if key in raw:
                return _parse_answers(raw[key])
        return [str(raw)]
    if isinstance(raw, Iterable) and not isinstance(raw, (bytes, bytearray)):
        values: list[str] = []
        for item in raw:
            if isinstance(item, dict):
                for key in ("text", "answer", "value"):
                    if key in item:
                        values.extend(_parse_answers(item[key]))
                        break
                else:
                    values.append(str(item))
                continue
            values.append(str(item))
        return values or [""]
    return [str(raw)]


def _extract_document_path(question: str) -> tuple[str, str]:
    marker = "document_path:"
    if marker not in question:
        return question.strip(), ""
    main, tail = question.split(marker, 1)
    return main.strip(), tail.strip()


def normalize_docvqa_record(record: dict[str, Any]) -> dict[str, Any]:
    question_text, document_path = _extract_document_path(str(record.get("question") or ""))
    answers = [answer.strip() for answer in _parse_answers(record.get("answer") or record.get("ground_truth")) if answer.strip()]
    image_path = str(record.get("image_path") or document_path or "").strip()
    task_type = str(record.get("topic") or record.get("category") or "docvqa").strip() or "docvqa"
    return {
        "id": str(record.get("questionId") or record.get("id") or "").strip(),
        "question": question_text,
        "answer": answers[0] if answers else "",
        "answers": answers,
        "task_type": task_type,
        "subtask": task_type,
        "image_paths": [image_path] if image_path else [],
        "image_path": image_path,
        "questionId": str(record.get("questionId") or "").strip(),
        "docId": str(record.get("docId") or "").strip(),
        "ucsf_document_id": str(record.get("ucsf_document_id") or "").strip(),
        "ucsf_document_page_no": str(record.get("ucsf_document_page_no") or "").strip(),
        "source_split": str(record.get("source_split") or "").strip(),
        **{
            key: value
            for key, value in record.items()
            if key
            not in {
                "question",
                "answer",
                "ground_truth",
                "image_path",
                "topic",
                "category",
                "questionId",
                "id",
                "docId",
                "ucsf_document_id",
                "ucsf_document_page_no",
                "source_split",
            }
        },
    }


def _load_csv_records(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return [dict(row) for row in reader]


def _resolve_csv_path(path: Path) -> Path:
    if path.is_file():
        return path
    candidates = sorted(path.glob("*.csv"))
    if not candidates:
        raise FileNotFoundError(f"No CSV file found under {path}")
    return candidates[0]


def load_docvqa_records(path: Path | str) -> list[dict[str, Any]]:
    resolved = _resolve_csv_path(Path(path))
    return [normalize_docvqa_record(row) for row in _load_csv_records(resolved)]


def load_docvqa_dataset(path: Path | str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    root = Path(path)
    if is_split_dir(root):
        train_records = load_docvqa_records(root / "train")
        eval_records = load_docvqa_records(root / "val")
        if not eval_records:
            eval_records = load_docvqa_records(root / "test")
        return train_records, eval_records or list(train_records)
    records = load_docvqa_records(root)
    return records, list(records)


def build_docvqa_samples(records: list[dict[str, Any]]) -> list[SkillSample]:
    return [
        SkillSample(
            prompt=str(record.get("question", "")),
            expected_answer=str((record.get("answers") or [record.get("answer", "")])[0] or ""),
            metadata=dict(normalize_docvqa_record(record)),
        )
        for record in records
    ]


def _normalize_text(value: Any) -> str:
    if value is None:
        return ""
    return " ".join(str(value).strip().lower().split())


def _levenshtein_distance(a: str, b: str) -> int:
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)
    if len(a) > len(b):
        a, b = b, a
    previous = list(range(len(b) + 1))
    for index_a, char_a in enumerate(a, start=1):
        current = [index_a]
        for index_b, char_b in enumerate(b, start=1):
            current.append(
                min(
                    current[index_b - 1] + 1,
                    previous[index_b] + 1,
                    previous[index_b - 1] + (char_a != char_b),
                )
            )
        previous = current
    return previous[-1]


def extract_answer(text: str) -> str:
    lowered = text.lower()
    start = lowered.rfind("<answer>")
    end = lowered.rfind("</answer>")
    if start != -1 and end != -1 and end > start:
        return text[start + len("<answer>") : end].strip()
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return lines[-1] if lines else text.strip()


class DocVQAEvaluator(SkillEvaluator):
    threshold: float = 0.5

    def evaluate(self, prediction: str, sample: SkillSample) -> MetricResult:
        predicted_answer = extract_answer(prediction)
        gold_answers = list(sample.metadata.get("answers") or [sample.expected_answer])
        best_score = 0.0
        normalized_prediction = _normalize_text(predicted_answer)
        for gold in gold_answers:
            normalized_gold = _normalize_text(gold)
            if not normalized_prediction and not normalized_gold:
                best_score = 1.0
                break
            if not normalized_prediction or not normalized_gold:
                continue
            distance = _levenshtein_distance(normalized_prediction, normalized_gold)
            normalized_distance = distance / max(len(normalized_prediction), len(normalized_gold))
            if normalized_distance < self.threshold:
                best_score = max(best_score, 1.0 - normalized_distance)
        return MetricResult(
            score=best_score,
            passed=best_score >= 0.999,
            details={
                "predicted_answer": predicted_answer,
                "gold_answers": gold_answers,
                "anls": best_score,
            },
        )
