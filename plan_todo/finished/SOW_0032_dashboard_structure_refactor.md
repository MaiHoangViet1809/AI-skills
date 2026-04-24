# SOW: Dashboard Structure Refactor

- **Task**: Refactor the telemetry dashboard from the current prototype layout into a top-level `dashboard/` structure with separate frontend, backend, and static areas.
- **Location**: `~/Projects/AISkills/plan_todo/SOW_0032_dashboard_structure_refactor.md`, `~/Projects/AISkills/dashboard/**`, `~/Projects/AISkills/scripts/run_dashboard.py`, and related docs.
- **Why**: The current split between `dashboard_ui/` and `scripts/dashboard/` is hard to read and awkward to extend.
- **As-Is Diagram (ASCII)**:
```text
dashboard_ui/      -> frontend source
scripts/dashboard/ -> backend + static + boot
```
- **To-Be Diagram (ASCII)**:
```text
dashboard/
  frontend/
  backend/
  static/
scripts/
  run_dashboard.py
```
- **Deliverables**:
  - move frontend source to `dashboard/frontend/`
  - move backend source to `dashboard/backend/`
  - move static build output to `dashboard/static/`
  - update boot/build/import/docs paths
- **Done Criteria**:
  - dashboard still boots on port `9999`
  - frontend/backend layout is clear
  - no active runtime path still depends on `dashboard_ui/` or `scripts/dashboard/`
- **Out-of-Scope**:
  - UI redesign
  - telemetry schema changes
- **Proposed-By**: Codex GPT-5
- **plan**: `dashboard structure refactor`
- **Cautions / Risks**:
  - path rewiring must not break same-port serving
