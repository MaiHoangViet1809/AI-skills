"""Dashboard backend app — summary and runs list endpoints.

Usage:
    uv run uvicorn scripts.dashboard.app:app --port 9999
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import polars as pl
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse

from .loader import load_runs

# ---------------------------------------------------------------------------
# Repo root is two levels above this file: scripts/dashboard/app.py
# ---------------------------------------------------------------------------
_REPO_ROOT = Path(__file__).resolve().parents[2]

app = FastAPI(title="AISkills Telemetry Dashboard", version="0.1.0")

# Cache loaded at module import so repeated requests are cheap.
# In the final boot flow (SOW_0026) this will be refreshed on demand.
_df: pl.DataFrame = load_runs(_REPO_ROOT)


# ---------------------------------------------------------------------------
# Window parsing
# ---------------------------------------------------------------------------
_WINDOW_MAP: dict[str, timedelta] = {
    "1h": timedelta(hours=1),
    "6h": timedelta(hours=6),
    "12h": timedelta(hours=12),
    "24h": timedelta(hours=24),
    "2d": timedelta(days=2),
    "7d": timedelta(days=7),
    "30d": timedelta(days=30),
    "all": timedelta(days=36500),  # ~100 years — effectively no window cut
}


def _parse_window(window: str) -> timedelta | None:
    """Return timedelta for a window string, or None if unrecognised."""
    return _WINDOW_MAP.get(window.lower())


# ---------------------------------------------------------------------------
# Filter helpers
# ---------------------------------------------------------------------------
def _apply_filters(
    df: pl.DataFrame,
    window: str,
    skill: str | None,
    success_state: str | None,
    task_type: str | None,
) -> pl.DataFrame:
    """Apply window cut-off and equality filters to *df*."""
    # Time window — filter on started_at parsed as UTC datetime
    delta = _parse_window(window)
    if delta is not None and delta < timedelta(days=36500) and df.height > 0:
        cutoff = datetime.now(timezone.utc) - delta
        cutoff_str = cutoff.strftime("%Y-%m-%dT%H:%M:%S")
        df = df.filter(
            pl.col("started_at").str.slice(0, 19) >= cutoff_str
        )

    if skill:
        df = df.filter(pl.col("skill") == skill)
    if success_state:
        df = df.filter(pl.col("success_state") == success_state)
    if task_type:
        df = df.filter(pl.col("task_type") == task_type)

    return df


def _safe_int(val: Any) -> int | None:
    return None if val is None else int(val)


def _safe_float(val: Any, decimals: int = 2) -> float | None:
    if val is None:
        return None
    try:
        return round(float(val), decimals)
    except (TypeError, ValueError):
        return None


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/api/summary")
def get_summary(
    window: str = Query(default="12h", description="Time window: 1h 6h 12h 24h 2d 7d 30d all"),
    skill: str | None = Query(default=None),
    success_state: str | None = Query(default=None),
    task_type: str | None = Query(default=None),
) -> JSONResponse:
    """Return aggregate summary stats for the requested window and filters."""
    df = _apply_filters(_df, window, skill, success_state, task_type)

    total_runs = df.height

    if total_runs == 0:
        return JSONResponse({
            "window": window,
            "filters": {"skill": skill, "success_state": success_state, "task_type": task_type},
            "total_runs": 0,
            "accepted_runs": 0,
            "acceptance_rate": None,
            "total_codex_task_tokens": None,
            "total_claude_tokens": None,
            "avg_run_duration_ms": None,
            "total_tool_calls": None,
            "fallback_count": None,
        })

    accepted_runs = int(
        df.filter(pl.col("success_state") == "accepted").height
    )
    acceptance_rate = _safe_float(accepted_runs / total_runs if total_runs else None)

    total_codex_tokens = _safe_int(
        df.select(pl.col("codex_task_tokens").sum()).item()
    )
    total_claude_tokens = _safe_int(
        df.select(pl.col("claude_total_tokens").sum()).item()
    )
    avg_duration = _safe_float(
        df.select(pl.col("run_duration_ms").mean()).item()
    )

    codex_tools = df.select(pl.col("codex_tool_call_count").sum()).item() or 0
    claude_tools = df.select(pl.col("claude_tool_call_count").sum()).item() or 0
    total_tool_calls = _safe_int(codex_tools + claude_tools)

    fallback_count = int(
        df.filter(pl.col("fallback_flag") == True).height  # noqa: E712
    )

    return JSONResponse({
        "window": window,
        "filters": {"skill": skill, "success_state": success_state, "task_type": task_type},
        "total_runs": total_runs,
        "accepted_runs": accepted_runs,
        "acceptance_rate": acceptance_rate,
        "total_codex_task_tokens": total_codex_tokens,
        "total_claude_tokens": total_claude_tokens,
        "avg_run_duration_ms": avg_duration,
        "total_tool_calls": total_tool_calls,
        "fallback_count": fallback_count,
    })


@app.get("/api/runs")
def get_runs(
    window: str = Query(default="12h", description="Time window: 1h 6h 12h 24h 2d 7d 30d all"),
    skill: str | None = Query(default=None),
    success_state: str | None = Query(default=None),
    task_type: str | None = Query(default=None),
    limit: int = Query(default=100, ge=1, le=1000),
    offset: int = Query(default=0, ge=0),
) -> JSONResponse:
    """Return a paginated list of run records for the requested window and filters."""
    df = _apply_filters(_df, window, skill, success_state, task_type)

    total = df.height
    page = df.slice(offset, limit)

    # Serialize row-by-row — Polars to_dicts() handles nulls as None
    rows = page.to_dicts()

    return JSONResponse({
        "window": window,
        "filters": {"skill": skill, "success_state": success_state, "task_type": task_type},
        "total": total,
        "offset": offset,
        "limit": limit,
        "runs": rows,
    })
