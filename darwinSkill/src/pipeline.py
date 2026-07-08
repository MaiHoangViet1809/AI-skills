from __future__ import annotations

from darwinSkill.src.contracts import (
    PipelineConfig,
    RunArtifacts,
    RunContext,
    SkillBackend,
    SkillEvaluator,
    SkillSample,
    SkillStage,
)
from darwinSkill.src.storage import LocalArtifactStore, make_run_id, utc_now, isoformat
from darwinSkill.src.stages import run_stages


class SkillPipeline:
    def __init__(
        self,
        stages: list[SkillStage],
        *,
        backend: SkillBackend,
        evaluator: SkillEvaluator,
        artifact_store: LocalArtifactStore | None = None,
        config: PipelineConfig | None = None,
    ) -> None:
        self._stages = list(stages)
        self._backend = backend
        self._evaluator = evaluator
        self._artifact_store = artifact_store or LocalArtifactStore()
        self._config = config or PipelineConfig()

    def run(
        self,
        samples: list[SkillSample],
        *,
        config: PipelineConfig | None = None,
    ) -> RunArtifacts:
        active_config = config or self._config
        started_at = isoformat(utc_now())
        context = RunContext(
            run_id=make_run_id(),
            run_name=active_config.run_name,
            run_kind="pipeline",
            output_root=active_config.output_root,
            samples=list(samples),
            skill_text=active_config.initial_skill,
            backend=self._backend,
            evaluator=self._evaluator,
            started_at=started_at,
            history=[{"stage": "start", "started_at": started_at}],
        )
        context = run_stages(context, self._stages)
        if context.evaluation_report is None:
            raise ValueError("SkillPipeline requires an EvaluationStage before persistence.")
        return self._artifact_store.persist(context)
