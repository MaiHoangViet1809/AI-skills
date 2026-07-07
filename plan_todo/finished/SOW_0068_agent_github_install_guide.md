- **Status**: complete
- **Approval**: approved 2026-07-08
- **Task**: Remove `create-agents-md` and add a GitHub-hosted AI-agent install guide plus static skill manifest so agents can install AISkills skills without cloning the repo.
- **Location**: `skills/create-agents-md/`, root `INSTALL_FOR_AGENTS.md`, `skills/INDEX.md`, `skills/registry.json`, `README.md`, `scripts/skills/README.md`, `scripts/skills/`, `tests/test_skill_sync_scripts.py`, and `plan_todo/skill_design_decisions.md`.
- **Why**: `create-agents-md` solves project instruction-file bootstrap, not skill distribution. The repo should distribute skills through a single agent-facing GitHub instruction file that works across Codex, Claude Code, OpenCode, and unknown agents.
- **Depends-On**: `plan_todo/SOW_0066_remove_telemetry_dashboard.md`
- **As-Is Diagram (ASCII)**:
```text
skills/create-agents-md/
  -> creates AGENTS.md / CLAUDE.md from TEMPLATE_AGENTS.md

scripts/skills/sync_env_*.py
  -> local cloned-repo sync commands
```
- **To-Be Diagram (ASCII)**:
```text
raw GitHub INSTALL_FOR_AGENTS.md
  -> agent reads all instructions
  -> agent picks host destination
  -> agent reads skills/registry.json
  -> agent downloads every file for selected skills
  -> agent recreates native skill folder

scripts/skills/sync_env_*.py
  -> optional local cloned-repo convenience only
```
- **Deliverables**:
  - Delete `skills/create-agents-md/`.
  - Add root `INSTALL_FOR_AGENTS.md` written for AI agents, not only humans.
  - Add `skills/INDEX.md` listing installable skills and short descriptions.
  - Add `skills/registry.json` or equivalent manifest listing every file per skill with relative paths and raw GitHub URLs.
  - Ensure the install guide covers Codex, Claude Code, OpenCode, and other/unknown agents.
  - Ensure the install guide tells agents to ask before overwrite.
  - Ensure the install guide separates skill installation from project policy bootstrap.
  - Update `README.md` and `scripts/skills/README.md` to present the GitHub install guide as the primary agent install path.
  - Keep `scripts/skills/sync_env_*.py` documented as local cloned-repo convenience only.
  - Update tests or add a manifest validation check so `skills/registry.json` stays aligned with `skills/`.
- **Done Criteria**:
  - A user can give an AI agent one raw GitHub URL for `INSTALL_FOR_AGENTS.md`.
  - The guide does not require cloning this repo.
  - The guide does not require running `sync_env_*.py`.
  - The manifest is complete enough for an agent to recreate each selected skill folder.
  - `create-agents-md` no longer appears in active skill lists or install docs.
  - Existing skill sync tests still pass after `create-agents-md` removal.
  - Worktree changes do not include unrelated staged user deletions unless separately approved.
- **Out-of-Scope**:
  - Creating project policy files such as `AGENTS.md` or `CLAUDE.md`.
  - Removing local sync scripts.
  - Reintroducing a project policy bootstrap skill.
  - Regrouping `darwinSkill`.
- **Proposed-By**: Codex GPT-5
- **plan**: `plan_todo/agent_skill_library_cleanup_plan.md`
- **Cautions / Risks**:
  - Some skills include references, scripts, metadata, or assets; single-file raw `SKILL.md` install is insufficient.
  - Manifest generation must not advertise deleted or staged-for-deletion skills.
  - The guide must not imply all agents auto-load the same policy files.
