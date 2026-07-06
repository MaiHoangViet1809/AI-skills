# Agent Skill Sync Refine Plan

## Status

- **Status**: completed
- **Owner**: Codex GPT-5
- **Created**: 2026-07-07
- **Completed**: 2026-07-07
- **Related SOWs**:
  - `plan_todo/finished/SOW_0062_core_codex_skill_sync.md`
  - `plan_todo/finished/SOW_0063_claude_skill_sync.md`
  - `plan_todo/finished/SOW_0064_opencode_other_skill_sync.md`
  - `plan_todo/finished/SOW_0065_skill_sync_docs_verification.md`

## Problem

Current skill sync tooling is Codex-centric:

- `scripts/skills/install_skills.py` installs repo skills into `~/.codex/skills`.
- `scripts/skills/sync_environment.py` supports only `--target codex`.
- `scripts/skills/README.md` documents only local Codex sync.

This is not enough for working with one explicitly selected agent environment at a time:

- Codex on macOS / Windows 10 / Windows 11
- Claude Code on macOS / Windows 10 / Windows 11
- OpenCode on macOS / Windows 10 / Windows 11
- Other future agents with explicit target roots
- target-project scoped skills, where each project may need the selected agent's own skill root

## Source Facts

- Codex official docs list repo skills under `.agents/skills` and user skills under `$HOME/.agents/skills`.
- OpenCode uses `AGENTS.md` for rules and supports native skill paths under `.opencode/skills` and `~/.config/opencode/skills`.
- Claude Code official docs list project skills under `.claude/skills/<skill-name>/SKILL.md` and personal skills under `~/.claude/skills/<skill-name>/SKILL.md`.
- Windows should be supported through Python `Path.home()` and explicit `--target-root` / `--target-project`, not hardcoded POSIX paths.

## Design Boundary

This plan is only for **publishing existing AISkills repo-owned skills** into agent-visible skill directories.

It must not take ownership of project policy/rule initialization.

Separate concern:

```text
init-agent-env / create-agent-instructions skill
  -> create AGENTS.md / CLAUDE.md
  -> create .agents/rules or .claude project context when requested
  -> decide project-specific policy

sync/install scripts
  -> copy AISkills/skills/<skill> into one selected agent target at a time
  -> preserve overwrite/dry-run safeguards
  -> never invent project policy
```

## Target Model

### Skill Source

```text
AISkills/
  skills/
    <skill-name>/
      SKILL.md
      ...
```

### Destination Matrix

| Agent | Scope | Destination |
| --- | --- | --- |
| Codex | repo | `<target-project>/.agents/skills/<skill-name>/` |
| Codex | user | `$HOME/.agents/skills/<skill-name>/` |
| Codex | legacy-user | `$HOME/.codex/skills/<skill-name>/` |
| Claude Code | repo | `<target-project>/.claude/skills/<skill-name>/` |
| Claude Code | user | `$HOME/.claude/skills/<skill-name>/` |
| OpenCode | repo | `<target-project>/.opencode/skills/<skill-name>/` |
| OpenCode | user | `$HOME/.config/opencode/skills/<skill-name>/` |
| Other agents | explicit target | explicit `--target-root` only |

`legacy-user` exists only to support current local Codex setups that still depend on `~/.codex/skills`.

### Separate Entrypoints

Do not implement a hybrid `both` mode. If a user wants skills available to multiple agents, they should run the relevant command once per agent so each sync is explicit.

Preferred files:

| Entrypoint | Responsibility |
| --- | --- |
| `scripts/skills/sync_env_codex.py` | Codex destinations only |
| `scripts/skills/sync_env_claude.py` | Claude Code destinations only |
| `scripts/skills/sync_env_opencode.py` | OpenCode destinations only |
| `scripts/skills/sync_env_others.py` | Explicit custom target roots for unsupported agents |

Shared copy/path helpers may live in a small internal module under `scripts/skills/` if it removes real duplication. The public commands remain separate by agent.

### Valid Target Matrix

| Entrypoint | Scope arg | Valid | Notes |
| --- | --- | --- | --- |
| `sync_env_codex.py` | `repo` | yes | requires `--target-project` unless `--target-root` is supplied |
| `sync_env_codex.py` | `user` | yes | defaults to `$HOME/.agents/skills` |
| `sync_env_codex.py` | `legacy-user` | yes | defaults to `$HOME/.codex/skills` |
| `sync_env_claude.py` | `repo` | yes | requires `--target-project` unless `--target-root` is supplied |
| `sync_env_claude.py` | `user` | yes | defaults to `$HOME/.claude/skills` |
| `sync_env_claude.py` | `legacy-user` | no | fail clearly; Claude does not use Codex legacy skills |
| `sync_env_opencode.py` | `repo` | yes | requires `--target-project` unless `--target-root` is supplied |
| `sync_env_opencode.py` | `user` | yes | defaults to `$HOME/.config/opencode/skills` |
| `sync_env_opencode.py` | `legacy-user` | no | fail clearly; legacy-user is Codex-only |
| `sync_env_others.py` | explicit target | yes | requires explicit `--target-root` |

### Sync Profiles

Default behavior must be skill-sync-only:

```text
--profile skills
  -> copy skill directories only
  -> no hooks/config mutation
```

Codex hook/config sync is separate, Codex-only, and must be explicit:

```text
--profile codex-hooks
  -> may write ~/.codex/hooks.json
  -> may write ~/.codex/hooks/codex_hook_bridge.py
  -> may update ~/.codex/config.toml
```

Do not run hook/config sync as part of a normal skill install.
Non-Codex entrypoints must reject `--profile codex-hooks` or omit that option entirely.

## CLI Shape

Example command:

```bash
uv run python scripts/skills/sync_env_codex.py \
  --scope repo|user|legacy-user \
  --profile skills \
  --target-project /path/to/project \
  --skill <name>|--all \
  --overwrite \
  --dry-run
```

Compatibility path:

```bash
uv run python scripts/skills/install_skills.py --skill <name> --target-root <path>
```

`install_skills.py` may become the low-level copier, while each `sync_env_<agent>.py` entrypoint owns its own agent/scope/path resolution. If `install_skills.py` is kept as a public command, document it as low-level or legacy-compatible instead of the recommended agent-specific entrypoint.

`--all` means all discoverable repo skill folders under `AISkills/skills/` that contain `SKILL.md`. If a curated bundle is needed later, add a separate `--bundle core` or `--profile core-skills`; do not overload `--all`.

## SOW Breakdown

| SOW | Scope | Purpose |
| --- | --- | --- |
| `SOW_0062_core_codex_skill_sync.md` | Shared skill discovery/copy helpers plus `sync_env_codex.py` | Establish the safe base and Codex repo/user/legacy-user behavior first. |
| `SOW_0063_claude_skill_sync.md` | `sync_env_claude.py` | Add Claude Code repo/user sync without inheriting Codex legacy or hook behavior. |
| `SOW_0064_opencode_other_skill_sync.md` | `sync_env_opencode.py` and `sync_env_others.py` | Add OpenCode repo/user sync plus guarded explicit-target sync for unsupported agents. |
| `SOW_0065_skill_sync_docs_verification.md` | README, migration notes, and final matrix verification | Make the CLI usable on fresh macOS/Windows machines and record the final behavior. |

## Implementation Plan

1. SOW 0062 extracts shared skill discovery/copy helpers only where they remove real duplication.
2. SOW 0062 adds `sync_env_codex.py` with `repo`, `user`, and `legacy-user` scopes.
3. SOW 0062 keeps `skills` as the default profile and makes `codex-hooks` Codex-only and explicit.
4. SOW 0063 adds `sync_env_claude.py` with `repo` and `user` scopes only.
5. SOW 0063 rejects Claude `legacy-user` and any Codex hook/config profile.
6. SOW 0064 adds `sync_env_opencode.py` with `repo`, `user`, and `--target-root` behavior.
7. SOW 0064 adds `sync_env_others.py` with explicit `--target-root` behavior only.
8. Every SOW preserves dry-run output before copying anything and keeps overwrite opt-in.
9. SOW 0065 updates README with macOS and Windows examples for each supported entrypoint.
10. SOW 0065 adds final deterministic verification covering:
   - Codex repo target
   - Codex user target
   - Codex legacy user target
   - Claude repo target
   - Claude user target
   - invalid `claude legacy-user`
   - invalid non-Codex `codex-hooks`
   - OpenCode repo target
   - OpenCode user target
   - OpenCode explicit `--target-root`
   - `sync_env_others.py` requiring explicit `--target-root`
   - explicit temp-dir `--target-project` / `--target-root` paths so Windows users are not dependent on POSIX hardcoding

## Non-Goals

- Creating `AGENTS.md`, `CLAUDE.md`, or project rules.
- Syncing arbitrary non-skill files into target projects.
- Installing or configuring the Codex CLI / Claude Code CLI themselves.
- Installing plugins or marketplace bundles.
- Managing enterprise/admin skill paths.
- Mutating existing target project skills without `--overwrite`.
- Hybrid multi-agent sync in a single command.
- Guessing non-OpenCode unsupported-agent skill destinations.

## Open Questions

- Should `legacy-user` eventually be hidden behind a flag like `--legacy-codex-home`, or remain a normal scope during migration?
- Should the default target be `codex repo` when `--target-project` is provided, and `codex user` otherwise? Current implementation should prefer explicit `--scope`.
