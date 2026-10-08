# SOW_20260425_HX17BNV6 - move all telemetry logs global

- Status: UNKNOWN
- Approval: UNKNOWN
- create_dttm: 2026-04-25T00:36:55+07:00
- create_date: 2026-04-25
- create_dttm_source: filesystem_birthtime
- create_dttm_confidence: filesystem_proxy
- create_dttm_evidence: `plan_todo/finished/SOW_20261008_VO3LKN0L/creation-date-evidence.json` (record: SOW_20260425_HX17BNV6)
- approve_dttm: unknown
- finish_dttm: unknown
- legacy_id: SOW_0038
- legacy_path: plan_todo/finished/SOW_0038_move_all_telemetry_logs_global.md
- migrated_dttm: 2026-10-08T12:48:51+07:00

## Preserved Contract And Historical Evidence

- **Task**: Chuyển toàn bộ telemetry writes từ `logs_session_ai_agent` trong từng project sang global telemetry paths dưới `~/.logs/codex/telemetry/`.
- **Location**: `plan_todo/SOW_0038_move_all_telemetry_logs_global.md`, `~/Projects/AISkills/aiskills_common/telemetry/**`, `~/Projects/AISkills/skills/telemetry-flow/scripts/**`, `~/Projects/AISkills/skills/sow-delegate-flow/scripts/**`, `~/Projects/AISkills/scripts/telemetry/**`, và docs/reference telemetry liên quan
- **Why**: Dashboard đã đọc global ledger, nhưng raw/staging telemetry vẫn còn write local theo từng repo; điều này đi ngược mục tiêu centralized telemetry.
- **As-Is Diagram (ASCII)**:
```text
repo/logs_session_ai_agent/
  -> telemetry-run-*.json
  -> claude-*.log

~/.logs/codex/telemetry/runs/
  -> normalized run summaries
```
- **To-Be Diagram (ASCII)**:
```text
~/.logs/codex/telemetry/
  -> runs/
  -> staging/
  -> claude/
  -> hook-debug/
  -> hook-state/

no telemetry writes into repo-local logs_session_ai_agent/
```
- **Deliverables**:
  - shared global path helpers cho `runs`, `staging`, `claude`
  - update telemetry hook / delegate parser / related scripts sang global paths
  - update docs/contracts đang còn nói `logs_session_ai_agent`
  - verify dashboard + telemetry flow vẫn hoạt động
- **Done Criteria**:
  - run staging không còn write vào project-local `logs_session_ai_agent`
  - Claude raw logs không còn write vào project-local `logs_session_ai_agent`
  - global ledger và parser paths vẫn chạy đúng
  - docs khớp với global-only telemetry storage
- **Out-of-Scope**:
  - dashboard redesign
  - thay đổi metric schema
- **Proposed-By**: Codex GPT-5
- **plan**: `global telemetry storage`
- **Cautions / Risks**:
  - cần naming/path đủ ổn để tránh collision cross-project
  - parser và backfill cũ phải chịu được dữ liệu lịch sử
  - không được làm vỡ hook/runtime sync sang `~/.codex`
