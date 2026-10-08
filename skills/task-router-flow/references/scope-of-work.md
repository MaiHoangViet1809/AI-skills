# Scope Of Work

## Definition

A Scope of Work is the approved task contract for a concrete change. It defines the implementation scope before code changes begin.

For code-changing work, do not start implementation until the active SOW is approved.

For docs, plan, or SOW-only edits, do not create a new SOW unless the request changes active implementation scope.

An optional parent plan follows [plan.md](plan.md). It owns aggregate outcomes;
each SOW owns exact implementation coverage and links its parent `G#` only when
that plan exists. Standalone SOWs need no plan or goal IDs. Preserve existing
router/project SOW requirements, exemptions, and approval gates.

For identity, placement, separate extensions, decisions and moves, use the
target project's declared contract first; otherwise follow
[Planning Bundles](planning-bundles.md). Apply it prospectively, not as migration
authority for existing records.

## Required Template

Use the repository's active SOW template. In this repo, the template is:

- **Status**: lifecycle state such as `draft`, `approved`, `in_progress`, or `done`
- **Approval**: explicit approval state such as `pending` or `approved`
- **create_dttm**: exact SOW creation datetime, for example `2026-09-11T15:42:07+07:00`
- **approve_dttm**: exact SOW approval datetime, or `null` while unapproved
- **finish_dttm**: exact SOW completion datetime, or `null` while unfinished
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
- Record every known `*_dttm` as a full ISO-8601 datetime with clock time to
  seconds and numeric timezone offset: `YYYY-MM-DDTHH:mm:ss+HH:MM`, for example
  `2026-09-11T15:42:07+07:00`. A date-only value such as `2026-09-11` is invalid.
  Set a future lifecycle event to `null`; never predict its time.
- Use `unknown` only when editing a historical SOW whose exact past event time
  cannot be established authoritatively. Do not derive it from file metadata or
  Git history.
- Before code changes begin, `Approval` must be `approved`.
- At verified SOW completion, set `Status` to a completed state such as `done`,
  even when it remains inside an active Plan.
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

## Identity And Placement

Follow [Planning Bundles](planning-bundles.md) for the default
`SOW_YYYYMMDD_RANDOM8` ID, ID-only folder and `<SOW_ID>_<task_name>.md` file.
Do not allocate sequential indices. Preserve identities of existing records.

## Lifecycle

- Create a standalone SOW bundle under the resolved active planning root;
  nest it in a Plan bundle only when it owns work under that optional Plan.
- At creation, set `create_dttm` to the current full timezone-aware datetime
  and keep `approve_dttm` and `finish_dttm` null.
- At explicit approval, set `approve_dttm`; at verified completion, set
  `finish_dttm`. Update each field only at its matching transition.
- Before writing code, confirm an approved SOW exists unless the repo explicitly exempts the task.
- If scope changes materially, update or extend the active SOW and get approval again.
- Create every new extension in its own parent-owned EXT file under the
  resolved bundle contract. Read the base plus applicable approved extensions
  in recorded order; stop on unresolved overlap. Draft extensions grant no scope.
- Every extension must contain its own `Status`, `Approval`, `create_dttm`,
  `approve_dttm`, and `finish_dttm`. Do not reuse the parent approval timestamp
  as the extension approval timestamp.
- On authorized reopen, apply the resolved parent SOW/Plan lifecycle; preserve
  prior evidence and completed sibling timestamps. A draft EXT alone does not
  reopen its parents. Record actual finish times again after renewed completion.
- A single SOW may have at most 3 approved extensions.
- If a follow-up change would become extension 4, create a replacement SOW.
- A replacement SOW should reference the prior SOW and carry forward only the still-relevant context, risks, and dependencies.
- Apply [Planning Bundles](planning-bundles.md) for standalone/aggregate moves,
  partial Plan completion, adoption and reference repair. Never detach completed
  children from an active Plan merely to place them in `finished/`.

## Branch Rule

- New code change not covered by an active SOW: draft a new SOW.
- Change to active scoped work under a plan: extend the plan first, then update the aligned SOW.
- Change to active scoped work not under a plan: extend the existing SOW only while it stays within the 3-extension limit.
- Debug request: find root cause first; apply repo SOW policy to every code fix,
  regardless of size. Reuse exact approved coverage or obtain approval for a new
  or extended SOW before code edits.
- Debug or follow-up work that would exceed the 3-extension limit: draft a new SOW and cross-reference the prior SOW.
- Docs, plan, or SOW-only request: no new SOW by default; use existing user
  authorization for the concrete edit when repo policy permits it. Material
  scope expansion still requires approval.
