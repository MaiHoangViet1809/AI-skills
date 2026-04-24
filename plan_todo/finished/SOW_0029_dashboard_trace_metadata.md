# SOW: Dashboard Trace Metadata

- **Task**: Add Codex-side telemetry metadata for `project_name`, `project_path`, and `sow_file`, then show them on the dashboard with hoverable full paths.
- **Location**: `~/Projects/AISkills/plan_todo/SOW_0029_dashboard_trace_metadata.md`, `~/Projects/AISkills/skills/telemetry-flow/scripts/telemetry_hook.py`, `~/Projects/AISkills/scripts/dashboard/**`, `~/Projects/AISkills/dashboard_ui/**`
- **Why**: Runs need clearer traceability by project and SOW file from the Codex side.
- **As-Is Diagram (ASCII)**:
```text
run telemetry
   |
   v
skill / plan / sow only
```
- **To-Be Diagram (ASCII)**:
```text
run telemetry
   |
   v
skill / sow_file / project_name / project_path
   |
   v
dashboard short labels + full-path hover
```
- **Deliverables**:
  - telemetry metadata fields
  - schema/loader support
  - dashboard table/detail rendering
- **Done Criteria**:
  - new runs contain the new Codex-side metadata
  - dashboard shows SOW file name and project name
  - hover reveals full path
- **Out-of-Scope**:
  - extra Claude metadata
  - large dashboard redesign
- **Proposed-By**: Codex GPT-5
- **plan**: `plan_todo/telemetry_dashboard_followup_plan.md`
- **Cautions / Risks**:
  - old runs will not have the new fields, so UI must handle nulls
