# Skill Design Decisions

This file records the main design decisions and reasons behind the custom workflow skills currently centralized in this repository:

- `task-router-flow`
- `sow-delegate-flow`

The goal is to preserve enough context that future refinements can continue from the current design without reconstructing the original conversations.

## 2026-09-15 Workflow Contract Consistency (SOW_0082)

- Keep the six workflow skills separate. Execution owns completion semantics;
  progress presents evidence-backed state and remains usable standalone.
- Treat required verification failures as blocking; non-blocking risks require
  explicit acceptance authority and a recorded follow-up. A severity label alone
  cannot waive a done criterion.
- Preserve unrelated work and its staging; evaluate the candidate commit content
  rather than assuming the dirty worktree is identical to the deliverable.
- Inline the tiny router/delegate commentary rule instead of installing a shared
  rule dependency. Duplication of two lines avoids external policy ownership.
- Browser cleanup follows task-session ownership. Global cleanup is an explicit
  user action, never an automatic recovery step.
- Review mode is provisional until evidence supports a conclusion; inventory and
  execution summaries use different table shapes.

## 2026-07-08 Active Distribution Decision

Decision:
- AISkills is a portable skill library, not a repo-owned telemetry or dashboard product.
- `telemetry-flow`, Codex hook templates, telemetry parsers, and the local dashboard runtime are retired from active maintenance in this repo.
- Detailed telemetry history is retained in finished planning docs only.
- AI-agent installation should follow `INSTALL_FOR_AGENTS.md` and `skills/registry.json`.
- Local Python sync scripts remain optional cloned-repo utilities that copy skill directories only.
- `create-agents-md` is retired; this repo no longer ships a skill that creates project policy files.

Reason:
- External OSS tooling now owns telemetry/dashboard behavior better than this repo should.
- Installation should be readable by Codex, Claude Code, OpenCode, and other agents without assuming a cloned repo or a Python script path.
- Project policy bootstrap is separate from skill installation.

## 1. Role Separation

Decision:
- `task-router-flow` is the front-door routing skill.
- `sow-delegate-flow` is the downstream execution skill for multi-SOW plans.

Reason:
- Routing and execution are different concerns.
- Mixing them made the workflow vague and harder to trigger correctly.
- The split lets one skill decide the branch and another run the approved execution flow.

## 2. Task Router Trigger

Decision:
- `task-router-flow` should trigger only when:
  - the user makes a real work request
  - the request may require a new SOW, an extension to existing scoped work, a debug/fix path, or docs/plan edits
  - the correct workflow branch has not yet been chosen

Final trigger sentence:
- `Use this skill when the user makes a work request that may require creating a new SOW, extending an existing SOW, debugging toward a fix, or editing docs/plan files, and the correct workflow branch has not yet been chosen.`

Reason:
- This keeps normal chat and simple Q&A from accidentally triggering the routing skill.
- The skill should only act as the intake gate for actual work state changes.

## 3. Task Router Branch Model

Decision:
- `task-router-flow` uses four branches:
  - new code change
  - existing scoped work change
  - debug request
  - docs / SOW / plan only

Reason:
- These four branches covered the repeated patterns seen in real usage.
- They are easier to reason about than one generic "make SOW or code" workflow.

## 4. SOW Definition Moved To Reference

Decision:
- The definition of SOW should not live inline inside `task-router-flow/SKILL.md`.
- It should live in a dedicated reference file and be linked from the skill.

Reason:
- Keeps `SKILL.md` short.
- Makes the SOW definition reusable.
- Avoids repeating template and lifecycle logic in multiple skills.

Current reference:
- `skills/task-router-flow/references/scope-of-work.md`

## 5. SOW Means Approved Task Contract

Decision:
- A SOW is the approved task contract for a concrete change.
- For code-changing work, implementation should not start until the active SOW is approved.
- Docs/plan/SOW-only edits normally do not require a new SOW.

Reason:
- This prevents SOWs from turning into vague notes.
- It makes the approval boundary explicit.

## 6. Plan Before SOW When Work Belongs To A Plan

Decision:
- If code change relates to an old SOW that belongs to a plan, extend the plan first.
- Then update the aligned SOW under that plan.
- Only extend a standalone SOW directly when the work is not plan-owned.

Reason:
- Extending only the SOW can make the parent plan drift away from the real execution state.
- The plan must remain the higher-level source of orchestration truth.

## 7. SOW Indexing

Decision:
- Every new SOW should use a unique 4-digit index from `0001` to `9999`.
- Recommended naming shape: `SOW_0001_short_name.md`.

Reason:
- Stable IDs are easier to reference in skills, summaries, and reviews.
- Plain free-form SOW names become harder to track over time.

## 8. Delegate Flow Trigger

Decision:
- `sow-delegate-flow` activates when the user explicitly delegates a task, SOW,
  or plan to a native Codex sub-agent or a custom/external agent through a
  supported transport, including GLM5.2 when registered natively.
- Implementation delegation requires an approved SOW. Review, investigation,
  plan drafting, and SOW drafting may be delegated before approval without
  implementation writes.
- The coordinator must classify `planning/read-only` versus `implementation`
  before spawning the child, so planning delegation does not inherit an
  implementation-only approval gate.
- The coordinator must classify native versus external transport before
  starting the delegate and enforce a fresh session for every new logical task
  on a non-native custom agent.

Reason:
- Explicit user delegation is the authority to use a sub-agent.
- Approval gates implementation authority, not read-only or planning work.

## 9. Approved SOW Is The Execution Source Of Truth

Decision:
- During delegate execution, the approved SOW is the source of truth for implementation scope.

Reason:
- This is the main guardrail against delegate drift.
- The delegate prompt should be short and point to the SOW path instead of pasting the whole task definition inline.

## 10. Precedence Rule

Decision:
- `AGENTS.md` / repo rules define process constraints and guardrails.
- The approved SOW defines the current task scope and deliverables.
- The coordinator remains responsible for sub-agent selection, scope, review,
  verification, repair decisions, and closeout.

Reason:
- Without an explicit precedence rule, conflicts between repo rules and delegate context become ambiguous.

## 11. Delegate Handoff Contract

Decision:
- Every delegate handoff should report the transport used, safe session lifecycle
  state, changed files, verification performed, remaining risks, and decisions
  needing coordinator or user approval.
- Native child status and final handoff are the normal evidence source for the
  native branch; external transports should return an equivalent bounded status.
- The coordinator must independently inspect the diff and verification evidence.

Reason:
- Native child-agent status and final responses already provide the lifecycle
  boundary. External transports may expose a different status shape, so the
  contract stays semantic rather than adopting a provider-specific schema.
- Delegate completion does not prove SOW completion.

## 12. Advice Loop And Feedback Loop

Decision:
- A sub-agent may ask for advice or report unresolved decisions.
- If a sub-agent says done but validation fails, Codex should send repair feedback and continue.
- `delegate done` is not equal to `SOW done`.

Reason:
- This mirrors a practical advisor/executor pattern.
- The coordinator must remain responsible for acceptance, not the delegate.

## 13. Failure Classes

Decision:
- Failures are grouped into:
  - `infra`
  - `quality`
  - `uncertainty`

Reason:
- Different failure classes need different control logic.
- This removed ambiguity from fallback decisions.

## 14. Validation Matrix

Decision:
- Validation should vary by SOW type:
  - docs-only
  - frontend
  - backend
  - migration
  - external-custom, including fresh-session and task-owned cleanup evidence
- Delegated implementation must also satisfy `task-execution-flow` runtime
  verification, evidence, gap-finding, and closeout hard gates.

Reason:
- One generic "run something" rule left too much operator judgment.
- A lightweight validation matrix makes closeout more repeatable.

## 15. Termination Policy

Decision:
- `quality`: allow up to 2 repair rounds, then finish locally or stop
- `infra`: if scope is clear, finish locally
- `uncertainty`: answer once; if still ambiguous, stop/escalate
- `unavailable requested model`: report it without silent model substitution
- `unavailable requested transport or fresh-session guarantee`: report it
  without reusing an old session or historical task context
- `scope drift`: interrupt the child and repair locally or update the SOW

Reason:
- Explicit stop conditions reduce ceremonial loops and make the workflow more predictable.

## 16. Delegate Transport And Session Lifecycle

Decision:
- Use native Codex sub-agent tools for spawn, wait, follow-up, and interrupt.
- Resolve user-named agents from the current session's catalog.
- When GLM5.2 is exposed as `router_custom_greennode_glm_5_2`, pass that role as
  `agent_type`; do not treat that role name as globally portable.
- A custom-named role is still native when it is exposed in that catalog; the
  transport, not the display name, determines the lifecycle.
- For a custom/external agent that is not native, use the requested documented
  CLI, process, or provider transport. Every new logical task must initialize a
  brand-new provider-owned session with no old task history, resume, continue,
  inherited session ID, or prior transcript.
- A same-task follow-up may reuse only that just-created session while its
  identity and isolation remain provable; otherwise start another fresh session.

Reason:
- Native lifecycle tools avoid provider-specific CLI, transcript, and parser
  coupling, while the external branch permits the user's selected transport
  without making one provider's command syntax canonical.
- Catalog resolution preserves the requested model while tolerating role-name
  changes across environments. Fresh external sessions prevent compaction and
  historical chat from contaminating a new delegated task.

## 17. Delegate Progress And Repair

Decision:
- Wait until completion, an advice request, failure, or repair need on either
  native or external transport.
- Use follow-up on the same native child or the same-task fresh external session
  for clarification or targeted repair; never attach an older task session.
- Allow at most two quality repair rounds.

Reason:
- The coordinator needs actionable state, not provider transport noise, while
  external follow-up remains bounded by the fresh-session rule.

## 18. No Provider-Specific Delegate Log Pipeline

Decision:
- Do not require Claude CLI, stream JSON, raw delegate logs, or a parser for the
  native sub-agent flow.
- Child-agent status and final handoff are the normal evidence source.
- The external/custom branch may use a provider CLI, process, or session
  lifecycle when the user selects one, but the generic skill must not require a
  specific provider, command syntax, log format, or parser.

Reason:
- Provider-specific transport artifacts duplicate the native coordinator
  lifecycle and create stale maintenance surfaces. Keeping external transport
  selection explicit preserves portability while still requiring fresh-session
  isolation.

## 19. Delegate Hygiene

Decision:
- Give each child one bounded SOW or non-overlapping ownership slice.
- Interrupt terminal, idle, or errored native children before closeout.
- Terminate only the task-owned external process or provider session before
  closeout; never perform global provider cleanup.

Reason:
- Bounded ownership prevents conflicting writes.
- Explicit cleanup prevents completed children from remaining active.

## 20. Code Context Benchmark Result

Decision:
- Do not adopt code-index tooling into the default delegate loop yet.
- Native tool usage remains the default.

Reason:
- A fair comparison against `cocoindex-code` and `cased/kit` did not justify making them part of the standard flow for this repo.

## 21. Datamart Review Owns One Merged Impact Matrix

Decision:
- `datamart-design-review` is a specialized AISkills-owned skill rather than an
  extension of the generic task review skill.
- A datamart impact report uses one merged table-and-column matrix covering
  lifecycle, grain, refresh, physical type, formula, reason, downstream migration
  and evidence status.
- The skill distinguishes observed source grain, proposed output grain and
  business-approved grain; runtime-dependent claims remain `UNVERIFIED` without
  exact evidence.

Reason:
- Generic task review should not carry domain-specific analytical modeling
  contracts or trigger on unrelated reviews.
- A single matrix keeps table lifecycle and column semantics traceable without
  forcing readers to reconstruct impact across separate summaries.
- Snapshot uniqueness and repository SQL are useful evidence but do not establish
  a timeless business grain or deployed target contract.

## 24. Centralization Strategy

Decision:
- Custom workflow skills should be centralized into `AISkills`.
- Built-in or third-party skills are not copied by default.

Reason:
- Only the custom design surface should be versioned and shared from this repo.
- Pulling in built-in or curated skills would blur ownership and add noise.

## 25. Agent Instruction File Targets

Date: 2026-07-07

Related SOW:
- `SOW_0061_agent_instruction_file_targets.md`

Decision:
- `TEMPLATE_AGENTS.md` remains the shared canonical policy template.
- Project policy bootstrap is separate from skill installation.
- This repo no longer ships a skill that creates `AGENTS.md`, `CLAUDE.md`, or other policy files.
- `INSTALL_FOR_AGENTS.md` is the primary agent-facing install guide for skills.

Reason:
- OpenAI Codex official docs identify `AGENTS.md` as project guidance: https://developers.openai.com/codex/guides/agents-md
- OpenCode official docs use `AGENTS.md` for custom rules: https://opencode.ai/docs/rules/
- Claude Code official docs use `CLAUDE.md` memory files and support `@path/to/import` from `CLAUDE.md`: https://code.claude.com/docs/en/memory
- Keeping one shared `AGENTS.md` policy plus tool entrypoint files reduces drift across Codex, OpenCode, and Claude Code.
- Skill installation should not mutate policy files unless a future approved SOW reintroduces a dedicated project-policy bootstrap flow.

## Related SOW Trail

The following finished SOWs capture the main implementation trail behind the current design:

- `SOW_0003_claude_delegate_probe.md`: initial Claude CLI delegation probe
- `SOW_0004_sow_delegate_flow_skill.md`: initial `sow-delegate-flow` build
- `SOW_0005_sow_delegate_flow_wording_trim.md`: wording reduction for lower context cost
- `SOW_0006_sow_delegate_flow_advisor_session.md`: advisor loop and session handling
- `SOW_0007_sow_delegate_flow_session_compaction.md`: compact-and-refresh session policy
- `SOW_0008_code_context_benchmark.md`: retrieval benchmark behind the native-tool default decision
- `SOW_0009_sow_delegate_flow_guardrails.md`: precedence, scope, validation-hint, failure class guardrails
- `SOW_0010_task_router_flow_skill.md`: initial `task-router-flow` build
- `SOW_0011_task_router_flow_plan_and_indexing.md`: plan-first updates and 4-digit SOW indexing
- `SOW_0012_sow_delegate_flow_json_first.md`: `json` default, `stream-json` only for deeper debugging
- `SOW_0013_sow_delegate_flow_output_filtering.md`: mandatory filtering of noisy delegate output
- `SOW_0014_sow_delegate_flow_log_parser.md`: first raw-log-first parsing design for Claude
- `SOW_0015_codex_otel_session_metrics.md`: first Codex session telemetry experiment
- `SOW_0016_codex_rollout_metrics_refactor.md`: switch from OTel to rollout-history metrics for Codex
- `SOW_0017_sow_delegate_flow_claude_raw_only.md`: Claude parser refactor to raw-only persistence
- `SOW_0018_sow_delegate_flow_refinements.md`: validation matrix, termination policy, and closeout template refinements
- `SOW_0019_telemetry_hook_skill_v1.md`: separate telemetry skill with start/finish hooks and run-level metrics
- `SOW_0061_agent_instruction_file_targets.md`: target-specific instruction filenames for Codex, OpenCode, Claude Code, shared, and custom modes

Use these SOWs as the primary historical trail when a later change needs original rationale beyond the summary decisions in this file.
