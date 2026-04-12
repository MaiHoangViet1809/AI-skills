#!/usr/bin/env python3
import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


def load_events(raw_text: str) -> List[Dict[str, Any]]:
    text = raw_text.strip()
    if not text:
        return []
    if text.startswith("["):
        data = json.loads(text)
        return [item for item in data if isinstance(item, dict)]

    events = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            parsed = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            events.append(parsed)
    return events


def normalize_error(result_event: Dict[str, Any], rate_limit_info: Optional[Dict[str, Any]]) -> Optional[str]:
    if rate_limit_info and rate_limit_info.get("status") not in (None, "allowed", "allowed_warning"):
        return "rate_limit"
    if result_event.get("is_error"):
        text = (result_event.get("result") or "").lower()
        if "rate limit" in text or "hit your limit" in text:
            return "rate_limit"
        return result_event.get("subtype") or "error"
    return None


def ensure_logs_dir(repo_root: Path) -> Path:
    path = repo_root / "logs_session_ai_agent"
    path.mkdir(parents=True, exist_ok=True)
    return path


def extract_summary(events: List[Dict[str, Any]], mode: str, raw_log_path: Path) -> Dict[str, Any]:
    result_event: Dict[str, Any] = {}
    assistant_event: Dict[str, Any] = {}
    rate_limit_event: Dict[str, Any] = {}
    session_id = None
    structured_output = None

    for event in events:
        session_id = session_id or event.get("session_id")
        if event.get("type") == "assistant":
            assistant_event = event
        elif event.get("type") == "rate_limit_event":
            rate_limit_event = event
        elif event.get("type") == "result":
            result_event = event
            if event.get("structured_output") is not None:
                structured_output = event.get("structured_output")

    if structured_output is None:
        structured_output = result_event.get("structured_output")

    rate_limit_info = rate_limit_event.get("rate_limit_info") if rate_limit_event else None
    usage = result_event.get("usage") or assistant_event.get("message", {}).get("usage") or {}
    result_text = result_event.get("result")

    if result_text is None and assistant_event:
        pieces = assistant_event.get("message", {}).get("content") or []
        texts = [piece.get("text") for piece in pieces if isinstance(piece, dict) and piece.get("type") == "text"]
        result_text = "\n".join([t for t in texts if t]) or None

    status = None
    if isinstance(structured_output, dict):
        status = structured_output.get("status")

    summary = {
        "session_id": result_event.get("session_id") or session_id,
        "mode": mode,
        "is_error": bool(result_event.get("is_error")),
        "error": normalize_error(result_event, rate_limit_info),
        "status": status,
        "result_text": result_text,
        "structured_output": structured_output,
        "rate_limit_info": {
            "status": rate_limit_info.get("status"),
            "rateLimitType": rate_limit_info.get("rateLimitType"),
            "resetsAt": rate_limit_info.get("resetsAt"),
            "utilization": rate_limit_info.get("utilization"),
            "overageStatus": rate_limit_info.get("overageStatus"),
            "isUsingOverage": rate_limit_info.get("isUsingOverage"),
        } if rate_limit_info else None,
        "usage": {
            "input_tokens": usage.get("input_tokens"),
            "output_tokens": usage.get("output_tokens"),
            "cache_creation_input_tokens": usage.get("cache_creation_input_tokens"),
            "cache_read_input_tokens": usage.get("cache_read_input_tokens"),
            "total_cost_usd": result_event.get("total_cost_usd"),
        },
        "duration_ms": result_event.get("duration_ms"),
        "stop_reason": result_event.get("stop_reason"),
        "raw_log_path": str(raw_log_path),
        "anomaly_flags": [],
    }

    if not summary["session_id"]:
        summary["anomaly_flags"].append("missing_session_id")
    if summary["is_error"] and not summary["error"]:
        summary["anomaly_flags"].append("unclassified_error")
    if mode == "json" and not result_event:
        summary["anomaly_flags"].append("missing_result_event")

    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-log", required=True)
    parser.add_argument("--mode", required=True, choices=["json", "stream-json"])
    parser.add_argument("--repo-root", required=True)
    args = parser.parse_args()

    raw_log = Path(args.raw_log).resolve()
    repo_root = Path(args.repo_root).resolve()
    logs_dir = ensure_logs_dir(repo_root)
    events = load_events(raw_log.read_text(encoding="utf-8"))
    summary = extract_summary(events, args.mode, raw_log)

    session_id = summary.get("session_id") or f"unknown-{int(datetime.now().timestamp())}"
    final_raw_log = logs_dir / f"claude-{session_id}.log"
    if raw_log != final_raw_log:
        final_raw_log.write_text(raw_log.read_text(encoding="utf-8"), encoding="utf-8")
        raw_log.unlink(missing_ok=True)
        summary["raw_log_path"] = str(final_raw_log)

    summary["parsed_at"] = datetime.now().astimezone().isoformat(timespec="seconds")
    print(json.dumps(summary, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
