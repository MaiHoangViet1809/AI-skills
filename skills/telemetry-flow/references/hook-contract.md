# Telemetry Hook Contract

## Purpose

`telemetry-flow` wraps an execution run with two commands only:

- `start`: create a stable `run_id`, write a staging record, and return marker strings
- `finish`: read the staging record, parse Codex rollout and Claude raw logs, then return normalized run metrics

This v1 does not create reports or dashboards. It only captures a single run summary that later tooling can aggregate.

## Canonical Files

- Staging record: `<repo>/logs_session_ai_agent/telemetry-run-<run_id>.json`
- Claude raw logs: `<repo>/logs_session_ai_agent/claude-<session-id>.log`
- Codex rollout logs: `~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl`

## Start Hook

Run before execution begins:

```bash
uv run python skills/telemetry-flow/scripts/telemetry_hook.py start \
  --repo-root "$REPO" \
  --skill sow-delegate-flow \
  --plan "telemetry hook skill v1" \
  --sow SOW_0019 \
  --task-type backend \
  --intent "delegate telemetry-aware execution"
```

Start output includes:

- `run_id`
- `staging_file`
- `started_at`
- `start_marker`
- `finish_marker`

## Marker Format

Markers are exact strings so rollout parsing can cross-check the time window:

```text
TELEMETRY_START run_id=<run_id> skill=<skill> plan=<plan> sow=<sow>
TELEMETRY_FINISH run_id=<run_id> skill=<skill> plan=<plan> sow=<sow>
```

Emit them only when stronger Codex-side matching or human-debug traceability is useful.

## Finish Hook

Run after execution, review, and validation, but before commit:

```bash
uv run python skills/telemetry-flow/scripts/telemetry_hook.py finish \
  --repo-root "$REPO" \
  --run-id "$RUN_ID" \
  --claude-log "$REPO/logs_session_ai_agent/claude-abc.log" \
  --success-state accepted \
  --validation-pass true
```

Useful optional inputs:

- `--codex-session-id`
- `--rollout-file`
- `--claude-mode json|stream-json`
- `--first-usable-at <iso>`
- `--repair-rounds <int>`
- `--scope-respected true|false`
- `--outcome <text>`

## Normalized Output

The finish hook should return one JSON object with at least these fields:

- `run_id`
- `skill`
- `plan`
- `sow`
- `task_type`
- `started_at`
- `finished_at`
- `run_duration_ms`
- `time_to_first_usable_result_ms`
- `codex_session_id`
- `codex_task_tokens`
- `codex_cached_input_tokens`
- `codex_fresh_input_tokens`
- `codex_output_tokens`
- `codex_reasoning_output_tokens`
- `codex_turn_count`
- `codex_avg_tokens_per_turn`
- `codex_last_turn_tokens`
- `claude_session_id`
- `claude_total_tokens`
- `claude_input_tokens`
- `claude_output_tokens`
- `claude_cache_creation_tokens`
- `claude_cache_read_tokens`
- `claude_duration_ms`
- `files_changed_count`
- `repair_rounds`
- `fallback_flag`
- `validation_pass`
- `success_state`
- `scope_respected`
- `outcome`
- `delegate_ratio`
- `codex_to_claude_ratio`
- `anomaly_flags`

## Metric Rules

- Metrics must be parsed or calculated directly from logs, timestamps, git state, or workflow metadata.
- No LLM-generated score or quality estimate is allowed.
- `codex_task_tokens` is the sum of task-local Codex turn usage inside the run window, excluding cached input tokens.
- Do not use cumulative session-token deltas as the main Codex task metric.
- `delegate_ratio` is `claude_total_tokens / (claude_total_tokens + codex_task_tokens)` when both sides exist.
- `codex_to_claude_ratio` is `codex_task_tokens / claude_total_tokens` when Claude tokens are non-zero.
- `time_to_first_usable_result_ms` is either explicitly passed in or derived from the earliest parsed Claude result timestamp.

## Integration With `sow-delegate-flow`

- Run `start` before the first Claude delegate call in a run.
- Keep the returned `run_id` active across repair or advice loops.
- Run `finish` once the run reaches a terminal workflow outcome.
