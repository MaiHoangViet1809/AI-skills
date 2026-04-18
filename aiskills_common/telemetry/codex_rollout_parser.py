from __future__ import annotations

import argparse
import glob
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence

from .time_utils import parse_timestamp, timestamp_to_iso


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


def collect_days(started_at: datetime, finished_at: Optional[datetime]) -> List[str]:
    days: List[str] = []
    cursor = started_at.date()
    final_day = (finished_at or started_at).date()
    while cursor <= final_day:
        days.append(cursor.isoformat())
        cursor += timedelta(days=1)
    return days


def rollout_paths_for_days(days: Sequence[str]) -> List[Path]:
    paths: List[Path] = []
    for day in days:
        yyyy, mm, dd = day.split("-")
        base = SESSIONS_ROOT / yyyy / mm / dd
        if not base.exists():
            continue
        paths.extend(sorted(base.glob("rollout-*.jsonl")))
    return paths


def payload(event: Dict[str, Any]) -> Dict[str, Any]:
    return event.get("payload") or {}


def event_timestamp(event: Dict[str, Any]) -> Optional[datetime]:
    return parse_timestamp(event.get("timestamp"))


def extract_token_events(events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    token_events: List[Dict[str, Any]] = []
    for event in events:
        if event.get("type") != "event_msg":
            continue
        p = payload(event)
        if p.get("type") != "token_count":
            continue
        token_events.append(
            {
                "timestamp": event.get("timestamp"),
                "payload": p,
                "total_token_usage": (p.get("info") or {}).get("total_token_usage") or {},
                "last_token_usage": (p.get("info") or {}).get("last_token_usage") or {},
            }
        )
    return token_events


def extract_messages(events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    messages: List[Dict[str, Any]] = []
    for event in events:
        if event.get("type") != "event_msg":
            continue
        p = payload(event)
        if p.get("type") not in {"agent_message", "user_message"}:
            continue
        messages.append(
            {
                "timestamp": event.get("timestamp"),
                "message": p.get("message"),
                "role": "assistant" if p.get("type") == "agent_message" else "user",
                "phase": p.get("phase"),
            }
        )
    return messages


def extract_tool_events(events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    tool_events: List[Dict[str, Any]] = []
    for event in events:
        ts = event.get("timestamp")
        if event.get("type") == "response_item":
            payload_obj = payload(event)
            payload_type = payload_obj.get("type")
            if payload_type in {"function_call", "function_call_output"}:
                tool_events.append(
                    {
                        "timestamp": ts,
                        "event_type": payload_type,
                        "name": payload_obj.get("name"),
                        "call_id": payload_obj.get("call_id"),
                    }
                )
        elif event.get("type") == "event_msg":
            payload_obj = payload(event)
            msg_type = payload_obj.get("type")
            if msg_type in {"exec_command_end", "exec_command_start"}:
                tool_events.append(
                    {
                        "timestamp": ts,
                        "event_type": msg_type,
                        "name": "exec_command",
                        "call_id": payload_obj.get("call_id"),
                    }
                )
    return tool_events


def classify_codex_tool(name: Optional[str]) -> str:
    if not name:
        return "unknown"
    if str(name).startswith("mcp__"):
        return "mcp"
    return "tool"


def total_tokens(usage: Dict[str, Any]) -> Optional[int]:
    value = usage.get("total_tokens")
    return int(value) if isinstance(value, int) else None


def usage_int(usage: Dict[str, Any], key: str) -> int:
    value = usage.get(key)
    return int(value) if isinstance(value, int) else 0


def last_event_before_or_at(items: Iterable[Dict[str, Any]], point: Optional[datetime]) -> Optional[Dict[str, Any]]:
    chosen: Optional[Dict[str, Any]] = None
    for item in items:
        ts = parse_timestamp(item.get("timestamp"))
        if not ts:
            continue
        if point is None or ts <= point:
            chosen = item
        else:
            break
    return chosen


def last_event_in_window(items: Iterable[Dict[str, Any]], started_at: Optional[datetime], finished_at: Optional[datetime]) -> Optional[Dict[str, Any]]:
    chosen: Optional[Dict[str, Any]] = None
    for item in items:
        ts = parse_timestamp(item.get("timestamp"))
        if not ts:
            continue
        if started_at and ts < started_at:
            continue
        if finished_at and ts > finished_at:
            continue
        chosen = item
    return chosen


def parse_metrics(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    session_meta = {}
    token_events = extract_token_events(events)
    task_complete = None
    agent_messages: List[Dict[str, Any]] = []
    user_messages: List[Dict[str, Any]] = []

    for event in events:
        event_type = event.get("type")
        p = payload(event)

        if event_type == "session_meta":
            session_meta = p
        elif event_type == "event_msg" and p.get("type") == "task_complete":
            task_complete = {"timestamp": event.get("timestamp"), "payload": p}
        elif event_type == "event_msg" and p.get("type") == "agent_message":
            agent_messages.append({"timestamp": event.get("timestamp"), "message": p.get("message"), "phase": p.get("phase")})
        elif event_type == "event_msg" and p.get("type") == "user_message":
            user_messages.append({"timestamp": event.get("timestamp"), "message": p.get("message")})

    last_token = token_events[-1].get("last_token_usage", {}) if token_events else {}
    total_token = token_events[-1].get("total_token_usage", {}) if token_events else {}
    rate_limits = token_events[-1].get("payload", {}).get("rate_limits", {}) if token_events else {}

    return {
        "session_id": session_meta.get("id"),
        "session_timestamp": session_meta.get("timestamp"),
        "cwd": session_meta.get("cwd"),
        "model_provider": session_meta.get("model_provider"),
        "task_complete": task_complete,
        "agent_messages": agent_messages,
        "user_messages": user_messages,
        "last_token_usage": last_token,
        "total_token_usage": total_token,
        "rate_limits": rate_limits,
        "token_event_count": len(token_events),
        "last_event_timestamp": events[-1].get("timestamp") if events else None,
    }


def find_message_windows(messages: List[Dict[str, Any]], started_at: Optional[datetime], finished_at: Optional[datetime]) -> Dict[str, Optional[datetime]]:
    first_user = None
    last_assistant = None
    for msg in messages:
        ts = parse_timestamp(msg.get("timestamp"))
        if not ts:
            continue
        if started_at and ts < started_at:
            continue
        if finished_at and ts > finished_at:
            continue
        if msg.get("role") == "user" and first_user is None:
            first_user = ts
        if msg.get("role") == "assistant":
            last_assistant = ts
    return {"first_user_at": first_user, "last_assistant_at": last_assistant}


def find_marker_windows(messages: List[Dict[str, Any]], start_marker: Optional[str], finish_marker: Optional[str]) -> Dict[str, Optional[datetime]]:
    start_at = None
    finish_at = None
    for msg in messages:
        text = msg.get("message")
        ts = parse_timestamp(msg.get("timestamp"))
        if not text or not ts:
            continue
        if start_marker and start_marker in str(text):
            start_at = ts
        if finish_marker and finish_marker in str(text):
            finish_at = ts
    return {"start_marker_at": start_at, "finish_marker_at": finish_at}


def compute_window_metrics(
    token_events: List[Dict[str, Any]],
    tool_events: List[Dict[str, Any]],
    started_at: Optional[datetime],
    finished_at: Optional[datetime],
) -> Dict[str, Any]:
    start_event = last_event_before_or_at(token_events, started_at)
    end_event = last_event_before_or_at(token_events, finished_at)
    last_window_event = last_event_in_window(token_events, started_at, finished_at)

    anomaly_flags: List[str] = []
    if not start_event or not end_event:
        anomaly_flags.append("missing_token_window")
        return {
            "matched_by": None,
            "started_at": timestamp_to_iso(started_at),
            "finished_at": timestamp_to_iso(finished_at),
            "anomaly_flags": anomaly_flags,
            "codex_task_tokens": 0,
            "codex_cached_input_tokens": 0,
            "codex_fresh_input_tokens": 0,
            "codex_output_tokens": 0,
            "codex_reasoning_output_tokens": 0,
            "codex_turn_count": 0,
            "codex_avg_tokens_per_turn": 0.0,
            "codex_last_turn_tokens": 0,
            "codex_tool_call_count": 0,
            "codex_tool_error_count": 0,
            "codex_mcp_call_count": 0,
            "codex_unique_tool_names": [],
            "codex_unique_mcp_tool_names": [],
        }

    start_total = start_event.get("total_token_usage", {})
    end_total = end_event.get("total_token_usage", {})
    codex_cached_input_tokens = max(0, usage_int(end_total, "cached_input_tokens") - usage_int(start_total, "cached_input_tokens"))
    codex_fresh_input_tokens = max(0, usage_int(end_total, "input_tokens") - usage_int(start_total, "input_tokens"))
    codex_output_tokens = max(0, usage_int(end_total, "output_tokens") - usage_int(start_total, "output_tokens"))
    codex_reasoning_output_tokens = max(0, usage_int(end_total, "reasoning_output_tokens") - usage_int(start_total, "reasoning_output_tokens"))
    codex_task_tokens = codex_fresh_input_tokens + codex_output_tokens

    window_token_events = []
    for event in token_events:
        ts = parse_timestamp(event.get("timestamp"))
        if not ts:
            continue
        if started_at and ts < started_at:
            continue
        if finished_at and ts > finished_at:
            continue
        window_token_events.append(event)

    turn_tokens = [total_tokens((event.get("last_token_usage") or {})) or 0 for event in window_token_events]
    codex_turn_count = len(turn_tokens)
    codex_avg_tokens_per_turn = (sum(turn_tokens) / codex_turn_count) if codex_turn_count else 0.0
    codex_last_turn_tokens = turn_tokens[-1] if turn_tokens else 0

    codex_tool_call_count = 0
    codex_tool_error_count = 0
    codex_mcp_call_count = 0
    codex_unique_tool_names = set()
    codex_unique_mcp_tool_names = set()

    for event in tool_events:
        ts = parse_timestamp(event.get("timestamp"))
        if not ts:
            continue
        if started_at and ts < started_at:
            continue
        if finished_at and ts > finished_at:
            continue
        if event.get("event_type") not in {"function_call", "exec_command_start"}:
            continue
        name = event.get("name")
        category = classify_codex_tool(name)
        if category == "mcp":
            codex_mcp_call_count += 1
            if name:
                codex_unique_mcp_tool_names.add(str(name))
        else:
            codex_tool_call_count += 1
            if name:
                codex_unique_tool_names.add(str(name))

    return {
        "matched_by": "marker",
        "started_at": timestamp_to_iso(started_at),
        "finished_at": timestamp_to_iso(finished_at),
        "last_window_event_at": last_window_event.get("timestamp") if last_window_event else None,
        "anomaly_flags": anomaly_flags,
        "codex_task_tokens": codex_task_tokens,
        "codex_cached_input_tokens": codex_cached_input_tokens,
        "codex_fresh_input_tokens": codex_fresh_input_tokens,
        "codex_output_tokens": codex_output_tokens,
        "codex_reasoning_output_tokens": codex_reasoning_output_tokens,
        "codex_turn_count": codex_turn_count,
        "codex_avg_tokens_per_turn": codex_avg_tokens_per_turn,
        "codex_last_turn_tokens": codex_last_turn_tokens,
        "codex_tool_call_count": codex_tool_call_count,
        "codex_tool_error_count": codex_tool_error_count,
        "codex_mcp_call_count": codex_mcp_call_count,
        "codex_unique_tool_names": sorted(codex_unique_tool_names),
        "codex_unique_mcp_tool_names": sorted(codex_unique_mcp_tool_names),
    }


def select_rollout_for_window(
    *,
    session_id: Optional[str],
    rollout_file: Optional[str],
    started_at: Optional[datetime],
    finished_at: Optional[datetime],
) -> Optional[Path]:
    if rollout_file:
        path = Path(rollout_file).resolve()
        return path if path.exists() else None
    if session_id:
        return find_rollout_by_session_id(session_id)
    if started_at:
        days = collect_days(started_at, finished_at)
        paths = rollout_paths_for_days(days)
        return paths[-1] if paths else None
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--session-id")
    parser.add_argument("--rollout-file")
    parser.add_argument("--cwd")
    parser.add_argument("--started-at")
    parser.add_argument("--finished-at")
    parser.add_argument("--start-marker")
    parser.add_argument("--finish-marker")
    args = parser.parse_args()

    started_at = parse_timestamp(args.started_at)
    finished_at = parse_timestamp(args.finished_at)

    rollout_path = select_rollout_for_window(
        session_id=args.session_id,
        rollout_file=args.rollout_file,
        started_at=started_at,
        finished_at=finished_at,
    )
    if rollout_path is None:
        print(json.dumps({"rollout_file": None, "metrics": {}, "window_metrics": {"matched_by": None, "anomaly_flags": ["missing_rollout_file"]}}, ensure_ascii=True, indent=2))
        return 0

    events = load_rollout(rollout_path)
    metrics = parse_metrics(events)
    messages = extract_messages(events)
    tool_events = extract_tool_events(events)

    marker_windows = find_marker_windows(messages, args.start_marker, args.finish_marker)
    matched_started_at = marker_windows.get("start_marker_at") or started_at
    matched_finished_at = marker_windows.get("finish_marker_at") or finished_at
    window_metrics = compute_window_metrics(
        extract_token_events(events),
        tool_events,
        matched_started_at,
        matched_finished_at,
    )
    if not marker_windows.get("start_marker_at") or not marker_windows.get("finish_marker_at"):
        window_metrics["matched_by"] = "time_window"
        window_metrics.setdefault("anomaly_flags", []).append("missing_markers")

    result = {
        "rollout_file": str(rollout_path),
        "metrics": metrics,
        "message_windows": {
            key: timestamp_to_iso(value) for key, value in find_message_windows(messages, started_at, finished_at).items()
        },
        "marker_windows": {
            key: timestamp_to_iso(value) for key, value in marker_windows.items()
        },
        "window_metrics": window_metrics,
    }
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
