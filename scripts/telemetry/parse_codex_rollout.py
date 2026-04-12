#!/usr/bin/env python3
import argparse
import glob
import json
from pathlib import Path
from typing import Any, Dict, List, Optional


SESSIONS_ROOT = Path.home() / ".codex" / "sessions"


def load_rollout(path: Path) -> List[Dict[str, Any]]:
    events: List[Dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict):
            events.append(obj)
    return events


def find_rollout_by_session_id(session_id: str) -> Optional[Path]:
    pattern = str(SESSIONS_ROOT / "*" / "*" / "*" / ("*%s*.jsonl" % session_id))
    matches = sorted(glob.glob(pattern))
    return Path(matches[-1]) if matches else None


def find_latest_rollout_for_day(day: str) -> Optional[Path]:
    yyyy, mm, dd = day.split("-")
    base = SESSIONS_ROOT / yyyy / mm / dd
    matches = sorted(base.glob("rollout-*.jsonl"))
    return matches[-1] if matches else None


def payload(event: Dict[str, Any]) -> Dict[str, Any]:
    return event.get("payload") or {}


def parse_metrics(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    session_meta = {}
    token_events: List[Dict[str, Any]] = []
    task_complete = None
    agent_messages: List[Dict[str, Any]] = []
    user_messages: List[Dict[str, Any]] = []

    for event in events:
        event_type = event.get("type")
        p = payload(event)

        if event_type == "session_meta":
            session_meta = p
        elif event_type == "event_msg" and p.get("type") == "token_count":
            token_events.append({"timestamp": event.get("timestamp"), "payload": p})
        elif event_type == "event_msg" and p.get("type") == "task_complete":
            task_complete = {"timestamp": event.get("timestamp"), "payload": p}
        elif event_type == "event_msg" and p.get("type") == "agent_message":
            agent_messages.append({"timestamp": event.get("timestamp"), "message": p.get("message"), "phase": p.get("phase")})
        elif event_type == "event_msg" and p.get("type") == "user_message":
            user_messages.append({"timestamp": event.get("timestamp"), "message": p.get("message")})

    last_token = token_events[-1]["payload"].get("info", {}).get("last_token_usage", {}) if token_events else {}
    total_token = token_events[-1]["payload"].get("info", {}).get("total_token_usage", {}) if token_events else {}
    rate_limits = token_events[-1]["payload"].get("rate_limits", {}) if token_events else {}

    return {
        "session_id": session_meta.get("id"),
        "session_timestamp": session_meta.get("timestamp"),
        "cwd": session_meta.get("cwd"),
        "originator": session_meta.get("originator"),
        "source": session_meta.get("source"),
        "model_provider": session_meta.get("model_provider"),
        "last_token_usage": last_token,
        "total_token_usage": total_token,
        "rate_limits": rate_limits,
        "task_complete": task_complete,
        "agent_messages": agent_messages,
        "user_messages": user_messages,
    }


def find_marker_windows(agent_messages: List[Dict[str, Any]], user_messages: List[Dict[str, Any]], skill: str, sow: str) -> Dict[str, Any]:
    start_text = f"--- START SKILL {skill} FOR SOW {sow} ---"
    finish_text = f"--- FINISH SKILL {skill} FOR SOW {sow} ---"
    starts = [m for m in agent_messages + user_messages if m.get("message") == start_text]
    finishes = [m for m in agent_messages + user_messages if m.get("message") == finish_text]
    return {
        "start_marker": start_text,
        "finish_marker": finish_text,
        "starts": starts,
        "finishes": finishes,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rollout-file")
    parser.add_argument("--session-id")
    parser.add_argument("--day")
    parser.add_argument("--marker-skill")
    parser.add_argument("--marker-sow")
    args = parser.parse_args()

    target: Optional[Path] = None
    if args.rollout_file:
        target = Path(args.rollout_file).expanduser().resolve()
    elif args.session_id:
        target = find_rollout_by_session_id(args.session_id)
    elif args.day:
        target = find_latest_rollout_for_day(args.day)

    if not target or not target.exists():
        raise SystemExit("rollout file not found")

    events = load_rollout(target)
    summary = {
        "rollout_file": str(target),
        "metrics": parse_metrics(events),
    }

    if args.marker_skill and args.marker_sow:
        summary["marker_windows"] = find_marker_windows(
            summary["metrics"]["agent_messages"],
            summary["metrics"]["user_messages"],
            args.marker_skill,
            args.marker_sow,
        )

    print(json.dumps(summary, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
