---
name: create-agents-md
description: Create project agent-instruction files from the repository TEMPLATE_AGENTS.md when a project does not already have the right entrypoint files. Use when Codex is asked to add, bootstrap, generate, or create coding-agent guardrails for Codex, OpenCode, Claude Code, all/shared tools, or an explicitly named custom instruction filename. Do not use for syncing skills into Codex.
---

# Create Agent Instruction Files

Use this skill to create project-level instruction files from `TEMPLATE_AGENTS.md`.

## Source Template

- Use `TEMPLATE_AGENTS.md` at the AISkills repository root as the shared policy template.
- Do not sync this skill or generated outputs into `~/.codex/skills`.
- Treat this as a docs-only workflow unless the user also asks to change code.

## Target Files

Choose output files from the requested tool:

| Target | Files to create when missing | Rule |
| --- | --- | --- |
| `codex` | `AGENTS.md` | Codex uses `AGENTS.md` as project guidance. |
| `opencode` | `AGENTS.md` | OpenCode rules use `AGENTS.md`. |
| `claude` | `CLAUDE.md` | Claude Code uses `CLAUDE.md`. |
| `all` or `shared` | `AGENTS.md` plus tool-specific entrypoints requested by the user | Keep `AGENTS.md` as the canonical shared policy. |
| explicit custom filename | the exact filename requested | Warn that unknown filenames may not be auto-loaded by any tool. |

For shared/cross-tool Claude support:

- Create or preserve `AGENTS.md` as the canonical policy file.
- Create `CLAUDE.md` as the Claude entrypoint.
- If `AGENTS.md` is canonical, make `CLAUDE.md` import it with `@AGENTS.md` instead of duplicating the full template.
- Put the import at the top of `CLAUDE.md`; add only clearly needed Claude-specific notes below it.

For Claude-only support:

- If the user does not want a shared `AGENTS.md`, create `CLAUDE.md` directly from `TEMPLATE_AGENTS.md`.

## Workflow

1. Resolve the target project root from the user's request or current working directory.
2. Resolve the target tool:
   - use the user's explicit target when provided;
   - default to `codex` only when no target is specified.
3. Determine the output file set from `Target Files`.
4. For each output file, check whether it already exists.
5. If any output file exists:
   - do not overwrite it by default;
   - summarize which files already exist;
   - offer a review or merge plan if the user wants alignment with the template.
6. If an output file is missing:
   - read `TEMPLATE_AGENTS.md`;
   - create the missing instruction file according to the target rules;
   - preserve the template's strict SOW-first policy for code changes;
   - preserve the docs/SOW/plan-only exemption from SOW creation;
   - preserve required-context rules for `PRODUCT_PRINCIPLE_DESIGN.md` and `.agents/rules/*.md`.
7. Keep project-specific edits minimal:
   - fill `Project Overrides` only when the user supplied clear project-specific commands or rules;
   - otherwise leave override placeholders for later review.
8. Run a final file check:
   - confirm the requested output files exist at the target root;
   - confirm no unrelated files changed;
   - report whether each file was created, skipped, or left for review.

## Safety Rules

- Never overwrite an existing instruction file without explicit user approval.
- Never invent project-specific commands, framework rules, or paths.
- Never remove the strict code-change SOW requirement from the template.
- Never make this workflow create a SOW for docs-only instruction-file creation.
- If the target project has nested instruction files, do not modify them unless explicitly requested.
- Do not claim a custom filename will be auto-loaded unless that behavior is verified from official docs or provided by the user.
