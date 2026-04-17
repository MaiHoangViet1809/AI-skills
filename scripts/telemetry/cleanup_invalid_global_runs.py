#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


GLOBAL_RUNS_DIR = Path.home() / ".logs" / "codex" / "telemetry" / "runs"
CHECK_FIELDS = ("skill", "plan", "sow", "task_type", "intent")


def is_placeholder(value: object) -> bool:
    return isinstance(value, str) and value.startswith("<") and value.endswith(">")


def invalid_reason(payload: dict, include_missing_project: bool) -> str | None:
    result = payload.get("result") or payload
    for field in CHECK_FIELDS:
        if is_placeholder(result.get(field)):
            return f"placeholder:{field}"
    if not include_missing_project:
        return None
    project_name = result.get("project_name") or payload.get("project_name")
    project_path = result.get("project_path") or payload.get("project_path")
    if not project_name or not project_path:
        return "missing-project"
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--include-missing-project", action="store_true")
    args = parser.parse_args()

    removed = 0
    checked = 0
    for path in sorted(GLOBAL_RUNS_DIR.glob("*.json")):
        checked += 1
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            print(f"skip invalid json {path}")
            continue
        reason = invalid_reason(payload, include_missing_project=args.include_missing_project)
        if not reason:
            continue
        print(f"{'delete' if args.apply else 'would-delete'} {path} {reason}")
        if args.apply:
            path.unlink(missing_ok=True)
            removed += 1

    print(json.dumps({"checked": checked, "removed": removed, "apply": args.apply}, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
