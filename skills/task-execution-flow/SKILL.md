---
name: task-execution-flow
description: Use when task scope is already approved or otherwise clear and you need the repo's execution discipline for carrying work from context gathering through implementation, repair loops, verification, double-check gap finding, and closeout.
---

# Task Execution Flow

Use this skill after routing is already done.

This skill is for executing a task, not for deciding the task branch and not for reporting progress format.

## Use This Skill When

- an approved SOW already exists
- a docs-only scope is clearly allowed
- the branch is already clear and the remaining question is how to execute well

If branch or scope is still unclear, use `task-router-flow` first.

## Core Rules

- Read local repo rules and the active scope contract before editing.
- Build context from the codebase or problem first. Do not lead with assumptions.
- Sharpen success criteria before broad implementation.
- Widen adjacent coverage before declaring the task narrow.
- Break work into the smallest meaningful mini-tasks that still produce real progress.
- Use micro-checks during implementation when they reduce wasted work.
- Treat `verify` and `double-check` as different steps.
- Do not close out while a repair loop is still open.

## Execution Loop

```text
read rules + scope
-> gather context
-> sharpen success criteria
-> widen adjacent coverage
-> break into mini-tasks

-> for each mini-task
   -> pick next smallest meaningful mini-task
   -> implement smallest meaningful slice
   -> micro-check during implementation
   -> verify slice
      -> prove the slice works as intended
   -> assess slice result
      -> pass: continue to next mini-task
      -> fail: diagnose earliest broken stage
               -> re-enter at cheapest correct stage
      -> unclear: ask user or narrow scope

-> task-level verify
   -> confirm the whole task works against agreed success criteria

-> double-check / gap-finding pass
   -> challenge implementation and execution quality
   -> look for:
      -> shallow implementation
      -> incomplete coverage
      -> wrong or weak approach
      -> adjacent surfaces left inconsistent
      -> output that technically passes but does not really solve the problem
   -> if a gap is found:
      -> convert it into a repair mini-task
      -> re-enter at the cheapest correct stage
   -> if clean:
      -> continue

-> final quality check
   -> rerun relevant checks
   -> review scope fit
   -> review changed files / worktree
   -> confirm no open repair loop remains

-> final summary
   -> if `progress-reporting-flow` is present for this task, invoke it once here
   -> do not invoke it repeatedly during normal execution unless the user explicitly asks for additional structured progress reports

-> commit

-> escalate only when all 3 signals are present
   -> same failure mode repeats
   -> no meaningful progress is being made
   -> missing information or authority needed to continue
```

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

Micro-checks do not replace verify. They are a cheap signal during implementation.

## Verify vs Double-Check

`verify`:

- asks whether the intended slice or task works
- is tied to the current success criteria

`double-check`:

- tries to falsify confidence in the implementation
- looks for gaps in the solution quality, not flaws in the existence of a verify step
- should actively search for shallow fixes, partial fixes, and technically-passing-but-wrong outcomes

If double-check finds a gap, reopen the loop. Do not treat the task as done.

## Cheapest Correct Re-Entry Point

When a check fails, do not restart from the top by default.

Return to the earliest stage that can fix the problem correctly without wasting work.

Typical re-entry points:

- context gap -> go back to `gather context`
- success-criteria mismatch -> go back to `sharpen success criteria`
- adjacent coverage gap -> go back to `widen adjacent coverage`
- code defect or weak solution -> go back to `implement smallest meaningful slice`
- weak or missing validation -> go back to `verify`

If the failure origin is uncertain, bias one stage earlier.

## Escalation Rule

Escalate only when all 3 signals are present:

- the same failure mode is repeating
- there is no meaningful progress
- required information or decision authority is missing

Do not escalate merely because the work is hard or needs another repair pass.

## Closeout Rule

Only close out when all of these are true:

- mini-task work is complete
- task-level verify passed
- double-check found no unresolved gap
- final quality check passed
- the worktree still matches the approved scope

Commit with a scoped message unless the user explicitly deferred commits.

## Composition With Other Skills

- Use `task-router-flow` when branch or scope is unclear.
- Use `code-context-search-policy` when deciding how to inspect the codebase.
- Use `sow-delegate-flow` only when the task is being delegated to Claude.
