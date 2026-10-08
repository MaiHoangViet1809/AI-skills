# SOW_20260425_1L07OWX9 - Dashboard Structure Refactor

- Status: UNKNOWN
- Approval: UNKNOWN
- create_dttm: 2026-04-25T00:36:55+07:00
- create_date: 2026-04-25
- create_dttm_source: filesystem_birthtime
- create_dttm_confidence: filesystem_proxy
- create_dttm_evidence: `plan_todo/finished/SOW_20261008_VO3LKN0L/creation-date-evidence.json` (record: SOW_20260425_1L07OWX9)
- approve_dttm: unknown
- finish_dttm: unknown
- legacy_id: SOW_0032
- legacy_path: plan_todo/finished/SOW_0032_dashboard_structure_refactor.md
- migrated_dttm: 2026-10-08T12:48:51+07:00
- legacy_title: SOW: Dashboard Structure Refactor

## Preserved Contract And Historical Evidence

- **Task**: Refactor the telemetry dashboard from the current prototype layout into a top-level `dashboard/` structure with separate frontend, backend, and static areas.
- **Location**: `plan_todo/SOW_0032_dashboard_structure_refactor.md`, `~/Projects/AISkills/dashboard/**`, `~/Projects/AISkills/scripts/run_dashboard.py`, and related docs.
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
