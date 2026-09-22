---
name: task-escalation-flow
description: Use when a lower-capability executor such as OpenAI Luna, a GLM-family model at high reasoning, or Claude Sonnet/Haiku is genuinely stuck after bounded attempts and needs a stronger read-only advisor; escalate first to gpt-5.6-sol at medium reasoning, then gpt-6-astra at low reasoning, with isolated context and evidence-backed handoff.
---

# Task Escalation Flow

Use this skill when the current executor cannot make meaningful progress on a
concrete task and needs an advisor with a stronger reasoning tier. Covered
source executors include OpenAI Luna, GLM-family models running at high
reasoning, and Claude Sonnet or Haiku. Family membership alone is not failure
evidence; the retry gate still applies. This is an advisor pattern, not
permission to bypass SOW, approval, verification, or ownership rules.

## Source Executor Families

Apply the same escalation gate when the current executor is:

- OpenAI Luna, such as the current catalog's `gpt-5.6-luna` or its resolved
  equivalent.
- A GLM-family model running at high reasoning, such as a currently registered
  GLM role.
- Claude Sonnet or Haiku through a documented native or external transport.

Resolve the current model identity and transport before dispatch. Do not guess
provider-specific IDs, treat the family name as proof of failure, or silently
substitute a different executor.

## Trigger

Activate when at least one of these is true:

- The current lower-capability executor, including a covered OpenAI, GLM, or
  Claude source family, has made **three materially different,
  evidence-backed attempts** without satisfying the acceptance check.
- The same failure mode persists after targeted repair; at most five total
  attempts are allowed before escalation.
- The model is looping, contradicting its own evidence, or cannot identify a
  safe next experiment for a bounded task.
- The user explicitly asks to escalate, ask a stronger advisor, or use the
  advisor pattern.

Do not escalate merely because a task is difficult, because one command failed,
or because the scope/approval/evidence is missing. Route authority gaps to the
user or the appropriate planning skill instead of spending retries.

## Retry Gate

Before escalation, record each attempt as:

- attempt number
- hypothesis or intended change
- action or experiment
- observed result and concrete evidence
- what changed, and why the next attempt is justified

Count only attempts that change the hypothesis, patch, probe, or verification
path. Do not count duplicate commands, no-op retries, prompt rephrasing, or
unexplained waiting. For async, stateful, UI, or high-risk work, escalate after
three failed meaningful attempts rather than consuming all five.

If the task is blocked by missing approval, an unavailable runtime, an unknown
contract, or an unsafe destructive operation, stop and report that blocker; do
not manufacture retry evidence.

## Escalation Ladder

Use one fresh advisor pass at each tier, in order:

1. **Tier 1 — Sol:** resolve the currently available Sol role as
   `gpt-5.6-sol` with reasoning effort `medium`.
2. **Tier 2 — Astra:** if Sol cannot produce a safe, evidence-backed next step
   or the uncertainty remains, resolve Astra as `gpt-6-astra` with reasoning
   effort `low` (light).

Do not silently substitute another model, skip a requested available tier, or
loop back to a lower tier. If a requested model is unavailable, report that
fact and stop or ask the user to choose an explicit alternative.

The advisor is read-only by default. It diagnoses, proposes the next bounded
step, and defines verification; it does not edit product code, tests, scripts,
configuration, or runtime contracts unless the user explicitly delegates that
write and an approved SOW covers it.

## Context Isolation

- Every advisor pass starts with a task-local context.
- Native Codex child dispatch **MUST** use `fork_turns: "none"`; never pass the
  parent conversation with `fork_turns: "all"` unless the user explicitly
  requests history sharing and accepts the exposure.
- Non-native custom agents **MUST** start a brand-new provider-owned session
  with no resume, continue, old task ID, or prior transcript.
- The handoff must be self-contained and contain only the goal, relevant
  artifact paths, acceptance/behavior lock, constraints, attempt evidence, and
  the exact question for the advisor. Do not paste the full parent chat,
  unrelated task history, secrets, or raw credential-bearing output.
- If clean isolation cannot be proven, do not dispatch. If the advisor reveals
  unrelated parent context, discard its result, interrupt or terminate the
  task-owned session, and restart only with a fresh bounded handoff.

Apply the transport and lifecycle rules from `sow-delegate-flow`; this skill
adds the capability ladder and does not weaken its session boundary.

## Benchmark Baseline

Use `references/baseline-test-case.md` when a controlled advisor-path check is
needed. It records one short public BBH `navigate` item plus observed Luna-max,
Sol-medium, and Astra-low results. Re-run it in fresh isolated sessions; never
assume a model-specific fail/pass from benchmark reputation or from the
reference alone. A correct lower-tier answer means `no escalation needed`.

## Advisor Handoff Contract

Send a compact brief with this shape:

```text
Advisor request
- Goal:
- SOW/plan and approval state:
- Acceptance or behavior lock:
- Current model and task mode:
- Attempts and evidence:
- Exact blocker:
- Constraints and out-of-scope:
- Question: What is the safest next bounded step, and how should it be verified?
```

Require the advisor to return:

- diagnosis tied to the supplied evidence
- recommended next bounded action
- assumptions and unresolved uncertainty
- verification command or scenario
- stop condition if the recommendation fails

Do not request or persist a full transcript. Keep only the minimum sanitized
handoff and result needed for the current task.

## Coordinator Loop

1. Confirm the retry gate and record the evidence contract.
2. Dispatch Sol in an isolated read-only context.
3. Inspect the advice against the active SOW, repository rules, and actual
   evidence; do not treat advisor confidence as proof.
4. Apply the smallest authorized next step locally and verify it.
5. If unresolved and the Sol result is insufficient, dispatch Astra once with a
   fresh, concise handoff containing the updated evidence only.
6. After the final advisor pass, either repair and verify locally, ask the user
   for missing authority, or stop as unresolved. Do not create an escalation
   loop.

Implementation remains governed by `task-execution-flow`: use the approved SOW,
run real implementation verification, complete the post-implementation
gap-finding pass, and keep residual risk explicit.

## Stop Conditions

Stop and report instead of escalating further when:

- Astra cannot identify a safe, evidence-backed next step.
- The requested model or transport is unavailable.
- Context isolation, task ownership, approval, or SOW scope is uncertain.
- The next action would materially expand scope without approval.
- The task still fails after the bounded advisor ladder.

Use `implemented but not fully verified` when implementation exists but the
required runtime evidence is unavailable. Never present advisor output alone as
task completion.

## Final Response Contract

Close with:

- why escalation triggered and how many meaningful attempts were made
- which advisor tier(s) ran and their reasoning effort
- evidence-backed diagnosis and recommendation
- action taken and implementation verification
- remaining gaps, risks, or `none found`

If no advisor was needed, do not invent an escalation report; continue with the
normal task flow.
