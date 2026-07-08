# Install AISkills For Agents

This file is the agent-facing install instruction. Follow it step by step when
a user asks you to install AISkills from GitHub.

## Source

- Index: `https://raw.githubusercontent.com/MaiHoangViet1809/AI-skills/main/skills/INDEX.md`
- Registry: `https://raw.githubusercontent.com/MaiHoangViet1809/AI-skills/main/skills/registry.json`

## Rules

- Install all skills listed in `skills/registry.json` by default.
- Install a subset only when the user explicitly names one or more skill names
  and asks for only those skills.
- Do not ask the user to choose skill names just to complete a normal AISkills
  install.
- Do not create or edit project policy files such as `AGENTS.md`, `CLAUDE.md`,
  `.agents/rules`, or `.claude` context files.
- Do not overwrite an existing local skill directory without user approval.
- Do not clone this repo or run repo scripts unless the user explicitly asks for
  the local cloned-repo path.
- Treat `skills/registry.json` as the authoritative skill list and file list.

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

1. Read `skills/registry.json` from the Registry URL above.
2. Select skills:
   - default: every skill in the registry;
   - subset: only exact registry names explicitly requested by the user.
3. If a requested subset name is missing or ambiguous, report the available
   registry names and stop for clarification.
4. Resolve the destination root from the table.
5. For each selected skill, create `<destination-root>/<skill-name>/`.
6. Download every file listed for that skill in `skills/registry.json`.
7. Preserve relative paths under the skill directory.
8. Verify that `SKILL.md` exists in each installed skill directory.
9. Report whether this was an all-skill install or subset install, the installed
   skill count, skill names, and destination paths.

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
