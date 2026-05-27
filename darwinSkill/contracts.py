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
    initial_skill: str = ""
    output_root: Path | str = Path("outputs") / "darwinSkill"
    run_name: str = "train"

    def __post_init__(self) -> None:
        self.output_root = Path(self.output_root)
        _validate_positive("num_epochs", self.num_epochs)
        _validate_positive("batch_size", self.batch_size)
        _validate_run_name(self.run_name)


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
    last_stage: str
    sample_count: int
    prediction_count: int
    evaluation_count: int
    skill_text: str
    history: list[RunStateEntry] = field(default_factory=list)


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
    predictions: list[str] = field(default_factory=list)
    evaluations: list[SampleEvaluation] = field(default_factory=list)
    evaluation_report: EvaluationReport | None = None
    history: list[dict[str, Any]] = field(default_factory=list)


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
