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

This is not enough for working across:

- Codex on macOS / Windows 10 / Windows 11
- Claude Code on macOS / Windows 10 / Windows 11
- target-project scoped skills, where each project may need its own `.agents/skills` or `.claude/skills`

## Source Facts

- Codex official docs list repo skills under `.agents/skills` and user skills under `$HOME/.agents/skills`.
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
  -> copy AISkills/skills/<skill> into target skill directories
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

`legacy-user` exists only to support current local Codex setups that still depend on `~/.codex/skills`.

## CLI Shape

Preferred unified command:

```bash
uv run python scripts/skills/sync_environment.py \
  --agent codex|claude|both \
  --scope repo|user|legacy-user \
  --target-project /path/to/project \
  --skill <name>|--all \
  --overwrite \
  --dry-run
```

Compatibility path:

```bash
uv run python scripts/skills/install_skills.py --skill <name> --target-root <path>
```

`install_skills.py` may become the low-level copier, while `sync_environment.py` owns agent/scope/path resolution.

## Implementation Plan

1. Refactor path resolution into explicit target resolvers.
2. Add `--agent`, `--scope`, `--target-project`, `--skill`, `--all`, `--target-root`, `--overwrite`, and `--dry-run` where needed.
3. Preserve dry-run output before copying anything.
4. Keep overwrite opt-in.
5. Update README with macOS and Windows examples.
6. Add a clear note that project-specific policy/rules are handled by the init skill, not by sync.
7. Add tests or a deterministic dry-run verification path covering:
   - Codex repo target
   - Codex user target
   - Codex legacy user target
   - Claude repo target
   - Claude user target
   - Windows-style target-project path simulation where feasible with explicit paths

## Non-Goals

- Creating `AGENTS.md`, `CLAUDE.md`, or project rules.
- Syncing arbitrary non-skill files into target projects.
- Installing or configuring the Codex CLI / Claude Code CLI themselves.
- Installing plugins or marketplace bundles.
- Managing enterprise/admin skill paths.
- Mutating existing target project skills without `--overwrite`.

## Open Questions

- Should `legacy-user` be hidden behind a flag like `--legacy-codex-home`, or remain a normal scope?
- Should the default target be `codex repo` when `--target-project` is provided, and `codex user` otherwise?
- Should `sync_environment.py` keep telemetry hook sync as a separate `--profile codex-hooks` operation instead of mixing it with skill sync?
