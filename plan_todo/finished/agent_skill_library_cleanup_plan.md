# Agent Skill Library Cleanup Plan

## Status

- **Status**: complete
- **Owner**: Codex GPT-5
- **Created**: 2026-07-08
- **Related SOWs**:
  - `plan_todo/SOW_0066_remove_telemetry_dashboard.md`
  - `plan_todo/SOW_0067_review_darwinskill_regroup.md`
  - `plan_todo/SOW_0068_agent_github_install_guide.md`
  - `plan_todo/SOW_0069_final_skill_library_cleanup.md`

## Goal

Refocus AISkills into a clean, portable agent-skill library:

1. Remove repo-owned telemetry skill/runtime/dashboard surfaces because that responsibility is moving to external OSS tooling.
2. Review and regroup `darwinSkill` so its package, tests, scripts, docs, and active planning docs are easier to reason about.
3. Replace the current `create-agents-md` skill with a pure GitHub-hosted agent install guide that any AI agent can follow to install skills into its own native skill location.

## Non-Goals

- Do not keep a custom telemetry/dashboard stack in this repo.
- Do not make the install guide require cloning the repo and running `scripts/skills/sync_env_*.py`.
- Do not remove the Python sync scripts only because the agent-facing install guide exists. They remain useful for users who clone this repo and want local scripted sync.
- Do not create project policy files such as `AGENTS.md`, `CLAUDE.md`, `.agents/rules`, or `.claude` during skill installation.
- Do not keep `create-agents-md` as a skill. It should be removed.
- Do not migrate `darwinSkill` files before the regroup review chooses a target layout.
- Do not touch unrelated staged user changes.

## Current Observations

### Telemetry And Dashboard

Telemetry/dashboard is spread across:

```text
skills/telemetry-flow/
scripts/telemetry/
aiskills_common/telemetry/
dashboard/
.codex/hooks.json.template
scripts/skills/sync_environment.py
scripts/skills/sync_env_codex.py
plan_todo/telemetry_dashboard_master_plan.md
plan_todo/telemetry_dashboard_followup_plan.md
plan_todo/skill_design_decisions.md
```

There are also workflow-skill references to telemetry markers and hook behavior. Removal must audit references before deleting files.

### darwinSkill

`darwinSkill` is currently split across:

```text
darwinSkill/
scripts/darwinSkill/
tests/darwinSkill/
plan_todo/SOW_0047_*.md ... SOW_0055_*.md
plan_todo/codex_skill_improvement_data_plan.md
plan_todo/skill_framework_distillation_plan.md
references/SkillOpt/
```

The split is not automatically wrong, but it is hard to review because framework code, demos, tests, and historical planning are far apart.

### Agent Installation

The current `create-agents-md` skill creates project instruction files from `TEMPLATE_AGENTS.md`. That is not the desired distribution model.

The desired model is:

```text
User gives an AI agent one GitHub URL
  -> agent reads INSTALL_FOR_AGENTS.md
  -> agent detects its host and target scope
  -> agent copies selected skill folders from GitHub into its own native skill location
  -> no repo clone required
  -> no project policy bootstrap unless separately requested
```

External patterns reviewed:

- `INSTALL_FOR_AGENTS.md`: agent-facing install guide that tells an agent to read the whole file, detect the host, choose install path, and fetch companion raw files.
- Direct raw `SKILL.md` install: simple skill libraries publish raw GitHub URLs and tell agents or users to copy them into host-specific skill directories.
- Multi-agent repositories list host-specific destinations and commands, but still keep install per host explicit.

## Target Model

### Skill Source Layout

AISkills should keep skills under:

```text
skills/
  <skill-name>/
    SKILL.md
    references/
    scripts/
    agents/
    assets/
```

Install guidance must treat a skill as a folder, not only as a single `SKILL.md`, because several skills include references, scripts, metadata, or assets.

### Agent-Facing Install Guide

Add:

```text
INSTALL_FOR_AGENTS.md
```

This file is the canonical agent-facing entrypoint. README can point humans to it, but the install guide itself should be written for AI agents.

Required install-guide behavior:

1. Read the entire file before acting.
2. Detect the current agent host:
   - Codex
   - Claude Code
   - OpenCode
   - other/unknown
3. Ask the user only if host or scope cannot be inferred.
4. Choose native skill destination:

| Host | Project Scope | User Scope |
| --- | --- | --- |
| Codex | `<project>/.agents/skills/<skill-name>/` | `$HOME/.agents/skills/<skill-name>/` |
| Claude Code | `<project>/.claude/skills/<skill-name>/` | `$HOME/.claude/skills/<skill-name>/` |
| OpenCode | `<project>/.opencode/skills/<skill-name>/` | `$HOME/.config/opencode/skills/<skill-name>/` |
| Other | ask user for target root | ask user for target root |

5. Copy the selected skill folder from GitHub into the chosen destination.
6. Preserve folder contents and relative paths.
7. Never overwrite an existing skill without explicit user approval.
8. Do not create `AGENTS.md`, `CLAUDE.md`, `.agents/rules`, or other project policy files.

Because GitHub raw URLs are file-based, the guide should include or point to a static skill index/manifest:

```text
skills/INDEX.md
skills/registry.json
```

The registry must list each installable skill and every file that belongs to it, including relative path and raw GitHub URL. Agents can then download each file without cloning the repository and recreate the skill folder locally.

The guide may also describe the local developer path:

```text
git clone this repo
  -> run scripts/skills/sync_env_<agent>.py
```

That path is explicitly for humans or agents operating inside a cloned checkout. It is not the primary agent-facing install path.

### Project Policy Bootstrap

Remove:

```text
skills/create-agents-md/
```

If project policy bootstrap is ever needed again, it should be a separate documented workflow, not a skill installed into every agent.

## Proposed SOW Breakdown

### SOW 0066 - Remove Telemetry Skill And Dashboard

Scope:

- Delete `skills/telemetry-flow/`.
- Delete the active `dashboard/` runtime. If historical context is needed, keep only migration notes in finished planning docs, not runnable dashboard code.
- Delete `scripts/telemetry/`.
- Delete `aiskills_common/telemetry/` if no remaining runtime imports need it.
- Delete `.codex/hooks.json.template` if it only serves telemetry hooks.
- Remove telemetry hook/config behavior from `scripts/skills/sync_environment.py` and `scripts/skills/sync_env_codex.py`.
- Keep the Python skill-sync scripts as local cloned-repo utilities, but make them skill-copy-only after telemetry removal.
- Remove `telemetry-flow` from legacy skill bundles and docs.
- Clean workflow-skill docs that instruct agents to start/finish telemetry.
- Move obsolete telemetry/dashboard plans to `plan_todo/finished/` or archive notes as appropriate.

Done criteria:

- Active owned-path scans for `telemetry-flow`, `scripts/telemetry`, and `dashboard` exclude only `references/` and `plan_todo/finished/` historical records.
- Skill sync tests pass without telemetry skill.
- No install path writes Codex telemetry hooks/config.
- Local cloned-repo sync commands still work for Codex, Claude Code, OpenCode, and explicit custom target roots.
- No dashboard runtime remains in active code.

### SOW 0067 - Review And Regroup darwinSkill

Scope:

- Inventory `darwinSkill/`, `scripts/darwinSkill/`, `tests/darwinSkill/`, active SOWs, reference docs, and generated/cache files.
- Propose one target layout before moving files.
- Decide whether to:
  - keep conventional top-level `darwinSkill/`, `tests/darwinSkill/`, `scripts/darwinSkill/`; or
  - group under a clearer project boundary such as `projects/darwinSkill/` or `darwinSkill_workspace/`.
- Review whether active SOWs 0047-0055 are still valid, stale, or should be moved/rewritten.
- Identify tracked/generated cache artifacts if any are present; do not remove them in this review SOW.

Done criteria:

- A reviewed target layout exists with migration risks and test impact.
- No file move is performed without an approved migration SOW.
- Active/stale darwinSkill planning docs are classified.

### SOW 0068 - Replace create-agents-md With GitHub Agent Install Guide

Scope:

- Delete `skills/create-agents-md/`.
- Add root `INSTALL_FOR_AGENTS.md`.
- Add `skills/INDEX.md` and `skills/registry.json` or equivalent static install manifest.
- Update `README.md` and `scripts/skills/README.md` to point to the agent-facing install guide.
- Keep `scripts/skills/sync_env_*.py` as local cloned-repo convenience only, not the primary agent install path.
- Remove docs that present `create-agents-md` as the project instruction bootstrap answer.

Done criteria:

- A user can give an AI agent one raw GitHub URL for `INSTALL_FOR_AGENTS.md`.
- The guide lets the agent install selected skills by copying skill folders/files from GitHub into native host locations.
- The registry or equivalent manifest is complete enough for an agent to recreate each skill folder without cloning the repo.
- The guide does not require cloning this repo.
- The guide does not require running `sync_env_*.py`.
- The guide clearly separates skill installation from project policy bootstrap.
- Existing skill sync tests still pass after `create-agents-md` removal.

### SOW 0069 - Final Library Cleanup And Verification

Scope:

- Re-run active owned-path reference scans, with `references/` and `plan_todo/finished/` treated as historical context rather than active product surface.
- Update `skill_design_decisions.md` with the new distribution decision.
- Ensure active skills list contains only supported skills.
- Ensure README presents AISkills as a portable skill library, not a telemetry/dashboard product.
- Verify install docs against Codex, Claude Code, OpenCode, and other-agent custom target roots.

Done criteria:

- No active docs claim telemetry/dashboard is maintained in this repo.
- No active docs claim `create-agents-md` exists.
- Agent-facing install guide is the primary distribution path.
- Local cloned-repo sync scripts are documented as optional convenience commands, not agent-install requirements.
- Worktree contains only approved cleanup scope.

## Recommended Execution Order

1. SOW 0066: remove telemetry/dashboard first because it affects sync scripts and docs.
2. SOW 0068: replace `create-agents-md` with `INSTALL_FOR_AGENTS.md` after telemetry skill removal so the install guide does not advertise deleted skills.
3. SOW 0067: review `darwinSkill` grouping separately because it may become a larger migration.
4. SOW 0069: final cleanup pass after the other workstreams settle.

## Risks

- Telemetry removal may break existing Codex hook configs on machines that already installed this repo's hooks. The removal SOW should document manual cleanup, not silently mutate user global files.
- Some skills include supporting files, so single raw `SKILL.md` copy is not enough for all skills.
- `darwinSkill` regrouping can easily become a large import-path migration. Review first, migrate second.
- Existing staged deletions in the worktree must not be mixed into these SOWs unless explicitly approved.
