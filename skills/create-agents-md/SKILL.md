---
name: create-agents-md
description: Create a project AGENTS.md from the repository TEMPLATE_AGENTS.md when a project does not already have one. Use when Codex is asked to add, bootstrap, generate, or create AGENTS.md guardrails for a project, especially from the AISkills template. Do not use for syncing skills into Codex.
---

# Create AGENTS.md

Use this skill to create a portable project-level `AGENTS.md` from `TEMPLATE_AGENTS.md`.

## Source Template

- Use `TEMPLATE_AGENTS.md` at the AISkills repository root as the source template.
- Do not sync this skill or generated outputs into `~/.codex/skills`.
- Treat this as a docs-only workflow unless the user also asks to change code.

## Workflow

1. Resolve the target project root from the user's request or current working directory.
2. Check whether `<target-project>/AGENTS.md` already exists.
3. If `AGENTS.md` exists:
   - do not overwrite it by default;
   - summarize that it already exists;
   - offer a review or merge plan if the user wants alignment with the template.
4. If `AGENTS.md` does not exist:
   - read `TEMPLATE_AGENTS.md`;
   - create `<target-project>/AGENTS.md` from that template;
   - preserve the template's strict SOW-first policy for code changes;
   - preserve the docs/SOW/plan-only exemption from SOW creation;
   - preserve required-context rules for `PRODUCT_PRINCIPLE_DESIGN.md` and `.agents/rules/*.md`.
5. Keep project-specific edits minimal:
   - fill `Project Overrides` only when the user supplied clear project-specific commands or rules;
   - otherwise leave override placeholders for later review.
6. Run a final file check:
   - confirm `AGENTS.md` exists at the target root;
   - confirm no unrelated files changed;
   - report whether the file was created, skipped, or left for review.

## Safety Rules

- Never overwrite an existing `AGENTS.md` without explicit user approval.
- Never invent project-specific commands, framework rules, or paths.
- Never remove the strict code-change SOW requirement from the template.
- Never make this workflow create a SOW for docs-only `AGENTS.md` creation.
- If the target project has nested `AGENTS.md` files, do not modify them unless explicitly requested.
