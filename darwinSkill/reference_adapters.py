from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from darwinSkill.adapters import InMemoryDatasetAdapter
from darwinSkill.benchmarks import BenchmarkSpec, build_benchmark_samples, get_benchmark_spec, load_initial_skill
from darwinSkill.contracts import SkillSample


@dataclass(slots=True)
class ReferenceBenchmarkAdapter(InMemoryDatasetAdapter):
    benchmark: BenchmarkSpec | None = field(default=None)

    @classmethod
    def from_records(cls, name: str, records: list[dict[str, Any]]) -> "ReferenceBenchmarkAdapter":
        spec = get_benchmark_spec(name)
        samples = build_benchmark_samples(name, records)
        return cls(train_samples=samples, eval_samples=list(samples), benchmark=spec)

    @property
    def initial_skill(self) -> str:
        if self.benchmark is None:
            raise ValueError("ReferenceBenchmarkAdapter requires a benchmark spec.")
        return load_initial_skill(self.benchmark.name)


class SearchQAAdapter(ReferenceBenchmarkAdapter):
    @classmethod
    def from_records(cls, records: list[dict[str, Any]]) -> "SearchQAAdapter":
        base = super().from_records("searchqa", records)
        return cls(train_samples=base.train_samples, eval_samples=base.eval_samples, benchmark=base.benchmark)


class DocVQAAdapter(ReferenceBenchmarkAdapter):
    @classmethod
    def from_records(cls, records: list[dict[str, Any]]) -> "DocVQAAdapter":
        base = super().from_records("docvqa", records)
        return cls(train_samples=base.train_samples, eval_samples=base.eval_samples, benchmark=base.benchmark)


class OfficeQAAdapter(ReferenceBenchmarkAdapter):
    @classmethod
    def from_records(cls, records: list[dict[str, Any]]) -> "OfficeQAAdapter":
        base = super().from_records("officeqa", records)
        return cls(train_samples=base.train_samples, eval_samples=base.eval_samples, benchmark=base.benchmark)


class ALFWorldAdapter(ReferenceBenchmarkAdapter):
    @classmethod
    def from_records(cls, records: list[dict[str, Any]]) -> "ALFWorldAdapter":
        base = super().from_records("alfworld", records)
        return cls(train_samples=base.train_samples, eval_samples=base.eval_samples, benchmark=base.benchmark)


class SpreadsheetBenchAdapter(ReferenceBenchmarkAdapter):
    @classmethod
    def from_records(cls, records: list[dict[str, Any]]) -> "SpreadsheetBenchAdapter":
        base = super().from_records("spreadsheetbench", records)
        return cls(train_samples=base.train_samples, eval_samples=base.eval_samples, benchmark=base.benchmark)


class LiveMathematicianBenchAdapter(ReferenceBenchmarkAdapter):
    @classmethod
    def from_records(cls, records: list[dict[str, Any]]) -> "LiveMathematicianBenchAdapter":
        base = super().from_records("livemathematicianbench", records)
        return cls(train_samples=base.train_samples, eval_samples=base.eval_samples, benchmark=base.benchmark)
