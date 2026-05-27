from __future__ import annotations

from darwinSkill.adapters import InMemoryDatasetAdapter
from darwinSkill.benchmarks import (
    build_benchmark_evaluator,
    build_benchmark_samples,
    load_benchmark_dataset,
    load_initial_skill,
)
from darwinSkill.contracts import EvaluationConfig, EvaluationReport, RunArtifacts, SkillBackend, SkillEvaluator, SkillSample, TrainingConfig
from darwinSkill.reference_adapters import ReferenceBenchmarkAdapter
from darwinSkill.trainer import SkillTrainer


def build_trainer(
    *,
    backend: SkillBackend,
    evaluator: SkillEvaluator,
    config: TrainingConfig | None = None,
) -> SkillTrainer:
    return SkillTrainer(backend=backend, evaluator=evaluator, config=config)


def run_training(
    *,
    backend: SkillBackend,
    evaluator: SkillEvaluator,
    samples: list[SkillSample],
    config: TrainingConfig | None = None,
    eval_samples: list[SkillSample] | None = None,
) -> RunArtifacts:
    trainer = build_trainer(backend=backend, evaluator=evaluator, config=config)
    return trainer.fit(samples, config=config, eval_samples=eval_samples)


def run_evaluation(
    *,
    backend: SkillBackend,
    evaluator: SkillEvaluator,
    samples: list[SkillSample],
    config: EvaluationConfig,
) -> EvaluationReport:
    trainer = build_trainer(backend=backend, evaluator=evaluator)
    return trainer.evaluate(samples, config=config)


def run_with_adapter(
    *,
    backend: SkillBackend,
    evaluator: SkillEvaluator,
    adapter: InMemoryDatasetAdapter,
    config: TrainingConfig | None = None,
) -> RunArtifacts:
    trainer = build_trainer(backend=backend, evaluator=evaluator, config=config)
    return trainer.fit(
        adapter.get_train_samples(),
        config=config,
        eval_samples=adapter.get_eval_samples(),
    )


def run_reference_benchmark(
    *,
    name: str,
    backend: SkillBackend,
    evaluator: SkillEvaluator | None = None,
    records: list[dict[str, object]],
    config: TrainingConfig | None = None,
) -> RunArtifacts:
    samples = build_benchmark_samples(name, records)
    active_config = config or TrainingConfig()
    benchmark_config = TrainingConfig(
        num_epochs=active_config.num_epochs,
        batch_size=active_config.batch_size,
        edit_budget=active_config.edit_budget,
        initial_skill=load_initial_skill(name),
        output_root=active_config.output_root,
        run_name=active_config.run_name,
        resume_from=active_config.resume_from,
        use_slow_update=active_config.use_slow_update,
        use_meta_skill=active_config.use_meta_skill,
    )
    return run_training(
        backend=backend,
        evaluator=evaluator or build_benchmark_evaluator(name),
        samples=samples,
        config=benchmark_config,
        eval_samples=list(samples),
    )


def run_reference_benchmark_from_path(
    *,
    name: str,
    path: str,
    backend: SkillBackend,
    evaluator: SkillEvaluator | None = None,
    config: TrainingConfig | None = None,
) -> RunArtifacts:
    train_records, eval_records = load_benchmark_dataset(name, path)
    train_samples = build_benchmark_samples(name, train_records)
    eval_samples = build_benchmark_samples(name, eval_records)
    active_config = config or TrainingConfig()
    benchmark_config = TrainingConfig(
        num_epochs=active_config.num_epochs,
        batch_size=active_config.batch_size,
        edit_budget=active_config.edit_budget,
        initial_skill=load_initial_skill(name),
        output_root=active_config.output_root,
        run_name=active_config.run_name,
        resume_from=active_config.resume_from,
        use_slow_update=active_config.use_slow_update,
        use_meta_skill=active_config.use_meta_skill,
    )
    return run_training(
        backend=backend,
        evaluator=evaluator or build_benchmark_evaluator(name),
        samples=train_samples,
        config=benchmark_config,
        eval_samples=eval_samples,
    )


def run_reference_adapter(
    *,
    backend: SkillBackend,
    evaluator: SkillEvaluator | None = None,
    adapter: ReferenceBenchmarkAdapter,
    config: TrainingConfig | None = None,
) -> RunArtifacts:
    active_config = config or TrainingConfig()
    if adapter.benchmark is None:
        raise ValueError("Reference benchmark adapters require an attached benchmark spec.")
    benchmark_config = TrainingConfig(
        num_epochs=active_config.num_epochs,
        batch_size=active_config.batch_size,
        edit_budget=active_config.edit_budget,
        initial_skill=adapter.initial_skill,
        output_root=active_config.output_root,
        run_name=active_config.run_name,
        resume_from=active_config.resume_from,
        use_slow_update=active_config.use_slow_update,
        use_meta_skill=active_config.use_meta_skill,
    )
    return run_with_adapter(
        backend=backend,
        evaluator=evaluator or build_benchmark_evaluator(adapter.benchmark.name),
        adapter=adapter,
        config=benchmark_config,
    )
