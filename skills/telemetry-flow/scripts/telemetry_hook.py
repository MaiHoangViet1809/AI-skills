#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def parse_timestamp(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def parse_bool(value: str) -> bool:
    lowered = value.lower()
    if lowered in {"true", "1", "yes"}:
        return True
    if lowered in {"false", "0", "no"}:
        return False
    raise ValueError(f"invalid boolean value: {value}")


def ensure_logs_dir(repo_root: Path) -> Path:
    path = repo_root / "logs_session_ai_agent"
    path.mkdir(parents=True, exist_ok=True)
    return path


def staging_path(repo_root: Path, run_id: str) -> Path:
    return ensure_logs_dir(repo_root) / f"telemetry-run-{run_id}.json"


def run_git(repo_root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repo_root), *args],
        capture_output=True,
        text=True,
        check=False,
    )


def current_changed_files(repo_root: Path) -> List[str]:
    result = run_git(repo_root, "status", "--porcelain=v1", "-uall")
    if result.returncode != 0:
        return []

    changed: List[str] = []
    for line in result.stdout.splitlines():
        if len(line) < 4:
            continue
        path_text = line[3:]
        if " -> " in path_text:
            path_text = path_text.split(" -> ", 1)[1]
        changed.append(path_text)
    return sorted(set(changed))


def git_head(repo_root: Path) -> Optional[str]:
    result = run_git(repo_root, "rev-parse", "HEAD")
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def marker_text(kind: str, run_id: str, skill: str, plan: str, sow: str) -> str:
    return f"TELEMETRY_{kind} run_id={run_id} skill={skill} plan={plan or '-'} sow={sow or '-'}"


def write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def script_json(repo_root: Path, relative_script: str, args: List[str]) -> Dict[str, Any]:
    command = [sys.executable, str(repo_root / relative_script), *args]
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "command failed")
    return json.loads(result.stdout)


def usage_total(usage: Dict[str, Any]) -> int:
    total = 0
    for key in (
        "input_tokens",
        "output_tokens",
        "cache_creation_input_tokens",
        "cache_read_input_tokens",
    ):
        value = usage.get(key)
        if isinstance(value, int):
            total += value
    return total


def start_hook(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo_root).resolve()
    run_id = uuid.uuid4().hex
    started_at = utc_now_iso()
    skill = args.skill
    plan = args.plan or "-"
    sow = args.sow or "-"

    record = {
        "run_id": run_id,
        "repo_root": str(repo_root),
        "skill": skill,
        "plan": args.plan,
        "sow": args.sow,
        "task_type": args.task_type,
        "intent": args.intent,
        "started_at": started_at,
        "finished_at": None,
        "codex": {
            "session_id": args.codex_session_id,
            "start_marker": marker_text("START", run_id, skill, plan, sow),
            "finish_marker": marker_text("FINISH", run_id, skill, plan, sow),
        },
        "claude": {
            "raw_logs": [],
            "session_ids": [],
        },
        "baseline": {
            "git_head": git_head(repo_root),
            "changed_files": current_changed_files(repo_root),
        },
        "result": None,
    }

    path = staging_path(repo_root, run_id)
    write_json(path, record)

    print(
        json.dumps(
            {
                "run_id": run_id,
                "staging_file": str(path),
                "started_at": started_at,
                "start_marker": record["codex"]["start_marker"],
                "finish_marker": record["codex"]["finish_marker"],
                "baseline_changed_files_count": len(record["baseline"]["changed_files"]),
            },
            ensure_ascii=True,
            indent=2,
        )
    )
    return 0


def parse_claude_logs(repo_root: Path, raw_logs: List[str], mode: str) -> List[Dict[str, Any]]:
    summaries: List[Dict[str, Any]] = []
    for raw_log in raw_logs:
        summary = script_json(
            repo_root,
            "scripts/telemetry/parse_delegate_log.py",
            ["--raw-log", str(Path(raw_log).resolve()), "--mode", mode, "--repo-root", str(repo_root)],
        )
        raw_log_path = Path(summary["raw_log_path"])
        summary["finished_at"] = datetime.fromtimestamp(raw_log_path.stat().st_mtime, timezone.utc).isoformat().replace("+00:00", "Z")
        summaries.append(summary)
    summaries.sort(key=lambda item: item.get("finished_at") or "")
    return summaries


def parse_codex_window(
    repo_root: Path,
    started_at: str,
    finished_at: str,
    codex_session_id: Optional[str],
    rollout_file: Optional[str],
    start_marker: str,
    finish_marker: str,
) -> Dict[str, Any]:
    if rollout_file:
        args = ["--rollout-file", str(Path(rollout_file).resolve())]
    elif codex_session_id:
        args = ["--session-id", codex_session_id]
    else:
        args = [
            "--cwd",
            str(repo_root),
            "--started-at",
            started_at,
            "--finished-at",
            finished_at,
            "--start-marker",
            start_marker,
            "--finish-marker",
            finish_marker,
        ]
    if "--started-at" not in args:
        args.extend(["--started-at", started_at, "--finished-at", finished_at, "--start-marker", start_marker, "--finish-marker", finish_marker])
    return script_json(repo_root, "scripts/telemetry/parse_codex_rollout.py", args)


def finish_hook(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo_root).resolve()
    path = staging_path(repo_root, args.run_id)
    record = read_json(path)
    finished_at = args.finished_at or utc_now_iso()

    anomaly_flags: List[str] = []

    claude_summaries = parse_claude_logs(repo_root, args.claude_log or [], args.claude_mode) if args.claude_log else []
    if not claude_summaries:
        anomaly_flags.append("missing_claude_logs")

    latest_claude = claude_summaries[-1] if claude_summaries else {}
    latest_structured = latest_claude.get("structured_output") if isinstance(latest_claude.get("structured_output"), dict) else {}

    codex_summary = parse_codex_window(
        repo_root=repo_root,
        started_at=record["started_at"],
        finished_at=finished_at,
        codex_session_id=args.codex_session_id or record.get("codex", {}).get("session_id"),
        rollout_file=args.rollout_file,
        start_marker=record["codex"]["start_marker"],
        finish_marker=record["codex"]["finish_marker"],
    )

    window_metrics = codex_summary.get("window_metrics") or {}
    anomaly_flags.extend(window_metrics.get("anomaly_flags") or [])
    if window_metrics.get("matched_by") != "marker":
        anomaly_flags.append("degraded_codex_match")

    codex_total_tokens = window_metrics.get("codex_total_tokens")
    codex_last_tokens = window_metrics.get("codex_last_tokens")
    codex_session_id = (codex_summary.get("metrics") or {}).get("session_id")
    if not codex_session_id:
        anomaly_flags.append("missing_codex_session_id")

    claude_usage_totals = {
        "input_tokens": 0,
        "output_tokens": 0,
        "cache_creation_tokens": 0,
        "cache_read_tokens": 0,
    }
    claude_total_tokens = 0
    claude_duration_ms = 0
    claude_session_ids: List[str] = []
    for summary in claude_summaries:
        usage = summary.get("usage") or {}
        claude_usage_totals["input_tokens"] += int(usage.get("input_tokens") or 0)
        claude_usage_totals["output_tokens"] += int(usage.get("output_tokens") or 0)
        claude_usage_totals["cache_creation_tokens"] += int(usage.get("cache_creation_input_tokens") or 0)
        claude_usage_totals["cache_read_tokens"] += int(usage.get("cache_read_input_tokens") or 0)
        claude_total_tokens += usage_total(usage)
        claude_duration_ms += int(summary.get("duration_ms") or 0)
        if summary.get("session_id"):
            claude_session_ids.append(summary["session_id"])
        anomaly_flags.extend(summary.get("anomaly_flags") or [])

    started_dt = parse_timestamp(record["started_at"])
    finished_dt = parse_timestamp(finished_at)
    run_duration_ms = None
    if started_dt and finished_dt:
        run_duration_ms = int((finished_dt - started_dt).total_seconds() * 1000)

    first_usable_at = args.first_usable_at
    if not first_usable_at and claude_summaries:
        first_usable_at = min(summary["finished_at"] for summary in claude_summaries if summary.get("finished_at"))
    time_to_first_usable_result_ms = None
    if started_dt and first_usable_at:
        first_usable_dt = parse_timestamp(first_usable_at)
        if first_usable_dt:
            time_to_first_usable_result_ms = int((first_usable_dt - started_dt).total_seconds() * 1000)
    if (
        run_duration_ms is not None
        and time_to_first_usable_result_ms is not None
        and time_to_first_usable_result_ms > run_duration_ms
    ):
        anomaly_flags.append("first_usable_after_finish")
        time_to_first_usable_result_ms = run_duration_ms

    baseline_changed = set(record.get("baseline", {}).get("changed_files") or [])
    current_changed = set(current_changed_files(repo_root))
    files_changed_count = len(current_changed - baseline_changed)

    success_state = args.success_state
    fallback_flag = parse_bool(args.fallback_flag) if args.fallback_flag else success_state == "fallback_local"
    validation_pass = parse_bool(args.validation_pass)
    scope_respected = parse_bool(args.scope_respected) if args.scope_respected else latest_structured.get("scope_respected")
    repair_rounds = args.repair_rounds if args.repair_rounds is not None else max(0, len(claude_summaries) - 1)
    outcome = args.outcome or success_state

    total_tokens = None
    delegate_ratio = None
    codex_to_claude_ratio = None
    if isinstance(codex_total_tokens, int):
        total_tokens = codex_total_tokens + claude_total_tokens
        if total_tokens > 0:
            delegate_ratio = claude_total_tokens / total_tokens
    if claude_total_tokens > 0 and isinstance(codex_total_tokens, int):
        codex_to_claude_ratio = codex_total_tokens / claude_total_tokens

    result = {
        "run_id": record["run_id"],
        "skill": record.get("skill"),
        "plan": record.get("plan"),
        "sow": record.get("sow"),
        "task_type": record.get("task_type"),
        "intent": record.get("intent"),
        "started_at": record["started_at"],
        "finished_at": finished_at,
        "run_duration_ms": run_duration_ms,
        "time_to_first_usable_result_ms": time_to_first_usable_result_ms,
        "codex_session_id": codex_session_id,
        "codex_total_tokens": codex_total_tokens,
        "codex_last_tokens": codex_last_tokens,
        "claude_session_id": claude_session_ids[-1] if claude_session_ids else None,
        "claude_session_ids": claude_session_ids,
        "claude_input_tokens": claude_usage_totals["input_tokens"],
        "claude_output_tokens": claude_usage_totals["output_tokens"],
        "claude_cache_creation_tokens": claude_usage_totals["cache_creation_tokens"],
        "claude_cache_read_tokens": claude_usage_totals["cache_read_tokens"],
        "claude_total_tokens": claude_total_tokens,
        "claude_duration_ms": claude_duration_ms or None,
        "files_changed_count": files_changed_count,
        "repair_rounds": repair_rounds,
        "fallback_flag": fallback_flag,
        "validation_pass": validation_pass,
        "success_state": success_state,
        "scope_respected": scope_respected,
        "outcome": outcome,
        "delegate_ratio": delegate_ratio,
        "codex_to_claude_ratio": codex_to_claude_ratio,
        "anomaly_flags": sorted(set(anomaly_flags)),
        "codex_rollout_file": codex_summary.get("rollout_file"),
        "claude_raw_logs": [summary.get("raw_log_path") for summary in claude_summaries],
    }

    record["finished_at"] = finished_at
    record["claude"]["raw_logs"] = result["claude_raw_logs"]
    record["claude"]["session_ids"] = claude_session_ids
    record["codex"]["session_id"] = codex_session_id
    record["result"] = result
    write_json(path, record)

    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    start = subparsers.add_parser("start")
    start.add_argument("--repo-root", required=True)
    start.add_argument("--skill", required=True)
    start.add_argument("--plan")
    start.add_argument("--sow")
    start.add_argument("--task-type", required=True)
    start.add_argument("--intent")
    start.add_argument("--codex-session-id")

    finish = subparsers.add_parser("finish")
    finish.add_argument("--repo-root", required=True)
    finish.add_argument("--run-id", required=True)
    finish.add_argument("--claude-log", action="append")
    finish.add_argument("--claude-mode", default="json", choices=["json", "stream-json"])
    finish.add_argument("--codex-session-id")
    finish.add_argument("--rollout-file")
    finish.add_argument("--finished-at")
    finish.add_argument("--first-usable-at")
    finish.add_argument("--success-state", required=True, choices=["accepted", "repaired", "fallback_local", "stopped"])
    finish.add_argument("--validation-pass", required=True)
    finish.add_argument("--fallback-flag")
    finish.add_argument("--scope-respected")
    finish.add_argument("--repair-rounds", type=int)
    finish.add_argument("--outcome")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "start":
        return start_hook(args)
    return finish_hook(args)


if __name__ == "__main__":
    raise SystemExit(main())
