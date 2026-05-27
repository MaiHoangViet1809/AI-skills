from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from darwinSkill.contracts import EvaluationConfig, SkillFeedback, SkillSample, TrainingConfig
from darwinSkill.demo_text import DarwinMemoryBackend, demo_samples
from darwinSkill.evaluators import ExactMatchEvaluator
from darwinSkill.storage import load_run_state
from darwinSkill.trainer import SkillTrainer


class ExplodingEvaluator:
    def evaluate(self, prediction: str, sample: SkillSample):  # type: ignore[no-untyped-def]
        raise RuntimeError("boom")


class ExplodingBackend:
    def predict(self, skill_text: str, sample: SkillSample) -> str:
        raise RuntimeError("predict failed")

    def improve_skill(self, skill_text: str, feedback: list[SkillFeedback]) -> str:
        return skill_text


class TrainerTest(unittest.TestCase):
    def test_trainer_fit_and_evaluate_end_to_end(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            trainer = SkillTrainer(
                backend=DarwinMemoryBackend(),
                evaluator=ExactMatchEvaluator(),
                config=TrainingConfig(
                    num_epochs=1,
                    batch_size=2,
                    output_root=Path(temp_dir),
                    run_name="trainer-test",
                ),
            )

            artifacts = trainer.fit(demo_samples())
            self.assertEqual(artifacts.mean_score, 1.0)
            self.assertTrue(artifacts.summary_path.exists())
            self.assertTrue(artifacts.evaluations_path.exists())
            self.assertIn("Paris", artifacts.final_skill)

            report = trainer.evaluate(
                demo_samples(),
                config=EvaluationConfig(
                    skill_text=artifacts.final_skill,
                    output_root=Path(temp_dir),
                    run_name="trainer-eval",
                ),
            )
            self.assertEqual(report.mean_score, 1.0)
            self.assertEqual(report.pass_rate, 1.0)
            self.assertIsNotNone(report.artifacts)
            self.assertTrue(report.artifacts.run_state_path.exists())

            run_state = load_run_state(report.artifacts.run_state_path)
            self.assertEqual(run_state.run_kind, "evaluate")
            self.assertEqual(run_state.last_stage, "evaluate")
            self.assertEqual(run_state.sample_count, 3)
            self.assertEqual(run_state.evaluation_count, 3)

    def test_evaluate_persists_zero_sample_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            trainer = SkillTrainer(
                backend=DarwinMemoryBackend(),
                evaluator=ExactMatchEvaluator(),
            )

            report = trainer.evaluate(
                [],
                config=EvaluationConfig(
                    skill_text="",
                    output_root=Path(temp_dir),
                    run_name="empty-eval",
                ),
            )

            self.assertEqual(report.sample_count, 0)
            self.assertIsNotNone(report.artifacts)
            self.assertTrue(report.artifacts.summary_path.exists())
            self.assertTrue(report.artifacts.run_state_path.exists())

            run_state = load_run_state(report.artifacts.run_state_path)
            self.assertEqual(run_state.sample_count, 0)
            self.assertEqual(run_state.prediction_count, 0)
            self.assertEqual(run_state.evaluation_count, 0)

    def test_trainer_surfaces_backend_failures(self) -> None:
        trainer = SkillTrainer(
            backend=ExplodingBackend(),
            evaluator=ExactMatchEvaluator(),
        )

        with self.assertRaisesRegex(RuntimeError, "predict failed"):
            trainer.fit(demo_samples())

    def test_trainer_surfaces_evaluator_failures(self) -> None:
        trainer = SkillTrainer(
            backend=DarwinMemoryBackend(),
            evaluator=ExplodingEvaluator(),
        )

        with self.assertRaisesRegex(RuntimeError, "boom"):
            trainer.evaluate(
                demo_samples(),
                config=EvaluationConfig(skill_text="", run_name="exploding-eval"),
            )


if __name__ == "__main__":
    unittest.main()
