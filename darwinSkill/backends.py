from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Protocol

from darwinSkill.alfworld_env import ALFWorldAgentBackend, ALFWorldEpisodeEnvironment, run_alfworld_episode
from darwinSkill.contracts import SkillBackend, SkillFeedback, SkillSample
from darwinSkill.spreadsheetbench_env import SpreadsheetReactBackend, run_spreadsheet_react_session


SUPPORTED_BACKEND_FAMILIES = {
    "azure_openai",
    "openai_chat",
    "codex_exec",
    "claude_chat",
    "claude_code_exec",
    "qwen_chat",
}


class TargetBackend(Protocol):
    def predict(self, skill_text: str, sample: SkillSample) -> str:
        ...


class OptimizerBackend(Protocol):
    def improve_skill(self, skill_text: str, feedback: list[SkillFeedback]) -> str:
        ...


@dataclass(slots=True)
class SpreadsheetReactTargetBackend(TargetBackend):
    backend: SpreadsheetReactBackend
    max_turns: int = 30
    diagnostic_instruction: str = ""

    def predict(self, skill_text: str, sample: SkillSample) -> str:
        session = run_spreadsheet_react_session(
            backend=self.backend,
            sample=sample,
            skill_content=skill_text,
            max_turns=self.max_turns,
            diagnostic_instruction=self.diagnostic_instruction,
        )
        return str(session["prediction"])


@dataclass(slots=True)
class ALFWorldEpisodeTargetBackend(TargetBackend):
    backend: ALFWorldAgentBackend
    environment_factory: Callable[[SkillSample], ALFWorldEpisodeEnvironment]
    max_steps: int = 50
    diagnostic_instruction: str = ""

    def predict(self, skill_text: str, sample: SkillSample) -> str:
        episode = run_alfworld_episode(
            backend=self.backend,
            environment=self.environment_factory(sample),
            skill_content=skill_text,
            max_steps=self.max_steps,
            diagnostic_instruction=self.diagnostic_instruction,
        )
        return str(episode["prediction"])


@dataclass(slots=True, frozen=True)
class BackendRuntimeConfig:
    family: str
    model: str = ""
    options: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.family not in SUPPORTED_BACKEND_FAMILIES:
            raise ValueError(f"Unsupported backend family: {self.family}")


@dataclass(slots=True, frozen=True)
class RoutingConfig:
    target: BackendRuntimeConfig
    optimizer: BackendRuntimeConfig


@dataclass(slots=True)
class BackendRouter(SkillBackend):
    target_backend: TargetBackend
    optimizer_backend: OptimizerBackend
    routing: RoutingConfig | None = None

    def predict(self, skill_text: str, sample: SkillSample) -> str:
        return self.target_backend.predict(skill_text, sample)

    def improve_skill(self, skill_text: str, feedback: list[SkillFeedback]) -> str:
        return self.optimizer_backend.improve_skill(skill_text, feedback)


def single_backend_router(backend: SkillBackend) -> BackendRouter:
    return BackendRouter(target_backend=backend, optimizer_backend=backend)


def build_spreadsheetbench_router(
    *,
    target_backend: SpreadsheetReactBackend,
    optimizer_backend: OptimizerBackend,
    routing: RoutingConfig | None = None,
    max_turns: int = 30,
    diagnostic_instruction: str = "",
) -> BackendRouter:
    return BackendRouter(
        target_backend=SpreadsheetReactTargetBackend(
            backend=target_backend,
            max_turns=max_turns,
            diagnostic_instruction=diagnostic_instruction,
        ),
        optimizer_backend=optimizer_backend,
        routing=routing,
    )


def build_alfworld_router(
    *,
    target_backend: ALFWorldAgentBackend,
    optimizer_backend: OptimizerBackend,
    environment_factory: Callable[[SkillSample], ALFWorldEpisodeEnvironment],
    routing: RoutingConfig | None = None,
    max_steps: int = 50,
    diagnostic_instruction: str = "",
) -> BackendRouter:
    return BackendRouter(
        target_backend=ALFWorldEpisodeTargetBackend(
            backend=target_backend,
            environment_factory=environment_factory,
            max_steps=max_steps,
            diagnostic_instruction=diagnostic_instruction,
        ),
        optimizer_backend=optimizer_backend,
        routing=routing,
    )


def default_routing_for_family(family: str) -> RoutingConfig:
    if family == "codex_exec":
        return RoutingConfig(
            target=BackendRuntimeConfig(family="codex_exec"),
            optimizer=BackendRuntimeConfig(family="openai_chat"),
        )
    if family == "claude_code_exec":
        return RoutingConfig(
            target=BackendRuntimeConfig(family="claude_code_exec"),
            optimizer=BackendRuntimeConfig(family="openai_chat"),
        )
    if family == "qwen_chat":
        return RoutingConfig(
            target=BackendRuntimeConfig(family="qwen_chat"),
            optimizer=BackendRuntimeConfig(family="openai_chat"),
        )
    if family in {"claude_chat", "azure_openai", "openai_chat"}:
        return RoutingConfig(
            target=BackendRuntimeConfig(family=family),
            optimizer=BackendRuntimeConfig(family=family),
        )
    raise ValueError(f"Unsupported backend family: {family}")
