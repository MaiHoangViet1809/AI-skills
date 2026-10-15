# Task Complexity Contract

This shared contract classifies the whole requested task for the delegation
gates in `sow-delegate-flow`, `task-execution-flow`, and
`task-review-investigate-compare`. Reading it does not activate delegation.
Honor an explicit user model, transport, or local-only selection first.

## Classify Once

Classify before native model discovery, reclassify only on material new scope
or risk evidence, and record the classification plus concrete reason in the
existing task evidence. Do not split work into slices to evade delegation, or
inflate simple work to manufacture it. Ordinary file or tool counts alone are
not evidence.

## Simple

A task is simple only when scope, method, acceptance, and impact are clear, and
no complexity condition below applies. It MUST run in main without an automatic
delegate or reviewer, and MUST NOT probe model availability merely to satisfy
delegation.

Examples:

- review configuration against a known schema without tracing interactions;
- make or review a localized one-file edit with no shared-contract or
  cross-module change;
- make one tool or MCP call with known inputs and directly inspectable output;
- make a mechanical wording, metadata, or path update with settled intent;
- run one targeted check and report the result without root-cause investigation.

## Large Or Complex

A task is large or complex when at least one condition is demonstrated:

- coordinated changes across dependent modules;
- broad code-path investigation or competing root-cause hypotheses;
- architecture, ownership, API, schema, or migration decisions;
- meaningful async, state, race, cancellation, security, data-correctness, or
  performance risk;
- broad or high-risk review that benefits from an independent perspective;
- substantial independent workstreams.

When exact native `greennode/glm-5.3` with `reasoning_effort=max` is available
and a safe authorized workstream exists, the caller MUST delegate that
meaningful workstream or one independent review pass. Keep integration and
acceptance in main. Do not repeat handoffs per slice or duplicate investigation
solely for compliance.

## Overrides And Boundaries

- One-file concurrency, authentication, shared-API, or system-wide interaction
  work is not automatically simple.
- A destructive one-call operation needs impact assessment when approval or
  blast radius is not already settled.
- If relevant uncertainty remains after bounded inspection, classify complex
  unless scope or authority itself is unresolved; unresolved authority stops work.
- Complexity does not grant mutation permission; existing approval and safety
  gates still apply.
- When this contract is missing, leave classification unresolved, report the
  missing companion, and do not invent a simple exemption or auto-install it.
