from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from darwinSkill.contracts import EvaluationConfig, TrainingConfig
from darwinSkill.demo_text import DarwinMemoryBackend, demo_samples
from darwinSkill.evaluators import ExactMatchEvaluator
from darwinSkill.trainer import SkillTrainer


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


if __name__ == "__main__":
    unittest.main()
