from __future__ import annotations

from darwinSkill.contracts import PipelineConfig
from darwinSkill.demo_text import DarwinMemoryBackend, demo_samples
from darwinSkill.evaluators import ExactMatchEvaluator
from darwinSkill.pipeline import SkillPipeline
from darwinSkill.stages import EvaluationStage, ImprovementStage, PredictionStage


def main() -> None:
    pipeline = SkillPipeline(
        [PredictionStage(), EvaluationStage(), ImprovementStage(), PredictionStage(), EvaluationStage()],
        backend=DarwinMemoryBackend(),
        evaluator=ExactMatchEvaluator(),
        config=PipelineConfig(run_name="demo-pipeline"),
    )
    artifacts = pipeline.run(demo_samples())
    print(f"pipeline output: {artifacts.output_dir}")
    print(f"pipeline score: {artifacts.mean_score:.2f}")


if __name__ == "__main__":
    main()
