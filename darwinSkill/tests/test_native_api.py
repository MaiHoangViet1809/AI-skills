from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from darwinSkill.src.adapters import InMemoryDatasetAdapter
from darwinSkill.src.contracts import EvaluationConfig, SkillFeedback, TrainingConfig
from darwinSkill.src.demo_text import DarwinMemoryBackend, demo_samples
from darwinSkill.src.evaluators import ExactMatchEvaluator
from darwinSkill.src.native import run_evaluation, run_training, run_with_adapter


class OptimizerOnlyBackend:
    def __init__(self) -> None:
        self.applied = 0

    def improve_skill(self, skill_text: str, feedback: list[SkillFeedback]) -> str:
        self.applied += len(feedback)
        return DarwinMemoryBackend().improve_skill(skill_text, feedback)


class TargetOnlyBackend:
    def predict(self, skill_text, sample):  # type: ignore[no-untyped-def]
        return DarwinMemoryBackend().predict(skill_text, sample)


class NativeApiTest(unittest.TestCase):
    def test_run_training_and_evaluation_helpers(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            artifacts = run_training(
                backend=DarwinMemoryBackend(),
                evaluator=ExactMatchEvaluator(),
                samples=demo_samples(),
                config=TrainingConfig(output_root=Path(temp_dir), run_name="native-train"),
            )
            self.assertEqual(artifacts.mean_score, 1.0)

            report = run_evaluation(
                backend=DarwinMemoryBackend(),
                evaluator=ExactMatchEvaluator(),
                samples=demo_samples(),
                config=EvaluationConfig(
                    skill_text=artifacts.final_skill,
                    output_root=Path(temp_dir),
                    run_name="native-eval",
                ),
            )
            self.assertEqual(report.mean_score, 1.0)
            self.assertIsNotNone(report.artifacts)

    def test_run_with_adapter(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            adapter = InMemoryDatasetAdapter(train_samples=demo_samples())
            artifacts = run_with_adapter(
                backend=DarwinMemoryBackend(),
                evaluator=ExactMatchEvaluator(),
                adapter=adapter,
                config=TrainingConfig(output_root=Path(temp_dir), run_name="adapter-train"),
            )
            self.assertEqual(artifacts.mean_score, 1.0)

    def test_run_with_adapter_uses_eval_split_for_final_report(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            adapter = InMemoryDatasetAdapter(
                train_samples=[demo_samples()[0]],
                eval_samples=[demo_samples()[1]],
            )
            artifacts = run_with_adapter(
                backend=DarwinMemoryBackend(),
                evaluator=ExactMatchEvaluator(),
                adapter=adapter,
                config=TrainingConfig(
                    num_epochs=1,
                    batch_size=1,
                    edit_budget=1,
                    output_root=Path(temp_dir),
                    run_name="adapter-eval-split",
                ),
            )
            self.assertEqual(artifacts.sample_count, 1)
            self.assertEqual(artifacts.mean_score, 0.0)


if __name__ == "__main__":
    unittest.main()
