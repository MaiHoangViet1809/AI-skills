# SOW_20260425_U27MN5Y0 - Dashboard Boot And Smoke

- Status: UNKNOWN
- Approval: UNKNOWN
- create_dttm: 2026-04-25T00:36:55+07:00
- create_date: 2026-04-25
- create_dttm_source: filesystem_birthtime
- create_dttm_confidence: filesystem_proxy
- create_dttm_evidence: `plan_todo/finished/SOW_20261008_VO3LKN0L/creation-date-evidence.json` (record: SOW_20260425_U27MN5Y0)
- approve_dttm: unknown
- finish_dttm: unknown
- legacy_id: SOW_0026
- legacy_path: plan_todo/finished/SOW_0026_dashboard_boot_and_smoke.md
- migrated_dttm: 2026-10-08T12:48:51+07:00
- legacy_title: SOW: Dashboard Boot And Smoke

## Preserved Contract And Historical Evidence

- **Task**: Hoàn thiện one-command boot flow cho telemetry dashboard trên port `9999`, serve frontend + API cùng một port, thêm docs chạy local, và smoke test end-to-end.
- **Location**: `plan_todo/SOW_0026_dashboard_boot_and_smoke.md`, `~/Projects/AISkills/scripts/dashboard/**`, frontend dashboard directory, và docs liên quan nếu cần.
- **Why**: Cần một entrypoint rõ ràng để dùng dashboard thật sự thay vì ghép tay backend/frontend.
- **As-Is Diagram (ASCII)**:
```text
backend slice + frontend slice
         |
         v
no final single-command dashboard boot
```
- **To-Be Diagram (ASCII)**:
```text
uv run python scripts/dashboard/run_dashboard.py
         |
         v
dashboard on :9999
```
- **Deliverables**:
  - one-command boot script
  - same-port frontend/API serving
  - local run docs
  - smoke test notes
- **Done Criteria**:
  - dashboard boots on `http://localhost:9999`
  - one command starts the usable local app
  - end-to-end smoke test passes on current repo telemetry data
- **Out-of-Scope**:
  - report pipeline
  - remote deployment
  - authentication
- **Proposed-By**: Codex GPT-5
- **plan**: `plan_todo/telemetry_dashboard_master_plan.md`
- **Cautions / Risks**:
  - frontend build/serve coupling should stay simple
