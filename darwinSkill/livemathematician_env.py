from __future__ import annotations

import glob
import hashlib
import json
import os
import random
import re
from pathlib import Path
from typing import Any

from darwinSkill.contracts import MetricResult, SkillEvaluator, SkillSample
from darwinSkill.reference_assets import is_split_dir


CHOICE_LABELS = ["A", "B", "C", "D", "E", "F", "G"]


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _iter_monthly_files(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    if path.is_dir():
        nested = glob.glob(os.path.join(str(path), "**", "qa_*_final.json"), recursive=True)
        flat = glob.glob(os.path.join(str(path), "qa_*_final.json"))
        return [Path(item) for item in sorted(set(nested + flat))]
    return []


def _coerce_choices(raw_choices: Any) -> list[dict[str, str]]:
    if isinstance(raw_choices, list):
        choices: list[dict[str, str]] = []
        for index, item in enumerate(raw_choices):
            if isinstance(item, dict):
                label = str(item.get("label") or CHOICE_LABELS[index]).strip()
                text = str(item.get("text") or item.get("content") or "").strip()
            else:
                label = CHOICE_LABELS[index]
                text = str(item).strip()
            if text:
                choices.append({"label": label, "text": text})
        return choices
    if isinstance(raw_choices, dict):
        labels = sorted(raw_choices.keys())
        return [
            {"label": str(label).strip(), "text": str(raw_choices[label]).strip()}
            for label in labels
            if str(raw_choices[label]).strip()
        ]
    return []


def _coerce_theorem_types(raw: Any) -> list[str]:
    if isinstance(raw, list):
        return [str(item).strip() for item in raw if str(item).strip()]
    text = str(raw or "").strip()
    return [text] if text else []


def normalize_label(text: str) -> str:
    return str(text).strip().upper().rstrip(".):")


def normalize_livemathematician_record(record: dict[str, Any], *, row_idx: int = 0, source_path: str = "") -> dict[str, Any]:
    mcq = record.get("mcq", {}) if isinstance(record.get("mcq"), dict) else {}
    question = str(mcq.get("question") or record.get("question") or "").strip()
    choices = _coerce_choices(mcq.get("choices") or record.get("choices") or [])
    correct = mcq.get("correct_choice") or record.get("correct_choice") or {}
    if isinstance(correct, dict):
        correct_label = normalize_label(correct.get("label", ""))
        correct_text = str(correct.get("text") or "").strip()
    else:
        correct_label = normalize_label(correct)
        correct_text = ""
    choice_by_label = {normalize_label(choice["label"]): choice["text"] for choice in choices}
    if correct_label and not correct_text:
        correct_text = choice_by_label.get(correct_label, "")
    if correct_label and correct_text and correct_label not in choice_by_label:
        choices.append({"label": correct_label, "text": correct_text})
    month = str(record.get("month") or "").strip()
    item_no = record.get("no", row_idx + 1)
    item_id = f"{month}:{item_no}" if month else str(item_no)
    return {
        "id": item_id,
        "month": month,
        "no": item_no,
        "paper_link": str(record.get("paper_link") or "").strip(),
        "theorem": str(record.get("theorem") or "").strip(),
        "sketch": str(record.get("sketch") or "").strip(),
        "theorem_type": _coerce_theorem_types(record.get("theorem_type")),
        "question": question,
        "choices": choices,
        "correct_choice": {
            "label": correct_label,
            "text": correct_text,
        },
        "source_path": source_path,
    }


def load_livemathematician_records(path: Path | str) -> list[dict[str, Any]]:
    data_path = Path(path)
    files = _iter_monthly_files(data_path)
    if not files:
        raise ValueError(
            "LiveMathematicianBench requires a qa_*_final.json file or a directory containing such files."
        )
    items: list[dict[str, Any]] = []
    for file_path in files:
        payload = _load_json(file_path)
        if not isinstance(payload, list):
            raise ValueError(f"Expected JSON array in {file_path}")
        for row_idx, record in enumerate(payload):
            normalized = normalize_livemathematician_record(record, row_idx=row_idx, source_path=str(file_path))
            if normalized["question"] and normalized["choices"] and normalized["correct_choice"]["label"]:
                items.append(normalized)
    if not items:
        raise ValueError(f"No valid LiveMathematicianBench items loaded from {data_path}")
    return items


def load_livemathematician_dataset(path: Path | str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    root = Path(path)
    if is_split_dir(root):
        train_records = load_livemathematician_records(root / "train")
        eval_records = load_livemathematician_records(root / "val")
        if not eval_records:
            eval_records = load_livemathematician_records(root / "test")
        return train_records, eval_records or list(train_records)
    records = load_livemathematician_records(root)
    return records, list(records)


def _format_choices(choices: list[dict[str, str]]) -> str:
    return "\n".join(f"{choice['label']}. {choice['text']}" for choice in choices)


def build_livemathematician_samples(records: list[dict[str, Any]]) -> list[SkillSample]:
    samples: list[SkillSample] = []
    for record in records:
        normalized = normalize_livemathematician_record(record)
        prompt = f"{normalized['question']}\n\nChoices:\n{_format_choices(normalized['choices'])}"
        samples.append(
            SkillSample(
                prompt=prompt,
                expected_answer=str(normalized["correct_choice"]["label"]),
                metadata=normalized,
            )
        )
    return samples


def shuffle_livemathematician_choices(record: dict[str, Any], seed: int) -> dict[str, Any]:
    normalized = normalize_livemathematician_record(record)
    digest = hashlib.sha256(f"{seed}:{normalized['id']}".encode("utf-8")).hexdigest()
    rng = random.Random(int(digest[:16], 16))
    shuffled = [dict(choice) for choice in normalized["choices"]]
    rng.shuffle(shuffled)
    correct_label = normalize_label(normalized["correct_choice"]["label"])
    remapped: list[dict[str, str]] = []
    new_correct = dict(normalized["correct_choice"])
    for index, choice in enumerate(shuffled):
        new_label = CHOICE_LABELS[index]
        old_label = normalize_label(choice["label"])
        remapped.append({"label": new_label, "text": choice["text"]})
        if old_label == correct_label:
            new_correct = {"label": new_label, "text": choice["text"]}
    updated = dict(normalized)
    updated["choices"] = remapped
    updated["correct_choice"] = new_correct
    return updated


def extract_answer(text: str) -> str:
    matches = re.findall(r"<answer>(.*?)</answer>", text, re.DOTALL | re.IGNORECASE)
    if matches:
        return matches[-1].strip()
    lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
    return lines[-1] if lines else text.strip()


def parse_choice_label(prediction_text: str, choices: list[dict[str, Any]]) -> str:
    answer = extract_answer(prediction_text)
    label = normalize_label(answer)
    valid_labels = {normalize_label(choice.get("label", "")) for choice in choices}
    if label in valid_labels:
        return label
    answer_lower = answer.lower()
    for choice in choices:
        choice_label = normalize_label(choice.get("label", ""))
        choice_text = str(choice.get("text", "")).strip()
        if choice_text and choice_text.lower() == answer_lower:
            return choice_label
    first_token = normalize_label(answer.split()[0]) if answer.split() else ""
    return first_token if first_token in valid_labels else label


class LiveMathematicianEvaluator(SkillEvaluator):
    def evaluate(self, prediction: str, sample: SkillSample) -> MetricResult:
        choices = list(sample.metadata.get("choices") or [])
        correct_choice = dict(sample.metadata.get("correct_choice") or {"label": sample.expected_answer, "text": ""})
        predicted_label = parse_choice_label(prediction, choices)
        correct_label = normalize_label(correct_choice.get("label", ""))
        predicted_text = ""
        for choice in choices:
            if normalize_label(choice.get("label", "")) == predicted_label:
                predicted_text = str(choice.get("text", "")).strip()
                break
        is_correct = float(predicted_label == correct_label)
        return MetricResult(
            score=is_correct,
            passed=bool(is_correct),
            details={
                "predicted_answer": predicted_label or extract_answer(prediction),
                "predicted_label": predicted_label,
                "predicted_text": predicted_text,
                "correct_label": correct_label,
                "correct_text": str(correct_choice.get("text", "")).strip(),
                "em": is_correct,
                "f1": is_correct,
                "sub_em": is_correct,
            },
        )
