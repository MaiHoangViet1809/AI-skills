# SOW: Skill Install Flow

- **Task**: Add a local script and docs to install repo skills into `~/.codex/skills` with support for installing all skills, one skill, dry-run, and overwrite.
- **Location**: `~/Projects/AISkills/plan_todo/SOW_0027_skill_install_flow.md`, `~/Projects/AISkills/scripts/skills/**`, and related docs if needed.
- **Why**: The repo needs a repeatable way to sync curated skills into Codex local skills without manual copy steps.
- **As-Is Diagram (ASCII)**:
```text
repo skills
   |
   v
manual copy / ad-hoc sync
```
- **To-Be Diagram (ASCII)**:
```text
uv run python scripts/skills/install_skills.py
   |
   v
~/.codex/skills synced from repo
```
- **Deliverables**:
  - install script
  - usage README
  - overwrite and dry-run safeguards
- **Done Criteria**:
  - can install all repo skills
  - can install one named skill
  - dry-run shows planned actions
  - overwrite is opt-in
- **Out-of-Scope**:
  - remote publishing
  - package registry distribution
- **Proposed-By**: Codex GPT-5
- **plan**: `plan_todo/telemetry_dashboard_followup_plan.md`
- **Cautions / Risks**:
  - overwrite must not be default because local skill edits may exist
  - only directories with `SKILL.md` should be considered installable
