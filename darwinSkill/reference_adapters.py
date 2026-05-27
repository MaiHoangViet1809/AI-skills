from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from darwinSkill.adapters import InMemoryDatasetAdapter
from darwinSkill.benchmarks import (
    BenchmarkSpec,
    build_benchmark_samples,
    get_benchmark_spec,
    load_benchmark_dataset,
    load_initial_skill,
)


@dataclass(slots=True)
class ReferenceBenchmarkAdapter(InMemoryDatasetAdapter):
    benchmark: BenchmarkSpec | None = field(default=None)

    @classmethod
    def from_records(cls, name: str, records: list[dict[str, Any]]) -> "ReferenceBenchmarkAdapter":
        spec = get_benchmark_spec(name)
        samples = build_benchmark_samples(name, records)
        return cls(train_samples=samples, eval_samples=list(samples), benchmark=spec)

    @classmethod
    def from_path(cls, name: str, path: str) -> "ReferenceBenchmarkAdapter":
        spec = get_benchmark_spec(name)
        train_records, eval_records = load_benchmark_dataset(name, path)
        train_samples = build_benchmark_samples(name, train_records)
        eval_samples = build_benchmark_samples(name, eval_records)
        return cls(train_samples=train_samples, eval_samples=eval_samples, benchmark=spec)

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

    @classmethod
    def from_path(cls, path: str) -> "SearchQAAdapter":
        base = super().from_path("searchqa", path)
        return cls(train_samples=base.train_samples, eval_samples=base.eval_samples, benchmark=base.benchmark)


class DocVQAAdapter(ReferenceBenchmarkAdapter):
    @classmethod
    def from_records(cls, records: list[dict[str, Any]]) -> "DocVQAAdapter":
        base = super().from_records("docvqa", records)
        return cls(train_samples=base.train_samples, eval_samples=base.eval_samples, benchmark=base.benchmark)

    @classmethod
    def from_path(cls, path: str) -> "DocVQAAdapter":
        base = super().from_path("docvqa", path)
        return cls(train_samples=base.train_samples, eval_samples=base.eval_samples, benchmark=base.benchmark)


class OfficeQAAdapter(ReferenceBenchmarkAdapter):
    @classmethod
    def from_records(cls, records: list[dict[str, Any]]) -> "OfficeQAAdapter":
        base = super().from_records("officeqa", records)
        return cls(train_samples=base.train_samples, eval_samples=base.eval_samples, benchmark=base.benchmark)

    @classmethod
    def from_path(cls, path: str) -> "OfficeQAAdapter":
        base = super().from_path("officeqa", path)
        return cls(train_samples=base.train_samples, eval_samples=base.eval_samples, benchmark=base.benchmark)


class ALFWorldAdapter(ReferenceBenchmarkAdapter):
    @classmethod
    def from_records(cls, records: list[dict[str, Any]]) -> "ALFWorldAdapter":
        base = super().from_records("alfworld", records)
        return cls(train_samples=base.train_samples, eval_samples=base.eval_samples, benchmark=base.benchmark)

    @classmethod
    def from_path(cls, path: str) -> "ALFWorldAdapter":
        base = super().from_path("alfworld", path)
        return cls(train_samples=base.train_samples, eval_samples=base.eval_samples, benchmark=base.benchmark)


class SpreadsheetBenchAdapter(ReferenceBenchmarkAdapter):
    @classmethod
    def from_records(cls, records: list[dict[str, Any]]) -> "SpreadsheetBenchAdapter":
        base = super().from_records("spreadsheetbench", records)
        return cls(train_samples=base.train_samples, eval_samples=base.eval_samples, benchmark=base.benchmark)

    @classmethod
    def from_path(cls, path: str) -> "SpreadsheetBenchAdapter":
        base = super().from_path("spreadsheetbench", path)
        return cls(train_samples=base.train_samples, eval_samples=base.eval_samples, benchmark=base.benchmark)


class LiveMathematicianBenchAdapter(ReferenceBenchmarkAdapter):
    @classmethod
    def from_records(cls, records: list[dict[str, Any]]) -> "LiveMathematicianBenchAdapter":
        base = super().from_records("livemathematicianbench", records)
        return cls(train_samples=base.train_samples, eval_samples=base.eval_samples, benchmark=base.benchmark)

    @classmethod
    def from_path(cls, path: str) -> "LiveMathematicianBenchAdapter":
        base = super().from_path("livemathematicianbench", path)
        return cls(train_samples=base.train_samples, eval_samples=base.eval_samples, benchmark=base.benchmark)
