# SOW_0079 — SOW Lifecycle Timestamps

## Lifecycle

- Status: in_progress
- Approval: approved by user
- create_dttm: `2026-09-11T15:25:56+07:00`
- approve_dttm: `2026-09-11T15:25:56+07:00`
- finish_dttm: `null`

## Task

Require concise lifecycle metadata for every SOW and each extension without
storing approval transcripts or redundant approval evidence.

## Location

- `skills/task-router-flow/SKILL.md`
- `skills/task-router-flow/references/scope-of-work.md`
- `skills/task-router-flow/references/routing-notes.md`
- `tests/skill_feedback_cases/task-router-flow.json`
- `plan_todo/SOW_0079_sow_lifecycle_timestamps.md`

## Why

Current SOWs record approval inconsistently and do not reliably distinguish
creation, approval, and completion times. Redundant approval evidence adds noise
without improving authority.

## As-Is Diagram (ASCII)

```text
Status + Approval + optional prose evidence
  -> creation/approval/finish times may be missing
  -> extensions may have no independent lifecycle
```

## To-Be Diagram (ASCII)

```text
SOW lifecycle                 each Extension lifecycle
  create_dttm                   create_dttm
  approve_dttm                  approve_dttm
  finish_dttm                   finish_dttm
  concise Approval marker       concise Approval marker
```

## Deliverables

- Define the three timestamp fields as ISO-8601 datetimes with timezone.
- Use `null` until approval or completion occurs; use `unknown` only for
  historical events whose exact time cannot be established.
- Give every extension its own Status, Approval, and three timestamps.
- Keep approval concise: state and approver when known; never add transcript,
  quoted chat, message ID, or `Approval-Evidence` field.
- Update timestamps at the actual lifecycle transition, not prospectively.

## Done Criteria

- The canonical template covers new SOWs, extensions, reopen, and finish cases.
- Expected, negative, and boundary feedback scenarios are recorded.
- `task-router-flow` passes structural validation and feedback/sync tests.
- Canonical and installed Codex copies match after exact single-skill sync.

## Out-of-Scope

- Backfilling untouched historical SOWs.
- Changing approval authority or treating a request as approval when repository
  policy requires a separate gate.
- Adding an approval evidence field, event ledger, parser, schema, or wrapper.
- Modifying `task-execution-flow`; the SOW contract remains the single lifecycle
  authority consumed by downstream execution.

## Proposed-By

Codex, from explicit user feedback on 2026-09-11.

## Plan / Reference

- `skill-evolution-flow`
- Feedback case `sow-lifecycle-timestamps-001`

## Cautions / Risks

- Date-only values are insufficient; timestamps must include timezone.
- Do not fabricate historical times from file metadata or Git history.
- Reopening a finished SOW clears only its top-level `finish_dttm`; completed
  extension timestamps remain immutable.
