from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from darwinSkill.benchmarks import build_benchmark_samples, get_benchmark_spec, load_initial_skill
from darwinSkill.demo_text import DarwinMemoryBackend
from darwinSkill.evaluators import ExactMatchEvaluator
from darwinSkill.native import run_reference_adapter, run_reference_benchmark
from darwinSkill.reference_adapters import OfficeQAAdapter
from darwinSkill.contracts import TrainingConfig


class BenchmarksTest(unittest.TestCase):
    def test_reference_skill_assets_are_available(self) -> None:
        spec = get_benchmark_spec("searchqa")
        self.assertTrue(spec.initial_skill_path.exists())
        self.assertTrue(load_initial_skill("searchqa"))

    def test_build_benchmark_samples_uses_family_field_mapping(self) -> None:
        samples = build_benchmark_samples(
            "officeqa",
            [{"question": "Capital of France?", "answer": "Paris", "id": 1}],
        )
        self.assertEqual(samples[0].prompt, "Capital of France?")
        self.assertEqual(samples[0].expected_answer, "Paris")
        self.assertEqual(samples[0].metadata["id"], 1)

    def test_run_reference_benchmark_uses_loaded_initial_skill(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            artifacts = run_reference_benchmark(
                name="searchqa",
                backend=DarwinMemoryBackend(),
                evaluator=ExactMatchEvaluator(),
                records=[
                    {"question": "Capital of France?", "answer": "Paris"},
                    {"question": "Largest planet?", "answer": "Jupiter"},
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
                evaluator=ExactMatchEvaluator(),
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
