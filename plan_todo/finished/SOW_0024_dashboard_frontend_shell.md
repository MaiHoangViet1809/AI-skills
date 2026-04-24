# SOW: Dashboard Frontend Shell

- **Task**: Scaffold frontend Vue 3 + Vite cho telemetry dashboard và dựng shell layout với summary cards cùng filter state cơ bản.
- **Location**: `~/Projects/AISkills/plan_todo/SOW_0024_dashboard_frontend_shell.md`, frontend directory dashboard mới, và file build config liên quan nếu cần.
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
