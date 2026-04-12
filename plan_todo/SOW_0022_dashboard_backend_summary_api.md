# SOW: Dashboard Backend Summary API

- **Task**: Xây backend app mỏng cho dashboard và expose summary API cùng runs list API dựa trên dataset Polars đã chuẩn hóa.
- **Location**: `/Users/maihoangviet/Projects/AISkills/plan_todo/SOW_0022_dashboard_backend_summary_api.md`, `/Users/maihoangviet/Projects/AISkills/scripts/dashboard/**`, và file cấu hình Python liên quan nếu cần.
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
