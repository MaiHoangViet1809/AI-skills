"""Build and serve the telemetry dashboard on port 9999."""

from __future__ import annotations

import subprocess
from pathlib import Path

import uvicorn

REPO_ROOT = Path(__file__).resolve().parents[2]
DASHBOARD_UI = REPO_ROOT / "dashboard_ui"
STATIC_INDEX = REPO_ROOT / "scripts" / "dashboard" / "static" / "index.html"

from scripts.dashboard.app import app


def ensure_frontend_built() -> None:
    if not DASHBOARD_UI.exists():
        raise SystemExit("dashboard_ui/ is missing")

    subprocess.run(["npm", "install"], cwd=DASHBOARD_UI, check=True)
    subprocess.run(["npm", "run", "build"], cwd=DASHBOARD_UI, check=True)

    if not STATIC_INDEX.exists():
        raise SystemExit("frontend build did not produce scripts/dashboard/static/index.html")


def main() -> int:
    ensure_frontend_built()
    uvicorn.run(app, host="127.0.0.1", port=9999, reload=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
