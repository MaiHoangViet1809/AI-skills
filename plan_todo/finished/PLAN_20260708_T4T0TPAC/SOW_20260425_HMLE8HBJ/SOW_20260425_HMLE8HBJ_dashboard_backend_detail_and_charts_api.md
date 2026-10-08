# SOW_20260425_HMLE8HBJ - Dashboard Backend Detail And Charts API

- Status: UNKNOWN
- Approval: UNKNOWN
- create_dttm: 2026-04-25T00:36:55+07:00
- create_date: 2026-04-25
- create_dttm_source: filesystem_birthtime
- create_dttm_confidence: filesystem_proxy
- create_dttm_evidence: `plan_todo/finished/SOW_20261008_VO3LKN0L/creation-date-evidence.json` (record: SOW_20260425_HMLE8HBJ)
- approve_dttm: unknown
- finish_dttm: unknown
- legacy_id: SOW_0023
- legacy_path: plan_todo/finished/SOW_0023_dashboard_backend_detail_and_charts_api.md
- migrated_dttm: 2026-10-08T12:48:51+07:00
- legacy_title: SOW: Dashboard Backend Detail And Charts API

## Preserved Contract And Historical Evidence

- **Task**: Mở rộng backend dashboard với run detail API, activity chart API, và duration chart API dựa trên dataset telemetry hiện có.
- **Location**: `plan_todo/SOW_0023_dashboard_backend_detail_and_charts_api.md`, `~/Projects/AISkills/scripts/dashboard/**`, và file cấu hình Python liên quan nếu cần.
- **Why**: Frontend charts và detail views cần contract dữ liệu riêng, nên tách khỏi summary API để delegate dễ hơn.
- **As-Is Diagram (ASCII)**:
```text
dashboard backend
   |
   +--> summary
   +--> runs list
```
- **To-Be Diagram (ASCII)**:
```text
dashboard backend
   |
   +--> summary
   +--> runs list
   +--> run detail
   +--> activity chart
   +--> duration chart
```
- **Deliverables**:
  - run detail endpoint
  - activity chart endpoint
  - duration chart endpoint
  - lightweight derived fields needed by those endpoints
- **Done Criteria**:
  - chart/detail responses are stable and frontend-ready
  - no duplicate loader logic
  - derived metrics remain calculable from existing telemetry fields
- **Out-of-Scope**:
  - frontend shell
  - frontend charts
  - final boot integration
- **Proposed-By**: Codex GPT-5
- **plan**: `plan_todo/telemetry_dashboard_master_plan.md`
- **Cautions / Risks**:
  - avoid over-enriching with expensive raw-log rescans on every request
