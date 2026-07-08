from __future__ import annotations

from darwinSkill.src.contracts import (
    EvaluationConfig,
    EvaluationReport,
    RunArtifacts,
    RunContext,
    SkillBackend,
    SkillEvaluator,
    SkillSample,
    TrainingConfig,
)
from darwinSkill.src.engine import ReflectiveSkillEngine
from darwinSkill.src.storage import LocalArtifactStore, isoformat, load_run_state, make_run_id, utc_now
from darwinSkill.src.stages import EvaluationStage, PredictionStage, run_stages


class SkillTrainer:
    def __init__(
        self,
        *,
        backend: SkillBackend,
        evaluator: SkillEvaluator,
        artifact_store: LocalArtifactStore | None = None,
        config: TrainingConfig | None = None,
        engine: ReflectiveSkillEngine | None = None,
    ) -> None:
        self._backend = backend
        self._evaluator = evaluator
        self._artifact_store = artifact_store or LocalArtifactStore()
        self._config = config or TrainingConfig()
        self._engine = engine or ReflectiveSkillEngine()

    def fit(
        self,
        samples: list[SkillSample],
        *,
        config: TrainingConfig | None = None,
        eval_samples: list[SkillSample] | None = None,
    ) -> RunArtifacts:
        active_config = config or self._config
        run_id = make_run_id()
        run_name = active_config.run_name
        output_root = active_config.output_root
        started_at = isoformat(utc_now())
        if active_config.resume_from is not None:
            resumed_state = load_run_state(active_config.resume_from / "run_state.json")
            run_id = resumed_state.run_id
            run_name = resumed_state.run_name
            output_root = active_config.resume_from.parent
            started_at = resumed_state.started_at
        history: list[dict[str, object]] = [{"stage": "start", "started_at": started_at}]
        final_context = RunContext(
            run_id=run_id,
            run_name=run_name,
            run_kind="train",
            output_root=output_root,
            samples=list(samples),
            skill_text=active_config.initial_skill,
            backend=self._backend,
            evaluator=self._evaluator,
            started_at=started_at,
            train_samples=list(samples),
            eval_samples=list(eval_samples or samples),
            history=history,
        )
        final_context = self._engine.run_training(final_context, config=active_config)
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
