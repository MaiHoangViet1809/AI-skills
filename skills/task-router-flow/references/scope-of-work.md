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

Apply [Planning Artifact Writing](../SKILL.md#planning-artifact-writing),
including when the project supplies its own template.

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
- **Progress**: owned items, current states, evidence or pending reasons, and
  next action/owner under the HITL Progress Gate below.
- **progress_updated_dttm**: actual last progress change, with seconds and offset.

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

## HITL Progress Gate

Use the target project's declared progress contract first; this is the default.
Before every turn-ending HITL handoff (approval, clarification, scope decision,
human blocker, review verdict or final acceptance), reconcile the owning
SOW/EXT and optional Plan, persist changed progress and read back the result.
This includes draft/pending records; progress never grants approval.

New records include this section; initialize touched active records lazily.
Do not rewrite finished history, require a Plan, or create a SOW for an exempt
task. Use its existing authorized work record; without one, report briefly in
chat. Base SOW owns base rows; each EXT owns delta rows. Parent/Plan aggregates
link evidence, not copied child lists. Draft EXT progress does not amend base
scope or reopen completed parents.

```md
## Progress
- progress_updated_dttm: <YYYY-MM-DDTHH:mm:ss+HH:MM>

| Item | Status | Evidence / Pending reason | Next action / Owner |
| --- | --- | --- | --- |
| T1: <deliverable/check> | PENDING | <actual reason> | <action / owner> |
```

- Reuse an existing deliverable/check ID or assign a unique document-local
  stable key in Item once. Never renumber on reorder or reuse keys. Retain DONE
  rows in the file; the chat report may show only open items.
- PENDING: not started; IN_PROGRESS: active work; AWAITING_VERIFICATION:
  implementation exists but required verification remains; DONE: that item's
  required criteria verified with evidence. A DONE item does not complete its
  SOW/Plan. Each non-done row needs an actual reason and next action/owner.
- BLOCKED: external/dependency impediment; WAITING_HITL: required human input
  or decision. If both apply, use WAITING_HITL and explain both. User-requested
  pause uses WAITING_HITL, reason user-paused, next action user resume; stop the
  affected work without repeated prompts or silent resume. No new lifecycle state.
- Item states do not replace lifecycle Status, approval or completion gates.
  Review may be DONE while implementation awaits approval. Never infer approval
  or completion from silence, percentages or an unverified delegate assertion.
- On resume, reread the owning record and approval. Coordinator owns key
  allocation and final writeback; delegates return item-level evidence for
  coordinator verification, not acceptance or parent-row writes.
- Immediately before writing, reread; match stable row key and expected prior
  content. Patch only owned rows, preserving unrelated edits. If a row changed,
  reconcile from current evidence; unresolved ownership/conflicts abort the write.
  Read back saved rows before claiming persistence. This is bounded conflict
  detection, not atomic writes or a new locking system.
- Unsafe/unwritable/conflicting writeback: report UNSAVED plus reason and next
  action; never claim the gate passed. UNSAVED is a persistence outcome, not an
  item state; keep truthful work states. Missing contract leaves dependent
  tracking unverified; do not invent a contract, auto-install or block unrelated
  exempt work. Resolve this contract through the harness/project authority.
- If reconciliation/readback confirms progress, evidence and requested human
  action are already current, no-op passes the gate. Change progress_updated_dttm
  only when persisted progress changes; use full seconds and numeric offset.
- Optional Plan reuses SOW Sequence and Acceptance per [plan.md](plan.md);
  update affected aggregate rows, pending reason/next action and its timestamp.
- Before the existing completion move, save final progress; read the destination
  after moving. Preserve approval and bundle lifecycle gates.
- File writeback is mandatory at HITL; invoking task-progress-report is separate:
  retain one default report at final closeout, not per tool call or handoff.
  Briefly state changed status, pending reason and required human decision.
  Do not invent percentages or derive completion from progress-row counts;
  chat percentages need a declared evidence-based denominator, otherwise N/A.

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
