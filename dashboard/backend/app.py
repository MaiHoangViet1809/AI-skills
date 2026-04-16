"""Dashboard backend app — API plus same-port static serving.

Usage:
    uv run uvicorn dashboard.backend.app:app --port 9999

Endpoints
---------
GET /api/summary          – aggregate stats for a time window
GET /api/runs             – paginated run list
GET /api/runs/{run_id}    – single run detail
GET /api/charts/activity  – daily token heatmap data
GET /api/charts/duration  – per-run duration time series
"""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import polars as pl
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from .loader import load_runs

# ---------------------------------------------------------------------------
# Repo root is two levels above this file: dashboard/backend/app.py
# ---------------------------------------------------------------------------
_REPO_ROOT = Path(__file__).resolve().parents[2]
_STATIC_DIR = _REPO_ROOT / "dashboard" / "static"
_STATIC_ASSETS_DIR = _STATIC_DIR / "assets"
_STATIC_INDEX = _STATIC_DIR / "index.html"

app = FastAPI(title="AISkills Telemetry Dashboard", version="0.1.0")

_cached_df: pl.DataFrame | None = None


def _reload_runs() -> pl.DataFrame:
    return load_runs(_REPO_ROOT)


def _refresh_cache() -> pl.DataFrame:
    global _cached_df
    _cached_df = _reload_runs()
    return _cached_df

if _STATIC_ASSETS_DIR.exists():
    app.mount("/assets", StaticFiles(directory=_STATIC_ASSETS_DIR), name="assets")


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
    "90d": timedelta(days=90),
    "365d": timedelta(days=365),
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
    df = _apply_filters(_reload_runs(), window, skill, success_state, task_type)

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
    df = _apply_filters(_reload_runs(), window, skill, success_state, task_type)

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


def _parse_iso_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)
    except ValueError:
        return None


def _window_date_range(window: str, rows: list[dict[str, Any]]) -> tuple[date, date]:
    today = datetime.now(timezone.utc).date()
    delta = _parse_window(window)
    if delta is not None and delta < timedelta(days=36500):
        return (today - delta), today

    first_seen = today
    for row in rows:
        dt = _parse_iso_datetime(row.get("started_at"))
        if dt is not None:
            first_seen = min(first_seen, dt.date())
    return first_seen, today


# ---------------------------------------------------------------------------
# Run detail
# ---------------------------------------------------------------------------

@app.get("/api/runs/{run_id}")
def get_run_detail(run_id: str) -> JSONResponse:
    """Return all fields for a single run by its run_id."""
    matches = _reload_runs().filter(pl.col("run_id") == run_id)
    if matches.height == 0:
        raise HTTPException(status_code=404, detail=f"run_id '{run_id}' not found")

    row = matches.row(0, named=True)
    return JSONResponse(row)


# ---------------------------------------------------------------------------
# Activity chart
# ---------------------------------------------------------------------------

@app.get("/api/charts/activity")
def get_activity_chart(
    window: str = Query(default="12h", description="Time window: 1h 6h 12h 24h 2d 7d 30d all"),
    skill: str | None = Query(default=None),
    success_state: str | None = Query(default=None),
    task_type: str | None = Query(default=None),
) -> JSONResponse:
    """Return daily token-burn data for a GitHub-style heatmap."""
    df = _apply_filters(_reload_runs(), window, skill, success_state, task_type)
    rows = df.select([
        "started_at",
        "success_state",
        "codex_task_tokens",
        "claude_total_tokens",
    ]).to_dicts()

    if not rows:
        return JSONResponse({
            "window": window,
            "filters": {"skill": skill, "success_state": success_state, "task_type": task_type},
            "metric_modes": ["total", "codex", "claude"],
            "range_start": None,
            "range_end": None,
            "days": [],
            "max_total_tokens": 0,
            "max_codex_tokens": 0,
            "max_claude_tokens": 0,
        })

    start_date, end_date = _window_date_range(window, rows)
    counts: dict[str, dict[str, int]] = {}
    for row in rows:
        started_at = _parse_iso_datetime(row.get("started_at"))
        if started_at is None:
            continue
        day_key = started_at.date().isoformat()
        bucket = counts.setdefault(day_key, {
            "date": day_key,
            "run_count": 0,
            "accepted_runs": 0,
            "codex_tokens": 0,
            "claude_tokens": 0,
            "total_tokens": 0,
        })
        codex_tokens = int(row.get("codex_task_tokens") or 0)
        claude_tokens = int(row.get("claude_total_tokens") or 0)
        total_tokens = codex_tokens + claude_tokens
        bucket["run_count"] += 1
        bucket["accepted_runs"] += 1 if row.get("success_state") == "accepted" else 0
        bucket["codex_tokens"] += codex_tokens
        bucket["claude_tokens"] += claude_tokens
        bucket["total_tokens"] += total_tokens

    days: list[dict[str, Any]] = []
    max_total = 0
    max_codex = 0
    max_claude = 0
    cursor = start_date
    while cursor <= end_date:
        key = cursor.isoformat()
        bucket = counts.get(key) or {
            "date": key,
            "run_count": 0,
            "accepted_runs": 0,
            "codex_tokens": 0,
            "claude_tokens": 0,
            "total_tokens": 0,
        }
        days.append(bucket)
        max_total = max(max_total, int(bucket["total_tokens"]))
        max_codex = max(max_codex, int(bucket["codex_tokens"]))
        max_claude = max(max_claude, int(bucket["claude_tokens"]))
        cursor += timedelta(days=1)

    return JSONResponse({
        "window": window,
        "filters": {"skill": skill, "success_state": success_state, "task_type": task_type},
        "metric_modes": ["total", "codex", "claude"],
        "range_start": start_date.isoformat(),
        "range_end": end_date.isoformat(),
        "days": days,
        "max_total_tokens": max_total,
        "max_codex_tokens": max_codex,
        "max_claude_tokens": max_claude,
    })


# ---------------------------------------------------------------------------
# Duration chart
# ---------------------------------------------------------------------------

@app.get("/api/charts/duration")
def get_duration_chart(
    window: str = Query(default="12h", description="Time window: 1h 6h 12h 24h 2d 7d 30d all"),
    skill: str | None = Query(default=None),
    success_state: str | None = Query(default=None),
    task_type: str | None = Query(default=None),
) -> JSONResponse:
    """Return per-run duration time series, ordered by started_at ascending.

    Each point contains:
    - ``run_id``          – unique run identifier
    - ``started_at``      – ISO-8601 start timestamp
    - ``run_duration_ms`` – wall-clock duration in milliseconds (null if unknown)
    - ``success_state``   – outcome label for colour-coding
    - ``skill``           – skill name for tooltip
    """
    df = _apply_filters(_reload_runs(), window, skill, success_state, task_type)

    cols = ["run_id", "started_at", "run_duration_ms", "success_state", "skill"]
    if df.height == 0:
        return JSONResponse({
            "window": window,
            "filters": {"skill": skill, "success_state": success_state, "task_type": task_type},
            "points": [],
        })

    points = (
        df
        .select(cols)
        .sort("started_at", descending=False, nulls_last=True)
        .to_dicts()
    )

    return JSONResponse({
        "window": window,
        "filters": {"skill": skill, "success_state": success_state, "task_type": task_type},
        "points": points,
    })


@app.post("/api/refresh")
def refresh_runs() -> JSONResponse:
    frame = _refresh_cache()
    return JSONResponse({
        "refreshed": True,
        "total_runs": frame.height,
        "refreshed_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    })


def _serve_index() -> FileResponse:
    if not _STATIC_INDEX.exists():
        raise HTTPException(status_code=503, detail="dashboard static assets are not built yet")
    return FileResponse(_STATIC_INDEX)


@app.get("/")
def get_dashboard_index() -> FileResponse:
    return _serve_index()


@app.get("/{full_path:path}")
def get_dashboard_spa(full_path: str) -> FileResponse:
    if full_path.startswith(("api/", "docs", "redoc", "openapi.json", "assets/")):
        raise HTTPException(status_code=404, detail="not found")
    return _serve_index()
