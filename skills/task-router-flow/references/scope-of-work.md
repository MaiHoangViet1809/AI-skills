# Scope Of Work

## Definition

A Scope of Work is the approved task contract for a concrete change. It defines the implementation scope before code changes begin.

For code-changing work, do not start implementation until the active SOW is approved.

For docs, plan, or SOW-only edits, do not create a new SOW unless the request changes active implementation scope.

## Required Template

Use the repository's active SOW template. In this repo, the template is:

- **Status**: lifecycle state such as `draft`, `approved`, `in_progress`, or `done`
- **Approval**: explicit approval state such as `pending` or `approved`
- **create_dttm**: exact SOW creation time
- **approve_dttm**: exact SOW approval time, or `null` while unapproved
- **finish_dttm**: exact SOW completion time, or `null` while unfinished
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
- Keep `Approval` short: record the state and approver when known. Do not add
  approval transcripts, quoted chat, message IDs, or an `Approval-Evidence`
  field.
- Record `create_dttm`, `approve_dttm`, and `finish_dttm` as ISO-8601 datetimes
  with timezone. Set a future lifecycle event to `null`; never predict its time.
- Use `unknown` only when editing a historical SOW whose exact past event time
  cannot be established authoritatively. Do not derive it from file metadata or
  Git history.
- Before code changes begin, `Approval` must be `approved`.
- When work is finished and the SOW is moved to `finished/`, set `Status` to a completed state such as `done`.
- When a plan document reaches its terminal completed state and is moved to `finished/`, make that completed state explicit in the plan file.
- If the target repository declares concept authority, add `Concept Compliance`
  to the SOW before approval.

## Conditional Concept Compliance

Activate this section only when the target repository declares concept
authority through `AGENTS.md` Project Overrides or an equivalent
repository-documented canonical concept index.

Required section:

```md
## Concept Compliance

- Applicable Concepts: <stable IDs or authority paths, or None with rationale>
- Concept Change: No | Yes
- Required Concept Updates: <None or exact concept IDs/files and intended change>
```

Rules:

- `Applicable Concepts: None` is allowed only with a concrete task-specific
  rationale after concept authority has already been detected.
- Use stable IDs or exact authority paths, not paraphrases of the concept.
- If implementation changes a concept, declare `Concept Change: Yes` before
  approval and keep the concept update in the same SOW.
- If no concept authority exists, omit `Concept Compliance` entirely.

## Indexing

Every new SOW should use a unique 4-digit index from `0001` to `9999`.

Recommended filename shape:

- `SOW_0001_short_name.md`
- `SOW_0002_short_name.md`

Choose the next available index by scanning the repository's planning area, including finished SOWs.

## Lifecycle

- Create SOW files in the repository's planning directory.
- In this repo, planning files live under `plan_todo/`.
- At creation, set `create_dttm` to the current timezone-aware datetime and keep
  `approve_dttm` and `finish_dttm` null.
- At explicit approval, set `approve_dttm`; at verified completion, set
  `finish_dttm`. Update each field only at its matching transition.
- Before writing code, confirm an approved SOW exists unless the repo explicitly exempts the task.
- If scope changes materially, update or extend the active SOW and get approval again.
- Every extension must contain its own `Status`, `Approval`, `create_dttm`,
  `approve_dttm`, and `finish_dttm`. Do not reuse the parent approval timestamp
  as the extension approval timestamp.
- When an extension reopens a completed SOW, return the top-level status to an
  active state and clear its top-level `finish_dttm` to `null`. Do not rewrite
  completed extension timestamps. Set the new top-level `finish_dttm` when the
  whole SOW is complete again.
- A single SOW may have at most 3 approved extensions.
- If a follow-up change would become extension 4, create a new SOW instead of adding another extension block.
- A replacement SOW should reference the prior SOW and carry forward only the still-relevant context, risks, and dependencies.
- When the work is complete, move the SOW into the repo's finished-plans location.
- In this repo, completed SOWs move to a `finished/` directory under the planning area.
- If a plan document becomes complete and no longer has active scoped work under it, move that completed plan into the same `finished/` directory under the planning area.
- Do not leave a completed plan in the active planning area once its owned work is complete.

## Branch Rule

- New code change not covered by an active SOW: draft a new SOW.
- Change to active scoped work under a plan: extend the plan first, then update the aligned SOW.
- Change to active scoped work not under a plan: extend the existing SOW only while it stays within the 3-extension limit.
- Debug request: find root cause first, then extend the SOW only if the fix becomes a substantial code change.
- Debug or follow-up work that would exceed the 3-extension limit: draft a new SOW and cross-reference the prior SOW.
- Docs, plan, or SOW-only request: no new SOW by default.
