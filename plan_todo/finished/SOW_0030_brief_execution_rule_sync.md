# SOW: Brief Execution Rule Sync

- **Task**: Add a repo-owned brief execution rule plus a sync script that copies the rule and selected skills into the local Codex environment.
- **Location**: `/Users/maihoangviet/Projects/AISkills/plan_todo/SOW_0030_brief_execution_rule_sync.md`, `/Users/maihoangviet/Projects/AISkills/rules/**`, `/Users/maihoangviet/Projects/AISkills/scripts/skills/**`, `/Users/maihoangviet/Projects/AISkills/skills/task-router-flow/SKILL.md`, `/Users/maihoangviet/Projects/AISkills/skills/sow-delegate-flow/SKILL.md`
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
