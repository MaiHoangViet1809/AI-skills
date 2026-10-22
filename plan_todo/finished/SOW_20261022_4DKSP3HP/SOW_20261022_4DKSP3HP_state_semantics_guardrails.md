# SOW_20261022_4DKSP3HP — State Semantics and Lifecycle Acceptance Guardrails

- Status: done
- Approval: approved by user; implementation, commit, push, and Codex skill sync
- create_dttm: 2026-10-22T18:21:15+07:00
- approve_dttm: 2026-10-22T18:27:54+07:00
- finish_dttm: 2026-10-22T18:52:32+07:00
- Proposed-By: Codex
- Plan / Reference: standalone; follows SOW_20260917_V7HK7IAU and the sanitized working-copy visibility incident discussed on 2026-10-22. References establish evidence, not ownership or inherited approval.
- Decision Log: material choices are specified below; no separate decision file required.

## Task

Clarify how review and execution distinguish consumer-visible state semantics from implementation control state, add lifecycle-composition acceptance cases, and mirror one portable rule in the repository policy/template.

## Why / Evidence

The observed incident received a dirty working revision but continued rendering committed content. Source inspection established a path where a request-generation counter also gated visibility: automatic commit-follow advanced it without restoring eligibility for the next edit. The exact navigation that triggered the reported screenshot was not traced, so this path is a confirmed code defect, not a claim of full runtime causality. A later proposal preserved the unsupported viewing gate instead of first rechecking the requested semantics.

The review and execution skills already require consumer-contract checks, proportional runtime verification, and gap-finding. This is an application failure with a specific procedure gap, not proof of missing skill loading, compaction, or a general need for stronger MUST language. Existing tests/review could verify the chosen gate while missing whether that gate was justified and whether edit/save/edit composition preserved the outcome.

Preflight on 2026-10-22:

- Ownership resolved in `skills/registry.json`; both target skills are AISkills-owned.
- Installed review skill matches canonical. Installed execution differs by unrelated Redmine tracking additions in canonical; that drift does not explain this incident and is not part of this change.
- `AGENTS.md` and `TEMPLATE_AGENTS.md` currently match. No target principle document, applicable nested rules, or declared concept authority was discovered; no Concept Compliance section is activated.
- Canonical execution skill and several unrelated files already have foreign changes. Preserve those hunks; do not stage whole mixed files or synchronize their incidental content.
- No local `docs/planning/README.md` exists. Use the installed task-router planning-bundles and scope-of-work contracts with the existing `plan_todo/active/` layout.

## Location

Implementation, only after explicit SOW approval:

- `skills/task-review-investigate-compare/SKILL.md`
- `skills/task-execution-flow/SKILL.md`
- `AGENTS.md` and `TEMPLATE_AGENTS.md` — identical short rule in existing design/verification sections only.
- `tests/skill_feedback_cases/task-review-investigate-compare.json`
- `tests/skill_feedback_cases/task-execution-flow.json`
- This SOW bundle: base document and `review.md`.
- Codex deployment targets: `~/.codex/skills/task-review-investigate-compare/` and `~/.codex/skills/task-execution-flow/` only, using a temporary export of the committed source and existing sync/verifier scripts.

No other skill, metadata, script, test implementation, registry, or project file is authorized by this SOW.

## As-Is Diagram (ASCII)

```text
consumer outcome
  -> agent-selected gate enters design/SOW
  -> implementation + isolated scenarios match that gate
  -> PASS despite composed user workflow violating outcome

request-generation / cancellation marker
  -> accidental business/view eligibility
  -> accepted new content can remain invisible
```

## To-Be Diagram (ASCII)

```text
explicit consumer outcome + governing constraints
  -> trace each outcome-blocking gate to its authority
  -> distinguish business state from request-control state
  -> reject unsupported gate OR surface genuine contract conflict
  -> verify transitions AND next operation after transition
  -> compare observed outcome with consumer contract, not gate itself
```

## Deliverables

### D1 — Review decision point

Extend the existing Consumer Contract / Outcome Path guidance, not a new workflow layer:

- For a proposed state-dependent gate, identify its user-visible effect and supporting explicit contract or concrete governing constraint.
- Verify the evidence for that constraint; safety/robustness labels and implementation convenience alone do not establish necessity. Automatic transitions and explicit user actions sharing one helper are not evidence of identical user intent.
- Distinguish persisted/domain state, displayed content, and request-control tokens when they affect the outcome. Do not infer user intent from a technical counter, token, cache state, or component lifecycle.
- A control token may reject stale/wrong-scope results; it must not silently introduce a new business permission, opt-in, or display prerequisite.
- Check proposal semantics against the explicit consumer contract even when an existing SOW or old test encodes the gate. If they materially conflict, identify the conflicting requirements and obtain a decision; neither silently override approved scope nor treat document consistency and passing tests as proof that the outcome is correct. An explicitly approved contract change remains valid and must not prompt redundant approval.
- Following a correction that challenges the model itself, reassess the outcome and owner before proposing another flag, mode, wrapper, or callback patch.

### D2 — Execution acceptance composition

Tighten existing behavior-lock and stateful verification instructions:

- Derive expected outcomes independently from the relevant explicit contract, not only from implementation branches or fixtures asserting those branches.
- For changed stateful behavior, exercise a proportional lifecycle sequence and a repeated operation after a meaningful transition; record the expected/observed consumer result.
- Incident example: modify -> visible unsaved content -> explicit save -> same visible content -> modify again -> immediately visible next change without reopen, re-arm, reload, or a second save.
- Preserve negative/boundary checks: stale responses, another identity/scope, rejected invalid content, and logout must not replace the current authorized view. Do not use this lesson to bypass validation or isolation.
- A missing required sequence leaves that behavior unverified; it does not force full Cartesian state exploration or a general benchmark framework.
- Keep product-specific transition outcomes conditional on the actual contract. A failed save retaining unsaved changes is part of the incident/example walkthrough, not a new universal transaction or recovery guarantee imposed on every product.

### D3 — Portable guardrail / rule

Add the same concise rule to `AGENTS.md` and `TEMPLATE_AGENTS.md`, with detail kept in the two skills:

> Implementation control state must not silently redefine the explicit consumer contract. Justify outcome-blocking gates using governing requirements or constraints, and verify affected stateful workflows across transitions, including the next repeated operation. Preserve legitimate validation, isolation, and stale-response protections.

This rule is general; it does not prescribe dashboard rendering, automatic history switching, persistence architecture, SSE, Pinia, or a save model for other products.

### D4 — Sanitized regression cases

Before behavior-bearing edits, append one case per existing fixture:

- `consumer-state-gate-authority-001` in the review fixture.
- `stateful-transition-repeat-001` in the execution fixture.

Each case follows the existing schema with expected, negative, and boundary scenarios. Include a second generic domain, such as an unsaved document preview, so the rule is not encoded as a dashboard-only workaround. No raw conversation, credentials, private identifiers, or machine-specific paths.

### D5 — Authorized delivery

After checks pass, commit only owned changes, push main to origin, then sync the two changed skills separately to the existing Codex legacy-user root. The user also explicitly approved pushing the pre-existing local commit `1ebefbf` with this delivery. No other uncommitted work may be committed or pushed.

Use a temporary export of the exact committed skill directories and existing sync/verify scripts so foreign uncommitted Redmine hunks are not deployed. Preview each single-skill command with `--dry-run --overwrite`, execute without `--dry-run`, and verify no missing/extra/changed files against that committed export. Remove the temporary packaging export after delivery. Do not modify sync tooling or another environment. Policy/template changes remain canonical in AISkills, not a global Codex policy overwrite.

## Done Criteria

1. D1/D2 are short edits at existing action points; no duplicate broad workflow, new skill, mandatory diagram artifact, or blanket ban on technical guards.
2. Both stable case IDs exist, are globally unique, and cover intended behavior, the incorrect gate/isolated-test false pass, and a legitimate security/validation boundary.
3. A source walkthrough rejects the unsupported visibility gate while retaining stale-response fencing; it distinguishes a documented constraint from an inferred convenience rule.
4. Scenario review covers modify/save/modify, save failure with unsaved work retained, invalid/stale/wrong-scope responses, and a contract where explicit preview confirmation is genuinely required. Do not impose the incident's semantics on that boundary product.
5. Policy mirror remains byte-identical (`cmp -s AGENTS.md TEMPLATE_AGENTS.md`). No task-specific incident rule is added to portable policy.
6. Use skill-creator and its available structural validator for both edited skills; run `uv run python -m unittest tests.test_skill_feedback_cases tests.test_skill_sync_scripts` and `git diff --check`. Update no validator/test code just to pass.
7. Separate structural validation and scenario reasoning from actual model behavior. No fresh-model forward-test or application runtime acceptance is claimed without an authorized observed run.
8. Final diff preserves foreign hunks and contains only authorized changes. Commit, then push the approved history to origin, then sync D5 and verify exact committed-source parity for both Codex skills. If delivery is partial, keep its status open and report the failed step; no unrelated policy/config installation.

## Out-of-Scope

- XVision source, tests, concepts, Plan/SOW status, runtime, DB, Agent sessions, or actual bug repair.
- Any new service/runtime, Git branch, sub-agent, or independent-model review in this side conversation.
- Changes to skill-evolution-flow, task-router-flow, diagram, governance, delegation, or system/plugin-owned skills.
- Registry, discovery metadata, Redmine changes, telemetry, persistent failure stores, new orchestration, or universal UI state machine.
- Sync/install/deploy beyond D5's two selected Codex skills; adoption of the new policy in other repositories or global Codex policy/config.

## Cautions / Risks

- Existing protections can be valid; a technical field is not wrong merely because it participates in eligibility. The defect is unjustified or contract-violating semantics, not the use of counters.
- Review must not invent missing user intent or reinterpret a genuine approved design change as a coding bug. Resolve a material conflict before implementation.
- Fixture validation does not demonstrate model adherence. No guaranteed-prevention claim.
- Preserve unrelated execution-skill hunks and policy ownership; stop if a mixed hunk cannot be safely separated.
- Approval now covers implementation and D5 delivery. It does not authorize product repair or distribution of unrelated uncommitted changes.

## Progress

- progress_updated_dttm: 2026-10-22T18:52:32+07:00

| Item | Status | Evidence / Pending reason | Next action / Owner |
| --- | --- | --- | --- |
| P1 scope/evidence | DONE | Canonical ownership, installed drift, existing gates, and incident path inspected | Preserve scope / Codex |
| P2 self-review 1 | DONE | review.md pass 1: causality bounded; approval/conflict semantics clarified | None |
| P3 self-review 2 | DONE | review.md pass 2: constraint evidence and contract-conditional lifecycle examples tightened | None |
| D1-D4 implementation | DONE | Two targeted skill additions, mirrored rule and two sanitized cases committed in a4789f1 | None |
| DC1-DC7 verification | DONE | Two structural validators, 13 tests, mirror/diff checks PASS; scenario reasoning recorded, model behavior not claimed | Preserve validation limits / Codex |
| D5 / DC8 delivery | DONE | a4789f1 pushed to origin/main; both selected Codex skills match exact committed export, no missing/extra/changed files; export removed | None |
