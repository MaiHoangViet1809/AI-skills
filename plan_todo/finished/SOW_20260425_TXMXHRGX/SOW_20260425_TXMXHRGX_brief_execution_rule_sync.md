# SOW_20260425_TXMXHRGX - Brief Execution Rule Sync

- Status: UNKNOWN
- Approval: UNKNOWN
- create_dttm: 2026-04-25T00:36:55+07:00
- create_date: 2026-04-25
- create_dttm_source: filesystem_birthtime
- create_dttm_confidence: filesystem_proxy
- create_dttm_evidence: `plan_todo/finished/SOW_20261008_VO3LKN0L/creation-date-evidence.json` (record: SOW_20260425_TXMXHRGX)
- approve_dttm: unknown
- finish_dttm: unknown
- legacy_id: SOW_0030
- legacy_path: plan_todo/finished/SOW_0030_brief_execution_rule_sync.md
- migrated_dttm: 2026-10-08T12:48:51+07:00
- legacy_title: SOW: Brief Execution Rule Sync

## Preserved Contract And Historical Evidence

- **Task**: Add a repo-owned brief execution rule plus a sync script that copies the rule and selected skills into the local Codex environment.
- **Location**: `plan_todo/SOW_0030_brief_execution_rule_sync.md`, `~/Projects/AISkills/rules/**`, `~/Projects/AISkills/scripts/skills/**`, `skills/task-router-flow/SKILL.md`, `skills/sow-delegate-flow/SKILL.md`
- **Why**: The brevity rule should live in the repo as source of truth, then sync into Codex now and other environments later.
- **As-Is Diagram (ASCII)**:
```text
execution brevity
   |
   v
ad-hoc preference only
```
- **To-Be Diagram (ASCII)**:
```text
repo rule
   |
   v
sync script
   |
   +--> codex rules
   +--> codex skills with refs
```
- **Deliverables**:
  - repo rule file
  - sync script
  - skill refs to the rule
- **Done Criteria**:
  - rule exists in repo
  - task-router-flow and sow-delegate-flow reference it
  - sync script copies rule into `~/.codex/rules`
  - sync script updates local Codex skill copies via repo source
- **Out-of-Scope**:
  - sync to Claude/OpenCode right now
  - force every skill to use the rule
- **Proposed-By**: Codex GPT-5
- **plan**: `global execution brevity rule`
- **Cautions / Risks**:
  - sync should not overwrite unrelated local Codex customizations outside the selected files
