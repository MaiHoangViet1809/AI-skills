# SOW_20260412_WEE9FNN1 - Codex Rollout Metrics Refactor

- Status: UNKNOWN
- Approval: UNKNOWN
- create_dttm: 2026-04-12T18:51:54+07:00
- create_date: 2026-04-12
- create_dttm_source: filesystem_birthtime
- create_dttm_confidence: filesystem_proxy
- create_dttm_evidence: `plan_todo/finished/SOW_20261008_VO3LKN0L/creation-date-evidence.json` (record: SOW_20260412_WEE9FNN1)
- approve_dttm: unknown
- finish_dttm: unknown
- legacy_id: SOW_0016
- legacy_path: plan_todo/finished/SOW_0016_codex_rollout_metrics_refactor.md
- migrated_dttm: 2026-10-08T12:48:51+07:00
- legacy_title: SOW: Codex Rollout Metrics Refactor

## Preserved Contract And Historical Evidence

- **Task**: Gỡ flow đo Codex bằng OTel, bỏ local OTel config khỏi Codex, và chuyển sang flow đo session metrics bằng Python parser đọc rollout history trong `~/.codex/sessions/`.
- **Location**: `plan_todo/SOW_codex_rollout_metrics_refactor.md`, `~/.codex/config.toml`, `scripts/telemetry/README_codex_otel.md`, `scripts/telemetry/parse_codex_otel_log.py`, `scripts/telemetry/codex_otel_collector.yaml`, skill docs liên quan nếu cần
- **Why**: Với mục tiêu hiện tại, rollout history của Codex đã chứa message body, token counts, task completion, và session metadata. Nó phù hợp hơn OTel cho việc đo session/task/SOW efficiency và bắt marker text. Giữ OTel lúc này chỉ làm hệ thống phức tạp hơn mà không tăng giá trị tương xứng.
- **As-Is Diagram (ASCII)**:
```text
Codex session
   |
   v
OTel export -> local collector -> raw OTel file
   |
   v
Parser reads codex.sse_event for session metrics
   |
   +--> marker text still not reliable in OTel
```
- **To-Be Diagram (ASCII)**:
```text
Codex session
   |
   v
Native rollout log written under ~/.codex/sessions/YYYY/MM/DD/
   |
   v
Python parser reads rollout history by session/date/path
   |
   v
Extract session metrics + token_count + marker windows
   |
   v
Use rollout history as primary Codex measurement source
```
- **Deliverables**:
  - Remove Codex OTel config from `~/.codex/config.toml`
  - Update telemetry docs to make rollout history the primary source for Codex metrics
  - Replace or refactor Codex parser tooling to read `~/.codex/sessions/.../rollout-*.jsonl`
  - Define the minimum rollout-derived metrics to extract
  - Note clearly that OTel is no longer required for the current Codex measurement path
- **Done Criteria**:
  - `~/.codex/config.toml` no longer contains the temporary `[otel]` block added for this experiment
  - Repo telemetry docs reflect rollout-history-first measurement for Codex
  - A Python parser can read a rollout file and extract usable session metrics
  - The documented measurement path supports timestamps, session ids, token usage, and marker-grep windows
  - Residual OTel collector setup is clearly marked unnecessary for the normal path
- **Out-of-Scope**:
  - Removing or uninstalling the downloaded `otelcol-contrib` binary from the machine
  - Reworking Claude telemetry
  - Historical migration of all prior Codex telemetry artifacts
- **Proposed-By**: Codex GPT-5
- **plan**: `plan_todo/SOW_codex_rollout_metrics_refactor.md`
- **Cautions / Risks**:
  - Rollout file schemas may vary slightly across Codex versions, so parser logic should target stable event types.
  - Historical rollout logs may contain large instruction blocks, so parser should avoid loading or printing irrelevant fields.
  - Marker strategy must stay practical; if user-visible markers are too noisy, use the least intrusive approach that still keeps measurement workable.

## Minimum Rollout Fields To Extract

- `session_meta.payload.id`
- `session_meta.payload.timestamp`
- `session_meta.payload.cwd`
- `session_meta.payload.source`
- `session_meta.payload.model_provider`
- `event_msg.token_count.payload.info.total_token_usage`
- `event_msg.token_count.payload.info.last_token_usage`
- `event_msg.task_complete.payload.turn_id`
- `event_msg.agent_message.payload.message`
- `response_item` / `event_msg` records needed to locate start/finish marker text windows

## Marker Note

For Codex, marker-grep feasibility should be based on rollout history, not OTel.

Preferred workflow:
- keep marker detection in rollout logs if user-visible marker text is acceptable
- otherwise document the cleanest fallback that still supports measuring skill/SOW windows from historical logs
