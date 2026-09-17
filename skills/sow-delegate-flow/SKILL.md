---
name: sow-delegate-flow
description: Use when the user asks to delegate a task, SOW, or plan to a native Codex sub-agent or custom external agent through a supported transport, especially GLM5.2 when registered natively. Keep approved SOWs authoritative, give each delegate a bounded ownership slice, initialize fresh non-native sessions, then review and verify locally.
---

# Sow Delegate Flow

Use this skill for native Codex or custom/external delegation:

```text
coordinator -> classify mode + transport
    -> native child lifecycle OR fresh external task session
    -> local review and verification -> repair or closeout
```

Keep execution-time commentary to one short sentence about status, next action
or a blocker. Keep the final response separate.

## Precedence

- `AGENTS.md` and repo rules define process constraints and guardrails.
- The approved SOW defines the active task scope and deliverables.

## Trigger And Routing

Activate when the user explicitly asks to delegate, assign, or hand off a task,
SOW, or plan to a native or custom/external agent. Treat these as direct
triggers:

- `delegate task ... cho GLM5.2`
- `delegate SOW ... cho GLM5.2`
- `delegate plan ... cho GLM5.2`
- `delegate task ... cho custom agent via CLI`
- an equivalent request naming a native or external agent

Do not activate for ordinary single-agent execution or a request merely
mentioning another model.

- Resolve the requested target against the current native agent catalog first.
  A custom-named role is native when the catalog exposes it; use the native
  lifecycle in that case. For `GLM5.2`, pass the currently registered role such
  as `router_custom_greennode_glm_5_2` as `agent_type`; never assume a role name
  is portable across environments.
- If the target is not native and the user selects a custom/external agent, use
  an available documented provider transport such as a CLI or process. Do not
  silently substitute another agent or transport.
- If the requested target or transport is unavailable, report it and stop; do
  not reuse an old session as a fallback.
- Delegating an implementation requires an approved SOW. A delegate may inspect
  or draft a plan/SOW before approval, but must not modify product code, tests,
  scripts, config, or runtime contracts in that mode.

## Session Boundary For Non-Native Agents

- Every new logical task delegated to a non-native custom agent **MUST** start a
  brand-new provider-owned session before the task prompt is sent.
- Use the provider's documented new-session mechanism and a unique task-owned
  identifier when the transport supports one. Do not guess provider flags.
- Never attach historical chat, an old task/thread/session ID, persisted task
  context, a resume/continue operation, or a prior transcript. A new process is
  not sufficient if it restores persisted history.
- Keep the fresh session bounded to this logical task and record only a safe
  session handle or lifecycle state; never persist secrets or full transcripts.
- A same-task follow-up may reuse only the fresh session created for that task
  while its identity and isolation remain provable. If it was compacted, has
  stale or wrong-task history, or isolation is uncertain, start another fresh
  session with a concise coordinator handoff.
- Native Codex children use the native lifecycle; do not create an external
  provider session for them.

## Rules

- Keep the approved SOW as the source of truth for the current implementation.
- Do not delegate implementation before approval. Scoped inspection, review,
  plan drafting, and SOW drafting may be delegated before approval when they do
  not modify implementation surfaces.
- Read local repo rules and inspect `git status --short` before delegating.
- Classify the transport before starting and enforce the non-native session
  boundary before sending any delegated prompt.
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
- When a native child reaches a terminal, idle, or errored state, call
  `interrupt_agent`; for an external delegate, terminate only the
  task-owned process or provider session before closeout.

## Flow

1. Read workspace rules.
2. Classify the delegation mode:
   - `planning/read-only`: define the permitted inspection or documentation
     scope; no approved SOW is required and implementation writes are forbidden
   - `implementation`: locate the approved SOW and verify that it covers the
     exact delegated write scope
3. Resolve the target transport:
   - native: select the requested role from the current catalog; use GLM5.2
     exactly when requested
   - external/custom: select an available documented CLI, process, or provider
     transport without silently substituting another one
4. Establish the session before sending the prompt:
   - native: use the native lifecycle; do not create an external session
   - external/custom: initialize a brand-new session under the Session Boundary
     rules and stop if fresh isolation cannot be proven
5. Start the delegate with a bounded prompt and clear ownership. Use
   `spawn_agent` for native children; use the selected documented transport for
   external agents and record only a safe task-owned handle.
6. Wait only until a real decision point: completion, question, failure, or
   repair need.
7. On a question, provide the minimum approved clarification with
   `followup_task` for native work or the equivalent same-session transport for
   external work; do not broaden scope or attach old task history.
8. On completion, independently review the diff, run implementation verification
   proportional to risk, record evidence, and complete a gap-finding pass.
9. If validation fails, send targeted repair feedback. Allow at most two repair
   rounds before local completion or escalation.
10. Clean up the delegate: interrupt the native child, or terminate only the
    task-owned external process/session.
11. If validation passes, close the SOW and move it to the repo's `finished/`
    planning directory when it is complete.
12. If the owning plan has no active SOW left and the plan itself is complete,
    move that plan to the same `finished/` directory.

## Delegate Prompt Contract

Every delegated prompt must include:

- one-sentence intent
- transport and lifecycle instruction:
  - native: use the selected native role and lifecycle only
  - external/custom: start a fresh session with no historical task context
- instruction to stop and ask when scope, approval, or required evidence is
  missing

Implementation-delegate prompts must also include:

- absolute SOW path and a direction to read it
- exact write scope
- explicit out-of-scope paths or behavior
- required verification and evidence to return

Require the delegate to return: transport used, safe session lifecycle state,
changed files, verification performed, remaining risks, and any decision that
needs coordinator or user approval. Do not request raw historical transcripts.

## Validation Matrix

Use repo-specific commands when available. These are minimum hints and never
replace the `task-execution-flow` hard gates:

- `docs-only`: `git diff --check` plus one focused cross-reference or grep check
- `frontend`: targeted build, test, or route/component check for the touched surface
- `backend`: targeted module test or `uv run pytest ...` for the changed area
- `migration`: backward-compat check plus one scan for legacy markers or old paths
- `external-custom`: execute a real task scenario when behavior changes, verify
  fresh-session evidence and absence of prior task context, then clean up only
  the task-owned process or session

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
- `unavailable requested transport or fresh-session guarantee`: report it and do
  not reuse an old session or historical task context
- `scope drift`: interrupt the sub-agent, preserve valid scoped work, and repair
  locally or stop for a SOW update
