# Skill Sync Flow

For AI-agent-driven installation from GitHub, prefer the root
`INSTALL_FOR_AGENTS.md` guide. The scripts in this folder are optional local
utilities for users who have cloned this repo and want a direct copy command.

Use one agent-specific command for the one agent environment that needs the skills.
Do not use a hybrid command to sync multiple agents at once.

## Source

All commands copy repo skills from:

```text
AISkills/skills/<skill-name>/SKILL.md
```

`--all` means every folder under `skills/` that contains `SKILL.md`.
`--overwrite` is required before an existing target skill directory is replaced.
`--dry-run` prints planned actions without copying files.

## Codex

Project-scoped Codex skills:

```bash
uv run python scripts/skills/sync_env_codex.py \
  --scope repo \
  --target-project /path/to/project \
  --skill task-router-flow \
  --dry-run
```

User-scoped Codex skills:

```bash
uv run python scripts/skills/sync_env_codex.py \
  --scope user \
  --all
```

Legacy Codex user skills:

```bash
uv run python scripts/skills/sync_env_codex.py \
  --scope legacy-user \
  --all
```

Codex sync copies skill directories only. It does not write hooks, bridge scripts, or config files.

## Claude Code

Project-scoped Claude Code skills:

```bash
uv run python scripts/skills/sync_env_claude.py \
  --scope repo \
  --target-project /path/to/project \
  --skill task-router-flow \
  --dry-run
```

User-scoped Claude Code skills:

```bash
uv run python scripts/skills/sync_env_claude.py \
  --scope user \
  --all
```

Claude sync rejects Codex-only `legacy-user`.

## OpenCode

Project-scoped OpenCode skills:

```bash
uv run python scripts/skills/sync_env_opencode.py \
  --scope repo \
  --target-project /path/to/project \
  --skill task-router-flow \
  --dry-run
```

User-scoped OpenCode skills:

```bash
uv run python scripts/skills/sync_env_opencode.py \
  --scope user \
  --all
```

OpenCode sync writes native OpenCode paths by default:

```text
repo: <target-project>/.opencode/skills/<skill-name>/
user: $HOME/.config/opencode/skills/<skill-name>/
```

Use `--target-root` only when you intentionally want a custom destination:

```bash
uv run python scripts/skills/sync_env_opencode.py \
  --target-root /path/to/custom/skills \
  --skill task-router-flow
```

## Other Agents

Unsupported agents must use an explicit target root:

```bash
uv run python scripts/skills/sync_env_others.py \
  --target-root /path/to/agent/skills \
  --skill task-router-flow \
  --dry-run
```

## Windows

Use explicit paths on Windows 10/11:

```powershell
uv run python scripts/skills/sync_env_codex.py `
  --scope repo `
  --target-project C:\Users\you\Projects\my-project `
  --skill task-router-flow `
  --dry-run
```

```powershell
uv run python scripts/skills/sync_env_claude.py `
  --target-root C:\Users\you\.claude\skills `
  --all `
  --dry-run
```

The scripts use `pathlib.Path` and do not hardcode POSIX-only separators.

## Compatibility

The old low-level installer still works for explicit target roots:

```bash
uv run python scripts/skills/install_skills.py --skill task-router-flow --target-root /path/to/skills
```

Without `--target-root`, `install_skills.py` keeps its legacy default of `~/.codex/skills`.

The old environment command remains for compatibility. It copies repo skills into the legacy Codex skill root `~/.codex/skills`:

```bash
uv run python scripts/skills/sync_environment.py --target codex --dry-run
```

## Boundary

These scripts only copy AISkills skill directories.
They do not create or modify project policy files such as `AGENTS.md`, `CLAUDE.md`, `.agents/rules`, or `.claude` project context.
