from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from typing import Any, Callable, Protocol

from darwinSkill.provider_logs import (
    ProviderMessage,
    ProviderPatchEvent,
    ProviderSession,
    ProviderTaskEvent,
    ProviderToolResult,
)


SOW_PATTERN = re.compile(r"\bSOW_\d{4}\b")
CONTINUATION_MARKERS = (
    "approve",
    "approved",
    "continue",
    "tiếp tục",
    "làm tiếp",
    "fix tiếp",
    "fill gap",
    "process",
)


def _truncate(text: str, limit: int = 280) -> str:
    compact = " ".join(text.split())
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3].rstrip() + "..."


def _message_texts(messages: list[ProviderMessage], *, role: str | None = None) -> list[str]:
    results: list[str] = []
    for item in messages:
        if role is not None and item.role != role:
            continue
        text = item.content.strip()
        if text:
            results.append(text)
    return results


def _assistant_text(turn_messages: list[ProviderMessage]) -> str:
    return "\n".join(_message_texts(turn_messages, role="assistant"))


def _user_text(turn_messages: list[ProviderMessage]) -> str:
    return "\n".join(_message_texts(turn_messages, role="user"))


def _distinct_scope_anchors(text: str) -> list[str]:
    results: list[str] = []
    for match in SOW_PATTERN.findall(text):
        if match not in results:
            results.append(match)
    return results


def _is_continuation_prompt(text: str) -> bool:
    lowered = text.strip().lower()
    if not lowered:
        return False
    if len(lowered) > 80:
        return False
    return any(marker in lowered for marker in CONTINUATION_MARKERS)


@dataclass(slots=True)
class WorkUnit:
    work_unit_id: str
    provider: str
    session_id: str
    turn_ids: list[str]
    start_timestamp: str
    end_timestamp: str
    prompt: str
    task_family: str
    scope_anchor: str = ""
    boundary_confidence: float = 0.0
    mixed_context: bool = False
    continuation_of_work_unit_id: str = ""
    raw_evidence_refs: list[str] = field(default_factory=list)
    files_touched: list[str] = field(default_factory=list)
    artifact_refs: list[dict[str, Any]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ExtractedTaskOutcome:
    work_unit_id: str
    polarity: str
    outcome_class: str
    gap_type: str
    severity: float
    confidence: float
    needs_review: bool
    task_summary: str
    accepted_resolution: str = ""
    derived_reasoning_summary: str = ""
    raw_evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class TrainableSkillExample:
    example_id: str
    work_unit_id: str
    provider: str
    skill_name: str
    task_family: str
    context_summary: str
    failure_evidence: str
    repair_actions: str
    accepted_resolution: str
    outcome_label: str
    outcome_class: str
    gap_type: str
    severity: float
    confidence: float
    raw_evidence_refs: list[str] = field(default_factory=list)
    derived_reasoning_summary: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class EvidenceBundle:
    session_id: str
    provider: str
    work_unit: WorkUnit
    prompt: str
    assistant_messages: list[str]
    user_messages: list[str]
    tool_summaries: list[str]
    patch_summaries: list[str]
    task_summaries: list[str]
    files_touched: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class EvidenceInterpreter(Protocol):
    def interpret(self, bundle: EvidenceBundle) -> ExtractedTaskOutcome:
        ...


class CallbackEvidenceInterpreter:
    def __init__(self, callback: Callable[[dict[str, Any]], dict[str, Any] | ExtractedTaskOutcome]) -> None:
        self._callback = callback

    def interpret(self, bundle: EvidenceBundle) -> ExtractedTaskOutcome:
        raw = self._callback(bundle.to_dict())
        if isinstance(raw, ExtractedTaskOutcome):
            return raw
        return ExtractedTaskOutcome(
            work_unit_id=bundle.work_unit.work_unit_id,
            polarity=str(raw.get("polarity") or "abstain"),
            outcome_class=str(raw.get("outcome_class") or "insufficient_evidence"),
            gap_type=str(raw.get("gap_type") or "unclear"),
            severity=float(raw.get("severity") or 0.0),
            confidence=float(raw.get("confidence") or 0.0),
            needs_review=bool(raw.get("needs_review", True)),
            task_summary=str(raw.get("task_summary") or bundle.prompt),
            accepted_resolution=str(raw.get("accepted_resolution") or ""),
            derived_reasoning_summary=str(raw.get("derived_reasoning_summary") or ""),
            raw_evidence_refs=list(raw.get("raw_evidence_refs") or bundle.work_unit.raw_evidence_refs),
            metadata=dict(raw.get("metadata") or {}),
        )


class HeuristicEvidenceInterpreter:
    def interpret(self, bundle: EvidenceBundle) -> ExtractedTaskOutcome:
        prompt = bundle.prompt.strip()
        assistant_text = "\n".join(bundle.assistant_messages).lower()
        user_text = "\n".join(bundle.user_messages).lower()
        combined = f"{prompt.lower()}\n{assistant_text}\n{user_text}"
        confidence = bundle.work_unit.boundary_confidence
        if bundle.work_unit.mixed_context or confidence < 0.45:
            return ExtractedTaskOutcome(
                work_unit_id=bundle.work_unit.work_unit_id,
                polarity="abstain",
                outcome_class="insufficient_evidence",
                gap_type="mixed_context",
                severity=0.0,
                confidence=confidence,
                needs_review=True,
                task_summary=_truncate(prompt or bundle.work_unit.task_family),
                derived_reasoning_summary="Evidence is mixed or task boundary confidence is too low for a strong label.",
                raw_evidence_refs=list(bundle.work_unit.raw_evidence_refs),
            )

        if "if you approve" in combined or "approve sow" in combined or "nếu bạn approve" in combined:
            return ExtractedTaskOutcome(
                work_unit_id=bundle.work_unit.work_unit_id,
                polarity="negative",
                outcome_class="not_done",
                gap_type="awaiting_approval",
                severity=0.65,
                confidence=max(confidence, 0.7),
                needs_review=False,
                task_summary=_truncate(prompt or bundle.work_unit.task_family),
                derived_reasoning_summary="The work unit ended in a pending-approval state instead of an accepted completion.",
                raw_evidence_refs=list(bundle.work_unit.raw_evidence_refs),
            )

        if "block" in combined or "need user input" in combined or "cannot proceed" in combined:
            return ExtractedTaskOutcome(
                work_unit_id=bundle.work_unit.work_unit_id,
                polarity="negative",
                outcome_class="blocked",
                gap_type="missing_information",
                severity=0.9,
                confidence=max(confidence, 0.75),
                needs_review=False,
                task_summary=_truncate(prompt or bundle.work_unit.task_family),
                derived_reasoning_summary="The work unit appears blocked by missing information or an explicit inability to proceed.",
                raw_evidence_refs=list(bundle.work_unit.raw_evidence_refs),
            )

        shallow_cues = (
            "shallow",
            "incomplete",
            "fill gap",
            "double-check found gap",
            "technically pass but",
        )
        if any(cue in combined for cue in shallow_cues):
            return ExtractedTaskOutcome(
                work_unit_id=bundle.work_unit.work_unit_id,
                polarity="negative",
                outcome_class="shallow_or_incomplete_solution",
                gap_type="incomplete_coverage",
                severity=0.75,
                confidence=max(confidence, 0.7),
                needs_review=False,
                task_summary=_truncate(prompt or bundle.work_unit.task_family),
                derived_reasoning_summary="The evidence indicates the implementation exists but is shallow, incomplete, or only technically passing.",
                raw_evidence_refs=list(bundle.work_unit.raw_evidence_refs),
            )

        wrong_approach_cues = (
            "wrong approach",
            "scope miss",
            "scope mismatch",
            "not really solve",
            "does not really solve",
        )
        if any(cue in combined for cue in wrong_approach_cues):
            return ExtractedTaskOutcome(
                work_unit_id=bundle.work_unit.work_unit_id,
                polarity="negative",
                outcome_class="scope_miss_or_wrong_approach",
                gap_type="wrong_approach",
                severity=0.85,
                confidence=max(confidence, 0.75),
                needs_review=False,
                task_summary=_truncate(prompt or bundle.work_unit.task_family),
                derived_reasoning_summary="The evidence indicates the task drifted outside scope or used an approach that does not solve the intended problem.",
                raw_evidence_refs=list(bundle.work_unit.raw_evidence_refs),
            )

        success_cues = (
            "worktree hiện sạch",
            "worktree is clean",
            "quality check passed",
            "ran 59 tests",
            "commit",
            "đã xử lý xong",
            "đã xong",
        )
        if any(cue in combined for cue in success_cues):
            repaired = any(token in combined for token in {"fix", "repair", "fill gap", "double-check"})
            return ExtractedTaskOutcome(
                work_unit_id=bundle.work_unit.work_unit_id,
                polarity="positive",
                outcome_class="accepted_with_repair_history" if repaired else "accepted_done",
                gap_type="resolved" if repaired else "none",
                severity=0.15 if repaired else 0.0,
                confidence=max(confidence, 0.8),
                needs_review=False,
                task_summary=_truncate(prompt or bundle.work_unit.task_family),
                accepted_resolution=_truncate(bundle.assistant_messages[-1] if bundle.assistant_messages else ""),
                derived_reasoning_summary="The work unit ended with an explicit completion signal and validation or commit-like closure cues.",
                raw_evidence_refs=list(bundle.work_unit.raw_evidence_refs),
            )

        return ExtractedTaskOutcome(
            work_unit_id=bundle.work_unit.work_unit_id,
            polarity="abstain",
            outcome_class="insufficient_evidence",
            gap_type="unclear",
            severity=0.0,
            confidence=min(confidence, 0.5),
            needs_review=True,
            task_summary=_truncate(prompt or bundle.work_unit.task_family),
            derived_reasoning_summary="The evidence bundle does not support a confident completion or failure judgment.",
            raw_evidence_refs=list(bundle.work_unit.raw_evidence_refs),
        )


def segment_session_into_work_units(session: ProviderSession) -> list[WorkUnit]:
    work_units: list[WorkUnit] = []
    previous_work_unit: WorkUnit | None = None
    for index, turn in enumerate(session.turns, start=1):
        user_messages = _message_texts(turn.messages, role="user")
        assistant_messages = _message_texts(turn.messages, role="assistant")
        prompt = "\n".join(user_messages).strip()
        combined_text = "\n".join(user_messages + assistant_messages)
        scope_anchors = _distinct_scope_anchors(combined_text)
        mixed_context = len(scope_anchors) > 1
        scope_anchor = scope_anchors[0] if scope_anchors else ""
        task_events = turn.task_events
        has_task_complete = any(item.event_type == "task_complete" for item in task_events)
        boundary_confidence = 0.9 if has_task_complete and not mixed_context else 0.65 if has_task_complete else 0.4
        if mixed_context:
            boundary_confidence = min(boundary_confidence, 0.35)
        files_touched: list[str] = []
        raw_evidence_refs: list[str] = []
        for message in turn.messages:
            raw_evidence_refs.append(message.event_id)
        for tool_call in turn.tool_calls:
            raw_evidence_refs.append(tool_call.event_id)
        for tool_result in turn.tool_results:
            raw_evidence_refs.append(tool_result.event_id)
        for patch_event in turn.patch_events:
            raw_evidence_refs.append(patch_event.event_id)
            for change in patch_event.changes:
                if change.path not in files_touched:
                    files_touched.append(change.path)
        for task_event in task_events:
            raw_evidence_refs.append(task_event.event_id)
        continuation_of = ""
        if previous_work_unit is not None and _is_continuation_prompt(prompt) and not scope_anchor:
            continuation_of = previous_work_unit.work_unit_id
            scope_anchor = previous_work_unit.scope_anchor
        task_family = scope_anchor or _truncate(
            prompt or (assistant_messages[0] if assistant_messages else f"turn-{index}"),
            120,
        )
        work_unit = WorkUnit(
            work_unit_id=f"{session.session_id}:wu:{index:04d}",
            provider=session.provider,
            session_id=session.session_id,
            turn_ids=[turn.turn_id],
            start_timestamp=turn.timestamp,
            end_timestamp=turn.timestamp,
            prompt=prompt,
            task_family=task_family,
            scope_anchor=scope_anchor,
            boundary_confidence=boundary_confidence,
            mixed_context=mixed_context,
            continuation_of_work_unit_id=continuation_of,
            raw_evidence_refs=raw_evidence_refs,
            files_touched=files_touched,
            artifact_refs=[asdict(item) for item in turn.artifact_refs],
            metadata={"cwd": turn.cwd, "turn_metadata": dict(turn.metadata)},
        )
        work_units.append(work_unit)
        previous_work_unit = work_unit
    return work_units


def _tool_summaries(tool_results: list[ProviderToolResult]) -> list[str]:
    results: list[str] = []
    for item in tool_results:
        snippet = _truncate(item.output, 160)
        results.append(f"{item.tool_name}: {snippet}")
    return results


def _patch_summaries(patch_events: list[ProviderPatchEvent]) -> list[str]:
    results: list[str] = []
    for item in patch_events:
        changed = ", ".join(change.path for change in item.changes[:5])
        if not changed:
            changed = "no-file-summary"
        results.append(f"patch success={item.success} files={changed}")
    return results


def _task_summaries(task_events: list[ProviderTaskEvent]) -> list[str]:
    results: list[str] = []
    for item in task_events:
        summary = _truncate(item.message, 140)
        results.append(f"{item.event_type}: {summary}")
    return results


def build_evidence_bundle(session: ProviderSession, work_unit: WorkUnit) -> EvidenceBundle:
    turns = [turn for turn in session.turns if turn.turn_id in work_unit.turn_ids]
    messages: list[ProviderMessage] = []
    tool_results: list[ProviderToolResult] = []
    patch_events: list[ProviderPatchEvent] = []
    task_events: list[ProviderTaskEvent] = []
    for turn in turns:
        messages.extend(turn.messages)
        tool_results.extend(turn.tool_results)
        patch_events.extend(turn.patch_events)
        task_events.extend(turn.task_events)
    return EvidenceBundle(
        session_id=session.session_id,
        provider=session.provider,
        work_unit=work_unit,
        prompt=work_unit.prompt,
        assistant_messages=_message_texts(messages, role="assistant"),
        user_messages=_message_texts(messages, role="user"),
        tool_summaries=_tool_summaries(tool_results),
        patch_summaries=_patch_summaries(patch_events),
        task_summaries=_task_summaries(task_events),
        files_touched=list(work_unit.files_touched),
    )


def build_trainable_examples(
    session: ProviderSession,
    *,
    skill_name: str = "",
    interpreter: EvidenceInterpreter | None = None,
) -> list[TrainableSkillExample]:
    active_interpreter = interpreter or HeuristicEvidenceInterpreter()
    examples: list[TrainableSkillExample] = []
    for index, work_unit in enumerate(segment_session_into_work_units(session), start=1):
        bundle = build_evidence_bundle(session, work_unit)
        outcome = active_interpreter.interpret(bundle)
        repair_actions = "\n".join(bundle.patch_summaries + bundle.tool_summaries)
        failure_evidence = "\n".join(bundle.task_summaries + bundle.assistant_messages[:2] + bundle.user_messages[:1])
        examples.append(
            TrainableSkillExample(
                example_id=f"{session.session_id}:example:{index:04d}",
                work_unit_id=work_unit.work_unit_id,
                provider=session.provider,
                skill_name=skill_name or work_unit.scope_anchor,
                task_family=work_unit.task_family,
                context_summary=outcome.task_summary,
                failure_evidence=_truncate(failure_evidence, 800),
                repair_actions=_truncate(repair_actions, 800),
                accepted_resolution=outcome.accepted_resolution,
                outcome_label=outcome.polarity,
                outcome_class=outcome.outcome_class,
                gap_type=outcome.gap_type,
                severity=outcome.severity,
                confidence=outcome.confidence,
                raw_evidence_refs=list(outcome.raw_evidence_refs),
                derived_reasoning_summary=outcome.derived_reasoning_summary,
                metadata={
                    "needs_review": outcome.needs_review,
                    "files_touched": list(work_unit.files_touched),
                    "boundary_confidence": work_unit.boundary_confidence,
                    "mixed_context": work_unit.mixed_context,
                    "continuation_of_work_unit_id": work_unit.continuation_of_work_unit_id,
                    "artifact_refs": list(work_unit.artifact_refs),
                    **dict(outcome.metadata),
                },
            )
        )
    return examples
