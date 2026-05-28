from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from darwinSkill.benchmarks import (
    build_benchmark_evaluator,
    build_benchmark_samples,
    get_benchmark_spec,
    load_initial_skill,
    resolve_benchmark_name,
)
from darwinSkill.demo_text import DarwinMemoryBackend
from darwinSkill.native import run_reference_adapter, run_reference_benchmark
from darwinSkill.reference_adapters import OfficeQAAdapter, build_reference_adapter, list_reference_adapters
from darwinSkill.contracts import TrainingConfig


class BenchmarksTest(unittest.TestCase):
    def test_reference_skill_assets_are_available(self) -> None:
        spec = get_benchmark_spec("searchqa")
        self.assertTrue(spec.initial_skill_path.exists())
        self.assertTrue(load_initial_skill("searchqa"))

    def test_benchmark_aliases_and_adapter_registry_are_resolved(self) -> None:
        self.assertEqual(resolve_benchmark_name("spreadsheet_bench"), "spreadsheetbench")
        self.assertIn("officeqa", list_reference_adapters())
        adapter = build_reference_adapter(
            "office_qa",
            records=[{"question": "Capital of France?", "answer": "Paris"}],
        )
        self.assertEqual(adapter.benchmark.name, "officeqa")

    def test_build_benchmark_samples_uses_family_field_mapping(self) -> None:
        samples = build_benchmark_samples(
            "officeqa",
            [{"question": "Capital of France?", "answer": "Paris", "id": 1}],
        )
        self.assertEqual(samples[0].prompt, "Capital of France?")
        self.assertEqual(samples[0].expected_answer, "Paris")
        self.assertEqual(samples[0].metadata["id"], "1")

    def test_build_benchmark_evaluator_returns_env_specific_metric(self) -> None:
        evaluator = build_benchmark_evaluator("searchqa")
        sample = build_benchmark_samples(
            "searchqa",
            [{"question": "Capital of France?", "answers": ["Paris"]}],
        )[0]
        metric = evaluator.evaluate("<answer>Paris</answer>", sample)
        self.assertTrue(metric.passed)
        self.assertEqual(metric.details["em"], 1.0)

    def test_run_reference_benchmark_uses_loaded_initial_skill(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            artifacts = run_reference_benchmark(
                name="searchqa",
                backend=DarwinMemoryBackend(),
                records=[
                    {"question": "Capital of France?", "answers": ["Paris"]},
                    {"question": "Largest planet?", "answers": ["Jupiter"]},
                ],
                config=TrainingConfig(
                    num_epochs=1,
                    batch_size=1,
                    edit_budget=1,
                    output_root=Path(temp_dir),
                    run_name="searchqa-benchmark",
                ),
            )
            self.assertEqual(artifacts.mean_score, 1.0)
            self.assertTrue(artifacts.best_skill_path.exists())

    def test_reference_adapter_wraps_records_and_initial_skill(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            adapter = OfficeQAAdapter.from_records(
                [{"question": "Capital of France?", "answer": "Paris"}]
            )
            artifacts = run_reference_adapter(
                backend=DarwinMemoryBackend(),
                adapter=adapter,
                config=TrainingConfig(
                    num_epochs=1,
                    batch_size=1,
                    edit_budget=1,
                    output_root=Path(temp_dir),
                    run_name="officeqa-benchmark",
                ),
            )
            self.assertEqual(artifacts.mean_score, 1.0)
            self.assertTrue(adapter.initial_skill)


if __name__ == "__main__":
    unittest.main()
