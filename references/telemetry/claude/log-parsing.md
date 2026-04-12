# Log Parsing

Use raw-log-first capture by default.

The coordinator should not read full Claude CLI output directly unless the parsed summary reports an anomaly or the current flow explicitly needs deep debugging.

## Canonical Paths

- Raw logs: `<repo>/logs_session_ai_agent/claude-<session-id>.log`
- No parsed artifact is persisted by default.
- No Claude usage ledger is persisted by default.

If `session_id` is unknown when the call starts, write to a temporary file first, then rename it after parsing the first stable `session_id`.

## Default Flow

```text
Claude CLI call
   |
   v
Write raw output to logs_session_ai_agent/<temp-or-session>.log
   |
   v
Run parser script on demand
   |
   v
Print compact summary to stdout
   |
   v
Coordinator reads parser output by default
   |
   +--> open raw log only on anomaly or deep delegate debugging
```

## Minimum Extracted Fields

The parser should extract only the smallest useful set:

- `session_id`
- `mode`
- `status`
- `error`
- `is_error`
- `result_text`
- `structured_output`
- `rate_limit_info`
- `usage`
- `duration_ms`
- `stop_reason`

## Normalized Parser Output

```json
{
  "session_id": "uuid",
  "mode": "json",
  "is_error": false,
  "error": null,
  "status": "success",
  "result_text": "OK",
  "structured_output": null,
  "rate_limit_info": {
    "status": "allowed_warning",
    "rateLimitType": "five_hour",
    "resetsAt": 1775995200,
    "utilization": 0.91,
    "overageStatus": null,
    "isUsingOverage": false
  },
  "usage": {
    "input_tokens": 2,
    "output_tokens": 4,
    "cache_creation_input_tokens": 22504,
    "cache_read_input_tokens": 0,
    "total_cost_usd": 0.08445599999999999
  },
  "duration_ms": 13771,
  "stop_reason": "end_turn",
  "raw_log_path": "/abs/repo/logs_session_ai_agent/claude-uuid.log",
  "anomaly_flags": []
}
```

## Stable Keys Seen In Practice

The parser should tolerate version drift, but the following keys were confirmed in a local probe:

- `assistant.message.usage.input_tokens`
- `assistant.message.usage.output_tokens`
- `assistant.message.usage.cache_creation_input_tokens`
- `assistant.message.usage.cache_read_input_tokens`
- `result.session_id`
- `result.is_error`
- `result.result`
- `result.stop_reason`
- `result.duration_ms`
- `result.total_cost_usd`
- `result.usage.input_tokens`
- `result.usage.output_tokens`
- `result.usage.cache_creation_input_tokens`
- `result.usage.cache_read_input_tokens`
- `rate_limit_event.rate_limit_info.status`
- `rate_limit_event.rate_limit_info.rateLimitType`
- `rate_limit_event.rate_limit_info.resetsAt`
- `rate_limit_event.rate_limit_info.utilization`
- `rate_limit_event.rate_limit_info.isUsingOverage`

Treat all other keys as optional.

## Anomaly Rule

Open the raw log only when one of these is true:

- the parser cannot decode the payload
- `session_id` is missing
- `structured_output` is required but missing
- `is_error` is true and `error` cannot be normalized
- the current flow explicitly requests deep delegate debugging

## Capture Examples

Write raw JSON output to a temp log, then parse it on demand:

```bash
tmp_log="$REPO/logs_session_ai_agent/claude-$(date +%s)-tmp.log"
claude -p --output-format json --json-schema "$SCHEMA" "$PROMPT" > "$tmp_log"
python /Users/maihoangviet/.codex/skills/sow-delegate-flow/scripts/parse_delegate_log.py \
  --raw-log "$tmp_log" \
  --mode json \
  --repo-root "$REPO"
```

Use `stream-json` only for deep delegate debugging, then parse the raw JSONL file the same way:

```bash
tmp_log="$REPO/logs_session_ai_agent/claude-$(date +%s)-tmp.log"
claude -p --output-format stream-json --json-schema "$SCHEMA" "$PROMPT" > "$tmp_log"
python /Users/maihoangviet/.codex/skills/sow-delegate-flow/scripts/parse_delegate_log.py \
  --raw-log "$tmp_log" \
  --mode stream-json \
  --repo-root "$REPO"
```
