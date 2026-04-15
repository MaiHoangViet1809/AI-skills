"""Smoke-load the current telemetry dataset for dashboard development."""

from __future__ import annotations

import json
from pathlib import Path

from .loader import load_runs


def main() -> int:
    repo_root = Path(__file__).resolve().parents[2]
    frame = load_runs(repo_root)
    summary = {
        "repo_root": str(repo_root),
        "run_count": frame.height,
        "columns": frame.columns,
    }
    print(json.dumps(summary, ensure_ascii=True, indent=2))
    if frame.height:
        print(frame.head(3))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
