from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from darwinSkill.contracts import SkillSample


_REPO_ROOT = Path(__file__).resolve().parent.parent
_REFERENCE_ROOT = _REPO_ROOT / "references" / "SkillOpt" / "skillopt" / "envs"


@dataclass(slots=True, frozen=True)
class BenchmarkSpec:
    name: str
    family: str
    initial_skill_path: Path
    prompt_field: str
    answer_field: str


def _spec(name: str, family: str, prompt_field: str, answer_field: str) -> BenchmarkSpec:
    return BenchmarkSpec(
        name=name,
        family=family,
        initial_skill_path=_REFERENCE_ROOT / name / "skills" / "initial.md",
        prompt_field=prompt_field,
        answer_field=answer_field,
    )


BENCHMARKS: dict[str, BenchmarkSpec] = {
    "searchqa": _spec("searchqa", "text-doc", "question", "answer"),
    "docvqa": _spec("docvqa", "text-doc", "question", "answer"),
    "officeqa": _spec("officeqa", "text-doc", "question", "answer"),
    "alfworld": _spec("alfworld", "interactive-tool", "task_description", "answer"),
    "spreadsheetbench": _spec("spreadsheetbench", "interactive-tool", "instruction", "answer"),
    "livemathematicianbench": _spec("livemathematicianbench", "interactive-tool", "question", "answer"),
}


def get_benchmark_spec(name: str) -> BenchmarkSpec:
    key = name.strip().lower()
    if key not in BENCHMARKS:
        raise KeyError(f"Unknown benchmark: {name}")
    return BENCHMARKS[key]


def load_initial_skill(name: str) -> str:
    spec = get_benchmark_spec(name)
    return spec.initial_skill_path.read_text(encoding="utf-8")


def build_benchmark_samples(name: str, records: list[dict[str, Any]]) -> list[SkillSample]:
    spec = get_benchmark_spec(name)
    samples: list[SkillSample] = []
    for record in records:
        prompt = record.get(spec.prompt_field, record.get("prompt", record.get("instruction", "")))
        answer = record.get(spec.answer_field, record.get("expected_answer", record.get("label", "")))
        metadata = dict(record)
        samples.append(
            SkillSample(
                prompt=str(prompt),
                expected_answer=str(answer),
                metadata=metadata,
            )
        )
    return samples

