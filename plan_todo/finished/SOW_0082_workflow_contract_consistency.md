# SOW_0082 - Workflow Contract Consistency

## Lifecycle

- Status: done
- Approval: approved by user
- create_dttm: `2026-09-14T14:40:31+07:00`
- approve_dttm: `2026-09-15T10:40:01+07:00`
- finish_dttm: `2026-09-15T10:51:46+07:00`

## Task

Correct seven reviewed workflow gaps across six skills while preserving their
separate routing, execution, delegation, review, reporting and browser roles.

## Why

Current instructions can close unrelated browser sessions, inconsistently gate
bugfixes and docs, depend on unpackaged references, reject unrelated dirty work,
confuse residual risk with incomplete work, report a clean review prematurely,
and turn inventory summaries into SOW progress reports.

## Location

- `skills/playwright-flow/SKILL.md`
- `skills/playwright-flow/references/cli.md`
- `skills/playwright-flow/references/workflows.md`
- `skills/task-router-flow/SKILL.md`
- `skills/task-router-flow/references/routing-notes.md`
- `skills/task-router-flow/references/scope-of-work.md`
- `skills/sow-delegate-flow/SKILL.md`
- `skills/task-execution-flow/SKILL.md`
- `skills/task-review-investigate-compare/SKILL.md`
- `skills/task-progress-report/SKILL.md`
- `skills/task-progress-report/agents/openai.yaml`
- `skills/registry.json` and `skills/INDEX.md` for aligned progress description only
- `tests/skill_feedback_cases/{playwright-flow,task-router-flow,sow-delegate-flow,task-execution-flow,task-review-investigate-compare,task-progress-report}.json`
- `tests/test_skill_sync_scripts.py` for a focused installed-resource check only
- `plan_todo/skill_design_decisions.md`
- This SOW, later `plan_todo/finished/SOW_0082_workflow_contract_consistency.md`
- Disposable verification artifacts under `output/sow_0082/`; do not commit them.

## Authority And Principles

Read `AGENTS.md`, `plan_todo/skill_design_decisions.md`, the six source skills and
their affected references before implementation. No root principle-design file
or declared concept authority was found during intake.

Apply DRY, SOLID and KISS: preserve each skill's responsibility, assign execution
completion semantics to execution flow, and keep installed skills self-contained.
Do not create a shared runtime, policy installer or new orchestration skill.

## As-Is Diagram (ASCII)

```text
router ------> ambiguous approval gates / external rule file
delegate ----> external rule file
execution ---> whole-worktree gate / conflicting residual-risk rules
progress ----> separate completion logic / summary always means SOW
review ------> no concrete finding before evidence -> clean conclusion
browser -----> close-all / kill-all -> other sessions at risk
```

## To-Be Diagram (ASCII)

```text
request -> router -> project policy + existing authorization -> execution
                     delegate -> bounded handoff ------------> execution
execution -> required checks + gap classification -> verified / pending
progress  <- evidence-backed execution state; render requested summary shape
review    -> provisional mode -> evidence -> findings / clean / unverified
browser   -> task-owned session -> cleanup that session only
```

## Deliverables And Behavior Locks

| ID | Change | Required behavior |
| --- | --- | --- |
| F1 | Browser ownership | Use a unique task-owned named session. Close only that session. Leave pre-existing sessions intact. Global close/kill requires explicit user authorization; lost ownership is not permission for global cleanup. |
| F2 | Routing authorization | Every code fix follows target-repo SOW policy regardless of size; reuse approved coverage when exact scope is already covered. Docs requests that already authorize the concrete edit do not require a second approval. Material expansion still needs approval. Align both router references. |
| F3 | Portable instructions | Remove external `../../rules/brief-execution.md` links from router and delegate; inline a short communication rule. A fresh skill copy must work without any legacy rule file or project-policy mutation. |
| F4 | Scoped dirty-worktree gate | Review and stage task-owned changes only; unrelated dirty/staged work remains intact and does not block verification. Overlapping ambiguous hunks require resolution before staging. |
| F5 | Completion and residual risk | A failed done criterion, required unverified behavior, or open repair is blocking. An accepted non-blocking risk may coexist with verified completion only when done criteria pass and the acceptance basis is explicit. Never use risk acceptance to waive required verification or scope approval. |
| F6 | Evidence-first review | Select an initial mode provisionally; gather evidence before declaring no actionable findings. Incomplete evidence produces an explicit unverified conclusion. Clarifying existing acceptance criteria permits writeback; changing required behavior or acceptance thresholds is a scope change. |
| F7 | Reporting selection | Inventory summaries use requested subject columns without invented SOW rows. Execution summaries retain overall/open-item tables. Derive done from required verification and gap status, not implementation alone. Invoke progress reporting once at final task closeout by default; explicit user status requests remain supported. |

Keep skill names stable. Update progress frontmatter and UI metadata together to
reflect inventory versus execution reporting; align registry/index descriptions
without changing the registered skill/file set. Do not merge whole skills.

Residual-risk acceptance must cite an existing approved scope allowance, explicit
user acceptance, or a repository policy that delegates that decision. The agent
cannot invent acceptance merely by labeling a finding low severity. Report the
risk, impact, acceptance basis and follow-up owner or action at closeout.

When execution flow is unavailable, progress reporting must remain standalone:
use actual reported verification evidence and mark unknown completion pending.
Do not require installation of another skill or infer completion from a percentage.
Keep ordinary short commentary distinct from invocation of the progress skill.

## Regression And Verification Matrix

Each feedback case records observed source evidence separately from hypothetical
runtime impact. Use one expected, one negative and one boundary scenario per case,
matching the existing fixture schema; do not claim fixture parsing proves agent behavior.

For behavioral evaluation, give the evaluator only the request, the candidate
skill and necessary scenario context. Keep expected_behavior, must_not, feedback,
review findings and this SOW out of its input; the coordinator scores the observed
actions against those fields afterward. Reading and agreeing with a checklist
does not count as a forward-test. Use disposable repositories for write/staging
scenarios so evaluation cannot mutate the real worktree or user index.

| Case ID | Expected | Negative | Boundary |
| --- | --- | --- | --- |
| browser-session-ownership-001 | Finish task A and close A | Task B remains open | Unknown ownership or stuck A never authorizes global kill |
| router-authorization-consistency-001 | Small code fix respects SOW policy | Authorized docs edit proceeds without approval repetition | Scope expansion still waits for authorization |
| portable-router-rule-001 | Fresh router install has all local resources | No legacy rule file is needed | Install into arbitrary root without modifying project policy |
| portable-delegate-rule-001 | Fresh delegate install has all local resources | No legacy rule file is needed | Standalone install retains concise communication guidance |
| scoped-worktree-closeout-001 | Commit only task-owned changes | Preserve unrelated staged and unstaged work | Mixed ownership in one file requires hunk-level resolution |
| residual-risk-closeout-001 | Passing criteria plus accepted non-blocking risk can close | Failed or unverified required criterion cannot close | Unaccepted or unclassified risk stays explicit and blocks completion decision |
| evidence-first-review-001 | Inspect evidence before a clean conclusion | Missing evidence is not a clean review | Material acceptance change routes as scope change |
| summary-shape-completion-001 | Skill inventory uses skill/agent columns | No invented SOW or overall row for inventory | User-requested status before final closeout reports pending verification accurately |
| final-progress-frequency-001 | One default progress report at final task closeout | Intermediate mini-task completion does not trigger another report | Explicit user status requests can produce additional reports without changing completion state |

## Execution Order

1. Capture the pre-existing diff and confirm approved exact scope.
2. Record the bounded feedback cases before changing their corresponding skills.
3. Update browser ownership, router authorization and portable references.
4. Align execution, review and progress contracts; record material decisions.
5. Verify source, installed-resource closure and behavioral scenarios; repair gaps.
6. Record evidence and limitations, move this SOW only on verified completion,
   then commit only approved task-owned changes.

## Done Criteria

- All F1-F7 behavior locks are represented consistently in affected entrypoints,
  examples, references and progress UI metadata.
- Structural validators pass for all six changed skills.
- `uv run python -m unittest tests.test_skill_feedback_cases tests.test_skill_sync_scripts`
  passes; feedback cases retain exactly three sanitized scenarios each.
- Fresh router/delegate copies in an isolated repo-local target have no broken
  required local references and no dependency on historical installed files.
- Browser ownership is verified with two disposable named sessions against a
  local page; closing session A leaves session B usable. Both are created solely
  for this probe and closed individually afterward. Never use a user's existing
  session as the test control. Keep page/evidence artifacts under the allowed root.
- Evaluate each regression case in an isolated context when available, recording
  request, observed response/actions, expected invariant and pass/fail. Reuse a
  suitable existing harness; do not build a new evaluation framework. If isolated
  evaluation is unavailable, label behavioral verification incomplete, keep the
  SOW open, and report the missing check for an explicit user decision.
- Perform the post-implementation gap check, including negative paths in the matrix.
- Record durable verification results in this SOW: case/scenario ID, candidate
  content hash or Git tree, evaluation method, observed result and limitations.
  Raw disposable artifacts may be omitted from Git; the committed evidence summary
  must remain understandable without them.
- `git diff --check` passes; only approved files/hunks are staged and committed.
- If unrelated changes were already staged, use isolated commit staging or an
  equivalent scoped commit that preserves the original unrelated index entries.
  Verify the actual commit diff; ordinary `git commit` after adding selected
  paths is insufficient when the index already contains unrelated work.
- Validate the exact candidate commit tree in an isolated repo-local snapshot,
  excluding pre-existing unstaged changes such as the telemetry patch. Reuse
  evidence only for identical candidate content; rerun affected checks when that
  tree differs from the tested worktree. Preserve the pre-existing patch in place.
- Preserve lifecycle metadata and repair references when moving this SOW. No
  parent plan is owned by this standalone task; any later completed owning plan
  must also move to its matching `finished/` folder.

## Out-of-Scope

- Skill merges, renames, new skills or rewriting the imported taste skill.
- Changes to concept governance, design-mirror skills, POC review, or evolution flow.
- Changes to browser wrapper implementation, sync implementation or dependency versions.
- Modifying global browser sessions, telemetry infrastructure or project policies.
- Live Codex/Claude/OpenCode installation, pushing commits or publishing skills.
- Rewriting historical SOWs/plans or implementing these changes before approval.

## Proposed-By

Codex.

## Plan / Reference

- Current seven-finding skill review requested by the user; standalone cross-skill SOW.
- `skills/INDEX.md`, `skills/registry.json`, `plan_todo/skill_design_decisions.md`.
- Prior narrow changes: [SOW_0074](SOW_0074_reimport_playwright_flow.md),
  [SOW_0081](SOW_0081_effective_sow_review_writeback.md).
- Existing uncommitted telemetry removal in router and its fixture predates this
  SOW. Preserve it; do not silently include it in this task's commit.

## Cautions / Risks

- Duplicated examples can retain unsafe commands after the primary rule is fixed.
- Residual-risk wording must not weaken verification or authorize scope reduction.
- Inventory reporting must not replace the existing plan/SOW progress table.
- Installed-resource parity does not by itself prove dependency closure or behavior.
- Isolated model or browser verification may be unavailable; record the exact
  limitation and keep unmet required checks visible instead of declaring done.

## Review Summary

Final local review incorporated blind forward-test inputs, durable evidence and
candidate-commit verification alongside the prior scope/closeout corrections.
No remaining actionable SOW finding; implementation is not approved or verified
by these document reviews.

## Implementation Verification

Verified on 2026-09-15. Candidate tree before closeout-only documentation edits:
`ed20270a8f12ea91baf16d1430c5f8ee465e1a10`; verified skills subtree:
`972cf884489ae61460dd6f9d0325753dbf229c7e`.
The candidate excludes the earlier uncommitted telemetry patch. Candidate source
was checked out from the index and tested separately from the dirty worktree.

- All six structural validators passed; feedback/sync suite: 13 tests passed.
- Fresh-copy resource checks passed for router and delegate without external rules.
- Four fresh evaluator contexts received only candidate instructions and raw
  scenario context, not feedback/expected answers. Coordinator scored 27 responses
  across the nine cases below. A fifth fresh context checked five affected
  closeout/reporting scenarios after the final wording repair; all passed.
- Behavioral response tests prove the observed decisions/output for supplied
  contexts, not universal model reliability or arbitrary project integrations.

| Case | Observed evidence and result |
| --- | --- |
| browser-session-ownership-001 | Three responses selected owned-session close and refused unknown/global cleanup. Real Chrome sessions A/B opened the local probe; after A closed, B remained listed and a button click changed 0 to 1. Both were then closed individually; final list had no browsers. Pass. |
| router-authorization-consistency-001 | Small fix required SOW; explicitly requested typo proceeded; redesign routed separately. Pass. |
| portable-router-rule-001 | Three responses used packaged references/project policy without legacy rules. Fresh-copy dependency test passed. |
| portable-delegate-rule-001 | Three responses used inline communication and project policy; absent agent catalog was correctly distinguished from missing resource dependency. Fresh-copy dependency test passed. |
| scoped-worktree-closeout-001 | Responses preserved unrelated dirty/staged work and stopped on ambiguous hunks. Actual disposable commit `6b802af9b7c86ad8a5032b4db16c6bdb80062de6` changed only task.txt; unrelated staged and unstaged diff bytes matched before/after. Pass. |
| residual-risk-closeout-001 | Accepted non-blocking risk allowed closeout; failed required test and unclassified risk did not. Final retest retained accepted follow-up in notes without an open SOW row. Pass. |
| evidence-first-review-001 | Responses inspected before conclusion, marked missing external schema unverified, and routed changed required output as scope change. Pass. |
| summary-shape-completion-001 | Inventory used Skill/Codex/Claude or deployment columns; pending runtime evidence remained pending without requiring execution skill installation. Pass. |
| final-progress-frequency-001 | Final report used overall 1/1; intermediate mini-task produced ordinary commentary; requested status reported pending verification. Final retest ordered commit handling before the final report. Pass. |

Post-implementation gap check repaired accepted-follow-up row handling and final
report ordering. Final required-contract, edge-case, preservation, ownership,
cleanup and scope checks found no remaining blocking issue. No runtime product
code or async compute/performance path was changed. Browser console's sole error
was the disposable page's missing favicon (HTTP 404); button/session checks passed.

No live skill deployment or push was performed; both remain outside this SOW.
Raw probe artifacts are disposable; this summary retains the relevant evidence.
