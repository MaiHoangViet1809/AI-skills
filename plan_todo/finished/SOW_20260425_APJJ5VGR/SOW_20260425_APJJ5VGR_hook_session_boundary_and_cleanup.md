# SOW_20260425_APJJ5VGR - hook session boundary and cleanup

- Status: UNKNOWN
- Approval: UNKNOWN
- create_dttm: 2026-04-25T00:36:55+07:00
- create_date: 2026-04-25
- create_dttm_source: filesystem_birthtime
- create_dttm_confidence: filesystem_proxy
- create_dttm_evidence: `plan_todo/finished/SOW_20261008_VO3LKN0L/creation-date-evidence.json` (record: SOW_20260425_APJJ5VGR)
- approve_dttm: unknown
- finish_dttm: unknown
- legacy_id: SOW_0036
- legacy_path: plan_todo/finished/SOW_0036_hook_session_boundary_and_cleanup.md
- migrated_dttm: 2026-10-08T12:48:51+07:00

## Preserved Contract And Historical Evidence

- **Task**: Sửa global hook telemetry để chỉ ghi run cho isolated skill session thật, đồng thời dọn các run sai đã ghi vào global ledger.
- **Location**: `~/Projects/AISkills/scripts/telemetry/codex_hook_bridge.py`, `skills/telemetry-flow/references/hook-contract.md`, `skills/task-router-flow/SKILL.md`, `~/Projects/AISkills/scripts/telemetry/**`, và `~/.logs/codex/telemetry/runs/`
- **Why**: Dashboard đang có false-positive run do hook quét marker từ toàn transcript và nuốt luôn placeholder metadata từ probe/prompt không hợp lệ.
- **As-Is Diagram (ASCII)**:
```text
Stop hook
  |
  v
scan whole transcript
  |
  +--> any old marker can match
  +--> placeholder values still accepted
```
- **To-Be Diagram (ASCII)**:
```text
Stop hook
  |
  v
read first user prompt only
  |
  +--> must start with CODEX_SKILL_RUN
  +--> reject placeholder values
  +--> otherwise no-op
```
- **Deliverables**:
  - tighten marker/session boundary in `codex_hook_bridge.py`
  - reject placeholder marker values such as `<sow>` and `<task_type>`
  - cleanup script or targeted cleanup for bad global runs
  - verify dashboard no longer shows false-positive rows
- **Done Criteria**:
  - main session without first-line marker no longer emits skill telemetry
  - new isolated skill session with valid marker still emits telemetry
  - placeholder rows are removed from global ledger
  - dashboard shows only valid rows after refresh
- **Out-of-Scope**:
  - dashboard redesign
  - schema changes to run metrics
- **Proposed-By**: Codex GPT-5
- **plan**: `global cross-project skill telemetry`
- **Cautions / Risks**:
  - transcript formats may vary, so first-user-message extraction must degrade safely
  - cleanup must avoid deleting valid historical runs
