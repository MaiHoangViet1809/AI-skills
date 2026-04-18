from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any, Mapping, Optional


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def run_json_command(command: list[str], env: Optional[Mapping[str, str]] = None) -> dict[str, Any]:
    result = subprocess.run(command, capture_output=True, text=True, check=False, env=dict(env) if env else None)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "command failed")
    return json.loads(result.stdout)
