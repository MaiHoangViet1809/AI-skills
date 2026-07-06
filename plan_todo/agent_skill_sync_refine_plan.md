# Agent Skill Sync Refine Plan

## Status

- **Status**: draft
- **Owner**: Codex GPT-5
- **Created**: 2026-07-07
- **Related SOW**: `plan_todo/SOW_0062_cross_agent_skill_sync.md`

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
- OpenCode uses `AGENTS.md` for rules, but its skill/runtime sync destination should be implemented only from confirmed docs or explicit user-provided target roots.
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
| OpenCode | repo/user | TBD only after confirmed docs or explicit `--target-root` |
| Other agents | repo/user | explicit `--target-root` only |

`legacy-user` exists only to support current local Codex setups that still depend on `~/.codex/skills`.

### Separate Entrypoints

Do not implement a hybrid `both` mode. If a user wants skills available to multiple agents, they should run the relevant command once per agent so each sync is explicit.

Preferred files:

| Entrypoint | Responsibility |
| --- | --- |
| `scripts/skills/sync_env_codex.py` | Codex destinations only |
| `scripts/skills/sync_env_claude.py` | Claude Code destinations only |
| `scripts/skills/sync_env_opencode.py` | OpenCode destinations only, after target semantics are confirmed |
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
| `sync_env_opencode.py` | any | pending | do not ship default destinations until confirmed |
| `sync_env_others.py` | custom | yes | requires explicit `--target-root` |

### Sync Profiles

Default behavior must be skill-sync-only:

```text
--profile skills
  -> copy skill directories only
  -> no hooks/config mutation
```

Codex hook/config sync is separate and must be explicit:

```text
--profile codex-hooks
  -> may write ~/.codex/hooks.json
  -> may write ~/.codex/hooks/codex_hook_bridge.py
  -> may update ~/.codex/config.toml
```

Do not run hook/config sync as part of a normal skill install.

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

## Implementation Plan

1. Extract shared skill discovery/copy helpers only where they remove real duplication.
2. Add separate public sync entrypoints for Codex, Claude, OpenCode, and other agents.
3. Add `--scope`, `--profile`, `--target-project`, `--skill`, `--all`, `--target-root`, `--overwrite`, and `--dry-run` where needed.
4. Preserve dry-run output before copying anything.
5. Keep overwrite opt-in.
6. Make `skills` the default profile and require explicit opt-in for `codex-hooks`.
7. Validate each entrypoint's scope matrix before building copy actions.
8. Update README with macOS and Windows examples.
9. Add a clear note that project-specific policy/rules are handled by the init skill, not by sync.
10. Add tests or a deterministic dry-run verification path covering:
   - Codex repo target
   - Codex user target
   - Codex legacy user target
   - Claude repo target
   - Claude user target
   - invalid `claude legacy-user`
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
- Guessing OpenCode skill destinations before target semantics are verified.

## Open Questions

- Should `legacy-user` eventually be hidden behind a flag like `--legacy-codex-home`, or remain a normal scope during migration?
- Should the default target be `codex repo` when `--target-project` is provided, and `codex user` otherwise? Current implementation should prefer explicit `--scope`.
- What is the correct OpenCode skill destination, if any, beyond rule files? Leave `sync_env_opencode.py` guarded until this is verified.
