from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from darwinSkill.contracts import PipelineConfig
from darwinSkill.demo_text import DarwinMemoryBackend, demo_samples
from darwinSkill.evaluators import ExactMatchEvaluator
from darwinSkill.pipeline import SkillPipeline
from darwinSkill.stages import EvaluationStage, ImprovementStage, PredictionStage


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
            self.assertIn("Jupiter", artifacts.final_skill)


if __name__ == "__main__":
    unittest.main()
