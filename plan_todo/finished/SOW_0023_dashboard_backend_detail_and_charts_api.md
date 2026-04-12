# SOW: Dashboard Backend Detail And Charts API

- **Task**: Mở rộng backend dashboard với run detail API, activity chart API, và duration chart API dựa trên dataset telemetry hiện có.
- **Location**: `/Users/maihoangviet/Projects/AISkills/plan_todo/SOW_0023_dashboard_backend_detail_and_charts_api.md`, `/Users/maihoangviet/Projects/AISkills/scripts/dashboard/**`, và file cấu hình Python liên quan nếu cần.
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
