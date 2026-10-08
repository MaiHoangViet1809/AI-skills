# SOW_20261006_A4274RON - Consumer-Contract And False-Negative Gates For Skill Workflows

- Status: COMPLETED
- Approval: approved by user in current side thread (`làm SOW đó đi`)
- create_dttm: 2026-10-06T13:08:27+07:00
- create_date: 2026-10-06
- create_dttm_source: original_creation_datetime
- create_dttm_confidence: explicit
- create_dttm_evidence: `plan_todo/finished/SOW_20261008_VO3LKN0L/creation-date-evidence.json` (record: SOW_20261006_A4274RON)
- approve_dttm: 2026-10-06T13:31:15+07:00
- finish_dttm: 2026-10-06T13:43:45+07:00
- legacy_id: SOW_0100
- legacy_path: plan_todo/finished/SOW_0100_consumer_contract_false_negative_gates.md
- migrated_dttm: 2026-10-08T12:48:51+07:00
- legacy_title: SOW_0100 - Consumer-Contract And False-Negative Gates For Skill Workflows

## Preserved Contract And Historical Evidence

## Lifecycle

- **Status**: COMPLETED
- **Approval**: approved by user in current side thread (`làm SOW đó đi`)
- **create_dttm**: `2026-10-06T13:08:27+07:00`
- **approve_dttm**: `2026-10-06T13:31:15+07:00`
- **finish_dttm**: `2026-10-06T13:43:45+07:00`
- **Proposed-By**: Codex
- **Plan / Reference**: `skill-evolution-flow` feedback correction

## Task

Strengthen `task-execution-flow` and `task-review-investigate-compare` so a
contract change cannot pass component-only checks while real callers still use
the old route, default, or gate.

## Why

A recent CDC framework change was implemented in the shared path and validated
with a synthetic override, but real caller declarations were not enumerated.
Several callers therefore retained the old gate and failed at runtime with a
missing compiled recipe. The reusable defect is incomplete caller coverage and
the absence of a negative check for the forbidden legacy route; it is not a
need for a new runtime registry or telemetry system.

## Location

- `skills/task-execution-flow/SKILL.md`
- `skills/task-review-investigate-compare/SKILL.md`
- `tests/skill_feedback_cases/task-execution-flow.json`
- `tests/skill_feedback_cases/task-review-investigate-compare.json`
- `plan_todo/finished/SOW_20261006_A4274RON/SOW_20261006_A4274RON_consumer_contract_false_negative_gates.md`

Canonical AISkills sources only. Installed copies, provider configuration,
project runtime code, and unrelated dirty files are out of scope.

## As-Is Diagram (ASCII)

```text
approved contract change
        |
        +--> shared helper/component test
        |       `--> PASS
        |
        `--> real callers not inventoried
                `--> old default/flag remains
                        `--> runtime failure is missed
```

## To-Be Diagram (ASCII)

```text
approved contract change
        |
        +--> inventory real callers and defaults
        +--> verify shared path + caller-shaped path
        +--> negative check: old route/default must fail validation
        +--> boundary check: unrelated consumers stay unchanged
        +--> skill tests + structural validation
                `--> close only when all required routes pass
```

## Behavior Contract

### `task-execution-flow`

1. Before implementation and before closeout, identify the real callers or
   declarations affected by the changed contract; a synthetic fixture or
   helper-only invocation is insufficient for a generic claim.
2. Enumerate every discoverable affected caller in the declared source scope;
   verify each caller-shaped path uses the approved contract, and make the
   negative check fail if any affected caller still retains the old default,
   flag, or gate. One representative caller is not sufficient for a generic
   claim.
3. Check the boundary: consumers outside the changed contract must retain their
   declared behavior and must not be forced into the new route.
4. If any affected caller is unverified or still follows the old route, keep
   the task unverified and do not close it.

### `task-review-investigate-compare`

1. When reviewing a behavior or policy change, trace it from the shared owner
   to all direct callers/consumer declarations before recommending approval.
2. Treat a component-only pass as insufficient evidence for a generic change.
3. Require an explicit negative check that covers every discoverable affected
   caller for the forbidden legacy route/default, plus a boundary check for
   non-target consumers.
4. Report missing caller evidence as a concrete finding and route material
   contract gaps instead of approving from document consistency alone.

## Deliverables

1. Add the execution caller-coverage, legacy-route negative-check, and boundary
   rules at the existing execution scope/verification gates.
2. Add the review caller-tracing and false-negative rules at the existing
   evidence/recommendation gates.
3. Extend each existing target-skill feedback fixture with one stable sanitized
   case containing exactly one expected, one negative, and one boundary
   scenario for this defect.
4. Record the caller inventory and each caller's approved/legacy/boundary
   disposition in the existing implementation or review evidence; do not add
   a new persistent registry for it.
5. Keep the guidance concise and reuse existing gates; do not add a new
   orchestration mechanism.

## Done Criteria

1. Both canonical skill bodies explicitly require real-caller inventory and
   caller-shaped verification for generic behavior changes.
2. Both skill bodies explicitly require a forbidden-old-route negative check
   and a non-target boundary check.
3. A component/helper-only fixture cannot satisfy the generic closeout or clean
   review recommendation by itself; caller inventory evidence is required.
4. The negative check fails when any discoverable affected caller retains the
   old route/default, while non-target consumers remain accepted.
5. The two feedback fixtures parse and contain unique metadata plus one
   expected, one negative, and one boundary scenario for this SOW.
6. The available skill structural validator, `uv run python -m unittest
   tests.test_skill_feedback_cases tests.test_skill_sync_scripts`, and
   `git diff --check` pass.
7. No installed copy, runtime product code, provider setting, or unrelated
   dirty file is changed.

## Out Of Scope

- Changing CDC, Airflow, Spark, or other product/runtime code.
- Adding a caller registry, AST/semantic index, telemetry, checkpoint store,
  polling service, or automatic impact-analysis engine.
- Requiring one search tool when direct repository inspection is sufficient.
- Syncing canonical skills to Codex, Claude, or other installed environments.
- Committing or pushing this SOW without a separate explicit request.

## Concept Compliance

- **Applicable Concepts**: None. AISkills has no declared project concept
  catalog; this SOW follows `AGENTS.md` and `skill-evolution-flow` ownership
  and validation rules.
- **Concept Change**: No
- **Required Concept Updates**: None

## Cautions / Risks

- Caller enumeration must stay proportional to the changed contract; this SOW
  does not authorize a repository-wide static-analysis product.
- A negative check proves the old route is rejected by the validation procedure;
  it does not prove every external runtime provider behaves identically.
- Existing user changes in the AISkills worktree must remain untouched.

## Decision Log

Read the [binding extracted record](SOW_20261006_A4274RON_decision.md) before execution; original authority is preserved there.

## Implementation Verification

- Both canonical skill validators: PASS.
- JSON parsing for both feedback fixtures: PASS.
- `uv run --no-sync --offline python -m unittest
  tests.test_skill_feedback_cases tests.test_skill_sync_scripts`: 13 tests
  PASS.
- `git diff --check`: PASS for the changed tracked files.
- Scoped commit `39a3e0e` was pushed to `origin/main`.
- The two canonical skills were synced and verified with parity `ok` in
  `/Users/maihoangviet/.codex/skills` and `/Users/maihoangviet/.claude/skills`.
- Pre-existing user changes remain outside this SOW.
