# Skill Install Flow

Install all repo skills into local Codex skills:

```bash
uv run python scripts/skills/install_skills.py --all
```

Install one skill:

```bash
uv run python scripts/skills/install_skills.py --skill telemetry-flow
```

Preview actions without copying:

```bash
uv run python scripts/skills/install_skills.py --all --dry-run
```

Replace existing local copies:

```bash
uv run python scripts/skills/install_skills.py --all --overwrite
```

Notes:

- source is `skills/` in this repo
- target defaults to `~/.codex/skills`
- overwrite is opt-in to avoid clobbering local edits
