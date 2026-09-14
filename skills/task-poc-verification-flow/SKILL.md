---
name: task-poc-verification-flow
description: Use when the user asks to review, double-check, final-review, or assess approval readiness for a POC SOW or POC implementation plan. Focus on whether the POC is self-contained, safe to run, grounded in repository guardrails, and verified through the intended runtime path. Do not use after approval when the user is asking to implement the POC; use task-execution-flow instead.
---

# Task POC Verification Flow

Use this skill to review SOWs and implementation plans whose deliverable is a proof of concept, smoke runner, runtime probe, or integration check.

This is a review skill. It does not implement the POC.

## Boundary

Use this skill for POC-specific review:

- POC SOW review, final review, or approval-readiness check
- POC runner design before implementation
- POC verification evidence review after a run
- runtime integration probes, smoke checks, and one-off compatibility checks

Do not use this skill for broad architecture comparison, general root-cause investigation, or non-POC planning review. Use `task-review-investigate-compare` for those.

Do not use this skill after the POC scope is approved and the user asks for implementation. Use `task-execution-flow` for execution.

## Review Workflow

1. Read target repo guardrails first.
2. Read the target SOW or plan completely.
3. Read the POC files, referenced helper code, and existing examples it depends on.
4. Check the POC boundary against the repo rules.
5. Check the verification path proves the intended runtime behavior.
6. Report findings with concrete file/line evidence.
7. Patch only planning/docs writeback when the finding is low-ambiguity and does not expand scope.
8. Stop before implementation. Route an approved implementation request to `task-execution-flow`.

## POC SOW Checklist

Verify the SOW states:

- exact POC folder and allowed files
- what runtime behavior or integration boundary the POC proves
- the command to run, with environment assumptions
- what output proves success
- what negative evidence would prove the POC still fails
- what is explicitly out of scope
- whether credentials, tokens, `.env`, endpoint values, or run outputs must not be printed or committed
- whether the POC is allowed to use external network, protected endpoints, local services, VPN, or real data

## POC Code Review Checklist

Verify the proposed or existing POC:

- stays self-contained unless the repo explicitly allows a scratch/workspace exception
- reuses existing project helpers instead of rebuilding auth/session/config logic
- avoids CLI/framework scaffolding when the repo POC style is direct `main` block execution
- does not introduce production APIs, wrappers, adapters, or compatibility shims
- does not read or print secrets, tokens, `.env` values, or full runtime config
- keeps error output useful enough for remote compute debugging without leaking sensitive values
- cleans only run-owned artifacts when cleanup is part of the POC
- avoids maintained test suites for one-off POC helpers unless explicitly approved

## Minimum Proof Gate

- Trace every proposed stage, artifact, helper, and persistent state to the POC
  hypothesis or a concrete runtime constraint. Remove anything with no such
  responsibility.
- Prefer the intended runtime path and the nearest fitting existing example over
  reconstructing framework, authentication, session, checkpoint, or orchestration
  behavior inside the POC.
- Do not turn possible future reuse into a parallel framework or generalized
  tool. Keep optional hardening outside the POC until separately authorized.
- Preserve the smallest checks needed to prove correctness, cleanup ownership,
  secret safety, and the stated negative case. Shorter code is not the goal;
  sufficient proof with no unrelated machinery is.

## Verification Review

Separate evidence into:

- `Implemented`: files or behavior that exist in the current checkout
- `Verified`: commands or runtime paths actually executed
- `Not verified`: live services, protected endpoints, network/VPN paths, or external auth that were not run
- `Risk`: likely ways the POC can pass locally but fail in the target runtime

Prefer the real POC runner over helper-only tests. Static checks are useful but do not prove an integration POC works.

## Output Contract

Use concise sections:

- `Scope`
- `Evidence`
- `Findings`
- `Recommendation`
- `Next action`

For actionable findings, use:

| Severity | Finding | Impact | Solution |
| --- | --- | --- | --- |

`Next action` must be one of:

- `approve`
- `patch SOW/docs`
- `route scope change`
- `do not approve yet`

If there are no actionable findings, say:

> No actionable findings found.
