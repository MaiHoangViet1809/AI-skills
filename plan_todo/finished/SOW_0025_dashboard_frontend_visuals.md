# SOW: Dashboard Frontend Visuals

- **Task**: Xây activity chart, duration chart, runs table, và run detail panel cho telemetry dashboard dựa trên backend APIs đã ổn định.
- **Location**: `~/Projects/AISkills/plan_todo/SOW_0025_dashboard_frontend_visuals.md`, frontend directory dashboard mới, và assets/config liên quan nếu cần.
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
