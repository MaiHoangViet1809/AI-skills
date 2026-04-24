# SOW: Dashboard Boot And Smoke

- **Task**: Hoàn thiện one-command boot flow cho telemetry dashboard trên port `9999`, serve frontend + API cùng một port, thêm docs chạy local, và smoke test end-to-end.
- **Location**: `~/Projects/AISkills/plan_todo/SOW_0026_dashboard_boot_and_smoke.md`, `~/Projects/AISkills/scripts/dashboard/**`, frontend dashboard directory, và docs liên quan nếu cần.
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
