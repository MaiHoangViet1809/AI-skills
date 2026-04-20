# Scope Of Work

## Definition

A Scope of Work is the approved task contract for a concrete change. It defines the implementation scope before code changes begin.

For code-changing work, do not start implementation until the active SOW is approved.

For docs, plan, or SOW-only edits, do not create a new SOW unless the request changes active implementation scope.

## Required Template

Use the repository's active SOW template. In this repo, the template is:

- **Status**: lifecycle state such as `draft`, `approved`, `in_progress`, or `done`
- **Approval**: explicit approval state such as `pending` or `approved`
- **Task**: one-sentence change
- **Location**: exact folder or file paths
- **Why**: business or technical driver
- **As-Is Diagram (ASCII)**: current behavior, architecture, or state
- **To-Be Diagram (ASCII)**: target behavior, architecture, or state
- **Deliverables**: files added or modified, exports, or concrete outputs
- **Done Criteria**: how completion is verified
- **Out-of-Scope**: what is explicitly excluded
- **Proposed-By**: agent name
- **plan**: related plan name or SOW path when relevant
- **Cautions / Risks**: likely failure modes or cautions

Rules:

- Every active SOW should show both `Status` and `Approval`.
- Before code changes begin, `Approval` must be `approved`.
- When work is finished and the SOW is moved to `finished/`, set `Status` to a completed state such as `done`.

## Indexing

Every new SOW should use a unique 4-digit index from `0001` to `9999`.

Recommended filename shape:

- `SOW_0001_short_name.md`
- `SOW_0002_short_name.md`

Choose the next available index by scanning the repository's planning area, including finished SOWs.

## Lifecycle

- Create SOW files in the repository's planning directory.
- In this repo, planning files live under `plan_todo/`.
- Before writing code, confirm an approved SOW exists unless the repo explicitly exempts the task.
- If scope changes materially, update or extend the active SOW and get approval again.
- When the work is complete, move the SOW into the repo's finished-plans location.
- In this repo, completed SOWs move to a `finished/` directory under the planning area.

## Branch Rule

- New code change not covered by an active SOW: draft a new SOW.
- Change to active scoped work under a plan: extend the plan first, then update the aligned SOW.
- Change to active scoped work not under a plan: extend the existing SOW.
- Debug request: find root cause first, then extend the SOW only if the fix becomes a substantial code change.
- Docs, plan, or SOW-only request: no new SOW by default.
