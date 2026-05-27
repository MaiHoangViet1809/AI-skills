from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol, Sequence


@dataclass(slots=True)
class SkillSample:
    prompt: str
    expected_answer: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class MetricResult:
    score: float
    passed: bool
    details: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class SampleEvaluation:
    sample: SkillSample
    prediction: str
    metric: MetricResult


@dataclass(slots=True)
class EvaluationReport:
    sample_count: int
    mean_score: float
    pass_rate: float
    skill_text: str
    results: list[SampleEvaluation] = field(default_factory=list)
    artifacts: "RunArtifacts | None" = None


@dataclass(slots=True)
class SkillFeedback:
    sample: SkillSample
    prediction: str
    metric: MetricResult


@dataclass(slots=True)
class TrainingConfig:
    num_epochs: int = 1
    batch_size: int = 4
    edit_budget: int = 4
    initial_skill: str = ""
    output_root: Path | str = Path("outputs") / "darwinSkill"
    run_name: str = "train"
    resume_from: Path | str | None = None
    use_slow_update: bool = True
    use_meta_skill: bool = True

    def __post_init__(self) -> None:
        self.output_root = Path(self.output_root)
        _validate_positive("num_epochs", self.num_epochs)
        _validate_positive("batch_size", self.batch_size)
        _validate_positive("edit_budget", self.edit_budget)
        _validate_run_name(self.run_name)
        if self.resume_from is not None:
            self.resume_from = Path(self.resume_from)


@dataclass(slots=True)
class EvaluationConfig:
    skill_text: str
    output_root: Path | str = Path("outputs") / "darwinSkill"
    run_name: str = "evaluate"

    def __post_init__(self) -> None:
        self.output_root = Path(self.output_root)
        _validate_run_name(self.run_name)


@dataclass(slots=True)
class PipelineConfig:
    initial_skill: str = ""
    output_root: Path | str = Path("outputs") / "darwinSkill"
    run_name: str = "pipeline"

    def __post_init__(self) -> None:
        self.output_root = Path(self.output_root)
        _validate_run_name(self.run_name)


def _validate_run_name(run_name: str) -> None:
    if not str(run_name).strip():
        raise ValueError("run_name must not be empty.")


def _validate_positive(name: str, value: int) -> None:
    if value <= 0:
        raise ValueError(f"{name} must be positive.")


@dataclass(slots=True)
class RunStateEntry:
    stage: str
    details: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class RunState:
    run_id: str
    run_name: str
    run_kind: str
    started_at: str
    finished_at: str
    current_epoch: int
    current_step: int
    best_step: int
    last_stage: str
    last_action: str
    sample_count: int
    prediction_count: int
    evaluation_count: int
    skill_text: str
    best_skill_text: str
    current_score: float
    best_score: float
    output_dir: str = ""
    current_skill_path: str = ""
    best_skill_path: str = ""
    history: list[RunStateEntry] = field(default_factory=list)


@dataclass(slots=True)
class BatchSpec:
    epoch: int
    step: int
    samples: list[SkillSample]


@dataclass(slots=True)
class SkillPatch:
    patch_id: str
    sample: SkillSample
    prediction: str
    metric: MetricResult
    instruction: str
    support_count: int = 1
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class PatchGroup:
    group_id: str
    instruction: str
    patches: list[SkillPatch]
    support_count: int
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class SelectionDecision:
    selected_groups: list[PatchGroup]
    selected_patches: list[SkillPatch]
    edit_budget: int
    total_candidates: int


@dataclass(slots=True)
class CandidateSkill:
    skill_text: str
    selection: SelectionDecision
    candidate_report: EvaluationReport | None = None


@dataclass(slots=True)
class GateDecision:
    action: str
    accepted_skill: str
    accepted_report: EvaluationReport
    best_skill: str
    best_report: EvaluationReport
    candidate_skill: str
    candidate_report: EvaluationReport
    previous_skill: str
    previous_report: EvaluationReport


@dataclass(slots=True)
class ComparisonPair:
    sample: SkillSample
    previous_prediction: str
    current_prediction: str
    previous_metric: MetricResult
    current_metric: MetricResult
    category: str


@dataclass(slots=True)
class SlowUpdateRecord:
    epoch: int
    guidance: str
    comparisons: list[ComparisonPair] = field(default_factory=list)


@dataclass(slots=True)
class MetaSkillRecord:
    epoch: int
    content: str
    comparisons: list[ComparisonPair] = field(default_factory=list)


@dataclass(slots=True)
class RunArtifacts:
    run_id: str
    run_name: str
    run_kind: str
    output_dir: Path
    started_at: str
    finished_at: str
    sample_count: int
    mean_score: float
    pass_rate: float
    final_skill: str
    summary_path: Path
    history_path: Path
    run_state_path: Path
    evaluations_path: Path
    final_skill_path: Path
    best_skill_path: Path
    steps_dir: Path
    skills_dir: Path


@dataclass(slots=True)
class RunContext:
    run_id: str
    run_name: str
    run_kind: str
    output_root: Path
    samples: list[SkillSample]
    skill_text: str
    backend: "SkillBackend"
    evaluator: "SkillEvaluator"
    started_at: str
    output_dir: Path | None = None
    predictions: list[str] = field(default_factory=list)
    evaluations: list[SampleEvaluation] = field(default_factory=list)
    evaluation_report: EvaluationReport | None = None
    history: list[dict[str, Any]] = field(default_factory=list)
    current_epoch: int = 0
    current_step: int = 0
    best_step: int = 0
    last_action: str = ""
    current_report: EvaluationReport | None = None
    best_skill_text: str = ""
    best_report: EvaluationReport | None = None
    step_records: list[dict[str, Any]] = field(default_factory=list)
    meta_skill: str = ""
    slow_update_guidance: str = ""


class SkillEvaluator(Protocol):
    def evaluate(self, prediction: str, sample: SkillSample) -> MetricResult:
        ...


class SkillBackend(Protocol):
    def predict(self, skill_text: str, sample: SkillSample) -> str:
        ...

    def improve_skill(
        self,
        skill_text: str,
        feedback: Sequence[SkillFeedback],
    ) -> str:
        ...


class SkillStage(Protocol):
    name: str

    def run(self, context: RunContext) -> RunContext:
        ...


class ArtifactStore(Protocol):
    def persist(self, context: RunContext) -> RunArtifacts:
        ...


class DatasetAdapter(Protocol):
    def get_train_samples(self) -> list[SkillSample]:
        ...

    def get_eval_samples(self) -> list[SkillSample]:
        ...

    def build_batches(self, config: TrainingConfig) -> list[BatchSpec]:
        ...
