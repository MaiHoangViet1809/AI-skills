from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


def _parse_jsonish(value: Any) -> Any:
    if not isinstance(value, str):
        return value
    text = value.strip()
    if not text:
        return value
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return value


def _message_text_from_content(content: Any) -> str:
    if isinstance(content, str):
        return content
    if not isinstance(content, list):
        return ""
    parts: list[str] = []
    for item in content:
        if not isinstance(item, dict):
            continue
        if item.get("type") in {"input_text", "output_text", "text"} and isinstance(item.get("text"), str):
            parts.append(item["text"])
    return "\n".join(part for part in parts if part.strip())


def _dict_list(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


@dataclass(slots=True)
class ArtifactReference:
    ref_id: str
    ref_type: str
    path: str = ""
    label: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ProviderMessage:
    event_id: str
    turn_id: str
    timestamp: str
    role: str
    content: str
    phase: str = ""
    source_type: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ProviderToolCall:
    event_id: str
    call_id: str
    turn_id: str
    timestamp: str
    tool_name: str
    source_type: str = ""
    arguments: Any = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ProviderToolResult:
    event_id: str
    call_id: str
    turn_id: str
    timestamp: str
    tool_name: str
    source_type: str = ""
    output: str = ""
    success: bool | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class PatchChange:
    path: str
    change_type: str
    unified_diff: str = ""
    content: str = ""
    move_path: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ProviderPatchEvent:
    event_id: str
    call_id: str
    turn_id: str
    timestamp: str
    source_type: str = ""
    status: str = ""
    success: bool | None = None
    stdout: str = ""
    stderr: str = ""
    changes: list[PatchChange] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ProviderTaskEvent:
    event_id: str
    turn_id: str
    timestamp: str
    event_type: str
    message: str = ""
    duration_ms: int | None = None
    time_to_first_token_ms: int | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ProviderTurn:
    turn_id: str
    timestamp: str = ""
    cwd: str = ""
    messages: list[ProviderMessage] = field(default_factory=list)
    tool_calls: list[ProviderToolCall] = field(default_factory=list)
    tool_results: list[ProviderToolResult] = field(default_factory=list)
    patch_events: list[ProviderPatchEvent] = field(default_factory=list)
    task_events: list[ProviderTaskEvent] = field(default_factory=list)
    artifact_refs: list[ArtifactReference] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ProviderSession:
    provider: str
    source_format_version: str
    session_id: str
    transcript_path: str
    cwd: str = ""
    started_at: str = ""
    session_metadata: dict[str, Any] = field(default_factory=dict)
    turns: list[ProviderTurn] = field(default_factory=list)
    provider_metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "ProviderSession":
        def artifact_ref_from(raw: dict[str, Any]) -> ArtifactReference:
            return ArtifactReference(
                ref_id=str(raw.get("ref_id") or ""),
                ref_type=str(raw.get("ref_type") or ""),
                path=str(raw.get("path") or ""),
                label=str(raw.get("label") or ""),
                metadata=dict(raw.get("metadata") or {}),
            )

        def message_from(raw: dict[str, Any]) -> ProviderMessage:
            return ProviderMessage(
                event_id=str(raw.get("event_id") or ""),
                turn_id=str(raw.get("turn_id") or ""),
                timestamp=str(raw.get("timestamp") or ""),
                role=str(raw.get("role") or ""),
                content=str(raw.get("content") or ""),
                phase=str(raw.get("phase") or ""),
                source_type=str(raw.get("source_type") or ""),
                metadata=dict(raw.get("metadata") or {}),
            )

        def tool_call_from(raw: dict[str, Any]) -> ProviderToolCall:
            return ProviderToolCall(
                event_id=str(raw.get("event_id") or ""),
                call_id=str(raw.get("call_id") or ""),
                turn_id=str(raw.get("turn_id") or ""),
                timestamp=str(raw.get("timestamp") or ""),
                tool_name=str(raw.get("tool_name") or ""),
                source_type=str(raw.get("source_type") or ""),
                arguments=raw.get("arguments"),
                metadata=dict(raw.get("metadata") or {}),
            )

        def tool_result_from(raw: dict[str, Any]) -> ProviderToolResult:
            return ProviderToolResult(
                event_id=str(raw.get("event_id") or ""),
                call_id=str(raw.get("call_id") or ""),
                turn_id=str(raw.get("turn_id") or ""),
                timestamp=str(raw.get("timestamp") or ""),
                tool_name=str(raw.get("tool_name") or ""),
                source_type=str(raw.get("source_type") or ""),
                output=str(raw.get("output") or ""),
                success=raw.get("success") if isinstance(raw.get("success"), bool) else None,
                metadata=dict(raw.get("metadata") or {}),
            )

        def patch_change_from(raw: dict[str, Any]) -> PatchChange:
            return PatchChange(
                path=str(raw.get("path") or ""),
                change_type=str(raw.get("change_type") or ""),
                unified_diff=str(raw.get("unified_diff") or ""),
                content=str(raw.get("content") or ""),
                move_path=str(raw["move_path"]) if raw.get("move_path") else None,
                metadata=dict(raw.get("metadata") or {}),
            )

        def patch_event_from(raw: dict[str, Any]) -> ProviderPatchEvent:
            return ProviderPatchEvent(
                event_id=str(raw.get("event_id") or ""),
                call_id=str(raw.get("call_id") or ""),
                turn_id=str(raw.get("turn_id") or ""),
                timestamp=str(raw.get("timestamp") or ""),
                source_type=str(raw.get("source_type") or ""),
                status=str(raw.get("status") or ""),
                success=raw.get("success") if isinstance(raw.get("success"), bool) else None,
                stdout=str(raw.get("stdout") or ""),
                stderr=str(raw.get("stderr") or ""),
                changes=[patch_change_from(item) for item in _dict_list(raw.get("changes"))],
                metadata=dict(raw.get("metadata") or {}),
            )

        def task_event_from(raw: dict[str, Any]) -> ProviderTaskEvent:
            return ProviderTaskEvent(
                event_id=str(raw.get("event_id") or ""),
                turn_id=str(raw.get("turn_id") or ""),
                timestamp=str(raw.get("timestamp") or ""),
                event_type=str(raw.get("event_type") or ""),
                message=str(raw.get("message") or ""),
                duration_ms=int(raw["duration_ms"]) if isinstance(raw.get("duration_ms"), int) else None,
                time_to_first_token_ms=int(raw["time_to_first_token_ms"]) if isinstance(raw.get("time_to_first_token_ms"), int) else None,
                metadata=dict(raw.get("metadata") or {}),
            )

        turns: list[ProviderTurn] = []
        for raw_turn in _dict_list(payload.get("turns")):
            turns.append(
                ProviderTurn(
                    turn_id=str(raw_turn.get("turn_id") or ""),
                    timestamp=str(raw_turn.get("timestamp") or ""),
                    cwd=str(raw_turn.get("cwd") or ""),
                    messages=[message_from(item) for item in _dict_list(raw_turn.get("messages"))],
                    tool_calls=[tool_call_from(item) for item in _dict_list(raw_turn.get("tool_calls"))],
                    tool_results=[tool_result_from(item) for item in _dict_list(raw_turn.get("tool_results"))],
                    patch_events=[patch_event_from(item) for item in _dict_list(raw_turn.get("patch_events"))],
                    task_events=[task_event_from(item) for item in _dict_list(raw_turn.get("task_events"))],
                    artifact_refs=[artifact_ref_from(item) for item in _dict_list(raw_turn.get("artifact_refs"))],
                    metadata=dict(raw_turn.get("metadata") or {}),
                )
            )
        return ProviderSession(
            provider=str(payload.get("provider") or ""),
            source_format_version=str(payload.get("source_format_version") or ""),
            session_id=str(payload.get("session_id") or ""),
            transcript_path=str(payload.get("transcript_path") or ""),
            cwd=str(payload.get("cwd") or ""),
            started_at=str(payload.get("started_at") or ""),
            session_metadata=dict(payload.get("session_metadata") or {}),
            turns=turns,
            provider_metadata=dict(payload.get("provider_metadata") or {}),
        )


def _artifact_ref_for_session(path: Path) -> ArtifactReference:
    return ArtifactReference(
        ref_id=f"artifact:{path.name}",
        ref_type="transcript",
        path=str(path),
        label=path.name,
    )


def _get_turn(turns: dict[str, ProviderTurn], turn_id: str, *, timestamp: str = "", cwd: str = "") -> ProviderTurn:
    turn = turns.get(turn_id)
    if turn is None:
        turn = ProviderTurn(turn_id=turn_id, timestamp=timestamp, cwd=cwd)
        turns[turn_id] = turn
        return turn
    if timestamp and not turn.timestamp:
        turn.timestamp = timestamp
    if cwd and not turn.cwd:
        turn.cwd = cwd
    return turn


def _patch_changes_from_payload(changes: Any) -> list[PatchChange]:
    if not isinstance(changes, dict):
        return []
    results: list[PatchChange] = []
    for path, payload in changes.items():
        if not isinstance(path, str) or not isinstance(payload, dict):
            continue
        results.append(
            PatchChange(
                path=path,
                change_type=str(payload.get("type") or "unknown"),
                unified_diff=str(payload.get("unified_diff") or ""),
                content=str(payload.get("content") or ""),
                move_path=str(payload["move_path"]) if payload.get("move_path") else None,
                metadata={key: value for key, value in payload.items() if key not in {"type", "unified_diff", "content", "move_path"}},
            )
        )
    return results


def load_codex_session(path: Path | str) -> ProviderSession:
    transcript_path = Path(path)
    turns: dict[str, ProviderTurn] = {}
    ordered_turn_ids: list[str] = []
    session_id = ""
    session_meta: dict[str, Any] = {}
    session_cwd = ""
    started_at = ""
    current_turn_id = ""
    line_index = 0

    with transcript_path.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            line_index += 1
            line = raw_line.strip()
            if not line:
                continue
            item = json.loads(line)
            timestamp = str(item.get("timestamp") or "")
            item_type = str(item.get("type") or "")
            payload = item.get("payload") if isinstance(item.get("payload"), dict) else {}
            payload_type = str(payload.get("type") or "")
            event_id = f"codex:{line_index}:{item_type}:{payload_type or 'none'}"

            if item_type == "session_meta":
                session_id = str(payload.get("id") or session_id)
                session_meta = dict(payload)
                session_cwd = str(payload.get("cwd") or session_cwd)
                started_at = str(payload.get("timestamp") or started_at)
                continue

            if item_type == "turn_context":
                current_turn_id = str(payload.get("turn_id") or "")
                if not current_turn_id:
                    continue
                turn = _get_turn(
                    turns,
                    current_turn_id,
                    timestamp=timestamp,
                    cwd=str(payload.get("cwd") or session_cwd),
                )
                turn.metadata.update({key: value for key, value in payload.items() if key not in {"turn_id", "cwd"}})
                if current_turn_id not in ordered_turn_ids:
                    ordered_turn_ids.append(current_turn_id)
                continue

            turn_id = str(payload.get("turn_id") or current_turn_id or "")
            if not turn_id:
                turn_id = f"unknown-turn-{line_index}"
            turn = _get_turn(turns, turn_id, timestamp=timestamp, cwd=str(payload.get("cwd") or session_cwd))
            if turn_id not in ordered_turn_ids:
                ordered_turn_ids.append(turn_id)

            if item_type == "response_item" and payload_type == "message":
                role = str(payload.get("role") or "unknown")
                content = _message_text_from_content(payload.get("content"))
                turn.messages.append(
                    ProviderMessage(
                        event_id=event_id,
                        turn_id=turn_id,
                        timestamp=timestamp,
                        role=role,
                        content=content,
                        phase=str(payload.get("phase") or ""),
                        source_type="response_item.message",
                        metadata={key: value for key, value in payload.items() if key not in {"type", "role", "content", "phase"}},
                    )
                )
                continue

            if item_type == "response_item" and payload_type in {"function_call", "custom_tool_call"}:
                turn.tool_calls.append(
                    ProviderToolCall(
                        event_id=event_id,
                        call_id=str(payload.get("call_id") or event_id),
                        turn_id=turn_id,
                        timestamp=timestamp,
                        tool_name=str(payload.get("name") or payload_type),
                        source_type=f"response_item.{payload_type}",
                        arguments=_parse_jsonish(payload.get("arguments")),
                        metadata={key: value for key, value in payload.items() if key not in {"type", "call_id", "name", "arguments"}},
                    )
                )
                continue

            if item_type == "response_item" and payload_type in {"function_call_output", "custom_tool_call_output"}:
                turn.tool_results.append(
                    ProviderToolResult(
                        event_id=event_id,
                        call_id=str(payload.get("call_id") or event_id),
                        turn_id=turn_id,
                        timestamp=timestamp,
                        tool_name=str(payload.get("tool_name") or payload_type),
                        source_type=f"response_item.{payload_type}",
                        output=str(payload.get("output") or ""),
                        metadata={key: value for key, value in payload.items() if key not in {"type", "call_id", "tool_name", "output"}},
                    )
                )
                continue

            if item_type == "event_msg" and payload_type in {"user_message", "agent_message"}:
                role = "user" if payload_type == "user_message" else "assistant"
                content = str(payload.get("message") or "")
                turn.messages.append(
                    ProviderMessage(
                        event_id=event_id,
                        turn_id=turn_id,
                        timestamp=timestamp,
                        role=role,
                        content=content,
                        phase=str(payload.get("phase") or ""),
                        source_type=f"event_msg.{payload_type}",
                        metadata={key: value for key, value in payload.items() if key not in {"type", "message", "phase"}},
                    )
                )
                continue

            if item_type == "event_msg" and payload_type.endswith("_call"):
                tool_name = payload_type.removesuffix("_call")
                turn.tool_calls.append(
                    ProviderToolCall(
                        event_id=event_id,
                        call_id=str(payload.get("call_id") or event_id),
                        turn_id=turn_id,
                        timestamp=timestamp,
                        tool_name=tool_name,
                        source_type=f"event_msg.{payload_type}",
                        arguments={key: value for key, value in payload.items() if key not in {"type", "call_id", "turn_id"}},
                    )
                )
                continue

            if item_type == "event_msg" and payload_type in {"exec_command_end", "mcp_tool_call_end", "web_search_end"}:
                tool_name = (
                    "exec_command"
                    if payload_type == "exec_command_end"
                    else str(payload.get("tool_name") or payload_type.removesuffix("_end"))
                )
                output = str(payload.get("aggregated_output") or payload.get("formatted_output") or payload.get("stdout") or "")
                success: bool | None = None
                if isinstance(payload.get("exit_code"), int):
                    success = int(payload["exit_code"]) == 0
                elif isinstance(payload.get("status"), str):
                    success = payload["status"] == "completed"
                turn.tool_results.append(
                    ProviderToolResult(
                        event_id=event_id,
                        call_id=str(payload.get("call_id") or event_id),
                        turn_id=turn_id,
                        timestamp=timestamp,
                        tool_name=tool_name,
                        source_type=f"event_msg.{payload_type}",
                        output=output,
                        success=success,
                        metadata={key: value for key, value in payload.items() if key not in {"type", "call_id", "turn_id", "aggregated_output", "formatted_output", "stdout"}},
                    )
                )
                continue

            if item_type == "event_msg" and payload_type == "patch_apply_end":
                turn.patch_events.append(
                    ProviderPatchEvent(
                        event_id=event_id,
                        call_id=str(payload.get("call_id") or event_id),
                        turn_id=turn_id,
                        timestamp=timestamp,
                        source_type="event_msg.patch_apply_end",
                        status=str(payload.get("status") or ""),
                        success=payload.get("success") if isinstance(payload.get("success"), bool) else None,
                        stdout=str(payload.get("stdout") or ""),
                        stderr=str(payload.get("stderr") or ""),
                        changes=_patch_changes_from_payload(payload.get("changes")),
                        metadata={key: value for key, value in payload.items() if key not in {"type", "call_id", "turn_id", "status", "success", "stdout", "stderr", "changes"}},
                    )
                )
                continue

            if item_type == "event_msg" and payload_type in {"task_started", "task_complete"}:
                turn.task_events.append(
                    ProviderTaskEvent(
                        event_id=event_id,
                        turn_id=turn_id,
                        timestamp=timestamp,
                        event_type=payload_type,
                        message=str(payload.get("message") or payload.get("last_agent_message") or ""),
                        duration_ms=int(payload["duration_ms"]) if isinstance(payload.get("duration_ms"), int) else None,
                        time_to_first_token_ms=int(payload["time_to_first_token_ms"]) if isinstance(payload.get("time_to_first_token_ms"), int) else None,
                        metadata={key: value for key, value in payload.items() if key not in {"type", "turn_id", "message", "last_agent_message", "duration_ms", "time_to_first_token_ms"}},
                    )
                )
                continue

            turn.metadata.setdefault("unclassified_events", []).append(
                {
                    "event_id": event_id,
                    "top_level_type": item_type,
                    "payload_type": payload_type,
                    "payload": payload,
                }
            )

    session = ProviderSession(
        provider="codex",
        source_format_version="codex_session_jsonl_v1",
        session_id=session_id or transcript_path.stem,
        transcript_path=str(transcript_path),
        cwd=session_cwd,
        started_at=started_at,
        session_metadata=session_meta,
        turns=[turns[turn_id] for turn_id in ordered_turn_ids if turn_id in turns],
        provider_metadata={"artifact_refs": [asdict(_artifact_ref_for_session(transcript_path))]},
    )
    for turn in session.turns:
        if not turn.artifact_refs:
            turn.artifact_refs.append(_artifact_ref_for_session(transcript_path))
    return session


def write_provider_session(path: Path | str, session: ProviderSession) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(session.to_dict(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_provider_session(path: Path | str) -> ProviderSession:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("Provider session artifact must be a JSON object.")
    return ProviderSession.from_dict(payload)
