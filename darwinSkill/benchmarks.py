from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from darwinSkill.alfworld_env import ALFWorldEvaluator, build_alfworld_samples, load_alfworld_dataset
from darwinSkill.docvqa_env import DocVQAEvaluator, build_docvqa_samples, load_docvqa_dataset
from darwinSkill.evaluators import ExactMatchEvaluator
from darwinSkill.livemathematician_env import (
    LiveMathematicianEvaluator,
    build_livemathematician_samples,
    load_livemathematician_dataset,
)
from darwinSkill.officeqa_env import OfficeQAEvaluator, build_officeqa_samples, load_officeqa_dataset
from darwinSkill.reference_assets import get_initial_skill_path, load_initial_skill_text
from darwinSkill.searchqa_env import SearchQAEvaluator, build_searchqa_samples, load_searchqa_dataset
from darwinSkill.spreadsheetbench_env import (
    SpreadsheetBenchEvaluator,
    build_spreadsheetbench_samples,
    load_spreadsheetbench_dataset,
)
from darwinSkill.contracts import SkillSample
from darwinSkill.contracts import SkillEvaluator


@dataclass(slots=True, frozen=True)
class BenchmarkSpec:
    name: str
    family: str
    initial_skill_path: Path
    prompt_field: str
    answer_field: str
    sample_builder: Callable[[list[dict[str, Any]]], list[SkillSample]]
    evaluator_factory: Callable[[], SkillEvaluator]
    dataset_loader: Callable[[Path | str], tuple[list[dict[str, Any]], list[dict[str, Any]]]] | None = None


def _build_generic_samples(records: list[dict[str, Any]], *, prompt_field: str, answer_field: str) -> list[SkillSample]:
    samples: list[SkillSample] = []
    for record in records:
        prompt = record.get(prompt_field, record.get("prompt", record.get("instruction", "")))
        answer = record.get(answer_field, record.get("expected_answer", record.get("label", "")))
        samples.append(
            SkillSample(
                prompt=str(prompt),
                expected_answer=str(answer),
                metadata=dict(record),
            )
        )
    return samples


def _spec(
    name: str,
    family: str,
    prompt_field: str,
    answer_field: str,
    *,
    sample_builder: Callable[[list[dict[str, Any]]], list[SkillSample]] | None = None,
    evaluator_factory: Callable[[], SkillEvaluator] | None = None,
    dataset_loader: Callable[[Path | str], tuple[list[dict[str, Any]], list[dict[str, Any]]]] | None = None,
) -> BenchmarkSpec:
    return BenchmarkSpec(
        name=name,
        family=family,
        initial_skill_path=get_initial_skill_path(name),
        prompt_field=prompt_field,
        answer_field=answer_field,
        sample_builder=sample_builder or (lambda records: _build_generic_samples(records, prompt_field=prompt_field, answer_field=answer_field)),
        evaluator_factory=evaluator_factory or ExactMatchEvaluator,
        dataset_loader=dataset_loader,
    )


BENCHMARKS: dict[str, BenchmarkSpec] = {
    "searchqa": _spec(
        "searchqa",
        "text-doc",
        "question",
        "answer",
        sample_builder=build_searchqa_samples,
        evaluator_factory=SearchQAEvaluator,
        dataset_loader=load_searchqa_dataset,
    ),
    "docvqa": _spec(
        "docvqa",
        "text-doc",
        "question",
        "answer",
        sample_builder=build_docvqa_samples,
        evaluator_factory=DocVQAEvaluator,
        dataset_loader=load_docvqa_dataset,
    ),
    "officeqa": _spec(
        "officeqa",
        "text-doc",
        "question",
        "answer",
        sample_builder=build_officeqa_samples,
        evaluator_factory=OfficeQAEvaluator,
        dataset_loader=load_officeqa_dataset,
    ),
    "alfworld": _spec(
        "alfworld",
        "interactive-tool",
        "task_description",
        "answer",
        sample_builder=build_alfworld_samples,
        evaluator_factory=ALFWorldEvaluator,
        dataset_loader=load_alfworld_dataset,
    ),
    "spreadsheetbench": _spec(
        "spreadsheetbench",
        "interactive-tool",
        "instruction",
        "answer",
        sample_builder=build_spreadsheetbench_samples,
        evaluator_factory=SpreadsheetBenchEvaluator,
        dataset_loader=load_spreadsheetbench_dataset,
    ),
    "livemathematicianbench": _spec(
        "livemathematicianbench",
        "interactive-tool",
        "question",
        "answer",
        sample_builder=build_livemathematician_samples,
        evaluator_factory=LiveMathematicianEvaluator,
        dataset_loader=load_livemathematician_dataset,
    ),
}


def get_benchmark_spec(name: str) -> BenchmarkSpec:
    key = name.strip().lower()
    if key not in BENCHMARKS:
        raise KeyError(f"Unknown benchmark: {name}")
    return BENCHMARKS[key]


def load_initial_skill(name: str) -> str:
    _ = get_benchmark_spec(name)
    return load_initial_skill_text(name)


def build_benchmark_samples(name: str, records: list[dict[str, Any]]) -> list[SkillSample]:
    spec = get_benchmark_spec(name)
    return spec.sample_builder(records)


def build_benchmark_evaluator(name: str) -> SkillEvaluator:
    spec = get_benchmark_spec(name)
    return spec.evaluator_factory()


def load_benchmark_dataset(name: str, path: Path | str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    spec = get_benchmark_spec(name)
    if spec.dataset_loader is None:
        raise ValueError(f"Benchmark {name} does not provide a dataset loader.")
    return spec.dataset_loader(path)
