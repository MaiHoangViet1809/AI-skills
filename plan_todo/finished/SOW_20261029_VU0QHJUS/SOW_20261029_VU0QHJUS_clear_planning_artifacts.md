# SOW_20261029_VU0QHJUS - Clear Planning Artifacts

- Status: DONE
- Approval: APPROVED by user
- Proposed-By: Codex
- create_dttm: 2026-10-29T11:59:15+07:00
- approve_dttm: 2026-10-29T12:36:00+07:00
- finish_dttm: 2026-10-29T12:49:58+07:00
- Plan / Reference: Standalone; `SOW_20261007_HU2ZJ4QS` (planning bundle contract).

## Task / Why

Make SOW, Plan, EXT, decision and finding records short, clear, template-compliant and easy for humans and agents to understand. Current templates specify required content but do not consistently guide concise authoring; the exact cause of verbose output is unverified.

## As-Is → To-Be

```text
Request → planning templates → potentially verbose records
Request → applicable template + shared writing guidance
        → concise record → unambiguous execution and review
```

## Location

- `skills/task-router-flow/SKILL.md` and `skills/task-router-flow/references/{scope-of-work,plan,planning-bundles}.md`: apply guidance at the appropriate authoring point.
- `skills/task-review-investigate-compare/SKILL.md`: only if needed to cover finding authoring without conflicting or duplicating existing rules.
- `skills/task-execution-flow/SKILL.md`: apply the same guidance during execution writeback, including project-owned templates.
- `tests/skill_feedback_cases/` and existing relevant tests: scenarios and verification.
- This SOW bundle: progress and evidence.

## Deliverables

- One coherent writing principle across all five artifact types: use the applicable project template, concise language and ASCII diagrams when they clarify flow, relationships or decisions; retain enough text for precise agent execution.
- Avoid repeated facts across artifacts: link to the owning record, retain the context needed locally. No arbitrary word or line limit.
- Preserve scope, required fields, lifecycle, approvals, decisions, risks, evidence, provenance and historical records; do not turn diagrams into a substitute for critical contracts.
- Place shared guidance at its appropriate owner and link consumers as needed; preserve project authority and current concurrent changes.
- Ensure project-owned templates and review/finding workflows reach the guidance without replacing project authority.

## Done Criteria

- Review representative SOW, Plan, EXT, decision and finding examples against their existing templates: concise, readable, required meaning and approval boundaries intact.
- Trace the writing entry points for all five artifact types, including project-owned templates and review findings; verify the shared guidance is reachable without changing project authority.
- Trace execution-time writeback when a project supplies its own planning contract.
- Include expected, negative and boundary feedback cases: verbosity/repetition; over-compression that removes evidence or scope; diagram unsuitable or insufficient.
- Run skill structural validation and affected feedback/contract tests; inspect the scoped diff. Distinguish static checks from any independently observed agent behavior.

## Out-of-Scope

- Editing skills before approval; bulk rewriting historical records; changing templates' mandatory fields or lifecycle semantics; altering other projects; sync/deploy or push without a separate request.

## Cautions / Risks

- Over-compression may hide important decisions or acceptance criteria; excessive diagrams can obscure simple facts.
- Router references already contain concurrent uncommitted changes; reconcile and preserve them, never overwrite.

## Progress

- progress_updated_dttm: 2026-10-29T12:49:58+07:00

| Item | Status | Evidence / Pending reason | Next action / Owner |
| --- | --- | --- | --- |
| T1: Guidance and verification | DONE | Router and review guidance; feedback case; 27 tests and two skill validators pass; diff checked | None |
| T2: Execution writeback gap | DONE | Execution entry point and feedback case added; 27 tests and validator pass | None |

First completion at 2026-10-29T12:36:53+07:00 was premature: execution with a project-owned contract could bypass the guidance. Actual future agent adherence is not proven by static checks. Delegation: side-conversation restriction; local review.
