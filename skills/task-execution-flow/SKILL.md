---
name: task-execution-flow
description: Use when task scope is already approved or otherwise clear and you need the repo's execution discipline for carrying work from context gathering through mandatory available-GLM-5.3-max delegation, repair loops, implementation verification, gap-finding, and closeout.
---

# Task Execution Flow

Use this skill after routing is already done.

This skill is for execution discipline, implementation verification, and closeout state.
It is not for deciding the task branch and not for reporting progress format.

## Use This Skill When

- an approved SOW already exists
- a docs-only scope is clearly allowed
- the branch is already clear and the remaining question is how to execute well

If branch or scope is still unclear, use `task-router-flow` first.

For plan-backed work, use the project's declared contract first; otherwise
locate `task-router-flow` via the harness's supplied skill location/catalog and
read `references/plan.md`, or use a supplied authoritative contract. Missing
contract leaves dependent plan handling unverified; do not invent or
auto-install it. Standalone tasks need no plan or `G#`; preserve existing SOW
routing and do not add a plan unless requested or excessive scope risks failure.

## Core Rules

- Read local repo rules and the active scope contract before editing.
- For architecture, ownership, persistence, migration, or runtime-boundary work, re-read the target project's authority documents; extract applicable invariants and forbidden designs before implementation.
- Confirm the approved SOW or decision maps the selected design and viable alternatives to those invariants. Missing or conflicting authority is a stop condition, not permission to select a convenience-driven design.
- When concept authority exists, run Concept Preflight before implementation
  and Concept Closeout before completion.
- Confirm the approved SOW covers the exact task before code changes begin.
- Before implementation or delegation, compare the planned route with the
  user's selected approach, relevant runtime/version, chosen POC and approved
  changes, including internal-only work. Keep demonstrated behavior distinct
  from remaining verification. An APPROVED label does not resolve a contradiction
  with an explicit user constraint; report the exact conflict before proceeding.
- Do not introduce an additional compatibility layer, shim, fallback backend,
  legacy alias or dual path without first explaining its need and obtaining
  explicit user approval. Reviewer advice, old tests or an agent-written SOW
  clause do not authorize it. Reuse prior explicit approval for the same scope;
  preserve existing authorized support. Report conflicting consumer requirements
  rather than silently adding or removing support or weakening tests.
- For a public API, CLI, UI action, SDK, or other caller-visible entrypoint,
  reconstruct the latest explicit consumer call and compare its abstraction,
  identifiers, inputs and result with the SOW. Stop and reopen scope when they
  differ; earlier approval does not override a later explicit correction.
- When the SOW contract includes lifecycle timestamps, confirm the base SOW and
  active extension each have `create_dttm`, `approve_dttm`, and `finish_dttm`.
  Every known timestamp must include clock time to seconds and a numeric
  timezone offset, such as `2026-09-11T15:42:07+07:00`; reject date-only values.
  Do not invent historical times or add approval-evidence prose.
- Build context from the codebase or problem first. Do not lead with assumptions.
- Reuse the nearest fitting project implementation when one is named or cheaply
  discoverable; do not rebuild its responsibilities inside task-specific code.
- For a remote or containerized runner, stage only the approved files, then run
  an import-only smoke with the exact interpreter and `PYTHONPATH` that will
  launch the action. Do not background a Spark, database, or other data action
  until that smoke passes; an import failure is a staging/environment gate.
- After approved scope is confirmed and before each implementation slice, run
  the mandatory GLM-5.3-max delegation gate below. When the exact target is
  available and a safe bounded slice can be defined, delegate it; do not skip
  because the work is simple, mechanical, routine, costly, or judged unsuitable.
  Only confirmed unavailability or an observed delegation failure permits
  automatic local fallback with evidence. If no safe authorized slice can be
  defined, stop for scope/authority clarification.
- Use `sow-delegate-flow`'s internal
  `automatic-execution-delegation` mode for this mandatory handoff. A later
  explicit human model/transport or local-only instruction wins for that named
  task and must be recorded as a user override.
- Run at least one direct inspection or experiment to confirm the likely implementation shape or root cause before editing when behavior is changing.
- Apply the smallest meaningful patch that satisfies the SOW.
- Keep behavior locks, invariants, and only authorized adjacent consistency in
  scope.
- Treat syntax or compile checks, implementation verification, and gap-finding as different steps.
- Do not present the task as complete while any repair loop or required verification remains open.
- Before claiming a requested sync, deploy, or packaged delivery is complete,
  identify the exact source revision/artifact it consumes. If it consumes
  committed Git state (for example, `HEAD`), verify the intended change is in
  that revision; a local-only edit was not delivered. When the user requested
  that delivery and repository policy permits it, make the required scoped
  commit as part of the task; do not stop at local-only or ask redundantly. If
  the user restricted commits, policy requires separate approval, or scoped
  commit safety is blocked, stop before delivery and report the exact blocker.
  For a local-only edit with no committed delivery requested, do not force a
  commit.

## Execution Loop

```text
Phase 0: scope check
-> confirm the approved SOW covers the exact task
-> if a parent plan exists, map the SOW to its goal and approved scope; confirm
   dependency exit gates passed before execution; plan approval or TBD is not
   SOW approval. Stop on material scope change and route for explicit approval
-> for caller-visible work, compare the latest explicit consumer contract with
   the SOW; a task-specific surface does not satisfy a generic request merely
   because its internals are generic
-> confirm the base SOW and active extension lifecycle metadata is consistent:
   -> creation and approval timestamps exist for approved current scope
   -> finish timestamps remain null while their scope is open
   -> every known timestamp includes date, time to seconds, and timezone offset;
      date-only values are invalid
   -> use unknown only for unavailable historical event times
-> for a design-bearing task, confirm the authority-to-design mapping and planned evidence are present
-> if the mapping is missing, authority is ambiguous, or the selected design conflicts:
   -> stop and return to project-authority review before implementation
-> if concept authority exists:
   -> read the mapped concepts
   -> extract applicable invariants and forbidden designs
   -> stop if `Concept Compliance` is missing, false, or conflicts with the selected design
-> if this is a regression or follow-up under an active SOW:
   -> extend that SOW only while it stays within the repo's extension limit
   -> otherwise open a replacement SOW that references the prior one
-> if scope or branch is still unclear:
   -> route back to `task-router-flow`

Phase 1: context and experiment
-> read the relevant code paths first
-> run at least one direct inspection or experiment to confirm the likely root cause or implementation shape before editing
-> sharpen success criteria and behavior locks
-> when changing a public surface, write down the consumer-shaped invocation
   and trace each caller-supplied identity/input to its actual owner
-> inspect adjacent scope only to confirm impact or the same proven defect;
   inspection does not expand authorized implementation scope
-> break the work into the smallest meaningful mini-tasks
-> for a generic or framework-wide contract change, enumerate every discoverable
   direct caller/declaration in the declared source scope
-> record each caller's approved, legacy, or boundary disposition in the
   existing implementation evidence; do not create a persistent caller registry
-> run the mandatory GLM-5.3-max delegation gate for the next slice:
   -> inspect current native catalog/list-models or documented transport
   -> exact model + max effort available and safe bounded slice exists:
      -> MUST enter sow-delegate-flow's internal automatic mode
   -> exact target unavailable:
      -> record capability evidence, then use the local fallback
   -> delegation launch/session/isolation/child/output failure:
      -> record concrete evidence, repair within bounds, then use local fallback
         only if the failure remains
   -> no safe authorized slice exists:
      -> stop for scope/authority clarification; do not execute locally
   -> explicit human model/transport/local-only instruction:
      -> record and follow that named override

Phase 2: implement
-> pick the next smallest meaningful mini-task
-> if the mandatory gate selected delegation, hand off one bounded
   non-overlapping slice and keep the coordinator out of its write scope
-> if the gate recorded confirmed unavailability or an observed delegation
   failure, apply the smallest local patch that satisfies the SOW and record
   the fallback evidence
-> do not silently convert an unsafe/unbounded/unverifiable slice into local work
-> keep invariants, behavior locks, and cleanup paths in scope
-> use micro-checks during implementation when they reduce wasted work

Phase 3: implementation verification
-> run implementation verification proportional to task severity
-> do not rely on syntax or compile checks alone
-> verify the changed behavior in the real runtime path when feasible
-> exercise the intended public entrypoint; when genericity is required, verify
   that the first product identity is not hardcoded behind a generic name
-> verify every discoverable affected caller follows the approved contract;
   one representative caller or helper-only fixture is not enough for a generic
   claim
-> run a negative check that fails when any affected caller retains the old
   route, default, flag, or gate, and verify non-target consumers remain on
   their declared behavior
-> inspect frontend and backend evidence when the task crosses that boundary
-> when a slice was delegated, treat delegate completion as handoff evidence;
   verify the changed behavior and isolation locally before accepting it
-> record verification evidence
-> if verification fails or remains incomplete:
   -> task state = implemented but not fully verified
   -> re-enter at the cheapest correct stage

Phase 4: gap-finding pass
-> re-read the changed code and challenge the solution
-> answer the required post-implementation gap checklist
-> if any answer is uncertain:
   -> do one more targeted inspection or runtime check
-> if concept authority exists:
   -> compare the final diff with the SOW's `Concept Compliance` mapping
   -> if semantics changed a concept without the same-SOW concept update:
      -> block closeout and reopen the loop
-> if a gap is found:
   -> report the actionable findings in a `Severity | Finding | Impact | Solution` table before choosing the next action
   -> classify it as an authorized in-scope defect, missing required evidence,
      or optional/out-of-scope improvement
   -> repair only the authorized defect; gather required evidence at the
      cheapest correct stage; report or route optional/out-of-scope work
   -> classify remaining risks using Completion And Risk Acceptance below;
      accepted non-blocking risks do not become mandatory repair loops
-> challenge each added mechanism against the approved outcome and nearest
   fitting baseline; report unsupported responsibility and remove it only when
   the approved scope permits, without weakening required correctness or safety

Phase 5: closeout
-> only enter after Phase 3 and Phase 4 are complete
-> reuse still-valid verification evidence; rerun only checks invalidated by
   changed code, inputs, dependencies, config, or missing evidence
-> review scope fit
-> if a parent plan exists, update SOW Sequence and Acceptance with actual
   results/gaps after each SOW; before plan closure, require evidence for all
   outcomes, preservation/ownership locks, and required integration/deployment
   -> SOW counts, prototype-only proof, or functional pass with ownership
      violations do not make the plan DONE
-> review changed files and worktree
-> confirm no repair loop remains open
-> if this task makes a SOW or plan complete:
   -> set the active extension's finish_dttm at its verified completion
   -> set the top-level SOW finish_dttm only when no owned scope remains open
   -> preserve completed extension timestamps
   -> move that completed planning file into the repo's `finished/` planning directory before commit
-> commit
   -> review task-owned changes against scope; preserve unrelated dirty work
   -> follow Scoped Commit Safety below, including pre-existing staged changes
   -> commit only owned changes with a descriptive summary message
   -> if the task is not fully verified, do not commit it as done; only use an explicit checkpoint commit that says verification is still pending
   -> if the user explicitly deferred commits, skip the commit and note that in the final response
-> produce the final summary after commit handling
   -> if `task-progress-report` is present for this task, invoke it once here and not earlier by default
   -> use a progress/closeout summary shape, not a findings table, unless actionable issues remain

Escalate immediately when required information or decision authority is
missing. For recoverable technical failures already within scope, escalate when
the same failure repeats and no meaningful progress is being made.
```

## Mandatory GLM-5.3-max Delegation Gate

Run this gate after the approved SOW and exact write scope are confirmed, and
before every implementation or substantive review slice. It is mandatory when
the exact target is available and a safe bounded slice exists.

- Inspect the current native catalog, `list-models` result, or documented
  transport. Only exact `greennode/glm-5.3` with `reasoning_effort=max` counts;
  aliases, variants, stale labels, and guessed availability do not qualify.
- When the exact target is available and a safe bounded non-overlapping slice
  exists, invoke `sow-delegate-flow` in
  `automatic-execution-delegation`. Do not skip because the work is simple,
  mechanical, routine, costly, or judged unsuitable.
- Hard rule: do not skip because the work is simple, mechanical, routine, costly, or judged unsuitable.
- If no safe authorized slice can be defined, stop for scope or authority
  clarification. Do not convert that condition into local execution.
- If the exact target is confirmed unavailable, record the capability evidence
  and use the local fallback. If delegation launch, transport, session,
  isolation, terminal child, or bounded output fails, record concrete evidence,
  allow bounded repair, and use local fallback only if the failure remains.
  Missing external evidence is unverified and requires a stop, not an invented
  failure or silent local fallback.
- A later explicit human model, transport, or local-only instruction wins for
  that named task and must be recorded as a user override.
- `sow-delegate-flow` owns prompt boundaries, native `fork_turns: "none"`,
  fresh non-native sessions, cleanup, and transport details. This skill owns
  availability, the mandatory decision, and evidence-backed fallback.
- When the user explicitly selects Claude Code for an approved implementation
  slice, route the external transport through `sow-delegate-flow` and use its
  Claude `sonnet` high-effort contract. This skill remains responsible for SOW
  scope, write ownership, verification and closeout; do not duplicate CLI
  syntax here.
- Record `delegation_decision` as `delegated`, `fallback-unavailable`,
  `fallback-failure`, `user-override`, or `blocked-no-safe-slice`, with reason,
  model/transport, availability evidence, isolation status, failure evidence,
  and verification result.

## Hard Gates

Do not mark the task complete if any of these are missing:

- real implementation verification was not performed
- only syntax or compile checks were run for a runtime behavior change
- end-to-end or runtime-path evidence was applicable but not inspected
- a post-implementation gap-finding pass was not done
- a delegated slice was accepted without coordinator-owned verification and
  isolation evidence

If verification cannot be completed:

- do not present the task as finished
- explicitly say what remains unverified
- stop at `implemented but not fully verified`

## Verification Severity

- Low-risk task:
  syntax plus code-path review may be enough only when no runtime behavior changed.
- Runtime behavior task:
  run at least one real scenario.
- Async, stateful, UI, or performance-sensitive task:
  run a multi-step scenario and inspect runtime evidence or logs.

## Evidence Contract

Implementation verification must include, when applicable:

- scenario or scenarios executed
- observed frontend evidence
- observed backend evidence
- whether the result matched the SOW behavior lock
- whether any gap or residual risk remained
- delegation decision and reason; when delegated, selected model, transport,
  availability evidence, lifecycle/isolation status, and handoff result

## Required Gap Checklist

After implementation, answer this checklist:

- contract complete?
- caller-visible abstraction, identifiers, inputs and result match the latest
  explicit user contract?
- all discoverable affected callers use the approved route/default, and is the
  caller inventory recorded in the existing evidence?
- does the negative check reject every affected caller that retains the old
  route/default/gate while preserving non-target consumers?
- edge cases covered?
- old behavior preserved?
- race or cancellation path safe?
- performance regression risk?
- cleanup or dispose path correct?
- logging and observability still sane?

If any answer is uncertain, do one more targeted inspection or runtime check before closing.

## Findings Output Standard

If the post-implementation gap check, double-check, regression analysis, or risk review finds actionable issues, prefer a compact table with these columns:

| Severity | Finding | Impact | Solution |
| --- | --- | --- | --- |

Use this table before deciding whether to:

- patch immediately
- open or extend a SOW
- leave the issue as an explicit residual risk

Do not force the table when there are no findings or when the result is just a short status update.

Do not use this findings table for a plain `summary`, `summarize`, or closeout recap unless actionable issues remain.

If there are no actionable findings, say directly:

> No actionable findings found.

## Syntax vs Implementation Verification

- Syntax or compile checks prove the code parses, type-checks, or builds.
- Implementation verification proves the changed behavior works in the intended runtime path.
- Syntax or compile checks are never enough for runtime behavior, async, stateful, UI, or performance-sensitive tasks.

## Mini-Task Discipline

- Prefer slices that are small enough to verify quickly.
- Do not split so far that the slices stop being meaningful.
- A slice pass is not a task pass.
- After one slice passes, move to the next approved slice. Inspect a repeated
  pattern when useful, but add work only when existing scope and authority cover it.

## Micro-Checks

Use micro-checks to reduce wasted loops before the main verify step.

Examples:

- read or update the nearby test while implementing
- grep for analogous surfaces or old call sites
- run one narrow check for the touched function or file
- inspect generated output or artifacts before broader validation

Micro-checks do not replace implementation verification. They are a cheap signal during implementation.

## Implementation Verification vs Gap-Finding

`implementation verification`:

- asks whether the intended behavior works in the real path that matters
- is tied to the current success criteria and behavior lock

`gap-finding`:

- tries to falsify confidence in the implementation
- looks for gaps in the solution quality, not flaws in the existence of a verify step
- should actively search for shallow fixes, partial fixes, and technically-passing-but-wrong outcomes

If gap-finding finds an authorized defect or missing required evidence, reopen
at the cheapest correct stage. Report or route optional/out-of-scope
improvements instead of silently adding them to the task.

## Cheapest Correct Re-Entry Point

When a check fails, do not restart from the top by default.

Return to the earliest stage that can fix the problem correctly without wasting work.

Typical re-entry points:

- context gap -> go back to `gather context`
- success-criteria mismatch -> go back to `sharpen success criteria`
- scope-impact gap -> inspect affected scope, then repair only what existing
  authority covers
- code defect or weak solution -> go back to `implement smallest meaningful slice`
- weak or missing validation -> go back to `implementation verification`

If the failure origin is uncertain, bias one stage earlier.

## Escalation Rule

Escalate immediately when required information or decision authority is
missing. For a recoverable technical failure already within the approved scope,
escalate when the same failure mode repeats and no meaningful progress is made.
Do not escalate merely because the work is hard or needs one bounded repair.

## Closeout States

- `in implementation`:
  code or docs are still being changed.
- `implemented but not fully verified`:
  the patch exists, but required implementation verification or gap-finding is still incomplete.
- `verified`:
  required implementation verification passed and no blocking gap remains;
  accepted non-blocking risks are explicitly recorded.
- `closed`:
  final summary is complete, task-owned changes match scope, and commit handling is complete.

Only `closed` may be presented as done.

## Closeout Rule

Only close out when all of these are true:

- mini-task work is complete
- implementation verification passed at the required severity for the task
- gap-finding found no blocking gap; remaining risks meet the acceptance rule below
- final quality check passed
- task-owned changes still match approved scope; unrelated work remains intact
- delegation decision evidence is recorded for every implementation slice that
  entered the mandatory GLM-5.3-max gate
- any SOW or plan completed by this task has been moved into the repo's `finished/` planning directory
- the active extension and top-level SOW have their correct completion
  timestamps before a finished move

## Completion And Risk Acceptance

- Failed done criteria, missing required verification and open required repairs
  block completion regardless of severity labels. Keep the task `implemented
  but not fully verified` until those gates pass.
- A non-blocking risk may remain only when all required criteria pass and its
  acceptance follows explicit user acceptance, an approved scope allowance or
  a repository policy delegating that decision. The agent cannot invent consent.
- Record the risk, impact, acceptance basis and follow-up owner or action.
  Unclassified or unaccepted risks require a decision before claiming completion.
- Do not convert optional/out-of-scope improvements into required repairs or
  use risk acceptance to waive verification, change scope or lower done criteria.

## Scoped Commit Safety

- Inspect both staged and unstaged changes before staging. Unrelated dirty work
  does not block task completion and must remain intact.
- Stage only task-owned files or hunks. Resolve ambiguous mixed ownership before
  staging; never stage an entire mixed file merely because its path is in scope.
- If unrelated work was already staged, use isolated commit staging or an
  equivalent scoped commit preserving those original index entries. Merely adding
  selected files then running ordinary `git commit` can include unrelated work.
- Inspect the actual commit diff against scope and preserve unrelated staged and
  unstaged changes. Use a descriptive commit summary and follow repo git policy.
- do not commit as done before implementation verification and gap-finding are complete
- if you need a checkpoint commit before full verification, label it explicitly as not yet fully verified
- if the user explicitly deferred commits, skip the commit and note that in the final response

## Final Response Contract

Final response must include:

- SOW reference, or explicitly say this was a docs-only scope
- what changed
- implementation verification performed
- remaining gaps or risks, or `none found`
- if not fully verified, say so explicitly

## Composition With Other Skills

- Use `task-router-flow` when branch or scope is unclear.
- Choose any available inspection method that provides sufficient codebase
  evidence; CodeGraph and a separate search-policy skill are optional, never
  required setup or invocation.
- Use `sow-delegate-flow` when the user explicitly delegates a task, SOW, or
  plan to a native or custom external agent, or when this skill's approved
  mandatory exact-model gate selects the internal
  `automatic-execution-delegation` mode. The delegate skill remains
  authoritative for model, transport, isolation, prompt, and cleanup behavior;
  this skill remains authoritative for the mandatory decision and
  evidence-backed fallback.
