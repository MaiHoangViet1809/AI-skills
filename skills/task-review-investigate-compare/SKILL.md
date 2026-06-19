---
name: task-review-investigate-compare
description: Use when the user wants to review a plan, SOW, request, or idea; investigate feasibility or root causes in the codebase or from internet sources; or compare implementation approaches before deciding whether to write back to planning docs, route to SOW changes, or hand off for later human-in-the-loop or execution follow-up.
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

## Operating Modes

Choose exactly one mode before gathering evidence.

### 1. Brainstorm

Use when the user is exploring and does not want file edits yet.

Output:
- clarify the real question
- surface assumptions, risks, and promising directions
- recommend next steps

Do not write files in this mode unless the user explicitly asks.

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
- do not stop only to ask for approval of the writeback itself

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
classify mode
-> normalize the question
-> gather evidence
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

- use `code-context-search-policy` for codebase investigation
- use `codegraph` first for symbols, callers, callees, impact, and structure questions
- use `rg` first for literal strings, config keys, logs, comments, and fuzzy text hunts
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

Keep each finding row concise but complete:

- `Severity`: `Critical`, `High`, `Medium`, `Low`, or `Info`
- `Finding`: the concrete issue
- `Impact`: why it matters in user, product, or technical terms
- `Solution`: the proposed fix or next investigation step

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

Escalate to `task-router-flow` when the findings would materially change scope rather than merely document it.

## Investigation Guardrails

- do not jump to implementation while the main job is still analysis
- do not report findings without deciding the implied next action
- do not treat internet evidence as repo fit by default; map it back to local constraints
- do not keep the task in brainstorm mode once the user clearly asked for writeback or routing
- do not ask for approval solely because a low-ambiguity planning writeback is possible
- do not execute the proposed work from this skill; stop at recommendation, writeback, or routing

## Closeout

End with:

- the mode used
- the recommendation
- the chosen next action

If writeback occurred, summarize what was updated.

If a scope change is required, hand off cleanly to `task-router-flow`.

If the review concludes the work should proceed, stop at `ready for HITL handoff` rather than executing from this skill.
