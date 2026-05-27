from __future__ import annotations

from darwinSkill.contracts import (
    EvaluationConfig,
    EvaluationReport,
    RunArtifacts,
    RunContext,
    SkillBackend,
    SkillEvaluator,
    SkillSample,
    TrainingConfig,
)
from darwinSkill.storage import LocalArtifactStore, isoformat, make_run_id, utc_now
from darwinSkill.stages import EvaluationStage, ImprovementStage, PredictionStage, run_stages


def _batched(samples: list[SkillSample], batch_size: int) -> list[list[SkillSample]]:
    return [
        samples[index : index + batch_size]
        for index in range(0, len(samples), batch_size)
    ]


class SkillTrainer:
    def __init__(
        self,
        *,
        backend: SkillBackend,
        evaluator: SkillEvaluator,
        artifact_store: LocalArtifactStore | None = None,
        config: TrainingConfig | None = None,
    ) -> None:
        self._backend = backend
        self._evaluator = evaluator
        self._artifact_store = artifact_store or LocalArtifactStore()
        self._config = config or TrainingConfig()

    def fit(
        self,
        samples: list[SkillSample],
        *,
        config: TrainingConfig | None = None,
    ) -> RunArtifacts:
        active_config = config or self._config
        run_id = make_run_id()
        started_at = isoformat(utc_now())
        history: list[dict[str, object]] = [{"stage": "start", "started_at": started_at}]
        skill_text = active_config.initial_skill

        for epoch in range(active_config.num_epochs):
            for batch_index, batch in enumerate(_batched(list(samples), active_config.batch_size), start=1):
                batch_context = RunContext(
                    run_id=run_id,
                    run_name=active_config.run_name,
                    run_kind="train",
                    output_root=active_config.output_root,
                    samples=batch,
                    skill_text=skill_text,
                    backend=self._backend,
                    evaluator=self._evaluator,
                    started_at=started_at,
                    history=[],
                )
                batch_context = run_stages(
                    batch_context,
                    [PredictionStage(), EvaluationStage(), ImprovementStage()],
                )
                skill_text = batch_context.skill_text
                history.append(
                    {
                        "stage": "batch",
                        "epoch": epoch + 1,
                        "batch_index": batch_index,
                        "mean_score": batch_context.evaluation_report.mean_score if batch_context.evaluation_report else 0.0,
                        "pass_rate": batch_context.evaluation_report.pass_rate if batch_context.evaluation_report else 0.0,
                    }
                )

        final_context = RunContext(
            run_id=run_id,
            run_name=active_config.run_name,
            run_kind="train",
            output_root=active_config.output_root,
            samples=list(samples),
            skill_text=skill_text,
            backend=self._backend,
            evaluator=self._evaluator,
            started_at=started_at,
            history=history,
        )
        final_context = run_stages(
            final_context,
            [PredictionStage(), EvaluationStage()],
        )
        return self._artifact_store.persist(final_context)

    def evaluate(
        self,
        samples: list[SkillSample],
        *,
        config: EvaluationConfig,
    ) -> EvaluationReport:
        started_at = isoformat(utc_now())
        context = RunContext(
            run_id=make_run_id(),
            run_name=config.run_name,
            run_kind="evaluate",
            output_root=config.output_root,
            samples=list(samples),
            skill_text=config.skill_text,
            backend=self._backend,
            evaluator=self._evaluator,
            started_at=started_at,
            history=[{"stage": "start", "started_at": started_at}],
        )
        context = run_stages(context, [PredictionStage(), EvaluationStage()])
        report = context.evaluation_report
        if report is None:
            raise ValueError("SkillTrainer.evaluate() requires an evaluation report.")
        report.artifacts = self._artifact_store.persist(context)
        return report
