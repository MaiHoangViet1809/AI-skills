# Skill Design Decisions

This file records the main design decisions and reasons behind the custom workflow skills currently centralized in this repository:

- `task-router-flow`
- `sow-delegate-flow`
- `telemetry-flow`

The goal is to preserve enough context that future refinements can continue from the current design without reconstructing the original conversations.

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
- Stable IDs are easier to reference in skills, summaries, telemetry, and reviews.
- Plain free-form SOW names become harder to track over time.

## 8. Delegate Flow Trigger

Decision:
- `sow-delegate-flow` is intended for work executed as a plan with multiple sequential SOWs.

Reason:
- This is its real sweet spot.
- For single small tasks, the overhead is not worth it.

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
- `CLAUDE.md` provides Claude-specific helper context only.

Reason:
- Without an explicit precedence rule, conflicts between repo rules and delegate context become ambiguous.

## 11. Claude Structured Output Contract

Decision:
- Claude should return structured output with fields like:
  - `status`
  - `failure_type`
  - `changed_files`
  - `summary`
  - `open_questions`
  - `scope_respected`
  - `validation_hint`
  - `fallback_needed`

Reason:
- Machine-readable handoff is much more reliable than parsing free-form prose.
- It reduces noisy review loops and makes fallback logic deterministic.

## 12. Advice Loop And Feedback Loop

Decision:
- Claude may return `needs_advice` with `open_questions`.
- If Claude says done but validation fails, Codex should send repair feedback and continue.
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

Reason:
- One generic "run something" rule left too much operator judgment.
- A lightweight validation matrix makes closeout more repeatable.

## 15. Termination Policy

Decision:
- `quality`: allow up to 2 repair rounds, then finish locally or stop
- `infra`: if scope is clear, finish locally
- `uncertainty`: answer once; if still ambiguous, stop/escalate
- `rate-limit`: if partial diff is usable and scope is clear, finish locally

Reason:
- Explicit stop conditions reduce ceremonial loops and make the workflow more predictable.

## 16. JSON First, Stream Only For Debug

Decision:
- Claude CLI should use `json` output by default.
- Use `stream-json` only when deeper delegate debugging is needed.

Reason:
- `stream-json` produced too much event noise.
- `json` still captured limit errors and enough final metadata for the normal path.

## 17. Output Filtering Is Mandatory By Default

Decision:
- Captured delegate output should drop `system`-typed noise by default.
- Only keep normally dropped output when the flow or user explicitly requires it.

Reason:
- System/init payloads added context cost without helping normal review or fallback.

## 18. Claude Parsing Became Raw-Only

Decision:
- Claude telemetry/logging should keep only raw logs:
  - `~/.logs/codex/telemetry/claude/<project>/claude-<session-id>.log`
- No persisted parsed artifact by default
- No persisted Claude usage ledger by default
- Parse on demand using Python

Reason:
- Raw log is enough as source of truth.
- Persisting extra parsed files and ledgers created unnecessary file sprawl.

Relevant files:

## 19. Global Ledger Is The Dashboard Source Of Truth

Decision:
- Dashboard reads only from `~/.logs/codex/telemetry/runs/`
- project-local telemetry files are debug or backfill sources only

Reason:
- cross-project tracking is incomplete if the dashboard reads per-repo logs directly

## 20. Hook-Based Skill Pilot Starts With `task-router-flow`

Decision:
- the first hook-based skill telemetry pilot is `task-router-flow`
- current `sow-delegate-flow` keeps the explicit `start/finish` telemetry path
- the pilot uses Codex hook events to self-trigger telemetry for a skill-run session

Reason:
- this validates cleaner skill/session boundaries without risking the existing delegate flow

## 21. Prompt Marker Is The Pilot Routing Signal

Decision:
- `UserPromptSubmit` carries the pilot routing signal through a first-line marker like:
  - `CODEX_SKILL_RUN skill=task-router-flow ...`
- `Stop` finishes the same run

Reason:
- `UserPromptSubmit` and `Stop` are available now
- prompt metadata is a more reliable skill signal than guessing from later tool events
- `skills/sow-delegate-flow/scripts/parse_delegate_log.py`
- `skills/sow-delegate-flow/references/log-parsing.md`

## 19. Cost / Session Hygiene

Decision:
- Resume a delegate session only while it stays short and clean.
- If it gets long or noisy, compact the useful history and continue in a fresh session.

Reason:
- Long-running sessions accumulate context cost.
- Compact-and-refresh is usually cheaper than blindly resuming forever.

## 20. Code Context Benchmark Result

Decision:
- Do not adopt code-index tooling into the default delegate loop yet.
- Native tool usage remains the default.

Reason:
- A fair comparison against `cocoindex-code` and `cased/kit` did not justify making them part of the standard flow for this repo.

## 21. Telemetry Became A Separate Skill

Decision:
- Run-level telemetry should live in its own skill, not inside `task-router-flow` or `sow-delegate-flow`.

Reason:
- Execution and measurement are separate concerns.
- A separate skill is easier to reuse across different workflows later.

## 22. Telemetry Uses Two Hooks Only

Decision:
- `telemetry-flow` v1 should use exactly two hooks:
  - `start`
  - `finish`
- Reporting or aggregation is deferred to a later phase.

Reason:
- This keeps the first integration small.
- It captures the run facts needed for later dashboards without forcing reporting design too early.

## 23. Hybrid Run Matching

Decision:
- Use a staging record with `run_id` as the primary source of run identity.
- Use marker text in Codex rollout as a secondary cross-check and debug aid.

Reason:
- Marker-only matching is too fragile.
- Timestamp-only matching is not stable enough for repeated runs in the same repo.

## 24. Metrics Must Be Calculable

Decision:
- Telemetry metrics must be parsed or calculated from logs, timestamps, git state, or explicit workflow metadata.
- Do not add LLM-judged metrics such as quality scores or understanding scores.

Reason:
- Later dashboards need stable, reproducible numbers.
- Calculable metrics are easier to compare across runs, repos, and skills.

## 25. Codex Task Metric Must Be Task-Local

Decision:
- The main Codex task metric should be task-local turn usage inside the run window.
- Do not present cumulative session-token deltas as the primary per-task Codex metric.

Reason:
- Session-accumulated deltas are easy to misread as "token cost of one task."
- Task-local turn usage is much easier to interpret in dashboards and reviews.

## 26. Tool And MCP Metrics Belong In Telemetry

Decision:
- Run telemetry should include calculable tool and MCP call metrics for both Codex and Claude when event-level logs contain them.

Reason:
- Tool usage is part of the real cost and execution shape of an agentic run.
- These metrics are useful for later dashboards without requiring subjective scoring.
- Prompt narrowing and precise file/symbol targeting gave better ROI.

## 21. Codex Metrics Source Changed From OTel To Rollout History

Decision:
- Codex should be measured from native rollout history under:
  - `~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl`
- OTel is not required for the current Codex measurement path.

Reason:
- Rollout logs already contain:
  - session metadata
  - assistant and user messages
  - token counts
  - task completion
- OTel added setup complexity and did not preserve assistant marker text in a useful way.

Relevant file:
- `scripts/telemetry/parse_codex_rollout.py`

## 22. Marker Strategy For Codex

Decision:
- If marker-based measurement is needed, use rollout history as the detection surface.
- Do not rely on Codex OTel to preserve marker text.

Reason:
- A direct test showed marker text spoken in the conversation appeared in rollout logs but not in useful OTel fields.

## 23. Session-First Measurement

Decision:
- Measure Codex and Claude at the session level first.
- Map sessions to task/SOW efficiency later at the analysis layer.

Reason:
- This keeps telemetry collection simple.
- It avoids overfitting collection logic to every single downstream metric.

## 24. Centralization Strategy

Decision:
- Custom skills and telemetry design inputs should be centralized into `AISkills`.
- Built-in or third-party skills are not copied by default.

Reason:
- Only the custom design surface should be versioned and shared from this repo.
- Pulling in built-in or curated skills would blur ownership and add noise.

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

Use these SOWs as the primary historical trail when a later change needs original rationale beyond the summary decisions in this file.
