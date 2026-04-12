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

## Scope-of-Work (SoW) Template (MUST use before coding)
Agent MUST present below SoW for approval before applying patches:
- **Task**: <one-sentence change>
- **Location**: <exact folder/file paths>
- **Why**: <business/tech driver>
- **As-Is Diagram (ASCII)**: <current behavior/architecture/state machine>
- **To-Be Diagram (ASCII)**: <target behavior/architecture/state machine>
- **Deliverables**: <files added/modified, funcs/classes exported>
- **Done Criteria**: <compiles, style checks pass, demo runnable, etc.>
- **Out-of-Scope**: <what is explicitly excluded>
- **Proposed-By**: <AI Agent Name, e.g., "Claude Opus 4.5", "Codex GPT5.2", "Gemini", etc.>
- **plan**: <plan name if task related to plan under plan_todo>
- **Cautions / Risks**: list down cautions might happen


### SoW Compliance Guardrail
- Before writing code or editing files, STOP and confirm an approved SoW exists for the task at hand. If not, draft one and obtain approval.
- At each major task switch, re-check that the active SoW still covers the work. If the scope changes, pause and update/seek approval.
- Document the SoW reference (file name or timestamp) when summarizing work so reviewers can trace it quickly.
- NEVER need a SoW to modify/patch another SOW

## Planning & Task Files
- All project planning, status, task-tracking, and SOW markdown documents must live under the `plan_todo/` directory at the repo root.
- Examples: `plan_todo/implementation_plan.md`, `plan_todo/task.md`, `plan_todo/frontend_review.md`, `plan_todo/SOW_*.md`.
- When creating new plan/task/status docs, add them directly to `plan_todo/` instead of the project root.

## Git Version Control
- Always commit task related to code change with summary into message using 'git add' and 'git commit -m <summary>'
- Before finishing any coding task, run through this commit checklist:
  1. Verify worktree only contains changes covered by the approved SoW.
  2. Stage only those files (`git add …`).
  3. Commit with a descriptive summary (`git commit -m "feat: …"`).
- If the user explicitly defers commits, note that in the final response; otherwise assume a commit is required.

## SOW Lifecycle
- When a SOW is completed, move its file into `plan_todo/finished/` and keep AGENTS.md notes in sync so future work references stay accurate.
