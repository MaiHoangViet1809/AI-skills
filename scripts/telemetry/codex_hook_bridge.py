#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
GLOBAL_ROOT = Path.home() / ".logs" / "codex" / "telemetry"
STATE_DIR = GLOBAL_ROOT / "hook-state"
DEBUG_DIR = GLOBAL_ROOT / "hook-debug"
MARKER_PREFIX = "CODEX_SKILL_RUN"
PILOT_SKILL = "task-router-flow"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def ensure_dirs() -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    DEBUG_DIR.mkdir(parents=True, exist_ok=True)


def debug_write(event_name: str, payload: dict[str, Any]) -> None:
    ensure_dirs()
    session_id = extract_session_id(payload) or "unknown-session"
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = DEBUG_DIR / f"{stamp}-{event_name}-{session_id}.json"
    path.write_text(json.dumps(payload, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def nested_get(payload: Any, *keys: str) -> Any:
    current = payload
    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def extract_session_id(payload: dict[str, Any]) -> str | None:
    for value in (
        payload.get("session_id"),
        nested_get(payload, "session", "id"),
        nested_get(payload, "payload", "session_id"),
        nested_get(payload, "payload", "session", "id"),
    ):
        if isinstance(value, str) and value:
            return value
    return None


def extract_cwd(payload: dict[str, Any]) -> str | None:
    for value in (
        payload.get("cwd"),
        nested_get(payload, "session", "cwd"),
        nested_get(payload, "payload", "cwd"),
        nested_get(payload, "payload", "session", "cwd"),
    ):
        if isinstance(value, str) and value:
            return value
    return None


def extract_prompt(payload: dict[str, Any]) -> str:
    candidates = (
        payload.get("prompt"),
        payload.get("input"),
        nested_get(payload, "payload", "prompt"),
        nested_get(payload, "payload", "input"),
        nested_get(payload, "payload", "text"),
        nested_get(payload, "user_prompt"),
    )
    for value in candidates:
        if isinstance(value, str) and value:
            return value
    return ""


def extract_transcript_path(payload: dict[str, Any]) -> str | None:
    for value in (
        payload.get("transcript_path"),
        nested_get(payload, "payload", "transcript_path"),
        nested_get(payload, "session", "transcript_path"),
    ):
        if isinstance(value, str) and value:
            return value
    return None


def state_path(session_id: str) -> Path:
    ensure_dirs()
    return STATE_DIR / f"{session_id}.json"


def load_state(session_id: str) -> dict[str, Any]:
    path = state_path(session_id)
    if not path.exists():
        return {"session_id": session_id}
    return json.loads(path.read_text(encoding="utf-8"))


def save_state(session_id: str, state: dict[str, Any]) -> None:
    state_path(session_id).write_text(json.dumps(state, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def global_run_path(project_name: str, run_id: str) -> Path:
    safe_project = project_name.replace("/", "_")
    return GLOBAL_ROOT / "runs" / f"{safe_project}__{run_id}.json"


def parse_marker(prompt: str) -> dict[str, str]:
    metadata: dict[str, str] = {}
    for line in prompt.splitlines():
        stripped = line.strip()
        if not stripped.startswith(MARKER_PREFIX):
            continue
        parts = stripped.split()
        for part in parts[1:]:
            if "=" not in part:
                continue
            key, value = part.split("=", 1)
            metadata[key.strip()] = value.strip()
    return metadata


def script_json(args: list[str]) -> dict[str, Any]:
    result = subprocess.run(args, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "command failed")
    return json.loads(result.stdout)


def prompt_from_transcript(transcript_path: str | None) -> str:
    if not transcript_path:
        return ""
    path = Path(transcript_path)
    if not path.exists():
        return ""
    prompts: list[str] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            payload = event.get("payload")
            if not isinstance(payload, dict):
                continue
            if event.get("type") == "event_msg" and payload.get("type") == "user_message":
                message = payload.get("message")
                if isinstance(message, str) and message:
                    prompts.append(message)
                continue
            if payload.get("type") != "message" or payload.get("role") != "user":
                continue
            content = payload.get("content")
            if not isinstance(content, list):
                continue
            parts: list[str] = []
            for item in content:
                if not isinstance(item, dict):
                    continue
                if item.get("type") in {"input_text", "text"} and isinstance(item.get("text"), str):
                    parts.append(item["text"])
            if parts:
                prompts.append("\n".join(parts))
    for prompt in reversed(prompts):
        if MARKER_PREFIX in prompt:
            return prompt
    return prompts[-1] if prompts else ""


def telemetry_start(session_id: str, metadata: dict[str, str], started_at: str | None = None) -> dict[str, Any]:
    command = [
        sys.executable,
        str(REPO_ROOT / "skills" / "telemetry-flow" / "scripts" / "telemetry_hook.py"),
        "start",
        "--repo-root",
        str(REPO_ROOT),
        "--skill",
        metadata.get("skill", PILOT_SKILL),
        "--plan",
        metadata.get("plan", "subagent telemetry pilot"),
        "--sow",
        metadata.get("sow", "SOW_0033"),
        "--task-type",
        metadata.get("task_type", "docs"),
        "--intent",
        metadata.get("intent", "task-router hook pilot"),
        "--codex-session-id",
        session_id,
    ]
    if started_at:
        command.extend(["--started-at", started_at])
    return script_json(command)


def telemetry_finish(session_id: str, run_id: str, metadata: dict[str, str]) -> dict[str, Any]:
    command = [
        sys.executable,
        str(REPO_ROOT / "skills" / "telemetry-flow" / "scripts" / "telemetry_hook.py"),
        "finish",
        "--repo-root",
        str(REPO_ROOT),
        "--run-id",
        run_id,
        "--codex-session-id",
        session_id,
        "--success-state",
        metadata.get("success_state", "accepted"),
        "--validation-pass",
        metadata.get("validation_pass", "true"),
        "--scope-respected",
        metadata.get("scope_respected", "true"),
        "--repair-rounds",
        metadata.get("repair_rounds", "0"),
        "--outcome",
        metadata.get("outcome", "hook_subagent_pilot"),
    ]
    try:
        return script_json(command)
    except RuntimeError as exc:
        return {
            "run_id": run_id,
            "skill": metadata.get("skill", PILOT_SKILL),
            "finished_at": utc_now_iso(),
            "anomaly_flags": ["hook_finish_failed", str(exc)],
        }


def write_fallback_run_record(state: dict[str, Any], finish_result: dict[str, Any]) -> None:
    staging_file = state.get("telemetry_staging_file")
    if not staging_file:
        return
    path = Path(staging_file)
    if not path.exists():
        return
    record = json.loads(path.read_text(encoding="utf-8"))
    record["finished_at"] = finish_result.get("finished_at")
    record["result"] = finish_result
    project_name = record.get("project_name") or REPO_ROOT.name
    global_path = global_run_path(project_name, record["run_id"])
    global_path.parent.mkdir(parents=True, exist_ok=True)
    global_path.write_text(json.dumps(record, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def handle_session_start(payload: dict[str, Any]) -> int:
    session_id = extract_session_id(payload)
    if not session_id:
        return 0
    state = load_state(session_id)
    state["session_id"] = session_id
    state["cwd"] = extract_cwd(payload)
    state["session_started_at"] = utc_now_iso()
    state["transcript_path"] = extract_transcript_path(payload)
    save_state(session_id, state)
    return 0


def handle_user_prompt_submit(payload: dict[str, Any]) -> int:
    session_id = extract_session_id(payload)
    if not session_id:
        return 0
    prompt = extract_prompt(payload)
    metadata = parse_marker(prompt)
    if metadata.get("skill") != PILOT_SKILL:
        return 0
    state = load_state(session_id)
    state["prompt"] = prompt
    state["metadata"] = metadata
    state["cwd"] = extract_cwd(payload) or state.get("cwd")
    if state.get("run_id"):
        save_state(session_id, state)
        return 0
    start_result = telemetry_start(session_id, metadata, state.get("session_started_at"))
    state["run_id"] = start_result["run_id"]
    state["telemetry_started_at"] = start_result["started_at"]
    state["telemetry_staging_file"] = start_result["staging_file"]
    save_state(session_id, state)
    return 0


def handle_stop(payload: dict[str, Any]) -> int:
    session_id = extract_session_id(payload)
    if not session_id:
        return 0
    state = load_state(session_id)
    transcript_path = extract_transcript_path(payload) or state.get("transcript_path")
    prompt = state.get("prompt") or prompt_from_transcript(transcript_path)
    metadata = state.get("metadata") or parse_marker(prompt)
    state["transcript_path"] = transcript_path
    if metadata.get("skill") != PILOT_SKILL:
        save_state(session_id, state)
        return 0
    run_id = state.get("run_id")
    if not run_id:
        start_result = telemetry_start(session_id, metadata, state.get("session_started_at"))
        run_id = start_result["run_id"]
        state["run_id"] = run_id
        state["telemetry_started_at"] = start_result["started_at"]
        state["telemetry_staging_file"] = start_result["staging_file"]
        state["metadata"] = metadata
        state["prompt"] = prompt
    if state.get("telemetry_finished"):
        return 0
    finish_result = telemetry_finish(session_id, run_id, metadata)
    if "hook_finish_failed" in (finish_result.get("anomaly_flags") or []):
        write_fallback_run_record(state, finish_result)
    state["telemetry_finished"] = True
    state["finished_at"] = finish_result.get("finished_at")
    state["finish_result"] = finish_result
    state["result_file"] = str((Path.home() / ".logs" / "codex" / "telemetry" / "runs").resolve())
    save_state(session_id, state)
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("event", choices=["session-start", "user-prompt-submit", "stop"])
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    payload = json.load(sys.stdin)
    debug_write(args.event, payload)
    if args.event == "session-start":
        return handle_session_start(payload)
    if args.event == "user-prompt-submit":
        return handle_user_prompt_submit(payload)
    return handle_stop(payload)


if __name__ == "__main__":
    raise SystemExit(main())
