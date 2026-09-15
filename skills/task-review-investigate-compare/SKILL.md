---
name: task-review-investigate-compare
description: Use when the user wants to review a plan, SOW, request, or idea; investigate feasibility or root causes; or compare approaches. Default concrete, low-ambiguity findings back into a known existing plan or SOW unless the user explicitly requests discussion only; route material contract changes separately.
---

# Task Review Investigate Compare

Use this skill when the main job is to understand, challenge, compare, or recommend before any later human or execution handoff.

This skill is for review and decision support. It is not an execution skill.

## Use This Skill When

- the user asks to review a `plan`, `SOW`, request, or proposal
- the user wants to compare the current repo approach with an internet or external approach
- the user wants feasibility, fit, tradeoff, or impact analysis before implementation
- the user wants investigation first, with code changes only as a possible later outcome
- the user wants findings mapped back into existing planning docs without treating every update as a new approval gate
- the user wants a review-only pass that stops before implementation

## Do Not Use This Skill When

- the user already has an approved scope and wants implementation now
- the task is purely execution, validation, or repair with no real decision to make
- the request is only to route a concrete code change into a new or updated SOW

Use `task-router-flow` when the job is mainly branch selection for implementation work.

Execution belongs to a later skill or human-in-the-loop step after this review is complete.

## Project Guardrail Conformance Audit

Before choosing a review mode for a design-bearing request:

1. Read the target project's authority documents and nested rules.
2. Extract relevant invariants and prohibited designs.
3. Compare every viable option and recommendation against those rules.
4. Identify evidence that would prove the recommended direction preserves them.
5. Treat missing or conflicting authority as a decision blocker, not freedom to
   choose an implementation-convenient architecture.

For a non-design review, record that this audit is not applicable and continue
with the normal review flow. This audit is project-derived and must not impose a
domain, storage model, or ownership model of its own.

## Operating Modes

Choose one provisional mode, gather evidence, then confirm or revise the mode.
Mode selection is not a finding or verification result.

Default selection:

```text
known existing plan/SOW?
├─ no  -> Brainstorm -> gather evidence
└─ yes -> inspect artifact and relevant evidence
          -> concrete, low-ambiguity finding?
          ├─ no  -> evidence sufficient? clean conclusion : unverified conclusion
          └─ yes -> materially changes the contract?
                    ├─ yes -> Scope Change
                    └─ no  -> Review And Writeback
```

- Do not choose `Brainstorm` merely because the user says `review`.
- Treat `review again`, `double-check`, and `final review` as continuation of `Review And Writeback` when the same artifact has already been edited in the current workstream.
- Override that default only when the user explicitly requests discussion-only, no-writeback, or no file edits.

### 1. Brainstorm

Use when no target artifact is known, findings are still exploratory or ambiguous, or the user explicitly does not want file edits yet.

Output:
- clarify the real question
- surface assumptions, risks, and promising directions
- recommend next steps

Do not write files in this mode unless the user explicitly asks.

Do not use this mode solely because the request is phrased as a review.

### 2. Review And Writeback

Use when findings should update existing `plan`, `SOW`, or related docs, and the update does not materially change the implementation contract.

Examples:
- tighten wording
- add clarified findings
- record tradeoffs
- update notes, rationale, or follow-up items
- align plan text with already-established conclusions

Default rule:
- if ambiguity is low and the writeback only clarifies existing planning artifacts, update them directly
- if the review finds a concrete issue that belongs in a known planning artifact, patch it in the same turn; the user does not need to separately say `patch`
- do not stop only to ask for approval of the writeback itself

Typical writeback findings clarify already-established acceptance criteria,
persistence boundaries, consumer coverage, validation, risks and naming. Adding
new required behavior or changing acceptance thresholds is a Scope Change, even
when the edit is small. Do not treat a missing requirement as already approved.

When concept authority exists:

- treat missing, false, or stale `Concept Compliance` mapping as an actionable
  finding
- patch low-ambiguity mapping gaps directly in the existing SOW
- route material concept changes for explicit approval instead of silently
  rewriting the mapping

### 3. Scope Change

Use when findings materially change the contract and need explicit routing.

Examples:
- deliverables change
- done criteria change
- out-of-scope boundaries change
- implementation direction changes in a substantial way
- sequencing across SOWs or plans changes materially

In this mode:
- summarize the findings
- explain why this is a scope change
- hand off to `task-router-flow`

## Review Loop

```text
select provisional mode
-> normalize the question
-> gather evidence
-> confirm mode and evidence sufficiency
-> separate facts from inference
-> test adjacent scope and blast radius
-> compare viable options
-> recommend the next action
```

## Normalize The Question

Before deep investigation, restate the task in working terms:

- what is being proposed or questioned
- what problem it is trying to solve
- what constraints appear real
- what decision must be made at the end

If the question is still ambiguous after this pass, narrow the ambiguity before doing broad analysis.

## Evidence Rules

Build evidence from the right source first.

### Exact runtime-contract evidence

Before recommending or writing back a mutation to a schema, API payload,
persisted storage, connection/config contract, or other external runtime
surface:

- identify the exact runtime identity: target or path, owner or producer,
  environment or deployment lane, connection or provider, and relevant version;
- require authoritative evidence tied to that identity, such as direct read-only
  inspection or an explicitly authoritative current contract artifact;
- treat producer code, representative or synthetic fixtures, naming
  conventions, adjacent environments, and similarly named objects as
  hypotheses only;
- if exact evidence is unavailable, mark the premise unverified and do not
  write the mutation into an approved plan or SOW as fact;
- invalidate prior evidence when any runtime identity dimension changes, then
  reverify affected consumers.

Review premise truth separately from document consistency. Repeated review must
not turn a consistent assumption into evidence.

- choose an available inspection method that fits the question and produces
  sufficient repository evidence
- CodeGraph may help with symbols, callers, impact, or structure when already
  available, but never require its setup or invocation
- `rg` is useful for literal strings, config keys, logs, comments, and fuzzy
  text hunts, but it is not a universal mandatory first step
- when the reviewed behavior is UI-visible, gather rendered UI evidence when
  feasible, such as a browser smoke path, screenshot comparison, DOM/CSS
  inspection, or component-level rendered artifact
- do not claim UI quality, visual fit, or interaction completeness from source
  grep, unit tests, or build success alone
- for UI-visible output/data surfaces, verify data-present and empty-state paths
  separately when feasible
- if the real UI or runtime path cannot be checked, state that visual
  verification is incomplete and list the concrete residual UI risks
- browse official or primary internet sources when the comparison depends on current external facts, changing APIs, version behavior, specs, or recommendations

When using internet sources:
- separate verified facts from your own inference
- prefer official docs, primary sources, or canonical project documentation
- do not rely on memory for changeable facts

## Comparison Frame

When comparing approaches, cover only the dimensions that matter for the request. Typical dimensions:

- fit with the current codebase
- implementation complexity
- migration cost
- maintenance burden
- operational risk
- blast radius
- reversibility
- evidence strength and unknowns

Do not pad comparisons with generic pros and cons that do not affect the actual decision.

## Simplicity And Responsibility Gate

For code, design, SOW, and implementation reviews, apply this gate before a
clean recommendation or `ready for HITL handoff`. Skip it for purely editorial
work.

- Inspect the closest named or cheaply discoverable project baseline before
  designing a replacement. If none is available, state that evidence limit.
- Compare the requested outcome, the baseline, and the proposed responsibilities.
  Every material added mechanism must serve the authorized outcome or a concrete
  governing constraint, and the review must explain why a simpler existing
  mechanism is insufficient.
- Treat wrappers, adapters, persistence, checkpoints, orchestration, retries,
  validation passes, compatibility paths, and duplicated framework behavior as
  complexity to justify. Labels such as robustness, best practice, or future
  flexibility are not evidence of necessity.
- Evidence of a problem establishes the problem, not permission for a new
  feature or a particular solution. Keep optional improvements outside the
  effective contract until authorized.
- For implementation review, compare the actual diff with both the approved
  design and baseline. Passing tests, earlier approval, or moving code into more
  files does not justify unnecessary responsibility.
- Preserve complexity required for correctness, security, destructive-operation
  safety, data semantics, intentional config, or an explicit runtime contract.
  Line count is only a warning signal.

Unsupported material complexity is an actionable finding and blocks a clean
approval recommendation. Keep this review proportional; do not require a new
worksheet, numeric complexity budget, or exhaustive repository search.

## Output Contract

Structure the result around these sections:

- `Question`
- `Evidence`
- `Findings`
- `Options`
- `Recommendation`
- `Next action`

`Findings` should be concrete, not generic observations.

When reporting actionable findings, prefer a compact table with these columns:

| Severity | Finding | Impact | Solution |
| --- | --- | --- | --- |

Use this table for review findings, regressions, root-cause findings, architecture drift, actionable risk notes, and issue-shaped as-is vs desired gaps.

Do not force the table when:

- there are no findings
- the user asked for prose only
- the answer is a simple status or yes/no
- the content is not issue-shaped

If there are no actionable findings, say directly:

> No actionable findings found.

Use that conclusion only after sufficient inspection of the reviewed scope.
When required evidence is unavailable, report the concrete unverified premise
and next investigation step instead of implying the review is clean. Verified
findings may still be reported alongside explicitly unverified scope.

Keep each finding row concise but complete:

- `Severity`: `Critical`, `High`, `Medium`, `Low`, or `Info`
- `Finding`: the concrete issue
- `Impact`: why it matters in user, product, or technical terms
- `Solution`: the proposed fix or next investigation step

If the user asks for a plain `summary`, `summarize`, or status recap and does not ask for review findings, do not use the findings table. Use concise prose or hand off to `task-progress-report` when the request is plan/SOW progress-shaped.

`Recommendation` should say what to do, not just what was observed.

`Next action` must be one of:

- `no writeback`
- `write back to existing plan/SOW`
- `route as scope change`
- `ready for HITL handoff`

## Writeback Decision Rule

Do not treat every planning-doc change as a new approval gate.

Write back directly when all of these are true:

- the target is an existing `plan`, `SOW`, or related doc
- the update mainly records or clarifies findings
- the implementation contract is not materially changing
- ambiguity is low

A concrete finding in a known artifact is sufficient authorization for this docs-only writeback unless the user explicitly requests discussion-only or no edits.

For repeated reviews of the same artifact:

- finding found: patch it, verify the resulting document, and report the writeback
- no finding found: report `No actionable findings found.` and leave the file unchanged
- never return `no writeback` after making a qualifying writeback

Escalate to `task-router-flow` when the findings would materially change scope rather than merely document it.

### Keep Active Plans And SOWs Current

When actionable redundancy or inconsistency is found, update effective sections
in place. Check Task, diagrams, deliverables, done criteria and out-of-scope text
for superseded or conflicting instructions. Avoid append-only `Review Pass`
histories; use at most one short review summary when useful for handoff, subject
to explicit repository reporting requirements. A clean artifact needs no edit
or new summary; discussion-only requests remain read-only.

- Keep current requirements, approval gates, unresolved questions, risks and
  execution evidence visible. Resolved decisions can still govern execution;
  remove redundant discussion, not their effective requirements.
- Preserve base/extension IDs, approval states and lifecycle timestamps. A newer
  draft does not supersede an approved contract; distinguish proposed scope
  from authorized work and route material changes through the existing gate.
- Use the repository's existing decision log for historical alternatives,
  rejected choices and superseded rationale. Preserve any material rationale
  there before removing its sole SOW copy, avoid duplicate entries and repair
  affected links. If no decision-log authority exists, retain minimum necessary
  rationale locally rather than inventing a governance structure.
- Preserve decision-log chronology and leave completed historical artifacts
  alone unless their modification is explicitly in scope.

## Investigation Guardrails

- do not jump to implementation while the main job is still analysis
- do not report findings without deciding the implied next action
- do not treat internet evidence as repo fit by default; map it back to local constraints
- do not keep the task in brainstorm mode once the user clearly asked for writeback or routing
- do not ask for approval solely because a low-ambiguity planning writeback is possible
- do not execute the proposed work from this skill; stop at recommendation, writeback, or routing
- do not present a false dichotomy when an authority-compliant alternative exists; include that alternative in the comparison
- if the repository has no declared concept authority, keep concept compliance
  out of scope rather than inferring a concept catalog from incidental docs

## Closeout

End with:

- the mode used
- the recommendation
- the chosen next action

If writeback occurred, summarize what was updated.

If a scope change is required, hand off cleanly to `task-router-flow`.

If the review concludes the work should proceed, stop at `ready for HITL handoff` rather than executing from this skill.
