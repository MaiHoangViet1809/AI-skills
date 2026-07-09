# AGENTS.md Template - Repo Operating Contract

This file defines the default operating rules for AI agents working in this repository.
Use RFC2119 keywords: **MUST**, **SHOULD**, **MAY**, **NEVER**.

---

## Communication

- Agents **MUST** answer briefly, directly, and only with the detail needed for the task.
- When working, status updates should describe what is being done in one short sentence.
- Prefer flat bullets and short paragraphs. Use deeper explanation only when risk or ambiguity requires it.
- When diagrams are useful, prefer ASCII unless the user asks for another format.

---

## Read First

Before proposing or changing anything, agents **MUST** inspect the current repository state:

- Read this `AGENTS.md` and any nested `AGENTS.md` in the target path.
- Read relevant code, docs, plans, and existing tests before drawing conclusions.
- Check `git status --short` before editing so user changes are not overwritten.
- Prefer existing project patterns and helpers over introducing new structure.
- Before drafting a code-change SOW, inspect the current implementation and run
  a cheap targeted check or experiment when feasible. Do not write SOWs from
  assumptions alone.

Before code, design, architecture, refactor, or runtime-contract work, agents **MUST** also read these files if they exist:

- `PRODUCT_PRINCIPLE_DESIGN.md` at the repository root.
- `.agents/rules/*.md`:
  - if `README.md` or `INDEX.md` exists, read it first;
  - if there are only a few rule files, read all of them;
  - if there are many, read the files whose names match the task scope and state which files were read.

`PRODUCT_PRINCIPLE_DESIGN.md` is the design source of truth when it exists.
If the requested change conflicts with it, stop and ask for explicit user approval.
When a task is governed by that document, agents **MUST** state the relevant principle in the SOW, plan, or closeout summary.
Agents **MUST NOT** silently drift from the principle design through hybrid ownership, transitional adapters, or local convenience changes.

---

## Task Routing

Use this routing before execution:

| Request Type | Required Flow |
| --- | --- |
| New code change, feature, refactor, cleanup, or test-code change | Draft or find an approved SOW before editing code. |
| Change to work already covered by an active SOW | Update or extend that SOW before widening code scope. |
| Debug or regression investigation | Find root cause first; require SOW only when the fix becomes a code change. |
| Docs, SOW, or plan-only change | Do **not** create a new SOW by default; show a concrete edit plan and edit directly after approval/request. |

Docs-only edits include markdown docs, planning files, SOW files, diagrams, and decision notes.
They do not require a SOW unless they change approved implementation scope.

---

## Strict SOW-First For Code Changes

For any code-changing work, agents **MUST NOT** edit source code, tests, scripts, config, runtime contracts, or generated code until an approved SOW covers the exact task.

An approved SOW **MUST** include:

- **Status**: approved or in progress
- **Approval**: approved marker and approver when available
- **Task**: one-sentence change
- **Location**: exact files or folders allowed to change
- **Why**: business or technical driver
- **As-Is Diagram (ASCII)**: current state when behavior or architecture changes
- **To-Be Diagram (ASCII)**: target state when behavior or architecture changes
- **Deliverables**: files, exports, behavior, or artifacts changed
- **Done Criteria**: checks, tests, smoke path, or review criteria
- **Out-of-Scope**: what must not be changed
- **Proposed-By**: agent name or tool identity
- **Plan / Reference**: related plan, issue, ticket, or investigation when applicable
- **Cautions / Risks**: likely failure modes

Agents **MUST** re-check the active SOW at each major task switch.
If scope expands, stop and update the SOW before continuing.
If a bug or regression is caused by a previous SOW, extend that same SOW instead of creating an unrelated standalone SOW.
Closeout summaries for code work **MUST** include the SOW reference so reviewers can trace the change.

---

## Decision Logging

For code-changing work, agents **MUST** record material implementation decisions that are not already specified by the SOW or user.
Use the active SOW, an existing decision log, or the repo's planning folder.

A decision note should include:

- context
- options considered
- chosen strategy and why
- tradeoffs accepted
- edge cases or risks

If the repo defines a dedicated decision-log path in Project Overrides, use that path.
Do not block trivial mechanical edits on a decision note.

---

## Design Principles

Agents **MUST** follow DRY, SOLID, and KISS.

Practical rules:

- Prefer simple, direct code over clever abstractions.
- Reuse existing helpers, types, modules, and project conventions first.
- Do not create facade, wrapper, adapter, compatibility shim, or workaround layers unless the SOW explicitly requires them.
- Do not keep old and new ownership paths alive by default; prefer one clear source of truth.
- When APIs evolve, update call sites directly instead of adding temporary aliases.
- Abstractions must earn their place by removing real duplication, hiding genuine complexity, or enabling necessary tests.
- Avoid single-use helper functions that only move code around without clarifying behavior.
- Do not create a function, class, wrapper, or adapter that is only used once unless it hides genuine complexity or is required for testing.
- Apply the 2+ rule: extract reusable code only after the same logic exists in at least two places.
- Do not wrap an API just to rename parameters, provide defaults, or pass arguments through.
- Prefer fail-fast ownership cuts over prolonged hybrid compatibility paths when the approved target architecture is clear.
- NEVER create empty files.
- NEVER create `__init__.py`. Prefer explicit imports or a clear SDK/API entrypoint module.
- If packaging, tooling, or test discovery appears to require `__init__.py`, stop and ask for explicit user approval instead of creating it.

---

## Architecture Boundaries

Agents **MUST** keep ownership boundaries clean:

- Product/runtime code must not contain task-specific, SOW-specific, demo-only, or smoke-test-only logic.
- Repo-local validation and one-off probes belong in docs, tests, or clearly marked tooling locations.
- Public APIs, CLI commands, storage schemas, and shared contracts must not change without explicit SOW coverage.
- Do not move business logic into UI, glue, or wrapper layers for convenience.
- Do not write runtime artifacts outside the repository unless the user explicitly approves it.

Before adding a route, command, hook, config key, or shared type, ask:

```text
Is this a generic product capability, or only local validation/tooling?
```

If it is only validation/tooling, keep it out of product-facing surfaces.

---

## Implementation Discipline

- Keep edits limited to the SOW `Location` for code work.
- Prefer structured parsers and project APIs over ad-hoc string manipulation.
- Add comments only for non-obvious intent, invariants, tradeoffs, or edge cases.
- Keep comments and docstrings synchronized with the code when touched.
- Do not introduce new dependencies without checking existing alternatives and updating the lockfile/tooling as required.
- Never hardcode secrets, tokens, private paths, or machine-specific credentials.

Package management should follow the repository's existing toolchain.
If the repo uses `uv`, use `uv` for Python dependency and script workflows.

---

## Verification

Agents **MUST** verify at the right abstraction layer before claiming completion.

Minimum verification discipline:

- Run targeted checks matching the changed files and SOW done criteria.
- For UI-visible behavior, verify through the real UI or API path when feasible.
- For architecture changes, verify ownership and boundary correctness, not only passing tests.
- Perform one negative check before closeout:

```text
What would prove this is still not truly implemented?
```

Closeout summaries **MUST** separate:

- definitely implemented
- approximated or simulated
- not implemented or not verified

If tests or checks were not run, say so directly and explain why.

---

## Git Safety

- Never revert, overwrite, or delete user-authored changes without explicit approval.
- Before destructive changes such as delete, move, or broad rewrite, present a file-level impact list.
- For rollback of scoped uncommitted work, prefer `git restore -- <exact files>` only when those files are cleanly owned by the current task.
- NEVER use broad rollback commands such as `git restore .`, `git checkout -- .`, or `git reset --hard` unless the user explicitly approves.
- Stage only files covered by the task.
- For code changes, commit after successful verification unless the user explicitly defers commits.
- For docs-only changes, commit only when the user or repo policy requires it.
- Never push unless the user explicitly asks.

---

## Planning Files

Planning, SOW, status, and investigation files should live under the repository's planning directory, usually `plan_todo/`.

For single-agent projects, a simple layout is acceptable:

```text
plan_todo/
  active/
  finished/
  finding/
```

For multi-agent projects, prefer per-agent namespaces:

```text
plan_todo/
  <agent>/
    finished/
  finding/
  deprecated/
```

Rules:

- If per-agent namespaces exist, create SOWs and plans only inside the current agent's folder.
- Do not create numbered SOWs directly under `plan_todo/` root when namespaced folders exist.
- Completed SOWs and plans should move to the matching `finished/` folder using `git mv`.
- Research, investigation, and handoff docs should go under `plan_todo/finding/`.
- A SOW is approved only when it has an explicit approval marker such as `Status: APPROVED` or `Approved-By: <name>`.
- When moving or renaming planning files, update markdown references in the same change.

---

## Project Overrides

Fill this section with project-specific rules only when needed.
Keep the generic contract above portable.

### Package And Commands

- Install:
- Format:
- Lint:
- Type check:
- Targeted tests:
- Full test suite:

### Architecture Source Of Truth

- Principle/design docs:
- Runtime ownership boundaries:
- API or schema rules:

### Technology Conventions

- Language versions:
- Framework conventions:
- File/folder placement rules:
- Naming rules:

### Local Exceptions

- SOW exemptions:
- Tests that must not be run automatically:
- Slow or destructive commands requiring explicit approval:
