from __future__ import annotations

import os
import sys

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(os.path.dirname(_SCRIPT_DIR))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from darwinSkill.contracts import EvaluationConfig, TrainingConfig
from darwinSkill.demo_text import DarwinMemoryBackend, demo_samples
from darwinSkill.evaluators import ExactMatchEvaluator
from darwinSkill.trainer import SkillTrainer


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


if __name__ == "__main__":
    main()
