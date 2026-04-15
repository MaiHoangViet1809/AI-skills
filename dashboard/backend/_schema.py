"""Explicit Polars schema and TypedDict for telemetry run records.

This module is the single source of truth for the dashboard data model.
Later backend SOWs import RUNS_SCHEMA and RunRecord from here — do not
add fields without also updating both the schema dict and the TypedDict.
"""
from __future__ import annotations

from typing import Optional

import polars as pl

# One-row-per-run schema.  All nullable columns use Optional types in RunRecord.
RUNS_SCHEMA: dict[str, pl.DataType] = {
    # --- identity ---
    "run_id": pl.Utf8,
    "skill": pl.Utf8,
    "plan": pl.Utf8,
    "sow": pl.Utf8,
    "sow_file": pl.Utf8,
    "project_name": pl.Utf8,
    "project_path": pl.Utf8,
    "task_type": pl.Utf8,
    "intent": pl.Utf8,
    # --- timing ---
    "started_at": pl.Utf8,
    "finished_at": pl.Utf8,
    "run_duration_ms": pl.Int64,
    "time_to_first_usable_result_ms": pl.Int64,
    # --- codex metrics ---
    "codex_session_id": pl.Utf8,
    "codex_task_tokens": pl.Int64,
    "codex_cached_input_tokens": pl.Int64,
    "codex_fresh_input_tokens": pl.Int64,
    "codex_output_tokens": pl.Int64,
    "codex_reasoning_output_tokens": pl.Int64,
    "codex_turn_count": pl.Int64,
    "codex_avg_tokens_per_turn": pl.Float64,
    "codex_last_turn_tokens": pl.Int64,
    "codex_tool_call_count": pl.Int64,
    "codex_tool_error_count": pl.Int64,
    "codex_mcp_call_count": pl.Int64,
    # --- claude metrics ---
    "claude_session_id": pl.Utf8,
    "claude_input_tokens": pl.Int64,
    "claude_output_tokens": pl.Int64,
    "claude_cache_creation_tokens": pl.Int64,
    "claude_cache_read_tokens": pl.Int64,
    "claude_total_tokens": pl.Int64,
    "claude_duration_ms": pl.Int64,
    "claude_tool_call_count": pl.Int64,
    "claude_tool_error_count": pl.Int64,
    "claude_mcp_call_count": pl.Int64,
    # --- outcome ---
    "files_changed_count": pl.Int64,
    "repair_rounds": pl.Int64,
    "fallback_flag": pl.Boolean,
    "validation_pass": pl.Boolean,
    "success_state": pl.Utf8,
    "scope_respected": pl.Boolean,
    "outcome": pl.Utf8,
    "delegate_ratio": pl.Float64,
    "codex_to_claude_ratio": pl.Float64,
    # --- loader meta ---
    "source_file": pl.Utf8,
    "has_anomalies": pl.Boolean,
}


class RunRecord(dict):  # type: ignore[type-arg]
    """Typed dict representing one normalized telemetry run row.

    Inherits from plain dict so it can be passed directly into
    ``pl.DataFrame([records], schema=RUNS_SCHEMA)`` without extra work.
    All Optional fields may be None; Polars will cast them to null.
    """

    # identity
    run_id: Optional[str]
    skill: Optional[str]
    plan: Optional[str]
    sow: Optional[str]
    sow_file: Optional[str]
    project_name: Optional[str]
    project_path: Optional[str]
    task_type: Optional[str]
    intent: Optional[str]
    # timing
    started_at: Optional[str]
    finished_at: Optional[str]
    run_duration_ms: Optional[int]
    time_to_first_usable_result_ms: Optional[int]
    # codex
    codex_session_id: Optional[str]
    codex_task_tokens: Optional[int]
    codex_cached_input_tokens: Optional[int]
    codex_fresh_input_tokens: Optional[int]
    codex_output_tokens: Optional[int]
    codex_reasoning_output_tokens: Optional[int]
    codex_turn_count: Optional[int]
    codex_avg_tokens_per_turn: Optional[float]
    codex_last_turn_tokens: Optional[int]
    codex_tool_call_count: Optional[int]
    codex_tool_error_count: Optional[int]
    codex_mcp_call_count: Optional[int]
    # claude
    claude_session_id: Optional[str]
    claude_input_tokens: Optional[int]
    claude_output_tokens: Optional[int]
    claude_cache_creation_tokens: Optional[int]
    claude_cache_read_tokens: Optional[int]
    claude_total_tokens: Optional[int]
    claude_duration_ms: Optional[int]
    claude_tool_call_count: Optional[int]
    claude_tool_error_count: Optional[int]
    claude_mcp_call_count: Optional[int]
    # outcome
    files_changed_count: Optional[int]
    repair_rounds: Optional[int]
    fallback_flag: Optional[bool]
    validation_pass: Optional[bool]
    success_state: Optional[str]
    scope_respected: Optional[bool]
    outcome: Optional[str]
    delegate_ratio: Optional[float]
    codex_to_claude_ratio: Optional[float]
    # meta (always present)
    source_file: str
    has_anomalies: bool
