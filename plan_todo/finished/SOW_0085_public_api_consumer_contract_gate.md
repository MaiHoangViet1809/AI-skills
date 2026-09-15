# SOW_0085 — Public API Consumer Contract Gate

## Lifecycle

- Status: completed
- Approval: approved by explicit user skill-evolution request
- create_dttm: `2026-09-16T02:55:36+07:00`
- approve_dttm: `2026-09-16T02:55:36+07:00`
- finish_dttm: `2026-09-16T02:59:19+07:00`

## Task

Prevent planning review and execution from substituting a task-specific public
entrypoint when the user requested a generic consumer API.

## Why

A dashboard lifecycle implementation had a generic lower-level deletion engine,
but its public entrypoint was delivered as `delete_mvp1(...)`. The user had
requested a generic caller surface shaped like
`delete_dashboard(name=..., label=..., url=...)`. Repeated contract review and
runtime verification proved internal safety while missing the caller-visible
abstraction mismatch.

## Feedback Contract

- Target skills: `task-review-investigate-compare`, `task-execution-flow`
- Trigger: a request or SOW creates or changes a public API, CLI, UI action, SDK,
  or other consumer entrypoint
- Observed behavior: internal mechanics and tests pass while the public surface
  narrows a generic requirement to one named product or workflow
- Expected behavior: reconstruct the requested consumer call, preserve its
  abstraction level and identifier meaning, and verify the real public surface
- Reusable invariant: a generic core does not make a task-specific entrypoint a
  generic API; caller-visible contract fit is independent from internal
  correctness
- Cause class: incomplete review and execution decision procedure
- Evidence reference: `sanitized:user-feedback-generic-dashboard-delete-2026-09-16`

## As-Is Diagram (ASCII)

```text
generic user call -> task-specific SOW/API -> internally correct tests -> wrong UX
```

## To-Be Diagram (ASCII)

```text
latest user call shape
  -> abstraction + identifiers + arguments + result
  -> SOW/public API comparison
  -> implementation through that public surface
  -> consumer-shaped verification
```

## Location

- `skills/task-review-investigate-compare/SKILL.md`
- `skills/task-execution-flow/SKILL.md`
- `tests/skill_feedback_cases/task-review-investigate-compare.json`
- `tests/skill_feedback_cases/task-execution-flow.json`
- this SOW, later
  `plan_todo/finished/SOW_0085_public_api_consumer_contract_gate.md`
- Post-commit deployment: the two matching directories under
  `~/.codex/skills/`, one exact skill sync at a time

## Deliverables

1. Add a proportional consumer-contract gate to public-surface reviews.
2. Treat an explicit user invocation example as acceptance evidence unless the
   user marks it illustrative.
3. Check abstraction level, identifier semantics, parameters, result and the
   ownership layer exposed to callers.
4. Reject a product-specific convenience function as satisfaction of a generic
   operation merely because it calls generic internals.
5. During execution, compare the latest explicit caller contract with the SOW
   before editing. Stop and reopen scope when they differ, even if the stale SOW
   was previously approved.
6. Verify changed behavior through the public entrypoint. A genericity claim
   must include evidence that identity is caller-supplied rather than fixed to
   the first implementation case.
7. Add sanitized expected, negative and boundary regression scenarios to both
   skill fixtures.
8. Keep skill descriptions and `agents/openai.yaml` unchanged because trigger
   scope does not change.

## Done Criteria

- Review cannot approve a generic public capability whose proposed caller API
  is hardcoded to one product identity.
- Execution stops when the approved SOW conflicts with a later explicit
  user-facing call contract.
- Internal genericity is not accepted as proof of public genericity.
- Purely internal changes and explicitly product-specific APIs do not incur an
  irrelevant generic-surface requirement.
- Structural validators and feedback/sync unit tests pass.
- Installed Codex copies are synced only after the canonical commit and exact
  parity is verified.

## Out-of-Scope

- Fixing the dashboard project implementation or its SOW.
- Prescribing one universal API naming convention.
- Requiring public API examples for internal-only changes.
- Editing `task-router-flow`, adding new scripts or changing skill metadata.
- Pushing the canonical commit.

## Proposed-By

Codex, from explicit user feedback on 2026-09-16.

## Plan / Reference

- `skill-evolution-flow`
- `skill-creator`
- SOW_0084 anti-overengineering gate

## Cautions / Risks

- Do not turn one dashboard example into a universal `name` parameter rule.
- The gate checks caller-visible intent; project authority still decides the
  concrete API design and destructive-operation safeguards.
- Preserve unrelated pending `task-router-flow` work in the dirty tree.

## Verification Evidence

- Both canonical skills passed the `skill-creator` structural validator.
- `uv run python -m unittest tests.test_skill_feedback_cases
  tests.test_skill_sync_scripts` passed 13 tests.
- Expected, negative and boundary fixtures were manually checked against the
  new gates. Isolated model forward-testing was unavailable because subagents
  are prohibited in this side conversation.
