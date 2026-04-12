# Codex Rollout Metrics

Codex session metrics should be read from native rollout history under `~/.codex/sessions/`, not from OpenTelemetry.

## Why

- Rollout logs already contain session metadata, token counts, task completion, and assistant message bodies.
- Marker text can be located in rollout history if needed.
- This path avoids running a local collector and avoids noisy OTel export errors.

## Source Files

- Historical rollout logs: `~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl`
- Parser: `scripts/telemetry/parse_codex_rollout.py`

## What The Parser Extracts

- `session_meta.payload.id`
- `session_meta.payload.timestamp`
- `session_meta.payload.cwd`
- `session_meta.payload.originator`
- `session_meta.payload.source`
- `session_meta.payload.model_provider`
- `event_msg.token_count.payload.info.total_token_usage`
- `event_msg.token_count.payload.info.last_token_usage`
- `event_msg.task_complete.payload.turn_id`
- `event_msg.agent_message.payload.message`
- marker windows based on assistant/user message text

## Example

Parse a specific rollout file:

```bash
python3 "$REPO/scripts/telemetry/parse_codex_rollout.py" \
  --rollout-file "$HOME/.codex/sessions/2026/04/12/rollout-2026-04-12T18-28-18-019d8173-1d19-7083-bc92-662961020ab4.jsonl"
```

Parse the latest rollout from a day:

```bash
python3 "$REPO/scripts/telemetry/parse_codex_rollout.py" \
  --day 2026-04-12
```

Find a session by session id:

```bash
python3 "$REPO/scripts/telemetry/parse_codex_rollout.py" \
  --session-id 019d8173-1d19-7083-bc92-662961020ab4
```

Search for marker windows in the parsed stream:

```bash
python3 "$REPO/scripts/telemetry/parse_codex_rollout.py" \
  --session-id 019d8173-1d19-7083-bc92-662961020ab4 \
  --marker-skill sow-delegate-flow \
  --marker-sow SOW_0001
```

Parse a run window by repo, time range, and exact markers:

```bash
uv run python scripts/telemetry/parse_codex_rollout.py \
  --cwd "$REPO" \
  --started-at 2026-04-12T12:20:13Z \
  --finished-at 2026-04-12T12:20:20Z \
  --start-marker "TELEMETRY_START run_id=<run_id> skill=sow-delegate-flow plan=<plan> sow=<sow>" \
  --finish-marker "TELEMETRY_FINISH run_id=<run_id> skill=sow-delegate-flow plan=<plan> sow=<sow>"
```

## Notes

- OTel is not required for the current Codex measurement path.
- Token/cost measurement for Codex should be session-first, then mapped to task/SOW analytically later.
- If marker text is too noisy for user-facing runs, keep rollout parsing focused on token and completion data and use a cleaner marker strategy later.
- For run-level telemetry, use a staging record as the primary match source and marker text only as a cross-check or debug aid.
