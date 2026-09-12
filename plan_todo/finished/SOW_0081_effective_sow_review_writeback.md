# SOW_0081 — Effective SOW Review Writeback

## Lifecycle

- Status: done — canonical implementation; optional deployment not requested
- Approval: approved by user
- create_dttm: `2026-09-12T19:19:50+07:00`
- approve_dttm: `2026-09-12T19:26:11+07:00`
- finish_dttm: `2026-09-12T19:27:17+07:00`

## Task

Make repeated plan/SOW reviews rewrite the effective current contract concisely,
while keeping superseded alternatives and review history in the owning decision
log when one exists.

## Location

- `skills/task-review-investigate-compare/SKILL.md`
- `tests/skill_feedback_cases/task-review-investigate-compare.json`
- `plan_todo/finished/SOW_0081_effective_sow_review_writeback.md`
- Exact post-commit deployment target, if separately approved:
  `~/.codex/skills/task-review-investigate-compare/`

## Why

The current skill correctly writes concrete findings back, but does not define
how repeated reviews should consolidate the artifact. This can produce
append-only `Review Pass` sections and leave superseded contracts beside the
final contract, making the SOW longer and less authoritative.

## Feedback Contract

- Target skill: `task-review-investigate-compare`
- Trigger: repeated review or final review of a known plan/SOW
- Observed behavior: append detailed review history and retain superseded
  contract text in the active artifact
- Expected behavior: rewrite the artifact to one concise effective contract;
  retain only unresolved decisions and current evidence
- Reusable invariant: active planning artifacts describe what is currently
  decided and executable; decision history belongs in the declared decision
  authority
- Cause class: incomplete review/writeback procedure
- Evidence reference: `sanitized:user-feedback-effective-sow-writeback-2026-09-12`

## As-Is Diagram (ASCII)

```text
review 1 -> append Review Pass 1
review 2 -> append Review Pass 2
final    -> append Final Review
             + old and new contracts coexist
```

## To-Be Diagram (ASCII)

```text
repeated/final review
  -> update effective sections in place
  -> remove redundant review notes and superseded contract text
  -> keep unresolved gates visible
  -> optional one-line review summary
  `-> historical rationale -> decision log
```

## Deliverables

- Add a planning-artifact consolidation rule to `Review And Writeback`:
  repeated reviews update the effective sections in place instead of appending
  per-pass review histories.
- Apply consolidation only to an artifact with actionable redundancy or
  inconsistency. Respect discussion-only requests; a clean artifact with no
  findings needs no edit or new review-summary entry.
- Require the final review to detect conflicting current/superseded Task,
  diagram, deliverable, done-criteria and out-of-scope text.
- Keep the SOW/plan focused on the current contract, current approval gates,
  unresolved questions, current evidence and remaining work.
- When the repository declares a decision log, move or retain alternatives,
  rejected choices, superseded decisions and chronological rationale there.
- Permit at most one very short review summary when it materially helps handoff
  or the repository requires it; forbid `Review Pass 1/2/3` ledgers by default.
- Never remove an unresolved decision, pending approval, active risk, current
  deliverable, current done criterion or evidence needed to execute safely.
- Preserve base and extension IDs, approval states and lifecycle timestamps.
  A newer draft does not supersede an approved contract until authorized;
  clearly separate the approved scope from proposed changes.
- A resolved decision may still govern implementation. Remove its redundant
  discussion, not its effective requirement. Preserve links and material
  rationale in the existing decision log before removing their sole SOW copy;
  do not duplicate history already recorded there.
- When no decision-log authority exists, retain the minimum current rationale
  needed to understand the contract; do not invent a new governance structure.
- Do not rewrite completed historical artifacts merely to normalize style.
- Add regression case `effective-planning-writeback-001` with expected,
  negative and boundary scenarios.
- Keep frontmatter and `agents/openai.yaml` unchanged because trigger scope and
  user-facing purpose do not change.

## Regression Scenarios

| Kind | Scenario | Required behavior |
| --- | --- | --- |
| Expected | Final review finds old and new implementation contracts plus three review-pass sections in an active SOW with a decision log | Consolidate the SOW to the effective contract; keep history in the decision log; retain only a concise summary if useful |
| Negative | User asks to review a historical decision log or audit chronology | Preserve chronological entries; do not collapse decision history into only the latest outcome |
| Boundary | An active SOW contains an unresolved option or pending approval | Keep the unresolved item visible in the SOW and route material scope change; do not treat it as superseded |
| Boundary | An active plan has no declared decision-log authority | Keep minimum current rationale in the plan; do not invent or assume a separate decision log |
| Boundary | An approved base SOW has a draft extension with a different design | Preserve both approval boundaries and lifecycle metadata; do not label the draft as the approved executable contract |
| Negative | A final review finds a concise, consistent SOW, or the user requests discussion only | Report the result without editing or appending a review record |

## Done Criteria

- The canonical skill distinguishes effective planning authority from historical
  decision authority.
- Repeated and final reviews consolidate active SOWs/plans instead of creating
  append-only review ledgers.
- The rule preserves unresolved gates, effective resolved requirements, base and
  extension approval metadata, current execution evidence and valid links.
- Regression case `effective-planning-writeback-001` contains sanitized
  expected, negative and boundary scenarios.
- The changed skill passes the available skill structural validator.
- `uv run python -m unittest tests.test_skill_feedback_cases tests.test_skill_sync_scripts`
  passes.
- A targeted forward-test is run in a clean isolated context when available;
  otherwise model behavior is explicitly unverified.
- Task-owned diff contains only the approved skill, fixture and this SOW;
  unrelated workspace changes remain untouched.
- Commit contains only approved AISkills files.
- If deployment is approved, dry-run and execution differ only by `--dry-run`,
  target only Codex legacy-user `task-review-investigate-compare`, and exact-copy
  parity passes.

## Out-of-Scope

- Changing review triggers, review modes, writeback authority or scope-change
  approval rules.
- Changing SOW templates, lifecycle timestamps or decision-log schemas.
- Modifying `task-router-flow`, `task-poc-verification-flow`,
  `task-execution-flow` or `skill-evolution-flow`.
- Automatically creating a decision log where project policy does not declare
  one.
- Rewriting existing finished SOWs/plans.
- Syncing multiple skills or agent environments.
- Pushing commits or publishing the skill.

## Proposed-By

Codex, from explicit user feedback on 2026-09-12.

## Plan / Reference

- `skill-evolution-flow`
- Existing feedback case `review-writeback-001`
- New feedback case `effective-planning-writeback-001`

## Cautions / Risks

- Over-aggressive cleanup could remove effective requirements or execution
  evidence; resolved does not mean obsolete.
- A declared decision log owns historical rationale; the active SOW still owns
  every current contract and approval gate needed for execution.
- Style cleanup must not become a material scope change.
- Installed-copy mutation before canonical commit would recreate source drift.

## Review Summary

Reviewed: preserve effective requirements, approval boundaries and evidence;
consolidate only actionable redundancy. No outstanding review finding.

## Verification

- Skill structural validator: passed; feedback/sync tests: 12 passed.
- Regression case: `effective-planning-writeback-001` with expected, negative
  and boundary scenarios; manual contract review and whitespace checks passed.
- Isolated model forward-test: not run; subagents are unavailable in this side
  conversation. Structural checks do not prove model behavior.
- Optional Codex deployment: not requested; installed copy remains unchanged.
