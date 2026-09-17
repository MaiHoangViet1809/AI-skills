# SOW_0087 — End-to-End Outcome Trace in Review Flow

## Lifecycle

- Status: done
- Approval: approved by user
- create_dttm: `2026-09-17T14:20:50+07:00`
- approve_dttm: `2026-09-17T15:04:01+07:00`
- finish_dttm: `2026-09-17T15:05:37+07:00`
- Proposed-By: Codex GPT-6
- plan: Standalone; follows [SOW_0086](finished/SOW_0086_skill_evolution_failure_diagnosis.md).

## Task

Add one compact review gate that traces selection or eligibility behavior from
the authoritative source through state/reconciliation to the final consumer,
and add a sanitized regression case for the missed downstream re-entry path.

## Why

The prior monitor SOW correctly changed the source inventory filter but did not
trace persisted outstanding state and the publisher. An excluded item could
therefore re-enter the final card even though the source filter passed. The
review skill needs to validate the stated outcome at every relevant boundary,
not only the first selector.

This is a review-procedure correction, not a runtime fix and not a reason to
expand every review into a full system audit.

## Evidence

- Sanitized evidence reference: `de-project-monitor-eligibility-reentry-2026-09-17`.
- DE-project `SOW_0270_ignore_unscheduled_dags_in_incident_monitor.md` scoped the
  change to the source inventory selector.
- DE-project `cores_rebuild/monitoring/teams_incident.py` then combines active
  inventory with persisted outstanding runs and publishes working runs; this is
  the downstream re-entry path the review missed.

## Location

- `skills/task-review-investigate-compare/SKILL.md`
- `tests/skill_feedback_cases/task-review-investigate-compare.json`
- This SOW only; no router, meta-skill, registry, metadata, or installed-copy changes.

## As-Is Diagram (ASCII)

```text
review SOW / implementation
  -> inspect named selector or filter
  -> check local acceptance criteria
  -> recommend approval or writeback
```

```text
selector excludes item
  -X-> source inventory
       ... downstream state/reconciliation/publisher not necessarily traced
       -> excluded item may still appear in final output
```

## To-Be Diagram (ASCII)

```text
review stated include/exclude outcome
  -> authoritative source/selector
  -> transforms, unions, retry/reconciliation, persisted or recovered state
  -> final consumer/publisher/UI
  -> compare included + excluded paths
  -> finding or verified outcome; route material scope change
```

```text
selector excludes item
  -> trace every applicable downstream re-entry path
  -> final output honors eligibility, or review reports the exact gap
```

## Deliverables

1. Add a conditional `Outcome Path Gate` to `task-review-investigate-compare`:
   - use it when the requested behavior includes/excludes, filters, selects, or
     exposes entities or states;
   - trace the authoritative selector to the final consumer, including
   persistence, recovery, retries, unions, and reconciliation when present;
   - require the SOW's Done Criteria to cover the path that can affect the
     stated outcome; a source-only pass is insufficient when downstream state
     can reintroduce an excluded item;
   - if the authoritative selector or final consumer/state path cannot be
     identified, mark the outcome `unverified` and do not recommend clean
     approval; do not invent the missing path;
   - remain proportional and mark the gate not applicable when no downstream
     state or consumer exists.
2. Add `outcome-path-trace-001` to the existing fixture with expected,
   negative, and boundary scenarios.
3. Keep the skill concise; do not add a new helper, checklist artifact,
   telemetry, persistence, or orchestration layer.

## Done Criteria

1. The skill names the source-to-consumer trace at the review decision point,
   including a negative check for already-persisted excluded items.
2. The fixture covers: downstream re-entry is found; a local filter with no
   state/consumer does not trigger unnecessary audit; and ambiguous historical
   visibility is surfaced instead of inferred.
3. Skill-creator structural validation, the existing feedback/sync unittest
   suite, and `git diff --check` pass.
4. Review the final wording for KISS/DRY: no duplicate generic SOW policy, no
   domain-specific monitor rule, and no change to runtime behavior.
5. Structural checks and fixture walkthrough are reported separately from
   actual model-behavior verification.
6. A review with an unidentified selector or final consumer/state path cannot
   conclude clean solely from a partial source trace.

## Out-of-Scope

- Any DE-project runtime, monitor, SOW, DAG, deployment, or production change.
- Changes to `task-router-flow` or `skill-evolution-flow`; neither is the
  evidenced owner of this missed end-to-end review step.
- Changes to registry/index/UI metadata or installed skill copies.
- A mandatory full-system audit for unrelated reviews.
- New telemetry, checkpoints, state stores, wrappers, or compatibility layers.
- Commit, push, or environment sync before explicit approval and validation.

## Cautions / Risks

- The gate must remain conditional; otherwise small local reviews become noisy.
- “Final consumer” must be interpreted from the reviewed behavior, not guessed
  from adjacent code.
- Historical visibility may intentionally differ from current eligibility;
  preserve that distinction and route unresolved semantics rather than choosing.
- The regression fixture proves instruction shape, not that a model will always
  discover every downstream path.

## Decision Log

- Decision D001 — 2026-09-17 — approved by user: patch only
  `task-review-investigate-compare` because the concrete failure is an
  incomplete review procedure, not a routing or evolution-entry failure.

## Implementation and Verification

- Added the conditional `Outcome Path Gate` to the canonical review skill.
- Added fixture case `outcome-path-trace-001` with expected, negative, and
  boundary scenarios.
- Structural validator: PASS.
- Feedback and sync unittest suite: 13 tests PASS.
- JSON parse and `git diff --check`: PASS.
- Two post-implementation review passes confirmed scope ownership, causal
  coverage, and negative-path behavior.
- Model behavior and installed-copy deployment remain unverified; no installed
  environment was selected for sync.
