- **Status**: complete
- **Approval**: approved 2026-07-08
- **Task**: Remove repo-owned telemetry skill, telemetry runtime, Codex telemetry hooks, and active dashboard runtime from AISkills while preserving local cloned-repo skill sync scripts as skill-copy-only utilities.
- **Location**: `skills/telemetry-flow/`, `scripts/telemetry/`, `aiskills_common/telemetry/`, `dashboard/`, `.codex/hooks.json.template`, `scripts/skills/sync_environment.py`, `scripts/skills/sync_env_codex.py`, `scripts/skills/README.md`, workflow skill docs under `skills/`, `plan_todo/telemetry_dashboard_master_plan.md`, `plan_todo/telemetry_dashboard_followup_plan.md`, `plan_todo/skill_design_decisions.md`, and focused tests under `tests/`.
- **Why**: AISkills should stop maintaining a custom telemetry/dashboard stack because an external OSS tool now owns that responsibility better. Keeping half of the old stack would leave dead install paths and confusing runtime hooks.
- **Depends-On**: `plan_todo/agent_skill_library_cleanup_plan.md`
- **As-Is Diagram (ASCII)**:
```text
skills/telemetry-flow/
  -> telemetry hook scripts
  -> parser wrappers

scripts/telemetry/
aiskills_common/telemetry/
.codex/hooks.json.template
scripts/skills/sync_environment.py
scripts/skills/sync_env_codex.py --profile codex-hooks
dashboard/
  -> local telemetry dashboard runtime
```
- **To-Be Diagram (ASCII)**:
```text
AISkills
  -> skill library only
  -> local sync scripts copy skills only
  -> no repo-owned telemetry hook/runtime/dashboard
  -> finished plans may keep historical migration notes
```
- **Deliverables**:
  - Delete `skills/telemetry-flow/`.
  - Delete active `dashboard/` runtime files; keep only historical notes in finished planning docs if needed.
  - Delete `scripts/telemetry/`.
  - Delete `aiskills_common/telemetry/` if no remaining active imports need it.
  - Delete `.codex/hooks.json.template` if it only exists for telemetry hooks.
  - Remove telemetry hook/config behavior from `scripts/skills/sync_environment.py` and `scripts/skills/sync_env_codex.py`.
  - Keep `scripts/skills/sync_env_codex.py`, `sync_env_claude.py`, `sync_env_opencode.py`, and `sync_env_others.py` as local cloned-repo skill-copy utilities.
  - Remove `telemetry-flow` from legacy skill bundles, README examples, and active docs.
  - Clean workflow-skill docs that tell agents to start/finish telemetry or rely on telemetry hooks.
  - Move obsolete active telemetry/dashboard planning docs to `plan_todo/finished/` with completed/obsolete status notes.
  - Update or remove tests that assume telemetry/dashboard runtime exists.
- **Done Criteria**:
  - Active owned-path scans for `telemetry-flow`, `scripts/telemetry`, and `dashboard` exclude only `references/` and `plan_todo/finished/` historical records.
  - `uv run python -m unittest tests/test_skill_sync_scripts.py` passes.
  - No install path writes Codex telemetry hooks/config.
  - Local cloned-repo sync commands still work for Codex, Claude Code, OpenCode, and explicit custom target roots.
  - No active dashboard runtime remains in repo code.
  - Worktree changes do not include unrelated staged user deletions unless separately approved.
- **Out-of-Scope**:
  - Installing, configuring, or integrating the replacement external OSS telemetry tool.
  - Deleting user-global `~/.codex` hook files from the local machine.
  - Changing `darwinSkill` layout.
  - Replacing `create-agents-md` with GitHub install docs.
- **Proposed-By**: Codex GPT-5
- **plan**: `plan_todo/agent_skill_library_cleanup_plan.md`
- **Cautions / Risks**:
  - Existing machines may still have old global Codex hooks installed. Document manual cleanup instead of mutating global files.
  - Removing telemetry parser utilities may break tests or docs that import them indirectly.
  - Do not let historical finished plans block deletion of active runtime files.
