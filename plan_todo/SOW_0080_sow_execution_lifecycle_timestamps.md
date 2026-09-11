# SOW_0080 — SOW Execution Lifecycle Timestamps

## Lifecycle

- Status: in_progress
- Approval: approved by user
- create_dttm: `2026-09-11T15:30:19+07:00`
- approve_dttm: `2026-09-11T15:30:19+07:00`
- finish_dttm: `null`

## Task

Make execution update the lifecycle timestamps already defined by the active
SOW contract, including the currently executed extension.

## Location

- `skills/task-execution-flow/SKILL.md`
- `tests/skill_feedback_cases/task-execution-flow.json`
- `plan_todo/SOW_0080_sow_execution_lifecycle_timestamps.md`

## Why

The router can create correct lifecycle fields, but execution owns the actual
start and finish transitions. Moving a completed SOW without setting its
timestamp leaves the template contract incomplete.

## As-Is Diagram (ASCII)

```text
approved SOW -> execute -> verify -> move finished
                                  `-> finish_dttm may remain null
```

## To-Be Diagram (ASCII)

```text
approved SOW/extension -> execute -> verify
  -> set matching finish_dttm at completion
  -> set top-level finish_dttm when whole SOW is complete
  -> move finished
```

## Deliverables

- Validate required lifecycle fields before implementation.
- Set the active extension's finish timestamp independently.
- Set top-level finish only when the whole SOW is complete.
- Never fabricate timestamps or add approval evidence/transcript fields.

## Done Criteria

- Execution rules cover base SOW, active extension, incomplete verification,
  and historical unknown timestamps.
- Expected, negative, and boundary regression scenarios are recorded.
- Structural validation and feedback/sync tests pass.
- Exact Codex skill sync and parity pass.

## Out-of-Scope

- Redefining the SOW template owned by `task-router-flow`.
- Backfilling untouched historical SOWs.
- Adding lifecycle parsers, schemas, wrappers, or telemetry.

## Proposed-By

Codex, from explicit user feedback on 2026-09-11.

## Plan / Reference

- `skill-evolution-flow`
- `SOW_0079_sow_lifecycle_timestamps`
- Feedback case `sow-execution-lifecycle-timestamps-001`

## Cautions / Risks

- Do not set `finish_dttm` before verification and gap-finding complete.
- An unfinished extension keeps the top-level SOW unfinished.
- Preserve authoritative historical timestamps; use `unknown` rather than
  guessing missing past values.
