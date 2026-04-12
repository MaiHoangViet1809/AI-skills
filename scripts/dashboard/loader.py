"""Load telemetry run records into a normalized Polars dataset."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import polars as pl

from ._schema import RUNS_SCHEMA, RunRecord


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _pick(result: dict[str, Any] | None, payload: dict[str, Any], key: str) -> Any:
    if result and key in result:
        return result.get(key)
    return payload.get(key)


def _resolve_sow_file(repo_root: Path, sow: str | None) -> str | None:
    if not sow:
        return None
    candidates = [
        *sorted((repo_root / "plan_todo").glob(f"{sow}*.md")),
        *sorted((repo_root / "plan_todo" / "finished").glob(f"{sow}*.md")),
    ]
    if not candidates:
        return None
    return str(candidates[0].resolve())


def _normalize_run(path: Path) -> RunRecord:
    payload = _read_json(path)
    result = payload.get("result") if isinstance(payload.get("result"), dict) else None
    anomalies = result.get("anomaly_flags") if result else None
    repo_root_value = payload.get("repo_root")
    repo_root = Path(str(repo_root_value)).resolve() if repo_root_value else None
    sow = _pick(result, payload, "sow")
    sow_file = _pick(result, payload, "sow_file")
    if not sow_file and repo_root:
        sow_file = _resolve_sow_file(repo_root, sow)
    project_name = _pick(result, payload, "project_name") or (repo_root.name if repo_root else None)
    project_path = _pick(result, payload, "project_path") or (str(repo_root) if repo_root else None)

    record: RunRecord = {
        "run_id": _pick(result, payload, "run_id"),
        "skill": _pick(result, payload, "skill"),
        "plan": _pick(result, payload, "plan"),
        "sow": sow,
        "sow_file": sow_file,
        "project_name": project_name,
        "project_path": project_path,
        "task_type": _pick(result, payload, "task_type"),
        "intent": _pick(result, payload, "intent"),
        "started_at": _pick(result, payload, "started_at"),
        "finished_at": _pick(result, payload, "finished_at"),
        "run_duration_ms": _pick(result, payload, "run_duration_ms"),
        "time_to_first_usable_result_ms": _pick(result, payload, "time_to_first_usable_result_ms"),
        "codex_session_id": _pick(result, payload, "codex_session_id"),
        "codex_task_tokens": _pick(result, payload, "codex_task_tokens"),
        "codex_cached_input_tokens": _pick(result, payload, "codex_cached_input_tokens"),
        "codex_fresh_input_tokens": _pick(result, payload, "codex_fresh_input_tokens"),
        "codex_output_tokens": _pick(result, payload, "codex_output_tokens"),
        "codex_reasoning_output_tokens": _pick(result, payload, "codex_reasoning_output_tokens"),
        "codex_turn_count": _pick(result, payload, "codex_turn_count"),
        "codex_avg_tokens_per_turn": _pick(result, payload, "codex_avg_tokens_per_turn"),
        "codex_last_turn_tokens": _pick(result, payload, "codex_last_turn_tokens"),
        "codex_tool_call_count": _pick(result, payload, "codex_tool_call_count"),
        "codex_tool_error_count": _pick(result, payload, "codex_tool_error_count"),
        "codex_mcp_call_count": _pick(result, payload, "codex_mcp_call_count"),
        "claude_session_id": _pick(result, payload, "claude_session_id"),
        "claude_input_tokens": _pick(result, payload, "claude_input_tokens"),
        "claude_output_tokens": _pick(result, payload, "claude_output_tokens"),
        "claude_cache_creation_tokens": _pick(result, payload, "claude_cache_creation_tokens"),
        "claude_cache_read_tokens": _pick(result, payload, "claude_cache_read_tokens"),
        "claude_total_tokens": _pick(result, payload, "claude_total_tokens"),
        "claude_duration_ms": _pick(result, payload, "claude_duration_ms"),
        "claude_tool_call_count": _pick(result, payload, "claude_tool_call_count"),
        "claude_tool_error_count": _pick(result, payload, "claude_tool_error_count"),
        "claude_mcp_call_count": _pick(result, payload, "claude_mcp_call_count"),
        "files_changed_count": _pick(result, payload, "files_changed_count"),
        "repair_rounds": _pick(result, payload, "repair_rounds"),
        "fallback_flag": _pick(result, payload, "fallback_flag"),
        "validation_pass": _pick(result, payload, "validation_pass"),
        "success_state": _pick(result, payload, "success_state"),
        "scope_respected": _pick(result, payload, "scope_respected"),
        "outcome": _pick(result, payload, "outcome"),
        "delegate_ratio": _pick(result, payload, "delegate_ratio"),
        "codex_to_claude_ratio": _pick(result, payload, "codex_to_claude_ratio"),
        "source_file": str(path),
        "has_anomalies": bool(anomalies),
    }
    return record


def load_run_records(repo_root: str | Path) -> list[RunRecord]:
    logs_dir = Path(repo_root).resolve() / "logs_session_ai_agent"
    run_files = sorted(logs_dir.glob("telemetry-run-*.json"))
    return [_normalize_run(path) for path in run_files]


def load_runs(repo_root: str | Path) -> pl.DataFrame:
    records = load_run_records(repo_root)
    if not records:
        return pl.DataFrame(schema=RUNS_SCHEMA)

    frame = pl.DataFrame(records, schema=RUNS_SCHEMA, orient="row")
    return frame.sort("started_at", descending=True, nulls_last=True)
