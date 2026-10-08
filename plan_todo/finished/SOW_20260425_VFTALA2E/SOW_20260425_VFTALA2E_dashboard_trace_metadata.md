# SOW_20260425_VFTALA2E - Dashboard Trace Metadata

- Status: UNKNOWN
- Approval: UNKNOWN
- create_dttm: 2026-04-25T00:36:55+07:00
- create_date: 2026-04-25
- create_dttm_source: filesystem_birthtime
- create_dttm_confidence: filesystem_proxy
- create_dttm_evidence: `plan_todo/finished/SOW_20261008_VO3LKN0L/creation-date-evidence.json` (record: SOW_20260425_VFTALA2E)
- approve_dttm: unknown
- finish_dttm: unknown
- legacy_id: SOW_0029
- legacy_path: plan_todo/finished/SOW_0029_dashboard_trace_metadata.md
- migrated_dttm: 2026-10-08T12:48:51+07:00
- legacy_title: SOW: Dashboard Trace Metadata

## Preserved Contract And Historical Evidence

- **Task**: Add Codex-side telemetry metadata for `project_name`, `project_path`, and `sow_file`, then show them on the dashboard with hoverable full paths.
- **Location**: `plan_todo/SOW_0029_dashboard_trace_metadata.md`, `~/Projects/AISkills/skills/telemetry-flow/scripts/telemetry_hook.py`, `~/Projects/AISkills/scripts/dashboard/**`, `~/Projects/AISkills/dashboard_ui/**`
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
