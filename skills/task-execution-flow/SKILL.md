---
name: task-execution-flow
description: Use when task scope is already approved or otherwise clear and you need the repo's execution discipline for carrying work from context gathering through implementation, repair loops, implementation verification, gap-finding, and closeout.
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

## Core Rules

- Read local repo rules and the active scope contract before editing.
- Confirm the approved SOW covers the exact task before code changes begin.
- Build context from the codebase or problem first. Do not lead with assumptions.
- Run at least one direct inspection or experiment to confirm the likely implementation shape or root cause before editing when behavior is changing.
- Apply the smallest meaningful patch that satisfies the SOW.
- Keep behavior locks, invariants, and adjacent consistency in scope.
- Treat syntax or compile checks, implementation verification, and gap-finding as different steps.
- Do not present the task as complete while any repair loop or required verification remains open.

## Execution Loop

```text
Phase 0: scope check
-> confirm the approved SOW covers the exact task
-> if this is a regression or follow-up under an active SOW:
   -> extend that SOW only while it stays within the repo's extension limit
   -> otherwise open a replacement SOW that references the prior one
-> if scope or branch is still unclear:
   -> route back to `task-router-flow`

Phase 1: context and experiment
-> read the relevant code paths first
-> run at least one direct inspection or experiment to confirm the likely root cause or implementation shape before editing
-> sharpen success criteria and behavior locks
-> widen adjacent coverage before declaring the task narrow
-> break the work into the smallest meaningful mini-tasks

Phase 2: implement
-> pick the next smallest meaningful mini-task
-> apply the smallest patch that satisfies the SOW
-> keep invariants, behavior locks, and cleanup paths in scope
-> use micro-checks during implementation when they reduce wasted work

Phase 3: implementation verification
-> run implementation verification proportional to task severity
-> do not rely on syntax or compile checks alone
-> verify the changed behavior in the real runtime path when feasible
-> inspect frontend and backend evidence when the task crosses that boundary
-> record verification evidence
-> if verification fails or remains incomplete:
   -> task state = implemented but not fully verified
   -> re-enter at the cheapest correct stage

Phase 4: gap-finding pass
-> re-read the changed code and challenge the solution
-> answer the required post-implementation gap checklist
-> if any answer is uncertain:
   -> do one more targeted inspection or runtime check
-> if a gap is found:
   -> convert it into a repair mini-task
   -> re-enter at the cheapest correct stage

Phase 5: closeout
-> only enter after Phase 3 and Phase 4 are complete
-> rerun relevant final checks
-> review scope fit
-> review changed files and worktree
-> confirm no repair loop remains open
-> produce the final summary
   -> if `progress-reporting-flow` is present for this task, invoke it once here and not earlier by default
-> commit
   -> verify the worktree only contains changes covered by the approved scope
   -> stage only the relevant files with `git add`
   -> commit with a descriptive summary message using `git commit -m "<summary>"`
   -> if the task is not fully verified, do not commit it as done; only use an explicit checkpoint commit that says verification is still pending
   -> if the user explicitly deferred commits, skip the commit and note that in the final response

Escalate only when all 3 signals are present:
-> the same failure mode repeats
-> no meaningful progress is being made
-> missing information or authority needed to continue
```

## Hard Gates

Do not mark the task complete if any of these are missing:

- real implementation verification was not performed
- only syntax or compile checks were run for a runtime behavior change
- end-to-end or runtime-path evidence was applicable but not inspected
- a post-implementation gap-finding pass was not done

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

## Required Gap Checklist

After implementation, answer this checklist:

- contract complete?
- edge cases covered?
- old behavior preserved?
- race or cancellation path safe?
- performance regression risk?
- cleanup or dispose path correct?
- logging and observability still sane?

If any answer is uncertain, do one more targeted inspection or runtime check before closing.

## Syntax vs Implementation Verification

- Syntax or compile checks prove the code parses, type-checks, or builds.
- Implementation verification proves the changed behavior works in the intended runtime path.
- Syntax or compile checks are never enough for runtime behavior, async, stateful, UI, or performance-sensitive tasks.

## Mini-Task Discipline

- Prefer slices that are small enough to verify quickly.
- Do not split so far that the slices stop being meaningful.
- A slice pass is not a task pass.
- After one slice passes, either move to the next slice or widen coverage if the same pattern clearly applies elsewhere.

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

If gap-finding finds a gap, reopen the loop. Do not treat the task as done.

## Cheapest Correct Re-Entry Point

When a check fails, do not restart from the top by default.

Return to the earliest stage that can fix the problem correctly without wasting work.

Typical re-entry points:

- context gap -> go back to `gather context`
- success-criteria mismatch -> go back to `sharpen success criteria`
- adjacent coverage gap -> go back to `widen adjacent coverage`
- code defect or weak solution -> go back to `implement smallest meaningful slice`
- weak or missing validation -> go back to `implementation verification`

If the failure origin is uncertain, bias one stage earlier.

## Escalation Rule

Escalate only when all 3 signals are present:

- the same failure mode is repeating
- there is no meaningful progress
- required information or decision authority is missing

Do not escalate merely because the work is hard or needs another repair pass.

## Closeout States

- `in implementation`:
  code or docs are still being changed.
- `implemented but not fully verified`:
  the patch exists, but required implementation verification or gap-finding is still incomplete.
- `verified`:
  implementation verification passed and gap-finding found no unresolved issue.
- `closed`:
  final summary is complete, worktree matches scope, and commit handling is complete.

Only `closed` may be presented as done.

## Closeout Rule

Only close out when all of these are true:

- mini-task work is complete
- implementation verification passed at the required severity for the task
- gap-finding found no unresolved gap
- final quality check passed
- the worktree still matches the approved scope

Commit discipline:

- verify the worktree only contains changes covered by the approved scope
- stage only the relevant files with `git add`
- commit with a descriptive summary message using `git commit -m "<summary>"`
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
- Use `code-context-search-policy` when deciding how to inspect the codebase.
- Use `sow-delegate-flow` only when the task is being delegated to Claude.
