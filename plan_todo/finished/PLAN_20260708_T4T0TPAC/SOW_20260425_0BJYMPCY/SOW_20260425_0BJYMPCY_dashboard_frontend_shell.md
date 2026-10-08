# SOW_20260425_0BJYMPCY - Dashboard Frontend Shell

- Status: UNKNOWN
- Approval: UNKNOWN
- create_dttm: 2026-04-25T00:36:55+07:00
- create_date: 2026-04-25
- create_dttm_source: filesystem_birthtime
- create_dttm_confidence: filesystem_proxy
- create_dttm_evidence: `plan_todo/finished/SOW_20261008_VO3LKN0L/creation-date-evidence.json` (record: SOW_20260425_0BJYMPCY)
- approve_dttm: unknown
- finish_dttm: unknown
- legacy_id: SOW_0024
- legacy_path: plan_todo/finished/SOW_0024_dashboard_frontend_shell.md
- migrated_dttm: 2026-10-08T12:48:51+07:00
- legacy_title: SOW: Dashboard Frontend Shell

## Preserved Contract And Historical Evidence

- **Task**: Scaffold frontend Vue 3 + Vite cho telemetry dashboard và dựng shell layout với summary cards cùng filter state cơ bản.
- **Location**: `plan_todo/SOW_0024_dashboard_frontend_shell.md`, frontend directory dashboard mới, và file build config liên quan nếu cần.
- **Why**: Cần một shell UI ổn định để cắm summary/runs data trước khi làm charts và detail interactions.
- **As-Is Diagram (ASCII)**:
```text
backend APIs only
      |
      v
no dashboard UI
```
- **To-Be Diagram (ASCII)**:
```text
backend APIs
    |
    v
Vue dashboard shell
    |
    +--> summary cards
    +--> filter/time window state
```
- **Deliverables**:
  - Vue 3 + Vite frontend scaffold
  - dashboard shell layout
  - summary cards row
  - shared filter/time-window state
- **Done Criteria**:
  - frontend runs locally against backend APIs
  - shell layout is responsive enough for desktop and laptop
  - no chart/detail implementation yet
- **Out-of-Scope**:
  - charts
  - run detail drawer
  - boot integration
- **Proposed-By**: Codex GPT-5
- **plan**: `plan_todo/telemetry_dashboard_master_plan.md`
- **Cautions / Risks**:
  - keep UI shell lean so API contract changes stay small
