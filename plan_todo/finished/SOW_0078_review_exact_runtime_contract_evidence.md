# SOW_0078 — Require Exact Runtime-Contract Evidence In Reviews

## Status

COMPLETE

## Approval

Approved-By: User, 2026-08-14, through explicit direction to persist the
correction in memory, project instructions, and the review skill.

## Task

Prevent review writeback from converting proxy or representative evidence into
facts about an exact runtime contract.

## Location

- `skills/task-review-investigate-compare/SKILL.md`
- `tests/skill_feedback_cases/task-review-investigate-compare.json`
- `plan_todo/SOW_0078_review_exact_runtime_contract_evidence.md`

## Why

A review changed production SQL column references from snake_case to camelCase
using producer code and a representative schema, without inspecting the exact
table through its deployed connection. Repeated reviews then checked internal
consistency instead of revalidating the premise.

## As-Is Diagram (ASCII)

```text
proxy evidence -> inferred contract -> SOW states fact -> mutation approved
```

## To-Be Diagram (ASCII)

```text
proposed contract mutation
          |
          v
exact object + exact environment evidence available?
       | yes                         | no
       v                             v
verify premise                 mark unverified
then review mutation           block/write no fact
```

## Deliverables

- Require evidence tied to the exact runtime object and environment before a
  review recommends or writes back schema, API, storage, connection, or other
  external-contract mutations.
- Explicitly reject producer code, synthetic fixtures, representative schemas,
  adjacent environments, and naming conventions as substitutes.
- Invalidate earlier evidence when producer ownership, target path, connection,
  environment, or deployment lane changes.
- Add expected, negative, and boundary regression scenarios.
- Preserve the unrelated existing summary-format skill edit.

## Done Criteria

- Canonical skill passes structural validation.
- Feedback-case and skill-sync unit tests pass.
- Canonical and installed Codex copies match after exact-skill sync.
- No unrelated AISkills working-tree changes are staged or committed.

## Out-of-Scope

- Adding domain-specific data-engineering rules to a generic review skill.
- Rewriting other review modes or existing summary behavior.
- Changing DE-project production code or SQL.

## Proposed-By

Codex, from explicit user feedback on 2026-08-14.

## Plan / Reference

- `skill-evolution-flow`
- Feedback case `exact-runtime-contract-evidence-001`

## Cautions / Risks

- Do not require live production access when an exact authoritative contract
  artifact is provided; require identity and authority, not one specific tool.
- Do not block purely local refactors that do not change an external contract.
- Do not commit pre-existing unrelated edits in the same skill file.

## Verification Evidence

- Feedback fixture JSON parsed successfully.
- Canonical skill passed `quick_validate.py`.
- `tests.test_skill_feedback_cases` and `tests.test_skill_sync_scripts`: 12
  tests passed.
- Exact-skill Codex sync and installed-copy parity are recorded in the commit
  closeout.
