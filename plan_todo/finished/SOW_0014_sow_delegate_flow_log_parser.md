# SOW: Sow Delegate Flow Log Parser

- **Task**: Cập nhật `sow-delegate-flow` để không đọc trực tiếp full Claude CLI output vào context, mà chuyển sang cơ chế `raw log file -> Python parser -> compact parsed summary`, đồng thời ghi usage/cost của Claude vào artifact có thể tổng hợp sau này.
- **Location**: `plan_todo/SOW_sow_delegate_flow_log_parser.md`, `~/.codex/skills/sow-delegate-flow/SKILL.md`, `~/.codex/skills/sow-delegate-flow/references/claude-delegate-contract.md`, reference mới cho output parsing, script Python mới nếu cần, `.gitignore`
- **Why**: Cả `json` và `stream-json` của Claude CLI đều có thể trả quá nhiều output vào context. Đọc trực tiếp output đó làm tăng token cost của coordinator. Cần giảm chi phí bằng cách chỉ đọc summary đã parse, và chỉ mở raw log khi có bất thường hoặc debug sâu.
- **As-Is Diagram (ASCII)**:
```text
Claude CLI call
   |
   v
CLI output returns directly to coordinator
   |
   v
Coordinator reads too much envelope/transcript noise
```
- **To-Be Diagram (ASCII)**:
```text
Claude CLI call
   |
   v
Write raw output to logs_session_ai_agent/claude-<session-id>.log
   |
   v
Python parser reads raw log
   |
   v
Write compact parsed artifact
   |
   v
Coordinator reads parsed artifact by default
   |
   +--> raw log only if anomaly or deep debug
```
- **Deliverables**:
  - Updated `sow-delegate-flow` contract describing file-based capture and parse flow
  - A Python parser specification or implementation for Claude output logs
  - A documented output artifact shape for the parsed summary
  - A documented usage/cost ledger shape for Claude calls
  - `.gitignore` updated so `logs_session_ai_agent/` is ignored
- **Done Criteria**:
  - Skill docs describe raw-log-first capture instead of direct context ingestion
  - `logs_session_ai_agent/` is the canonical log directory and is gitignored
  - Parser output shape is documented clearly enough that operator does not need to inspect raw output in the normal path
  - The spec lists the minimum fields to extract from Claude logs
  - The flow explicitly says raw logs are read only on anomaly/debug
- **Out-of-Scope**:
  - Full Codex token accounting
  - Productionizing a general-purpose observability system
  - Migrating all old logs or backfilling historical Claude sessions
- **Proposed-By**: Codex GPT-5
- **plan**: `plan_todo/SOW_sow_delegate_flow_log_parser.md`
- **Cautions / Risks**:
  - Claude JSON and stream output shapes may vary slightly by mode/version, so parser rules should target stable fields.
  - If the parser extracts too much, it defeats the token-saving goal.
  - If the parser extracts too little, raw-log fallback will be used too often.

## Parser Extraction Scope

The parser should aim to extract only the minimum useful fields from each Claude call:

- `session_id`
- `mode`: `json` or `stream-json`
- `status`: success / failed / needs_advice when available from parsed structured output
- `error`: normalized error type if present, especially `rate_limit`
- `result_text`: compact final result text when needed
- `structured_output`: parsed JSON-schema payload when present
- `rate_limit_info` when present:
  - `status`
  - `rateLimitType`
  - `resetsAt`
  - `overageStatus`
  - `isUsingOverage`
- usage/cost fields when present:
  - `input_tokens`
  - `output_tokens`
  - `cache_creation_input_tokens`
  - `cache_read_input_tokens`
  - `total_cost_usd`
- minimal execution metadata:
  - `duration_ms`
  - `is_error`
  - `stop_reason`

## Parsed Summary Artifact

The normal-path artifact should be compact and machine-friendly. Example target shape:

```json
{
  "session_id": "uuid",
  "mode": "json",
  "is_error": false,
  "error": null,
  "status": "success",
  "structured_output": {},
  "rate_limit_info": null,
  "usage": {
    "input_tokens": 0,
    "output_tokens": 0,
    "cache_creation_input_tokens": 0,
    "cache_read_input_tokens": 0,
    "total_cost_usd": 0.0
  },
  "duration_ms": 0,
  "stop_reason": "end_turn"
}
```

## Ledger Artifact

Each Claude call should also be able to append one compact usage row to a ledger. Example:

```json
{
  "ts": "2026-04-12T03:30:00+07:00",
  "agent": "claude",
  "skill": "sow-delegate-flow",
  "session_id": "uuid",
  "mode": "json",
  "input_tokens": 123,
  "output_tokens": 45,
  "cache_creation_input_tokens": 0,
  "cache_read_input_tokens": 2000,
  "cost_usd": 0.0123,
  "error": null
}
```

## Discovery Note

If needed before implementation, run one minimal `claude -p` probe and inspect the raw output shape to confirm the stable keys used by the parser.
