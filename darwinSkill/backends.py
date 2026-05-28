from __future__ import annotations

from dataclasses import dataclass, field
import inspect
import json
from typing import Any, Callable, Protocol

from darwinSkill.alfworld_env import ALFWorldAgentBackend, ALFWorldEpisodeEnvironment, run_alfworld_episode
from darwinSkill.benchmarks import get_benchmark_spec
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


def _parse_tool_arguments(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return dict(value)
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError:
            return {"raw": value}
        return parsed if isinstance(parsed, dict) else {"raw": value}
    return {}


def _normalize_tool_call_payload(raw: Any, index: int) -> dict[str, Any] | None:
    if not isinstance(raw, dict):
        return None
    function = raw.get("function") if isinstance(raw.get("function"), dict) else raw
    name = str(function.get("name") or raw.get("name") or "").strip()
    if not name:
        return None
    arguments = function.get("arguments", raw.get("arguments", {}))
    return {
        "id": str(raw.get("id") or f"tool_{index}"),
        "type": str(raw.get("type") or "function"),
        "name": name,
        "arguments": _parse_tool_arguments(arguments),
    }


def normalize_openai_chat_payload(raw: Any) -> dict[str, Any]:
    if isinstance(raw, str):
        return {"content": raw, "tool_calls": []}
    if not isinstance(raw, dict):
        raise TypeError("OpenAI-compatible payload must be a dict or string.")
    message = raw
    if isinstance(raw.get("choices"), list) and raw["choices"]:
        message = raw["choices"][0].get("message") or {}
    content = message.get("content") or ""
    if isinstance(content, list):
        text_parts: list[str] = []
        for item in content:
            if isinstance(item, dict) and item.get("type") in {"text", "output_text"}:
                text_parts.append(str(item.get("text") or ""))
        content = "".join(text_parts)
    tool_calls = [
        item
        for item in (_normalize_tool_call_payload(tool_call, index) for index, tool_call in enumerate(message.get("tool_calls") or [], start=1))
        if item is not None
    ]
    return {"content": str(content or ""), "tool_calls": tool_calls}


def normalize_claude_chat_payload(raw: Any) -> dict[str, Any]:
    if isinstance(raw, str):
        return {"content": raw, "tool_calls": []}
    if not isinstance(raw, dict):
        raise TypeError("Claude-compatible payload must be a dict or string.")
    payload = raw.get("result", raw)
    if isinstance(payload, dict) and isinstance(payload.get("tool_calls"), list):
        content = str(payload.get("content") or "")
        tool_calls = [
            item
            for item in (_normalize_tool_call_payload(tool_call, index) for index, tool_call in enumerate(payload.get("tool_calls") or [], start=1))
            if item is not None
        ]
        return {"content": content, "tool_calls": tool_calls}

    content_blocks = payload.get("content") if isinstance(payload, dict) else None
    if not isinstance(content_blocks, list):
        return {"content": str(payload or ""), "tool_calls": []}
    text_parts: list[str] = []
    tool_calls: list[dict[str, Any]] = []
    for index, block in enumerate(content_blocks, start=1):
        if not isinstance(block, dict):
            continue
        block_type = str(block.get("type") or "")
        if block_type == "text":
            text_parts.append(str(block.get("text") or ""))
            continue
        if block_type == "tool_use":
            tool_calls.append(
                {
                    "id": str(block.get("id") or f"tool_{index}"),
                    "type": "function",
                    "name": str(block.get("name") or ""),
                    "arguments": dict(block.get("input") or {}),
                }
            )
    return {"content": "".join(text_parts), "tool_calls": tool_calls}


def normalize_qwen_chat_payload(raw: Any) -> dict[str, Any]:
    return normalize_openai_chat_payload(raw)


def normalize_codex_chat_payload(raw: Any) -> dict[str, Any]:
    if isinstance(raw, dict) and "result" in raw and isinstance(raw.get("result"), dict):
        raw = raw["result"]
    return normalize_openai_chat_payload(raw)


def _invoke_with_supported_kwargs(callback: Callable[..., Any], **kwargs: Any) -> Any:
    signature = inspect.signature(callback)
    if any(param.kind == inspect.Parameter.VAR_KEYWORD for param in signature.parameters.values()):
        return callback(**kwargs)
    accepted: dict[str, Any] = {}
    for name, parameter in signature.parameters.items():
        if parameter.kind in {inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.KEYWORD_ONLY} and name in kwargs:
            accepted[name] = kwargs[name]
    return callback(**accepted)


@dataclass(slots=True)
class ProviderChatBackendAdapter:
    invoke: Callable[..., Any]
    normalizer: Callable[[Any], dict[str, Any]]

    def respond(
        self,
        *,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
        tool_choice: str = "auto",
        system: str = "",
        user: str = "",
    ) -> dict[str, Any]:
        raw = _invoke_with_supported_kwargs(
            self.invoke,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
            system=system,
            user=user,
        )
        return self.normalizer(raw)


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


def build_openai_compat_backend(invoke: Callable[..., Any]) -> ProviderChatBackendAdapter:
    return ProviderChatBackendAdapter(invoke=invoke, normalizer=normalize_openai_chat_payload)


def build_claude_compat_backend(invoke: Callable[..., Any]) -> ProviderChatBackendAdapter:
    return ProviderChatBackendAdapter(invoke=invoke, normalizer=normalize_claude_chat_payload)


def build_qwen_compat_backend(invoke: Callable[..., Any]) -> ProviderChatBackendAdapter:
    return ProviderChatBackendAdapter(invoke=invoke, normalizer=normalize_qwen_chat_payload)


def build_codex_compat_backend(invoke: Callable[..., Any]) -> ProviderChatBackendAdapter:
    return ProviderChatBackendAdapter(invoke=invoke, normalizer=normalize_codex_chat_payload)


def _runtime_config_from_family(value: str | BackendRuntimeConfig) -> BackendRuntimeConfig:
    if isinstance(value, BackendRuntimeConfig):
        return value
    return BackendRuntimeConfig(family=str(value))


def build_provider_compat_backend_for_family(
    family: str | BackendRuntimeConfig,
    invoke: Callable[..., Any],
) -> ProviderChatBackendAdapter:
    runtime = _runtime_config_from_family(family)
    if runtime.family in {"azure_openai", "openai_chat"}:
        return build_openai_compat_backend(invoke)
    if runtime.family in {"claude_chat", "claude_code_exec"}:
        return build_claude_compat_backend(invoke)
    if runtime.family == "qwen_chat":
        return build_qwen_compat_backend(invoke)
    if runtime.family == "codex_exec":
        return build_codex_compat_backend(invoke)
    raise ValueError(f"Unsupported provider compat family: {runtime.family}")


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


def build_interactive_router_for_benchmark(
    *,
    benchmark_name: str,
    target_family: str | BackendRuntimeConfig,
    target_invoke: Callable[..., Any],
    optimizer_backend: OptimizerBackend,
    routing: RoutingConfig | None = None,
    environment_factory: Callable[[SkillSample], ALFWorldEpisodeEnvironment] | None = None,
    max_turns: int = 30,
    max_steps: int = 50,
    diagnostic_instruction: str = "",
) -> BackendRouter:
    spec = get_benchmark_spec(benchmark_name)
    compat_backend = build_provider_compat_backend_for_family(target_family, target_invoke)
    if spec.name == "spreadsheetbench":
        return build_spreadsheetbench_router(
            target_backend=compat_backend,
            optimizer_backend=optimizer_backend,
            routing=routing,
            max_turns=max_turns,
            diagnostic_instruction=diagnostic_instruction,
        )
    if spec.name == "alfworld":
        if environment_factory is None:
            raise ValueError("ALFWorld interactive router requires an environment_factory.")
        return build_alfworld_router(
            target_backend=compat_backend,
            optimizer_backend=optimizer_backend,
            environment_factory=environment_factory,
            routing=routing,
            max_steps=max_steps,
            diagnostic_instruction=diagnostic_instruction,
        )
    raise ValueError(f"Interactive router helper does not support benchmark: {benchmark_name}")


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
