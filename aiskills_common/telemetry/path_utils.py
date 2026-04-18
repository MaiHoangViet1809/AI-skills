from __future__ import annotations

from pathlib import Path
from typing import Optional


GLOBAL_RUNS_ROOT = Path.home() / ".logs" / "codex" / "telemetry" / "runs"


def ensure_logs_dir(repo_root: Path) -> Path:
    path = repo_root / "logs_session_ai_agent"
    path.mkdir(parents=True, exist_ok=True)
    return path


def ensure_global_runs_dir() -> Path:
    GLOBAL_RUNS_ROOT.mkdir(parents=True, exist_ok=True)
    return GLOBAL_RUNS_ROOT


def staging_path(repo_root: Path, run_id: str) -> Path:
    return ensure_logs_dir(repo_root) / f"telemetry-run-{run_id}.json"


def global_run_path(project_name: str, run_id: str) -> Path:
    safe_project = project_name.replace("/", "_")
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
