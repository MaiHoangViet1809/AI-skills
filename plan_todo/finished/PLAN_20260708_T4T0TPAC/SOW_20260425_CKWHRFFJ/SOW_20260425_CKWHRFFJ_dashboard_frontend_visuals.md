# SOW_20260425_CKWHRFFJ - Dashboard Frontend Visuals

- Status: UNKNOWN
- Approval: UNKNOWN
- create_dttm: 2026-04-25T00:36:55+07:00
- create_date: 2026-04-25
- create_dttm_source: filesystem_birthtime
- create_dttm_confidence: filesystem_proxy
- create_dttm_evidence: `plan_todo/finished/SOW_20261008_VO3LKN0L/creation-date-evidence.json` (record: SOW_20260425_CKWHRFFJ)
- approve_dttm: unknown
- finish_dttm: unknown
- legacy_id: SOW_0025
- legacy_path: plan_todo/finished/SOW_0025_dashboard_frontend_visuals.md
- migrated_dttm: 2026-10-08T12:48:51+07:00
- legacy_title: SOW: Dashboard Frontend Visuals

## Preserved Contract And Historical Evidence

- **Task**: Xây activity chart, duration chart, runs table, và run detail panel cho telemetry dashboard dựa trên backend APIs đã ổn định.
- **Location**: `plan_todo/SOW_0025_dashboard_frontend_visuals.md`, frontend directory dashboard mới, và assets/config liên quan nếu cần.
- **Why**: Đây là phần giá trị trực quan chính của dashboard, nhưng nên tách khỏi shell để giảm rủi ro delegate.
- **As-Is Diagram (ASCII)**:
```text
frontend shell
   |
   +--> summary cards
   +--> filters
```
- **To-Be Diagram (ASCII)**:
```text
frontend shell
   |
   +--> activity chart
   +--> duration chart
   +--> runs table
   +--> run detail drawer
```
- **Deliverables**:
  - activity chart
  - duration chart
  - runs table
  - run detail panel or drawer
- **Done Criteria**:
  - charts render real telemetry data
  - table and detail panel work with selection/filter state
  - UI uses task-local metrics only
- **Out-of-Scope**:
  - backend API redesign
  - one-port production boot flow
- **Proposed-By**: Codex GPT-5
- **plan**: `plan_todo/telemetry_dashboard_master_plan.md`
- **Cautions / Risks**:
  - keep chart library choice pragmatic and low-overhead
