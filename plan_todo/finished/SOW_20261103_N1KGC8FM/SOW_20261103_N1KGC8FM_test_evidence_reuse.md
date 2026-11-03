# SOW N1KGC8FM — Reuse valid test evidence

- Status: DONE
- Approval: approved by user
- create_dttm: 2026-11-03T23:41:19+07:00
- approve_dttm: 2026-11-03T23:55:07+07:00
- finish_dttm: 2026-11-04T00:05:57+07:00
- Task: Make test-evidence reuse an explicit decision before test execution in `task-execution-flow`, and compact its overlapping guidance where safe.
- Location: `skills/task-execution-flow/SKILL.md`; `tests/skill_feedback_cases/` for the required sanitized case; this bundle.
- Why: A broad regression included previously passed tests; the existing reuse instruction is at closeout rather than before each test invocation. The available evidence does not establish that every test in that run was redundant.
- Proposed-By: Codex
- Plan / Reference: standalone; `skill-evolution-flow` and `task-execution-flow`.

## As-Is

```text
Work / follow-up → choose test → run → closeout mentions evidence reuse
```

## To-Be

```text
Before each test → valid evidence for this scope? → yes: reuse
                 → affected / unknown / requested? → run relevant checks
```

## Deliverables

- Put one concise decision at the test-execution point: compare test scope and prior result with relevant code, dependencies, configuration and runtime assumptions; reuse valid evidence and run only missing or invalidated coverage.
- Preserve explicit user requests to rerun, required release gates, relevant failures, and missing or stale evidence. Do not infer test coverage from an overlapping test count.
- Remove or consolidate genuinely redundant wording in this skill only, without dropping authority, security, required verification, delegation or closeout semantics. Minimize churn and preserve existing uncommitted changes.
- Add one sanitized feedback case with expected, negative and boundary scenarios before the skill edit; use `skill-creator` per `skill-evolution-flow`.

## Done Criteria

1. Review source and installed origin; confirm canonical ownership and preserve unrelated dirty work. Validate overlap of the target test scope, not merely command names.
2. Scenario review covers unchanged valid PASS (no rerun), changed relevant inputs or missing evidence (targeted rerun), and explicit rerun/release gate/failure (honor applicable requirement).
3. Review compacted instructions against the original: no lost guardrail or changed responsibility; no blanket ban on necessary testing. Report behavioral evidence separately from structural validation.
4. Run skill structural validation and the skill-feedback/sync unit tests required by `skill-evolution-flow`; inspect scoped diff and commit only authorized task changes if safe. Do not push.

## Out of Scope

- Changing other skills or repository-wide policy; changing the XVision main-thread files or runtime; automated test-result persistence; syncing other installations. The user approved syncing this skill to Codex and Claude after validation.

## Cautions / Risks

- A broad suite can contain both already-covered and new checks. Reuse only identifiable coverage; do not skip necessary tests to save time.
- Canonical `SKILL.md` has unrelated uncommitted edits. Reconcile ownership before changes or commit; do not overwrite them.

## Progress

- progress_updated_dttm: 2026-11-04T00:05:57+07:00

| Item | Status | Evidence / Pending reason | Next action / Owner |
| --- | --- | --- | --- |
| T1: Guard and safe compaction | DONE | Feedback case and scenario review; structural validator and 13 unit tests passed. Agent behavior has not been forward-tested. | None |
| T2: Verification and scoped commit | DONE | Scoped checkpoint fd057c3 pushed; both installations synced from that committed snapshot and parity verified. Unrelated Redmine edits preserved. | None |
