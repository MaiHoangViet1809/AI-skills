---
name: sow-delegate-flow
description: Use when the user asks to delegate a task, SOW, or plan to a Codex sub-agent, especially GLM5.2. Keep approved SOWs authoritative, give each sub-agent a bounded ownership slice, then review and verify locally.
---

# Sow Delegate Flow

Use this skill for Codex-native delegation:

```text
Codex coordinator -> classify mode -> native sub-agent -> local review and verification -> repair or closeout
```

Keep execution-time commentary to one short sentence about status, next action
or a blocker. Keep the final response separate.

## Precedence

- `AGENTS.md` and repo rules define process constraints and guardrails.
- The approved SOW defines the active task scope and deliverables.

## Trigger And Routing

Activate when the user explicitly asks to delegate, assign, or hand off a task,
SOW, or plan to a sub-agent. Treat these as direct triggers:

- `delegate task ... cho GLM5.2`
- `delegate SOW ... cho GLM5.2`
- `delegate plan ... cho GLM5.2`
- an equivalent request naming a registered Codex sub-agent

Do not activate for ordinary single-agent execution or a request merely
mentioning another model.

- When the user names `GLM5.2`, resolve it against the native agent catalog for
  the current session. When `router_custom_greennode_glm_5_2` is exposed, pass
  that registered role as `agent_type`; do not assume the role name exists in
  every environment or silently replace it with another model.
- When the user names another available sub-agent, honor that selection.
- When no model is named, choose an available native sub-agent appropriate to
  the work and state the selection briefly.
- Delegating an implementation requires an approved SOW. A delegate may inspect
  or draft a plan/SOW before approval, but must not modify product code, tests,
  scripts, config, or runtime contracts in that mode.

## Rules

- Keep the approved SOW as the source of truth for the current implementation.
- Do not delegate implementation before approval. Scoped inspection, review,
  plan drafting, and SOW drafting may be delegated before approval when they do
  not modify implementation surfaces.
- Read local repo rules and inspect `git status --short` before delegating.
- For implementation, delegate with the approved SOW path, short intent,
  explicit write scope, and verification requirements. For planning/read-only,
  provide the target question or artifact plus explicit non-implementation
  scope.
- Give one sub-agent one bounded SOW or non-overlapping ownership slice at a
  time. Do not run overlapping write scopes in parallel.
- The coordinator remains responsible for scope, review, validation, repair
  decisions, user communication, and closeout.
- A sub-agent completion is handoff evidence, not task completion. Independently
  apply the implementation-verification and gap-finding hard gates from
  `task-execution-flow` before closeout.
- If a sub-agent asks a resolvable question, answer it with `followup_task` and
  continue. If scope or approval is unclear, stop and escalate.
- If a sub-agent reports completion but local validation fails, send concise
  repair feedback and continue.
- Take over locally if the sub-agent fails, drifts, cannot use required tools,
  or exhausts the two repair rounds.
- When a child reaches a terminal, idle, or errored state, call
  `interrupt_agent` before closeout so it is not left working.

## Flow

1. Read workspace rules.
2. Classify the delegation mode:
   - `planning/read-only`: define the permitted inspection or documentation
     scope; no approved SOW is required and implementation writes are forbidden
   - `implementation`: locate the approved SOW and verify that it covers the
     exact delegated write scope
3. Select the requested native sub-agent; use GLM5.2 exactly when requested.
4. Start the sub-agent with `spawn_agent`, a bounded prompt, and clear ownership.
   Pass a registered custom role such as GLM5.2 through `agent_type`; use a model
   override only when the current tool schema exposes that selection as a model.
5. Wait only until a real decision point: completion, question, failure, or
   repair need.
6. On a question, provide the minimum approved clarification with
   `followup_task`; do not broaden scope.
7. On completion, independently review the diff, run implementation verification
   proportional to risk, record evidence, and complete a gap-finding pass.
8. If validation fails, send targeted repair feedback. Allow at most two repair
   rounds before local completion or escalation.
9. Interrupt the terminal child agent.
10. If validation passes, close the SOW and move it to the repo's `finished/`
    planning directory when it is complete.
11. If the owning plan has no active SOW left and the plan itself is complete,
    move that plan to the same `finished/` directory.

## Delegate Prompt Contract

Every implementation-delegate prompt must include:

- absolute SOW path and a direction to read it
- one-sentence intent
- exact write scope
- explicit out-of-scope paths or behavior
- required verification and evidence to return
- instruction to stop and ask when scope, approval, or required evidence is
  missing

Require the sub-agent to return: changed files, verification performed,
remaining risks, and any decision that needs coordinator or user approval.

## Validation Matrix

Use repo-specific commands when available. These are minimum hints and never
replace the `task-execution-flow` hard gates:

- `docs-only`: `git diff --check` plus one focused cross-reference or grep check
- `frontend`: targeted build, test, or route/component check for the touched surface
- `backend`: targeted module test or `uv run pytest ...` for the changed area
- `migration`: backward-compat check plus one scan for legacy markers or old paths

Do not close delegated implementation when any of these are missing:

- a real runtime scenario for changed runtime behavior
- multi-step runtime evidence for async, stateful, UI, or performance work
- verification against the SOW behavior lock
- a post-implementation gap-finding pass

If required verification is unavailable, stop at
`implemented but not fully verified` and list the unverified scope.

## Termination Policy

- `quality`: allow up to 2 repair rounds, then finish locally or stop
- `infra`: if scope is already clear, finish locally instead of waiting on
  sub-agent recovery
- `uncertainty`: answer once; if the task is still ambiguous, stop and escalate
- `unavailable requested model`: report the model unavailability; do not silently
  substitute another model
- `scope drift`: interrupt the sub-agent, preserve valid scoped work, and repair
  locally or stop for a SOW update
