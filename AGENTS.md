# Agent Instructions

This file contains instructions and conventions for AI agents working on this project.

## Package Management
- **Tool**: Use `uv` for all package management tasks.
- **Commands**:
    - Install dependencies: `uv pip install -r requirements.txt` or `uv sync` if using `uv.lock`.
    - Add package: `uv add <package>`
    - Run scripts: `uv run <script>`
    - Python version: Respect `.python-version` or `pyproject.toml` settings.

## Response Style
- By default, answer briefly and directly.
- Keep responses concise but complete enough to satisfy the request.
- Do not add long explanations unless the user explicitly asks for more detail.

## Scope-of-Work (SoW)
- Use `task-router-flow` as the front-door workflow for SOW decisions.
- Use `skills/task-router-flow/references/scope-of-work.md` as the source of truth for SOW definition, template, indexing, and lifecycle.
- For code-changing work, do not start implementation until the active SOW is approved unless the repo explicitly exempts the task.

## Planning & Task Files
- Planning, status, task-tracking, and SOW markdown documents live under `plan_todo/`.
- Use `skills/task-router-flow/references/scope-of-work.md` for planning and SOW location rules.

## Git Version Control
- Always commit task related to code change with summary into message using 'git add' and 'git commit -m <summary>'
- Before finishing any coding task, run through this commit checklist:
  1. Verify worktree only contains changes covered by the approved SoW.
  2. Stage only those files (`git add …`).
  3. Commit with a descriptive summary (`git commit -m "feat: …"`).
- If the user explicitly defers commits, note that in the final response; otherwise assume a commit is required.
