# SOW_20260425_6X92J74B - Dashboard Token Heatmap

- Status: UNKNOWN
- Approval: UNKNOWN
- create_dttm: 2026-04-25T00:36:55+07:00
- create_date: 2026-04-25
- create_dttm_source: filesystem_birthtime
- create_dttm_confidence: filesystem_proxy
- create_dttm_evidence: `plan_todo/finished/SOW_20261008_VO3LKN0L/creation-date-evidence.json` (record: SOW_20260425_6X92J74B)
- approve_dttm: unknown
- finish_dttm: unknown
- legacy_id: SOW_0028
- legacy_path: plan_todo/finished/SOW_0028_dashboard_token_heatmap.md
- migrated_dttm: 2026-10-08T12:48:51+07:00
- legacy_title: SOW: Dashboard Token Heatmap

## Preserved Contract And Historical Evidence

- **Task**: Replace the dashboard activity chart with a GitHub-style daily heatmap whose color intensity reflects token burn, with toggle modes for `total`, `codex`, and `claude`.
- **Location**: `plan_todo/SOW_0028_dashboard_token_heatmap.md`, `~/Projects/AISkills/scripts/dashboard/**`, `~/Projects/AISkills/dashboard_ui/**`
- **Why**: The current activity chart does not surface which days burned the most tokens.
- **As-Is Diagram (ASCII)**:
```text
dashboard row 2 left
   |
   v
stacked activity bars
```
- **To-Be Diagram (ASCII)**:
```text
dashboard row 2 left
   |
   v
github-style daily heatmap
   |
   +--> total tokens
   +--> codex tokens
   +--> claude tokens
```
- **Deliverables**:
  - backend daily token heatmap payload
  - frontend heatmap component
  - mode toggle and legend
- **Done Criteria**:
  - heatmap renders week-column/day-row grid
  - cell color intensity reflects selected token metric
  - tooltip shows date and token values
  - frontend build passes
- **Out-of-Scope**:
  - redesign of the duration chart
  - report/export features
- **Proposed-By**: Codex GPT-5
- **plan**: `plan_todo/telemetry_dashboard_followup_plan.md`
- **Cautions / Risks**:
  - sparse windows will naturally produce many empty cells
  - day grouping should stay consistent across API and UI
