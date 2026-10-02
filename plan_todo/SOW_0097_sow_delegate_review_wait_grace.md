# SOW_0097 - Bounded Wait Before Cutting A Running Review Delegate

## Lifecycle

- **Status**: COMPLETED
- **Approval**: Approved-By: user in current task thread
- **create_dttm**: `2026-10-03T03:23:19+07:00`
- **approve_dttm**: `2026-10-03T03:26:15+07:00`
- **finish_dttm**: `2026-10-03T03:28:07+07:00`
- **Proposed-By**: Codex
- **plan**: Standalone skill-evolution correction for `sow-delegate-flow`

## Task

Update `sow-delegate-flow` so a running review or independent-review
sub-agent is never cut immediately; the coordinator waits at most ten minutes
for a real terminal decision before deciding whether to stop it.

## Why

The current lifecycle says to clean up a native child at terminal, idle, or
errored state, but does not distinguish a still-running review delegate from a
completed child that is safe to interrupt. A review can therefore be stopped
before it returns findings. The correction must protect review evidence without
creating an unbounded wait or changing implementation-delegate cleanup.

## Governing Rules And Baseline

- `AGENTS.md` requires behavior-bearing skill edits to be covered by an
  approved SOW, preserve unrelated dirty work, and validate at the claimed
  layer.
- `skills/skill-evolution-flow/SKILL.md` requires canonical AISkills ownership,
  sanitized regression evidence, and canonical-first edits; installed copies
  are deployment targets only.
- `sow-delegate-flow` already owns delegate lifecycle, native cleanup, fresh
  non-native sessions, bounded prompts, and coordinator verification.
- `SOW_0096_task_execution_delegate_preference` established the current
  automatic-delegation composition boundary but does not define a bounded wait
  for an active review child.
- The canonical and installed `sow-delegate-flow` copies currently match;
  this is a source behavior gap, not deployment drift.

## Location

- `skills/sow-delegate-flow/SKILL.md`
- `tests/skill_feedback_cases/sow-delegate-flow.json`
- `plan_todo/SOW_0097_sow_delegate_review_wait_grace.md`

No installed skill copy, provider session, model catalog, project code,
delegated task, or unrelated fixture is in scope. Syncing the corrected skill
to an installed environment is a separate explicit action.

## Plan / Reference

- `skills/skill-evolution-flow/SKILL.md`
- `skills/sow-delegate-flow/SKILL.md`
- `plan_todo/finished/SOW_0096_task_execution_delegate_preference.md`
- `tests/skill_feedback_cases/sow-delegate-flow.json`

## As-Is Diagram (ASCII)

```text
review delegate starts
        |
        +--> coordinator sees idle/active lifecycle state
        |
        +--> cleanup rule may interrupt before findings arrive
        `--> review evidence can be lost
```

## To-Be Diagram (ASCII)

```text
review / independent-review delegate
        |
        +--> terminal or errored; final status/output is inspected
        |       `--> inspect result -> cleanup safely
        |
        +--> running or idle without a final result
                `--> wait in bounded increments, max 10 minutes
                        |
                        +--> completes / asks / fails -> handle decision
                        `--> still running or unresolved-idle after 10 minutes
                                `--> report timeout and explicitly decide
                                    whether to cut; never cut silently
```

## Behavior Contract

1. The rule applies to read-only review and independent-review delegates,
   including a review delegated through the native lifecycle or an approved
   external transport.
2. While such a delegate is genuinely `running`, the coordinator MUST NOT call
   `interrupt_agent` or terminate its task-owned external process immediately.
3. The coordinator may wait in bounded increments, up to ten minutes total,
   and should stop waiting earlier when the delegate completes, asks a
   question, fails, or reaches another real decision point.
4. When the ten-minute bound expires and the delegate is still running or
   idle without a final result, the coordinator MUST report the unchanged
   state and make an explicit cut/keep decision. If it cuts, the closeout
   records that the wait bound was reached; it must not present the review as
   completed.
5. A delegate already in a terminal or errored state may be cleaned up after
   its final output/status has been read. The rule does not require an
   unnecessary ten-minute delay for a completed result.
6. An `idle` status without a readable final result is not completion; it
   follows the same bounded wait and explicit-cut path as a still-running
   review. An idle delegate with a confirmed final result may be cleaned up.
7. Implementation delegates keep their existing approved-SOW lifecycle and
   repair/cleanup rules; this change does not turn implementation work into an
   open-ended wait.
8. The coordinator remains responsible for synthesis, verification, scope,
   and closeout. Waiting does not transfer ownership or authorize scope drift.

## Deliverables

1. Add the review-delegate wait/cut decision rule to the canonical
   `sow-delegate-flow` lifecycle and termination sections.
2. Add one sanitized feedback fixture with `expected`, `negative`, and
   `boundary` scenarios:
   - active review waits instead of being cut immediately;
   - terminal/completed review is cleaned up without an artificial delay;
   - a review still running or idle without a final result after ten minutes
     requires an explicit cut decision and is not reported as completed.
3. Validate the canonical skill structure and the existing feedback/sync test
   suite without changing installed copies.

## Done Criteria

1. The canonical skill clearly distinguishes running or unresolved-idle review
   delegates from terminal/errored delegates with a readable final result.
2. A running or unresolved-idle review delegate has a maximum ten-minute wait
   before any cut decision; no rule silently interrupts it earlier.
3. The ten-minute expiry path reports the review as incomplete/unverified and
   records the cut decision when one is made.
4. Implementation-delegate cleanup and explicit user/model/transport rules are
   unchanged.
5. The feedback fixture has unique metadata and exactly one expected, one
   negative, and one boundary scenario for this correction.
6. The skill structural validator, feedback-case tests, JSON parsing, and
   `git diff --check` pass.
7. No installed copy is edited or synced as part of this SOW.

## Out Of Scope

- Changing model selection, provider transport, session isolation, or
  `fork_turns` rules.
- Changing implementation delegation approval, repair limits, or verification
  gates.
- Killing remote Spark, Airflow, or business jobs as part of waiting for a
  review delegate.
- Adding a persistent wait-state store, telemetry, polling service, or new
  orchestration mechanism.
- Syncing or committing to any installed agent environment without a separate
  explicit authorization.

## Concept Compliance

- Applicable Concepts: None. AISkills has no declared project concept catalog;
  this SOW follows the repository's `AGENTS.md` and `skill-evolution-flow`
  ownership/validation rules.
- Concept Change: No
- Required Concept Updates: None

## Cautions / Risks

- Ten minutes is a bounded maximum, not a promise that the delegate will
  finish. A post-timeout cut can lose unfinished review findings and must be
  reported as unverified.
- An `idle` status must not be treated as completed without reading the
  delegate's final status/result; lifecycle status alone is insufficient.
- A running external process may have a transport-specific cleanup operation;
  terminate only the task-owned process after the explicit cut decision.
- Fixture assertions validate the written procedure, not provider scheduling
  or real-time sub-agent behavior.

## Decision Log

- Approved decision: protect running/unresolved-idle review delegates with a
  bounded ten-minute wait before any cut decision; terminal results may be
  cleaned up immediately. Implementation delegates retain their existing
  lifecycle. Approver: user, 2026-10-03.

## Implementation Verification

- Canonical skill validator: PASS.
- `uv run python -m json.tool tests/skill_feedback_cases/sow-delegate-flow.json`:
  PASS.
- `uv run python -m unittest tests.test_skill_feedback_cases
  tests.test_skill_sync_scripts`: 13 tests PASS.
- Scoped `git diff --check`: PASS.
- No installed skill copy was edited or synced.
- Forward behavior on a live review sub-agent is not exercised by repository
  tests; the written lifecycle and expected/negative/boundary fixture are the
  deterministic evidence.
