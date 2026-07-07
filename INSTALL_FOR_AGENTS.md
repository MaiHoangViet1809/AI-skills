# Install AISkills For Agents

This file is the agent-facing install instruction. Follow it step by step when
a user asks you to install AISkills from GitHub.

## Source

- Index: `https://raw.githubusercontent.com/MaiHoangViet1809/AI-skills/main/skills/INDEX.md`
- Registry: `https://raw.githubusercontent.com/MaiHoangViet1809/AI-skills/main/skills/registry.json`

## Rules

- Install only the skill or skills the user asks for.
- Do not create or edit project policy files such as `AGENTS.md`, `CLAUDE.md`,
  `.agents/rules`, or `.claude` context files.
- Do not overwrite an existing local skill directory without user approval.
- Do not clone this repo or run repo scripts unless the user explicitly asks for
  the local cloned-repo path.
- Treat `skills/registry.json` as the file list for each skill.

## Destination

Choose exactly one destination for the current agent.

| Agent | Project scope | User scope |
| --- | --- | --- |
| Codex | `<project>/.agents/skills/<skill-name>/` | `$HOME/.agents/skills/<skill-name>/` |
| Codex legacy | n/a | `$HOME/.codex/skills/<skill-name>/` |
| Claude Code | `<project>/.claude/skills/<skill-name>/` | `$HOME/.claude/skills/<skill-name>/` |
| OpenCode | `<project>/.opencode/skills/<skill-name>/` | `$HOME/.config/opencode/skills/<skill-name>/` |
| Other | ask user for a project skill root | ask user for a user skill root |

Use project scope when the user wants the skill only for the current repo. Use
user scope when the user wants the skill available across repos.

## Install Flow

1. Read the index and registry URLs above.
2. Select the requested skill names from the registry.
3. Resolve the destination root from the table.
4. For each selected skill, create `<destination-root>/<skill-name>/`.
5. Download every file listed for that skill in `skills/registry.json`.
6. Preserve relative paths under the skill directory.
7. Verify that `SKILL.md` exists in each installed skill directory.
8. Report installed skill names and destination paths.

## Manual Download Shape

For a registry entry like:

```json
{
  "path": "skills/task-router-flow/references/scope-of-work.md",
  "raw_url": "https://raw.githubusercontent.com/MaiHoangViet1809/AI-skills/main/skills/task-router-flow/references/scope-of-work.md"
}
```

install it as:

```text
<destination-root>/task-router-flow/references/scope-of-work.md
```

## Local Clone Path

If the user already cloned this repo and explicitly wants script-based sync,
read `scripts/skills/README.md` instead. That path copies skill directories
only; it is separate from this GitHub instruction install flow.
