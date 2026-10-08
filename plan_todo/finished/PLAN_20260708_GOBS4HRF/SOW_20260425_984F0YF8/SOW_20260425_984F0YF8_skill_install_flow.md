# SOW_20260425_984F0YF8 - Skill Install Flow

- Status: UNKNOWN
- Approval: UNKNOWN
- create_dttm: 2026-04-25T00:36:55+07:00
- create_date: 2026-04-25
- create_dttm_source: filesystem_birthtime
- create_dttm_confidence: filesystem_proxy
- create_dttm_evidence: `plan_todo/finished/SOW_20261008_VO3LKN0L/creation-date-evidence.json` (record: SOW_20260425_984F0YF8)
- approve_dttm: unknown
- finish_dttm: unknown
- legacy_id: SOW_0027
- legacy_path: plan_todo/finished/SOW_0027_skill_install_flow.md
- migrated_dttm: 2026-10-08T12:48:51+07:00
- legacy_title: SOW: Skill Install Flow

## Preserved Contract And Historical Evidence

- **Task**: Add a local script and docs to install repo skills into `~/.codex/skills` with support for installing all skills, one skill, dry-run, and overwrite.
- **Location**: `plan_todo/SOW_0027_skill_install_flow.md`, `~/Projects/AISkills/scripts/skills/**`, and related docs if needed.
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
