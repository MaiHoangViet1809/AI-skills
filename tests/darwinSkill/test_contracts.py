from __future__ import annotations

import unittest

from darwinSkill.contracts import EvaluationReport, MetricResult, PipelineConfig, SkillSample, TrainingConfig
from darwinSkill.evaluators import ExactMatchEvaluator


class ContractsTest(unittest.TestCase):
    def test_text_skill_contracts_are_constructible(self) -> None:
        sample = SkillSample(prompt="Capital of France?", expected_answer="Paris")
        evaluator = ExactMatchEvaluator()
        metric = evaluator.evaluate("Paris", sample)
        report = EvaluationReport(
            sample_count=1,
            mean_score=metric.score,
            pass_rate=1.0,
            skill_text="remember: Capital of France? => Paris",
            results=[],
        )
        config = TrainingConfig()

        self.assertEqual(sample.prompt, "Capital of France?")
        self.assertTrue(metric.passed)
        self.assertEqual(report.sample_count, 1)
        self.assertEqual(str(config.output_root), "outputs/darwinSkill")

    def test_exact_match_evaluator_normalizes_whitespace_and_case(self) -> None:
        sample = SkillSample(prompt="Largest planet?", expected_answer="Jupiter")
        metric: MetricResult = ExactMatchEvaluator().evaluate("  jupiter  ", sample)
        self.assertTrue(metric.passed)
        self.assertEqual(metric.score, 1.0)

    def test_configs_reject_invalid_values(self) -> None:
        with self.assertRaises(ValueError):
            TrainingConfig(num_epochs=0)
        with self.assertRaises(ValueError):
            TrainingConfig(batch_size=0)
        with self.assertRaises(ValueError):
            PipelineConfig(run_name="  ")


if __name__ == "__main__":
    unittest.main()
