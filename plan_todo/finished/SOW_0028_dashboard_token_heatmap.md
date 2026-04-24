# SOW: Dashboard Token Heatmap

- **Task**: Replace the dashboard activity chart with a GitHub-style daily heatmap whose color intensity reflects token burn, with toggle modes for `total`, `codex`, and `claude`.
- **Location**: `~/Projects/AISkills/plan_todo/SOW_0028_dashboard_token_heatmap.md`, `~/Projects/AISkills/scripts/dashboard/**`, `~/Projects/AISkills/dashboard_ui/**`
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
