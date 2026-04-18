#!/usr/bin/env python3
"""Backfill project-local telemetry summaries into the global ledger."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from aiskills_common.telemetry.io_utils import read_json
from aiskills_common.telemetry.path_utils import global_run_path

GLOBAL_RUNS_DIR = Path.home() / ".logs" / "codex" / "telemetry" / "runs"
PROJECTS_ROOT = Path.home() / "Projects"


def discover_run_files() -> list[Path]:
    return sorted(PROJECTS_ROOT.glob("*/logs_session_ai_agent/telemetry-run-*.json"))


def target_path(source: Path) -> Path:
    payload = read_json(source)
    project_name = payload.get("project_name") or Path(str(payload.get("repo_root") or source.parents[2])).name
    run_id = payload.get("run_id") or source.stem.removeprefix("telemetry-run-")
    return global_run_path(project_name, run_id)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    GLOBAL_RUNS_DIR.mkdir(parents=True, exist_ok=True)
    copied = 0
    for source in discover_run_files():
        dest = target_path(source)
        print(f"{source} -> {dest}")
        if not args.dry_run:
            shutil.copy2(source, dest)
        copied += 1
    print(f"done: {copied} file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
