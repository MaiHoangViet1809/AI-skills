from __future__ import annotations

from darwinSkill.src.contracts import EvaluationConfig, TrainingConfig
from darwinSkill.src.demo_text import DarwinMemoryBackend, demo_samples
from darwinSkill.src.evaluators import ExactMatchEvaluator
from darwinSkill.src.trainer import SkillTrainer


def main() -> None:
    trainer = SkillTrainer(
        backend=DarwinMemoryBackend(),
        evaluator=ExactMatchEvaluator(),
        config=TrainingConfig(num_epochs=1, batch_size=2, run_name="demo-train"),
    )
    samples = demo_samples()
    artifacts = trainer.fit(samples)
    report = trainer.evaluate(
        samples,
        config=EvaluationConfig(
            skill_text=artifacts.final_skill,
            run_name="demo-evaluate",
        ),
    )

    print(f"train output: {artifacts.output_dir}")
    print(f"final train score: {artifacts.mean_score:.2f}")
    print(f"eval score: {report.mean_score:.2f}")
    if report.artifacts is not None:
        print(f"eval output: {report.artifacts.output_dir}")


if __name__ == "__main__":
    main()
