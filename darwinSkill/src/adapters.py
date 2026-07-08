from __future__ import annotations

from dataclasses import dataclass, field

from darwinSkill.src.contracts import BatchSpec, DatasetAdapter, SkillSample, TrainingConfig


@dataclass(slots=True)
class InMemoryDatasetAdapter(DatasetAdapter):
    train_samples: list[SkillSample]
    eval_samples: list[SkillSample] = field(default_factory=list)

    def get_train_samples(self) -> list[SkillSample]:
        return list(self.train_samples)

    def get_eval_samples(self) -> list[SkillSample]:
        return list(self.eval_samples or self.train_samples)

    def build_batches(self, config: TrainingConfig) -> list[BatchSpec]:
        batches: list[BatchSpec] = []
        step = 0
        for epoch in range(1, config.num_epochs + 1):
            for index in range(0, len(self.train_samples), config.batch_size):
                step += 1
                batches.append(
                    BatchSpec(
                        epoch=epoch,
                        step=step,
                        samples=list(self.train_samples[index : index + config.batch_size]),
                    )
                )
        return batches or [BatchSpec(epoch=1, step=1, samples=[])]

