---
name: task-router-flow
description: Use this skill when the user makes a work request that may require creating a new SOW, extending an existing SOW, debugging toward a fix, or editing docs/plan files, and the correct workflow branch has not yet been chosen.
---

# Task Router Flow

Use this skill as the front-door router before execution begins.

For execution-time progress updates, follow [brief-execution.md](../../rules/brief-execution.md).

For the definition, template, approval rule, and lifecycle of a Scope of Work, see [scope-of-work.md](references/scope-of-work.md).

## Project Guardrail Conformance Audit

Run this audit before selecting a branch or drafting a SOW when the request may
affect architecture, ownership, persistence, migration, runtime boundaries, or
another project-defined design contract.

1. Read the target project's authority documents and nested rules.
2. Extract the invariants and prohibited designs relevant to the request.
3. Map viable directions to those invariants, including the selected direction.
4. State the evidence needed to prove the selected direction preserves them.
5. If authority is missing or conflicting, stop before drafting an
   implementation direction and request a project-authority decision.

Do not invent a project architecture from implementation convenience. This
audit derives rules from the target project; it does not prescribe a domain,
storage model, or ownership model.

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
- Check how many approved extensions the active SOW already has.
- If the next change would become extension 4, do not keep extending the same SOW.
- Draft a new SOW that references the prior SOW and carries forward only the still-relevant context.
- If the work belongs to a plan, extend the plan first and then update the aligned SOW.
- Otherwise extend or update the standalone SOW.
- Wait for approval.
- Hand off to the next execution step or downstream skill.

### 3. Debug Request

Use this branch when the user asks to debug, investigate, or fix a bug or regression.

Flow:
- Find the root cause first.
- Confirm user intent only if there is a real ambiguity or tradeoff.
- If the resulting fix is a big change, extend the active SOW before major edits unless that SOW already has 3 extensions.
- If the active SOW already has 3 extensions, draft a new SOW for the fix and link it back to the prior SOW.
- Continue to execution.
- Record the bug in `plan_todo/fix_bug.md`.

### 4. Docs / SOW / Plan Only

Use this branch when the request is limited to docs, SOW, or plan files.

Flow:
- Do not propose a new SOW.
- Show a concrete edit plan.
- Wait for approval.
- Edit the docs or planning files directly.
- If the edit makes a SOW or plan complete, move that completed file into `plan_todo/finished/` before closeout.

## Change Completeness Guardrail

Use this guardrail in every branch:
- Do not treat a request as a single-point fix by default.
- Check adjacent or analogous scope that can drift for the same reason.
- Present a short coverage note before execution:
  - what is directly requested
  - what analogous scope should also be handled
  - what is intentionally left out, if any
- If similar surfaces are likely affected, suggest a family-level fix path.
- If scope is intentionally narrow, explicitly mark it as a trade-off.

## SOW Extension Limit

- Treat 3 extensions as the hard maximum for a single SOW.
- Count each explicit extension section or equivalent approved addendum toward that limit.
- If a requested change would become extension 4, open a new SOW instead of appending more to the old one.
- The new SOW should reference the prior SOW so reviewers can trace continuity without letting one document grow indefinitely.
- Prefer carrying forward only active context, unresolved risks, and dependency notes rather than copying the entire old SOW.

## Closeout

After any branch finishes:
- run a final check
- if a SOW or plan became complete during this branch, move it into the repo's `finished/` planning directory before commit
- summarize the outcome
- commit with a clear message unless the user defers commits
- report the result to the user

## Global Hook Telemetry

When this skill runs in its own Codex session, emit one first-line marker:

```text
CODEX_SKILL_RUN skill=task-router-flow plan=<plan> sow=<sow> task_type=<task_type> intent=<intent>
```

Use real values, resolve the target project from the session working directory,
and let global hooks own timing. Do not run a second telemetry lifecycle from
this isolated routing session.

## Notes

- This skill decides the branch. It does not replace downstream execution skills.
- Use the repo's own SOW template and planning location.
- New SOWs should use a unique 4-digit index such as `SOW_0001_...`.
- For multi-SOW execution after routing, hand off to `sow-delegate-flow` or the local execution path as appropriate.
