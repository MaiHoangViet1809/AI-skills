from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from darwinSkill.src.contracts import TrainingConfig
from darwinSkill.src.demo_text import DarwinMemoryBackend, demo_samples
from darwinSkill.src.inspection import inspect_run, load_step_record, summarize_run
from darwinSkill.src.native import run_reference_benchmark_from_path
from darwinSkill.src.trainer import SkillTrainer
from darwinSkill.src.evaluators import ExactMatchEvaluator


class InspectionTest(unittest.TestCase):
    def test_inspection_helpers_expose_step_and_epoch_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            trainer = SkillTrainer(
                backend=DarwinMemoryBackend(),
                evaluator=ExactMatchEvaluator(),
                config=TrainingConfig(
                    num_epochs=2,
                    batch_size=1,
                    edit_budget=1,
                    output_root=Path(temp_dir),
                    run_name="inspect-run",
                ),
            )
            artifacts = trainer.fit(demo_samples())

            inspection = inspect_run(artifacts.output_dir)
            summary = summarize_run(artifacts.output_dir)
            first_step = load_step_record(artifacts.output_dir, 1)

            self.assertEqual(inspection.summary["run_name"], "inspect-run")
            self.assertGreaterEqual(len(inspection.steps), 1)
            self.assertGreaterEqual(len(inspection.epochs["slow_update"]), 1)
            self.assertGreaterEqual(len(inspection.epochs["meta_skill"]), 1)
            self.assertIn("gate", first_step)
            self.assertEqual(summary["run_name"], "inspect-run")
            self.assertGreaterEqual(summary["step_count"], 1)

    def test_run_reference_benchmark_from_path_uses_dataset_loader(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            for split, answer in (("train", "Paris"), ("val", "Rome"), ("test", "Berlin")):
                split_dir = root / split
                split_dir.mkdir(parents=True)
                (split_dir / "items.json").write_text(
                    json.dumps([{"id": split, "question": f"Capital {split}?", "answers": [answer]}]),
                    encoding="utf-8",
                )

            artifacts = run_reference_benchmark_from_path(
                name="searchqa",
                path=str(root),
                backend=DarwinMemoryBackend(),
                config=TrainingConfig(
                    num_epochs=1,
                    batch_size=1,
                    edit_budget=1,
                    output_root=root / "outputs",
                    run_name="searchqa-path-run",
                ),
            )
            self.assertEqual(artifacts.sample_count, 1)
            self.assertEqual(artifacts.mean_score, 0.0)


if __name__ == "__main__":
    unittest.main()
