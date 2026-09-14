# SOW_0084 — Workflow Anti-Overengineering Gates

## Lifecycle

- Status: completed
- Approval: approved by user
- create_dttm: `2026-09-15T03:22:00+07:00`
- approve_dttm: `2026-09-15T03:47:19+07:00`
- finish_dttm: `2026-09-15T03:53:34+07:00`

## Task

Prevent unjustified scope and implementation growth across routing, review,
POC review and execution while preserving required behavior and verification.

## Why

A reviewed one-off migration implementation accumulated checkpoint plumbing,
serialization, orchestration, validation and safety responsibilities that were
not all required by the user's direct request. Existing short migration tools
were not inspected as the baseline before the design was accepted. Repeated
reviews checked contract completeness but did not challenge whether the
contract itself had become unnecessarily large.

## Feedback Contract

- Target skills: `task-review-investigate-compare`, `task-router-flow`,
  `task-execution-flow`, `task-poc-verification-flow`
- Trigger: routing, reviewing or executing a bounded code change or POC
- Observed behavior: review rewards completeness and added guardrails without
  proving each responsibility is necessary, while skipping a known-good local
  baseline
- Expected behavior: compare against the closest existing pattern, separate
  required from added responsibilities, remove unsupported complexity and
  block approval while material complexity remains unjustified
- Reusable invariant: every material added mechanism must be necessary for the
  authorized outcome and justified against a simpler adequate alternative;
  evidence of a problem does not authorize an expanded solution
- Cause class: incomplete review decision procedure
- Evidence reference: `sanitized:user-feedback-review-overengineering-2026-09-15`
- Expanded review: [14-skill audit](finding/2026-09-15_skill_complexity_audit.md).
  All installed entrypoints matched canonical. Existing project KISS rules were
  not applied; conflicting skill pressures are contributors, not proven sole
  causes of all prior incidents.

## As-Is Diagram (ASCII)

```text
router expands adjacent scope -> review checks completeness
  -> execution turns every gap into repair -> more work/code
```

## To-Be Diagram (ASCII)

```text
request + repo baseline
          |
          v
required responsibilities | proposed responsibilities
          |                         |
          +------ trace each -------+
                    |
   needed for approved outcome + simplest sufficient mechanism?
              | yes                 | no / unknown
              v                     v
             keep             finding / proposal
                    |
                    v
             simplest sufficient design
```

## Location

- `skills/task-review-investigate-compare/SKILL.md`
- `skills/task-router-flow/SKILL.md`
- `skills/task-execution-flow/SKILL.md`
- `skills/task-poc-verification-flow/SKILL.md`
- Corresponding four JSON fixtures under `tests/skill_feedback_cases/`
- `plan_todo/finding/2026-09-15_skill_complexity_audit.md`
- this SOW, later
  `plan_todo/finished/SOW_0084_review_anti_overengineering_gate.md`
- Post-commit deployment scope, pending approval: the four matching directories
  under `~/.codex/skills/`, one explicit per-skill sync at a time. No bulk sync
  or other environment is included; canonical completion is not rollout.

## Deliverables

### Review gate

The following behavior belongs to `task-review-investigate-compare`.

1. Add a mandatory simplicity review for code/design/SOW/plan reviews before
   recommending approval or `ready for HITL handoff`.
2. Require inspection of the closest existing user/project implementation when
   one is named or cheaply discoverable. Do not design first and compare later.
3. For nontrivial changes, compare responsibilities against the requested
   outcome and baseline. Necessity and implementation are separate: a required
   responsibility may be reused or newly implemented; reuse alone does not
   justify an unnecessary step. Keep this analysis brief and proportional.
4. Require each material added mechanism to be necessary for the approved
   outcome or a concrete governing constraint, and explain why existing simpler
   mechanisms are insufficient. Evidence of a failure establishes a problem,
   not permission for a new feature or a particular solution. Labels such as
   robustness, best practice and future-proofing are not sufficient reasons.
   Unsupported material complexity blocks a clean review or recommendation to
   approve. Put optional enhancements outside the effective contract until
   authorized.
5. Treat new wrappers, adapters, persistence, checkpoints, orchestration,
   retries, validation passes, compatibility paths and duplicated framework
   behavior as complexity requiring justification, not automatic robustness.
6. When a comparable baseline is materially smaller or more direct, require a
   concrete explanation for the difference. Line count is only a warning signal,
   never the decision criterion.
7. Prefer reuse of an existing source, pipeline or helper over reconstructing
   its behavior inside a one-off script, after checking that its contract fits.
   Apply this principle to feature, refactor and implementation reviews too;
   the migration example must not narrow the rule to ad-hoc scripts.
8. Do not remove complexity that is required for correctness, security,
   destructive-operation safety or an explicit runtime contract merely to make
   code shorter. Name the concrete requirement or failure it addresses and
   retain the simplest sufficient protection; hypothetical risks do not justify
   speculative subsystems. Approval of an earlier SOW does not prove design
   necessity, but changing approved behavior still follows project policy.
9. Add regression case `review-anti-overengineering-001` with expected,
   negative and boundary scenarios.
10. Keep skill frontmatter and `agents/openai.yaml` unchanged because trigger
    scope and public purpose do not change.
11. On implementation reviews, compare the actual diff with the approved
    minimal design as well as the baseline. Flag new state stores, repeated
    scans, conversions and ownership layers introduced during implementation.
    Passing tests or a previous clean review cannot waive this check. Moving
    excess code into more files or helpers is not simplification.
12. Preserve behavior, ownership, data semantics and intentional config during
    proposed simplification. Review changes also for lost checkpoints, skipped
    data or validation guarantees. The review skill does not authorize code
    edits or external operations; write back findings and route changed
    behavior under existing project policy.
13. Add only a compact section to the existing review flow. No required new
    worksheet, numeric complexity budget, universal approval step, or exhaustive
    repository search. Inspect a named baseline when available; if unavailable,
    state the limit and assess the smallest viable design from current evidence.
    Skip this gate for purely editorial reviews.

### Companion corrections

| Owner | Minimal correction |
| --- | --- |
| task-router-flow | Replace pressure to widen every request with bounded adjacent inspection. A narrow request needs no invented tradeoff. Broader repairs require evidence and existing authority; suggestions do not enter approved scope automatically. |
| task-execution-flow | Reuse the nearest fitting implementation. Before repairing a gap, distinguish a required in-scope defect, missing required evidence, and optional/out-of-scope enhancement. Repair authorized defects; report or route new work. Resolve missing authority immediately; the repeated-failure rule applies only to recoverable technical work within scope. |
| task-execution-flow | Challenge added mechanisms against the approved outcome during the existing gap pass. Preserve meaningful verification but reuse valid unchanged evidence; do not repeat checks or build persistent validation machinery solely to satisfy a generic checklist. Replace conflicting wording rather than append a competing policy. |
| task-poc-verification-flow | Require every proposed stage/artifact to support the specific hypothesis or a concrete necessary runtime constraint. Reuse the intended runtime path and existing examples; do not grow a POC into a parallel framework, test suite or generalized tool. Preserve essential correctness checks. |

Keep skill roles independent and concise; no shared policy engine, mandatory
cross-skill invocation, new config, report template or extra approval protocol.
Do not touch delegation because it already uses execution flow for verification.
SOW_0082 owns reporting, dirty-worktree and other previously recorded fixes;
coordinate shared-file edits without absorbing those deliverables.

## Regression Scenarios

| Kind | Scenario | Required behavior |
| --- | --- | --- |
| Expected | Review an implementation against a simple approved migration plan and named local baseline; it adds its own serializer, orchestration, state store and repeated scan despite passing tests | Inspect baseline and diff, identify unsupported mechanisms, block a clean verdict and propose direct reuse; moving helpers to another file or citing prior approval is insufficient |
| Negative | Review a longer destructive migration with required recovery, checkpoint and validation guarantees; it already uses the simplest sufficient mechanisms | Preserve the guarantees and intentional config; allow a clean review without manufacturing findings, line limits or more process |
| Boundary | Review an integration with no usable baseline; a documented retry failure needs handling, while a durable retry service is proposed without authorization | Separate the proven requirement from solution authority, compare a bounded local solution, state evidence limits and keep the service a proposal; do not change code or require a fresh production failure |

## Done Criteria

- The canonical review skill contains the baseline-first and responsibility
  justification gates.
- A review cannot conclude `ready for HITL handoff` while an unsupported
  material responsibility remains.
- The correction does not turn line-count thresholds into architecture rules.
- The gate covers both proposed designs and implementation drift; reuse,
  previous approval, passing tests and file splitting cannot justify unnecessary
  mechanisms. It cannot silently remove approved behavior or expand scope.
- The procedure itself remains proportional: no mandatory inventory artifact,
  numerical budget or additional governance for trivial changes.
- Regression case `review-anti-overengineering-001` contains sanitized expected,
  negative and boundary scenarios.
- `uv run python -m unittest tests.test_skill_feedback_cases tests.test_skill_sync_scripts`
  passes.
- Targeted positive, negative and boundary forward-tests run in a clean isolated
  context when available; otherwise behavioral verification is explicitly
  incomplete. Subagents are prohibited in this side conversation. Manual
  scenario review and fixture checks must not be reported as isolated model
  evidence.
- Each companion fixture adds exactly three scenarios under a stable case ID:
  `router-bounded-adjacency-001`, `execution-scope-bounded-repair-001`, and
  `poc-minimum-proof-001`. Each includes a required scoped repair, a forbidden
  speculative expansion and a boundary preserving necessary safeguards.
- Cross-skill walkthrough: a small one-off request stays bounded from router
  through execution; a discovered required defect is repaired; a proposed new
  subsystem remains unapproved. Correctness, data semantics and mandatory
  verification must survive simplification. Manual walkthrough is not isolated
  model evidence.
- All four changed skills pass structural validation; only task-owned hunks,
  fixtures and planning documents are committed.
- When implementation and deployment are approved, dry-run then actual sync
  each of the four named skills to Codex with the same explicit target options;
  exact-copy parity passes for each. Do not report all active skills corrected
  while any of the four installed copies remains outdated. Preserve concurrent
  work; do not silently publish unrelated pending skill changes.

## Out-of-Scope

- Project application code or skills outside the four named change targets.
- Introducing a universal maximum line count or banning necessary complexity.
- Rewriting historical SOWs or implementations.
- Bulk sync, multiple agent environments or modifying installed skills as source.
- Pushing commits or deploying the installed skill without explicit approval.

## Proposed-By

Codex, from explicit user feedback on 2026-09-15.

## Plan / Reference

- `skill-evolution-flow`
- `skill-creator`
- Existing review fixture:
  `tests/skill_feedback_cases/task-review-investigate-compare.json`
- [All-skill findings](finding/2026-09-15_skill_complexity_audit.md)

## Cautions / Risks

- A blanket “shorter is better” rule can remove required correctness and safety
  behavior; responsibility traceability is the authority, not line count.
- Baselines can be obsolete or solve a different contract; the review must
  compare responsibilities and runtime constraints, not copy shape blindly.
- SOW_0082 also proposes edits to shared skills and fixtures. At implementation,
  reread their current diff and preserve that task's changes; neither pending
  SOW grants authority to implement the other's deliverables.
- These instructions affect runs using the changed skills; they do not guarantee
  compliance by every model/session or change third-party/system skills.

## Review Summary

Reviewed baseline/implementation drift, then safeguards and process bloat.
The subsequent all-skill audit found contributing rules in router and execution
plus a POC review gap. Four bounded corrections were implemented with distinct
ownership. All deterministic checks and installed-copy parity passed. Isolated
model forward-testing was unavailable in this side conversation, so behavioral
conformance remains unverified until later real invocations.
