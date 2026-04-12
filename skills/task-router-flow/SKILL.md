---
name: task-router-flow
description: Use this skill when the user makes a work request that may require creating a new SOW, extending an existing SOW, debugging toward a fix, or editing docs/plan files, and the correct workflow branch has not yet been chosen.
---

# Task Router Flow

Use this skill as the front-door router before execution begins.

For the definition, template, approval rule, and lifecycle of a Scope of Work, see [scope-of-work.md](references/scope-of-work.md).

## Branches

### 1. New Code Change

Use this branch when the user requests a new code change, feature, refactor, or other implementation work that is not already covered by an active approved SOW.

Flow:
- Draft a new SOW using the repo's active template.
- Revise it if the user requests changes.
- Wait for approval.
- Hand off to the next execution step or downstream skill.

### 2. Existing SOW Change

Use this branch when the user changes scope for work already covered by an active SOW or by a plan that owns one or more SOWs.

Flow:
- If the work belongs to a plan, extend the plan first and then update the aligned SOW.
- Otherwise extend or update the standalone SOW.
- Wait for approval.
- Hand off to the next execution step or downstream skill.

### 3. Debug Request

Use this branch when the user asks to debug, investigate, or fix a bug or regression.

Flow:
- Find the root cause first.
- Confirm user intent only if there is a real ambiguity or tradeoff.
- If the resulting fix is a big change, extend the active SOW before major edits.
- Continue to execution.
- Record the bug in `plan_todo/fix_bug.md`.

### 4. Docs / SOW / Plan Only

Use this branch when the request is limited to docs, SOW, or plan files.

Flow:
- Do not propose a new SOW.
- Show a concrete edit plan.
- Wait for approval.
- Edit the docs or planning files directly.

## Closeout

After any branch finishes:
- run a final check
- summarize the outcome
- commit with a clear message unless the user defers commits
- report the result to the user

## Notes

- This skill decides the branch. It does not replace downstream execution skills.
- Use the repo's own SOW template and planning location.
- New SOWs should use a unique 4-digit index such as `SOW_0001_...`.
- For multi-SOW execution after routing, hand off to `sow-delegate-flow` or the local execution path as appropriate.
