# SOW_0101 — Preserve Chosen Approaches And Require Compatibility Approval

## Lifecycle

- **Status**: COMPLETED
- **Approval**: approved by user
- **create_dttm**: `2026-10-07T04:40:25+07:00`
- **approve_dttm**: `2026-10-07T04:45:08+07:00`
- **finish_dttm**: `2026-10-07T04:46:22+07:00`
- **Proposed-By**: Codex
- **Plan / Reference**: Standalone; related SOW_0084, SOW_0085, SOW_0100; skill-evolution-flow diagnosis.

## Task

Update SOW authoring, review, and execution skills to preserve the user's chosen
implementation approach and require explicit user approval before introducing
additional compatibility behavior.

## Why / Evidence

A user chose a POC demonstrated on one runtime. During SOW review, compatibility
with another backend became a required deliverable without a user decision;
the executor then followed that changed SOW. The demonstrated failure is an
unsupported review recommendation becoming implementation authority.

Current inspection found that the Consumer Contract Gate in
`skills/task-review-investigate-compare/SKILL.md` permits skipping internal-only
changes, while the corresponding execution rule targets caller-visible APIs.
The existing simplicity gate already requires justification for compatibility
paths, but technical justification does not establish user permission.
Installed and canonical copies of the three target skill bodies matched during
inspection. This does not establish their state at every historical review.

## Location

- `skills/task-router-flow/SKILL.md`
- `skills/task-review-investigate-compare/SKILL.md`
- `skills/task-execution-flow/SKILL.md`
- `tests/skill_feedback_cases/task-router-flow.json`
- `tests/skill_feedback_cases/task-review-investigate-compare.json`
- `tests/skill_feedback_cases/task-execution-flow.json`
- `plan_todo/SOW_0101_chosen_approach_and_compatibility_approval.md` (then the matching `finished/` location at closeout)

Canonical AISkills sources only. Existing unrelated changes, including changes
already present in two target skill bodies, must be preserved through scoped
hunks. No project concept authority or principle-design file was found; the
applicable authority is AGENTS.md, particularly DRY/SOLID/KISS and scope control.

## As-Is Diagram (ASCII)

```text
user selects a demonstrated approach
  -> SOW / reviewer adds another backend for compatibility
  -> additional behavior becomes a required deliverable
  -> executor follows the changed SOW
```

## To-Be Diagram (ASCII)

```text
user decision + selected POC + applicable project contract
  -> preserve runtime/version, approach and approved boundaries in SOW
  -> review each proposed material change against those decisions
       -> within authorized scope: incorporate
       -> additional compatibility: explain and ask user first
  -> execution checks SOW against the same decisions before handoff/code
```

## Behavior Contract

1. **Preserve the selected approach.** When a user chooses a POC or
   implementation direction, carry its relevant runtime/version, execution
   path, and approved boundaries into the existing SOW/decision content.
   Distinguish demonstrated behavior from unverified assumptions; POC success
   alone does not prove production completeness or authorize unrelated scope.
2. **Compatibility requires user approval.** Agents MUST NOT introduce an
   additional compatibility layer, shim, fallback backend, legacy alias, or
   dual implementation path without first asking the user and obtaining
   explicit approval covering that behavior. Explain the concrete need and
   scope before asking. A reviewer recommendation, existing test dependency,
   generic robustness rationale, or agent-written SOW clause is insufficient.
3. **Honor existing authorization.** A user request already explicitly covering
   the same compatibility behavior satisfies the approval requirement; do not
   ask again. Preserve existing authorized compatibility. This rule does not
   authorize removing supported consumers or changing existing contracts.
4. **Review internal decisions too.** Apply approach/authority comparison to
   internal runtime, backend, and POC-promotion decisions, even when the public
   API is unchanged. Classify a review finding as an in-scope correction or an
   additional proposal before incorporating it into effective deliverables.
   A proven technical need can justify a proposal, but cannot supply approval.
5. **Verify before implementation handoff.** Compare the planned route with
   the user's selected approach and approved changes before code or delegation.
   An APPROVED label must not override an unresolved contradiction with an
   explicit user constraint. Report the exact conflict; do not silently choose
   another backend, weaken tests, or change the supported runtime.

Place these rules at existing authoring, finding-writeback, and execution
preflight gates. Keep each skill self-contained but avoid repeating a long
policy block or adding new tracking infrastructure.

## Deliverables

1. Router guidance carries selected POC/approach constraints into a SOW and
   separates proposed compatibility from authorized implementation.
2. Review guidance checks internal approach decisions and requires user
   approval before promoting additional compatibility into required scope.
3. Execution guidance verifies those decisions before handoff/code and blocks
   unauthorized compatibility without blocking work already explicitly covered.
4. Before changing skill bodies, add one sanitized stable feedback case per
   target skill to its existing JSON fixture, with expected, negative, and
   boundary scenarios. Follow skill-creator when editing the skill bodies.

## Done Criteria

- All three decision points apply the Behavior Contract, including internal-only
  changes; the public-API-only scope does not bypass approach checks.
- **Expected:** a selected runtime-A POC remains runtime A throughout SOW,
  review, and execution, with required production verification retained.
- **Negative:** a reviewer or old test suggests runtime B, a shim, or fallback;
  no such behavior becomes required implementation without user approval.
  Merely inserting it into an approved-looking SOW cannot satisfy this check.
- **Boundary:** explicitly requested A+B compatibility proceeds without another
  permission request; existing authorized compatibility remains supported.
- A genuine conflict with an existing supported consumer is reported for a
  decision; the rule neither silently adds support nor silently drops it.
- Feedback fixtures retain unique IDs and the existing expected/negative/boundary
  schema. The available skill-creator validator, `uv run python -m unittest
  tests.test_skill_feedback_cases tests.test_skill_sync_scripts`, and scoped
  `git diff --check` pass.
- Report scenario/text validation separately from model behavioral evidence.
  Structural test success must not be presented as proof that drift is eliminated.
- Review scoped hunks and preserve all pre-existing changes before any
  implementation commit. Canonical validation does not imply installed rollout.

## Out Of Scope

- Editing AGENTS.md, the policy template, skill-evolution-flow, provider settings,
  skill metadata/registry, or additional skills.
- Changing project runtime code, Spark/CDC implementations, or parent-thread work.
- Adding another review agent, mandatory extra review rounds, decision registries,
  telemetry, checkpoints, or memory mechanisms.
- Syncing installed skills, installing dependencies, running external model
  evaluations, or pushing Git changes. Any rollout needs a named authorized target.

## Cautions / Risks

- Avoid approval loops: ask only for additional compatibility not already
  explicitly authorized by the user.
- Preserve required correctness and existing supported behavior; exposing a
  conflict is not permission to weaken verification or remove old consumers.
- Keep generic skill guidance free of private transcripts, endpoint details,
  machine-specific paths, and task-specific runtime requirements.
- The worktree contains concurrent changes. File-level inclusion in Location
  does not grant ownership of existing edits in those files.

## Decision Log

### D001 — Correct the decision points instead of adding a duplicate policy

- **Date:** 2026-10-07
- **Status:** approved by user
- **Owner:** Codex
- **Context:** an extra compatibility backend entered a SOW despite a selected
  POC path. The user requests a requirement to ask before adding compatibility.
- **Options considered:** another project guardrail; only stronger generic
  wording; targeted authoring/review/execution procedure changes with fixtures.
- **Chosen strategy:** targeted changes in the three canonical workflow skills;
  preserve the user's chosen approach and require explicit approval for new
  compatibility behavior.
- **Tradeoffs / risks:** additional questions only for genuinely new compatibility;
  earlier explicit permission is reused. Existing support must not be removed.
- **Evidence / references:** current target skill bodies and feedback-case schema;
  SOW_0084, SOW_0085, SOW_0100; current skill-evolution-flow diagnosis.
- **Supersedes:** none; existing simplicity and consumer-contract checks remain.

## Self-Review — One Pass

- Checked scope against the request: selected-approach preservation plus a
  requirement to ask and obtain approval before adding compatibility.
- Checked the approval boundary: reviewer advice and an agent-written SOW
  clause cannot authorize new behavior; prior explicit user approval is reused.
- Checked internal-only coverage and existing-consumer preservation: neither
  an unchanged public API nor old tests authorize a new fallback, and existing
  support cannot be silently removed.
- Checked verification limits: fixtures cover expected, negative, and boundary
  behavior; structural validation is not claimed as model behavioral proof.
- Checked ownership: only this draft was created; skill/test changes, deployment,
  and unrelated dirty work remain outside the current planning action.
- **Result at drafting:** no unresolved planning findings; implementation was
  awaiting approval. No runtime tests were run for that SOW-only edit.

## Implementation Verification

- Updated the three canonical skill bodies at authoring, finding-writeback,
  and execution preflight; internal-only work now receives the approach check.
- Added cases `chosen-approach-compatibility-authoring-001`,
  `chosen-approach-compatibility-review-001`, and
  `chosen-approach-compatibility-handoff-001` before editing the skill bodies.
- Skill-creator `quick_validate.py`: all three skill folders PASS.
- `uv run --no-sync --offline python -m unittest tests.test_skill_feedback_cases
  tests.test_skill_sync_scripts`: 13 tests PASS.
- `git diff --check`: PASS. Self-review checked unapproved additions,
  already-approved compatibility, internal-only scope, and existing support;
  no unresolved implementation findings.
- Validation covers skill structure, fixture contracts, and coordinator scenario
  review. Independent model behavioral verification was not run; no claim of
  guaranteed drift prevention is made.
- Installed copies were not synced and no push was performed. Existing foreign
  Redmine hunks in two target files are excluded from this task's commit.
