from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from darwinSkill.src.contracts import PipelineConfig, RunContext
from darwinSkill.src.demo_text import DarwinMemoryBackend, demo_samples
from darwinSkill.src.evaluators import ExactMatchEvaluator
from darwinSkill.src.pipeline import SkillPipeline
from darwinSkill.src.stages import EvaluationStage, ImprovementStage, PredictionStage
from darwinSkill.src.storage import isoformat, utc_now


class PipelineTest(unittest.TestCase):
    def test_linear_pipeline_runtime_reuses_shared_contracts(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            pipeline = SkillPipeline(
                [PredictionStage(), EvaluationStage(), ImprovementStage(), PredictionStage(), EvaluationStage()],
                backend=DarwinMemoryBackend(),
                evaluator=ExactMatchEvaluator(),
                config=PipelineConfig(
                    output_root=Path(temp_dir),
                    run_name="pipeline-test",
                ),
            )

            artifacts = pipeline.run(demo_samples())
            self.assertEqual(artifacts.mean_score, 1.0)
            self.assertTrue(artifacts.history_path.exists())
            self.assertTrue(artifacts.run_state_path.exists())
            self.assertIn("Jupiter", artifacts.final_skill)

    def test_pipeline_requires_evaluation_before_persistence(self) -> None:
        pipeline = SkillPipeline(
            [PredictionStage()],
            backend=DarwinMemoryBackend(),
            evaluator=ExactMatchEvaluator(),
        )

        with self.assertRaisesRegex(ValueError, "requires an EvaluationStage"):
            pipeline.run(demo_samples())

    def test_stage_ordering_failures_raise_clear_errors(self) -> None:
        context = RunContext(
            run_id="run123",
            run_name="pipeline-order",
            run_kind="pipeline",
            output_root=Path("../../darwinSkill/tests"),
            samples=demo_samples(),
            skill_text="",
            backend=DarwinMemoryBackend(),
            evaluator=ExactMatchEvaluator(),
            started_at=isoformat(utc_now()),
            history=[],
        )

        with self.assertRaisesRegex(ValueError, "Predictions must align"):
            EvaluationStage().run(context)

        predicted = PredictionStage().run(context)
        with self.assertRaisesRegex(ValueError, "Evaluations must exist"):
            ImprovementStage().run(predicted)


if __name__ == "__main__":
    unittest.main()
