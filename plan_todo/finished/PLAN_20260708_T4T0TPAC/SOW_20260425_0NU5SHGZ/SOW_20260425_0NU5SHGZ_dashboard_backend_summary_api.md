# SOW_20260425_0NU5SHGZ - Dashboard Backend Summary API

- Status: UNKNOWN
- Approval: UNKNOWN
- create_dttm: 2026-04-25T00:36:55+07:00
- create_date: 2026-04-25
- create_dttm_source: filesystem_birthtime
- create_dttm_confidence: filesystem_proxy
- create_dttm_evidence: `plan_todo/finished/SOW_20261008_VO3LKN0L/creation-date-evidence.json` (record: SOW_20260425_0NU5SHGZ)
- approve_dttm: unknown
- finish_dttm: unknown
- legacy_id: SOW_0022
- legacy_path: plan_todo/finished/SOW_0022_dashboard_backend_summary_api.md
- migrated_dttm: 2026-10-08T12:48:51+07:00
- legacy_title: SOW: Dashboard Backend Summary API

## Preserved Contract And Historical Evidence

- **Task**: Xây backend app mỏng cho dashboard và expose summary API cùng runs list API dựa trên dataset Polars đã chuẩn hóa.
- **Location**: `plan_todo/SOW_0022_dashboard_backend_summary_api.md`, `~/Projects/AISkills/scripts/dashboard/**`, và file cấu hình Python liên quan nếu cần.
- **Why**: Frontend shell cần endpoint ổn định sớm để nối dữ liệu và state filters.
- **As-Is Diagram (ASCII)**:
```text
normalized run dataset
        |
        v
no HTTP API for dashboard
```
- **To-Be Diagram (ASCII)**:
```text
normalized run dataset
        |
        v
dashboard backend app
        |
        +--> summary API
        +--> runs list API
```
- **Deliverables**:
  - backend app entry under `scripts/dashboard/`
  - summary endpoint
  - runs list endpoint
  - basic window/filter parsing
- **Done Criteria**:
  - API returns JSON usable by frontend shell
  - endpoints read from shared data layer instead of duplicating file logic
  - scope stays API-only
- **Out-of-Scope**:
  - detail endpoint
  - chart endpoints
  - frontend code
  - boot flow
- **Proposed-By**: Codex GPT-5
- **plan**: `plan_todo/telemetry_dashboard_master_plan.md`
- **Cautions / Risks**:
  - filter contract should stay simple and stable
