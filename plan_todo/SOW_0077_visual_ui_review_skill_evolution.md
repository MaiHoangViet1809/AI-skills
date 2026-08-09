# SOW_0077 - Visual UI Review Verification Rule

- **Status**: in progress
- **Approval**: approved by user on 2026-08-09
- **Task**: Evolve `task-review-investigate-compare` so UI-visible double-checks require visual/runtime evidence when feasible, not only source grep, unit tests, or build checks.
- **Location**:
  - `skills/task-review-investigate-compare/SKILL.md`
  - `tests/skill_feedback_cases/task-review-investigate-compare.json`
  - optional exact local sync target after approval: `/Users/maihoangviet/.codex/skills/task-review-investigate-compare/`
- **Why**: A UI-visible output panel passed source/test/build double-checks but still had obvious visual defects in the real canvas: mismatched panel width, oversized title/header section, unnecessary refresh action, empty data area, and unconfirmed table component choice.
- **Proposed-By**: Codex GPT-5
- **Plan / Reference**:
  - User feedback on 2026-08-09: UI double-checks are insufficient when they do not inspect the rendered UI.
  - Triggering project: `/Users/maihoangviet/Projects/libraries`
  - Triggering feature: `SOW_0406_view_output_panel`
  - Target skill: `task-review-investigate-compare`

## Project Guardrail Audit

- `AGENTS.md` requires SOW-first for behavior-bearing skill edits.
- `skill-evolution-flow` requires canonical skill update in AISkills, a sanitized regression case, validation, commit, and one selected sync target.
- Existing AISkills worktree is dirty in related skill files; implementation must preserve unrelated existing changes and stage only approved files.

## As-Is Diagram (ASCII)

```text
User asks: double check UI feature
        |
        v
Source grep + unit tests + build
        |
        v
"No findings"
        |
        v
Rendered UI still visibly wrong
```

## To-Be Diagram (ASCII)

```text
User asks: double check UI-visible feature
        |
        v
Classify changed surface
        |
        +-- non-UI path -> source/tests/build may be enough
        |
        +-- UI-visible path
              |
              +-> inspect rendered UI when feasible
              +-> compare screenshot/DOM/CSS/component ownership
              +-> verify data-present and empty-state paths separately
              +-> state "not visually verified" if real UI was not checked
```

## Deliverables

- Add a general rule to `task-review-investigate-compare` that UI-visible review/double-check must include rendered UI evidence when feasible.
- Add a negative/abstain rule: do not claim UI quality from source grep, unit tests, or build alone.
- Add a boundary rule: if browser/runtime UI cannot be run, say visual verification is not complete and list residual visual risks.
- Add sanitized feedback fixture covering expected, negative, and boundary scenarios.
- Validate skill structure and feedback fixtures.
- Commit approved AISkills changes.
- Sync only `task-review-investigate-compare` to the selected local Codex skill root and verify parity, if approval includes deployment.

## Done Criteria

- The skill explicitly distinguishes static/code verification from rendered UI verification.
- Regression fixture includes this UI-double-check failure mode without private transcript or machine-specific details.
- `uv run python -m unittest tests.test_skill_feedback_cases tests.test_skill_sync_scripts` passes.
- Available skill validator passes for `skills/task-review-investigate-compare`.
- Diff review confirms no unrelated dirty AISkills changes were staged.
- Commit is created unless user explicitly defers.
- If deployed, exact dry-run sync, actual sync, and `verify_skill_copy.py` parity pass for only this skill.

## Out-of-Scope

- Changing app code in `/Users/maihoangviet/Projects/libraries`.
- Creating a generic UI automation framework.
- Updating unrelated skills or syncing all installed skills.
- Copying private screenshots or transcript text into fixtures.

## Cautions / Risks

- Visual verification may be infeasible when the app cannot be started; the skill must require honest residual-risk reporting, not force brittle automation.
- Existing uncommitted AISkills changes touch related skill files; implementation must avoid overwriting or staging unrelated edits.
- This skill update prevents future false confidence; it does not fix the current app UI defect by itself.
