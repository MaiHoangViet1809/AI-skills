from __future__ import annotations

from pathlib import Path
from typing import Optional


GLOBAL_TELEMETRY_ROOT = Path.home() / ".logs" / "codex" / "telemetry"
GLOBAL_RUNS_ROOT = GLOBAL_TELEMETRY_ROOT / "runs"
GLOBAL_STAGING_ROOT = GLOBAL_TELEMETRY_ROOT / "staging"
GLOBAL_CLAUDE_ROOT = GLOBAL_TELEMETRY_ROOT / "claude"


def _safe_project_name(project_name: str) -> str:
    return project_name.replace("/", "_")


def ensure_global_runs_dir() -> Path:
    GLOBAL_RUNS_ROOT.mkdir(parents=True, exist_ok=True)
    return GLOBAL_RUNS_ROOT


def ensure_global_staging_dir(project_name: str) -> Path:
    path = GLOBAL_STAGING_ROOT / _safe_project_name(project_name)
    path.mkdir(parents=True, exist_ok=True)
    return path


def ensure_global_claude_dir(project_name: str) -> Path:
    path = GLOBAL_CLAUDE_ROOT / _safe_project_name(project_name)
    path.mkdir(parents=True, exist_ok=True)
    return path


def staging_path(repo_root: Path, run_id: str) -> Path:
    return ensure_global_staging_dir(repo_root.name) / f"telemetry-run-{run_id}.json"


def claude_log_path(repo_root: Path, session_id: str) -> Path:
    return ensure_global_claude_dir(repo_root.name) / f"claude-{session_id}.log"


def global_run_path(project_name: str, run_id: str) -> Path:
    safe_project = _safe_project_name(project_name)
    return ensure_global_runs_dir() / f"{safe_project}__{run_id}.json"


def resolve_sow_file(repo_root: Path, sow: Optional[str]) -> Optional[str]:
    if not sow:
        return None

    repo_root = repo_root.resolve()
    search_roots = [repo_root / "plan_todo", repo_root / "plan_todo" / "finished"]
    normalized = sow.strip()

    exact_name = normalized if normalized.endswith(".md") else f"{normalized}.md"
    for root in search_roots:
        candidate = root / exact_name
        if candidate.exists():
            return str(candidate.resolve())

    prefix = normalized[:-3] if normalized.endswith(".md") else normalized
    candidates = []
    for root in search_roots:
        candidates.extend(sorted(root.glob(f"{prefix}*.md")))
    if not candidates:
        return None
    return str(candidates[0].resolve())
