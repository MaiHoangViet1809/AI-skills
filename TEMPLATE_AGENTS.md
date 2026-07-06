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

Before code, design, architecture, refactor, or runtime-contract work, agents **MUST** also read these files if they exist:

- `PRODUCT_PRINCIPLE_DESIGN.md` at the repository root.
- `.agents/rules/*.md`:
  - if `README.md` or `INDEX.md` exists, read it first;
  - if there are only a few rule files, read all of them;
  - if there are many, read the files whose names match the task scope and state which files were read.

`PRODUCT_PRINCIPLE_DESIGN.md` is the design source of truth when it exists.
If the requested change conflicts with it, stop and ask for explicit user approval.

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
- **Cautions / Risks**: likely failure modes

Agents **MUST** re-check the active SOW at each major task switch.
If scope expands, stop and update the SOW before continuing.

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
- Stage only files covered by the task.
- For code changes, commit after successful verification unless the user explicitly defers commits.
- For docs-only changes, commit only when the user or repo policy requires it.
- Never push unless the user explicitly asks.

---

## Planning Files

Planning, SOW, status, and investigation files should live under the repository's planning directory, usually `plan_todo/`.

Suggested layout:

```text
plan_todo/
  active/
  finished/
  finding/
```

When moving or renaming planning files, update markdown references in the same change.

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
