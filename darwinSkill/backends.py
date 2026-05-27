from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol

from darwinSkill.contracts import SkillBackend, SkillFeedback, SkillSample


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
