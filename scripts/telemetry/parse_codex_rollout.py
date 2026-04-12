#!/usr/bin/env python3
import argparse
import glob
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple


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


def parse_timestamp(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def timestamp_to_iso(value: Optional[datetime]) -> Optional[str]:
    if not value:
        return None
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


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


def find_message_windows(messages: List[Dict[str, Any]], start_text: str, finish_text: str) -> Dict[str, Any]:
    starts = [m for m in messages if (m.get("message") or "").strip() == start_text]
    finishes = [m for m in messages if (m.get("message") or "").strip() == finish_text]
    return {
        "start_marker": start_text,
        "finish_marker": finish_text,
        "starts": starts,
        "finishes": finishes,
    }


def find_marker_windows(agent_messages: List[Dict[str, Any]], user_messages: List[Dict[str, Any]], skill: str, sow: str) -> Dict[str, Any]:
    start_text = f"--- START SKILL {skill} FOR SOW {sow} ---"
    finish_text = f"--- FINISH SKILL {skill} FOR SOW {sow} ---"
    return find_message_windows(agent_messages + user_messages, start_text, finish_text)


def compute_window_metrics(
    events: List[Dict[str, Any]],
    started_at: Optional[datetime],
    finished_at: Optional[datetime],
    start_marker: Optional[str],
    finish_marker: Optional[str],
) -> Dict[str, Any]:
    token_events = extract_token_events(events)
    messages = extract_messages(events)

    marker_windows = None
    effective_started_at = started_at
    effective_finished_at = finished_at
    matched_by = "time_window"

    if start_marker or finish_marker:
        marker_windows = find_message_windows(messages, (start_marker or "").strip(), (finish_marker or "").strip())
        if marker_windows["starts"]:
            effective_started_at = parse_timestamp(marker_windows["starts"][0]["timestamp"]) or effective_started_at
            matched_by = "marker"
        if marker_windows["finishes"]:
            effective_finished_at = parse_timestamp(marker_windows["finishes"][-1]["timestamp"]) or effective_finished_at
            matched_by = "marker"

    end_snapshot = last_event_before_or_at(token_events, effective_finished_at)
    last_window_snapshot = last_event_in_window(token_events, effective_started_at, effective_finished_at) or end_snapshot
    anomaly_flags: List[str] = []
    window_token_events: List[Dict[str, Any]] = []
    for event in token_events:
        ts = parse_timestamp(event.get("timestamp"))
        if not ts:
            continue
        if effective_started_at and ts < effective_started_at:
            continue
        if effective_finished_at and ts > effective_finished_at:
            continue
        window_token_events.append(event)

    codex_task_tokens = 0
    codex_cached_input_tokens = 0
    codex_fresh_input_tokens = 0
    codex_output_tokens = 0
    codex_reasoning_output_tokens = 0
    codex_turn_count = 0
    codex_avg_tokens_per_turn = None
    codex_last_turn_tokens = None

    for event in window_token_events:
        usage = event.get("last_token_usage", {})
        total = total_tokens(usage)
        cached = usage_int(usage, "cached_input_tokens")
        fresh_input = max(usage_int(usage, "input_tokens") - cached, 0)
        output = usage_int(usage, "output_tokens")
        reasoning = usage_int(usage, "reasoning_output_tokens")
        turn_tokens = (total - cached) if total is not None else (fresh_input + output)

        codex_task_tokens += turn_tokens
        codex_cached_input_tokens += cached
        codex_fresh_input_tokens += fresh_input
        codex_output_tokens += output
        codex_reasoning_output_tokens += reasoning
        codex_turn_count += 1
        codex_last_turn_tokens = turn_tokens

    if codex_turn_count == 0:
        anomaly_flags.append("missing_codex_turn_usage")
    else:
        codex_avg_tokens_per_turn = codex_task_tokens / codex_turn_count

    if not effective_started_at:
        anomaly_flags.append("missing_effective_started_at")
    if not effective_finished_at:
        anomaly_flags.append("missing_effective_finished_at")

    return {
        "matched_by": matched_by,
        "effective_started_at": timestamp_to_iso(effective_started_at),
        "effective_finished_at": timestamp_to_iso(effective_finished_at),
        "codex_task_tokens": codex_task_tokens if codex_turn_count > 0 else None,
        "codex_cached_input_tokens": codex_cached_input_tokens if codex_turn_count > 0 else None,
        "codex_fresh_input_tokens": codex_fresh_input_tokens if codex_turn_count > 0 else None,
        "codex_output_tokens": codex_output_tokens if codex_turn_count > 0 else None,
        "codex_reasoning_output_tokens": codex_reasoning_output_tokens if codex_turn_count > 0 else None,
        "codex_turn_count": codex_turn_count,
        "codex_avg_tokens_per_turn": codex_avg_tokens_per_turn,
        "codex_last_turn_tokens": codex_last_turn_tokens,
        "marker_windows": marker_windows,
        "anomaly_flags": anomaly_flags,
    }


def select_rollout_for_window(
    cwd: str,
    started_at: datetime,
    finished_at: Optional[datetime],
    start_marker: Optional[str],
    finish_marker: Optional[str],
) -> Tuple[Optional[Path], List[Dict[str, Any]]]:
    best_path: Optional[Path] = None
    best_events: List[Dict[str, Any]] = []
    best_score: Tuple[int, datetime] = (-1, datetime.min.replace(tzinfo=timezone.utc))

    for path in rollout_paths_for_days(collect_days(started_at, finished_at)):
        events = load_rollout(path)
        if not events:
            continue

        metrics = parse_metrics(events)
        if metrics.get("cwd") != cwd:
            continue

        event_times = [event_timestamp(event) for event in events if event_timestamp(event)]
        if not event_times:
            continue

        first_seen = min(event_times)
        last_seen = max(event_times)
        if finished_at and first_seen > finished_at + timedelta(minutes=5):
            continue
        if last_seen < started_at - timedelta(minutes=5):
            continue

        window_metrics = compute_window_metrics(events, started_at, finished_at, start_marker, finish_marker)
        marker_hits = window_metrics.get("marker_windows") or {}
        score = 2 if marker_hits.get("starts") or marker_hits.get("finishes") else 1
        ranking = (score, last_seen)
        if ranking > best_score:
            best_score = ranking
            best_path = path
            best_events = events

    return best_path, best_events


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rollout-file")
    parser.add_argument("--session-id")
    parser.add_argument("--day")
    parser.add_argument("--cwd")
    parser.add_argument("--started-at")
    parser.add_argument("--finished-at")
    parser.add_argument("--start-marker")
    parser.add_argument("--finish-marker")
    parser.add_argument("--marker-skill")
    parser.add_argument("--marker-sow")
    args = parser.parse_args()

    target: Optional[Path] = None
    target_events: Optional[List[Dict[str, Any]]] = None
    if args.rollout_file:
        target = Path(args.rollout_file).expanduser().resolve()
    elif args.session_id:
        target = find_rollout_by_session_id(args.session_id)
    elif args.day:
        target = find_latest_rollout_for_day(args.day)
    elif args.cwd and args.started_at:
        started_at = parse_timestamp(args.started_at)
        finished_at = parse_timestamp(args.finished_at) if args.finished_at else None
        if not started_at:
            raise SystemExit("invalid started-at timestamp")
        target, target_events = select_rollout_for_window(
            cwd=str(Path(args.cwd).resolve()),
            started_at=started_at,
            finished_at=finished_at,
            start_marker=args.start_marker,
            finish_marker=args.finish_marker,
        )

    if not target or not target.exists():
        raise SystemExit("rollout file not found")

    events = target_events or load_rollout(target)
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

    if args.started_at or args.start_marker or args.finish_marker:
        summary["window_metrics"] = compute_window_metrics(
            events,
            parse_timestamp(args.started_at) if args.started_at else None,
            parse_timestamp(args.finished_at) if args.finished_at else None,
            args.start_marker,
            args.finish_marker,
        )

    print(json.dumps(summary, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
