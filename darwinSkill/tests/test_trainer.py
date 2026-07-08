from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from darwinSkill.src.contracts import EvaluationConfig, SkillFeedback, SkillSample, TrainingConfig
from darwinSkill.src.demo_text import DarwinMemoryBackend, demo_samples
from darwinSkill.src.evaluators import ExactMatchEvaluator
from darwinSkill.src.storage import load_run_state
from darwinSkill.src.trainer import SkillTrainer


class ExplodingEvaluator:
    def evaluate(self, prediction: str, sample: SkillSample):  # type: ignore[no-untyped-def]
        raise RuntimeError("boom")


class ExplodingBackend:
    def predict(self, skill_text: str, sample: SkillSample) -> str:
        raise RuntimeError("predict failed")

    def improve_skill(self, skill_text: str, feedback: list[SkillFeedback]) -> str:
        return skill_text


class RejectingBackend(DarwinMemoryBackend):
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

    def test_reflective_engine_persists_step_and_epoch_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            trainer = SkillTrainer(
                backend=DarwinMemoryBackend(),
                evaluator=ExactMatchEvaluator(),
                config=TrainingConfig(
                    num_epochs=2,
                    batch_size=1,
                    edit_budget=1,
                    output_root=Path(temp_dir),
                    run_name="reflective-engine",
                ),
            )

            artifacts = trainer.fit(demo_samples())
            self.assertTrue((artifacts.output_dir / "steps" / "step_0001" / "step_record.json").exists())
            self.assertTrue((artifacts.output_dir / "skills" / "skill_v0001.md").exists())
            self.assertTrue((artifacts.output_dir / "best_skill.md").exists())
            self.assertTrue((artifacts.output_dir / "slow_update" / "epoch_01" / "slow_update.json").exists())
            self.assertTrue((artifacts.output_dir / "meta_skill" / "epoch_01" / "meta_skill.json").exists())

            run_state = load_run_state(artifacts.run_state_path)
            self.assertGreaterEqual(run_state.current_step, 1)
            self.assertGreaterEqual(run_state.best_score, 1.0)

    def test_gate_can_reject_candidate_updates(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            trainer = SkillTrainer(
                backend=RejectingBackend(),
                evaluator=ExactMatchEvaluator(),
                config=TrainingConfig(
                    num_epochs=1,
                    batch_size=1,
                    edit_budget=1,
                    output_root=Path(temp_dir),
                    run_name="rejecting-engine",
                ),
            )

            artifacts = trainer.fit(demo_samples())
            run_state = load_run_state(artifacts.run_state_path)
            self.assertEqual(run_state.last_action, "reject")
            self.assertEqual(run_state.best_score, 0.0)

    def test_trainer_can_resume_from_saved_run_state(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            first = SkillTrainer(
                backend=DarwinMemoryBackend(),
                evaluator=ExactMatchEvaluator(),
                config=TrainingConfig(
                    num_epochs=1,
                    batch_size=1,
                    edit_budget=1,
                    output_root=Path(temp_dir),
                    run_name="resume-engine",
                ),
            ).fit(demo_samples())

            resumed = SkillTrainer(
                backend=DarwinMemoryBackend(),
                evaluator=ExactMatchEvaluator(),
                config=TrainingConfig(
                    num_epochs=2,
                    batch_size=1,
                    edit_budget=1,
                    output_root=Path(temp_dir),
                    run_name="resume-engine",
                    resume_from=first.output_dir,
                ),
            ).fit(demo_samples())

            resumed_state = load_run_state(resumed.run_state_path)
            self.assertEqual(resumed.output_dir, first.output_dir)
            self.assertGreaterEqual(resumed_state.current_step, 6)


if __name__ == "__main__":
    unittest.main()
