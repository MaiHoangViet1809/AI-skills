# SOW_20260708_ODVOSEOS - review darwinskill regroup

- Status: complete
- Approval: approved 2026-07-08
- create_dttm: 2026-07-08T01:30:08+07:00
- create_date: 2026-07-08
- create_dttm_source: filesystem_birthtime
- create_dttm_confidence: filesystem_proxy
- create_dttm_evidence: `plan_todo/finished/SOW_20261008_VO3LKN0L/creation-date-evidence.json` (record: SOW_20260708_ODVOSEOS)
- approve_dttm: unknown
- finish_dttm: unknown
- legacy_id: SOW_0067
- legacy_path: plan_todo/finished/SOW_0067_review_darwinskill_regroup.md
- migrated_dttm: 2026-10-08T12:48:51+07:00

## Preserved Contract And Historical Evidence

- **Status**: complete
- **Approval**: approved 2026-07-08
- **Task**: Review the scattered `darwinSkill` surfaces and produce a concrete regrouping recommendation without moving framework files in this SOW.
- **Location**: `darwinSkill/`, `scripts/darwinSkill/`, `tests/darwinSkill/`, `plan_todo/SOW_0047_*.md` through `plan_todo/SOW_0055_*.md`, `plan_todo/active/PLAN_20260529_6P2SEP78/PLAN_20260529_6P2SEP78_codex_skill_improvement_data_plan.md`, `plan_todo/finished/PLAN_20260527_IGLO2SVW/PLAN_20260527_IGLO2SVW_skill_framework_distillation_plan.md`, `references/SkillOpt/`, and a new review artifact under `plan_todo/`.
- **Why**: `darwinSkill` currently spans package code, scripts, tests, active SOWs, reference source, and docs. Before moving files, the repo needs a reviewed target layout and risk map.
- **Depends-On**: `plan_todo/agent_skill_library_cleanup_plan.md`
- **As-Is Diagram (ASCII)**:
```text
darwinSkill/              framework code + docs
scripts/darwinSkill/      demos and extraction scripts
tests/darwinSkill/        tests
plan_todo/SOW_0047-0055   active/stale implementation docs
references/SkillOpt/      upstream reference snapshot
```
- **To-Be Diagram (ASCII)**:
```text
review artifact
  -> current inventory
  -> recommended target layout
  -> stale/active SOW classification
  -> migration risks
  -> follow-up migration SOW if needed
```
- **Deliverables**:
  - Inventory all `darwinSkill` owned files and adjacent references.
  - Classify current surfaces as framework code, scripts, tests, docs, reference source, generated/cache, or planning.
  - Review whether active SOWs 0047-0055 are still valid, stale, partially complete, or should be moved to `finished/`.
  - Propose one target layout and explain why it is better than the current split.
  - Explicitly compare keeping the conventional layout versus grouping under a clearer project boundary such as `projects/darwinSkill/` or `darwinSkill_workspace/`.
  - Identify tracked/generated cache artifacts if any are present; do not remove them in this review SOW.
  - Create a review artifact under `plan_todo/` with recommended next SOWs.
- **Done Criteria**:
  - No `darwinSkill` code, test, or script file is moved in this SOW.
  - The review artifact lists exact paths and recommended disposition.
  - Active/stale planning docs are classified.
  - Any file-move or import-path migration is deferred to a separate approved SOW.
  - Worktree changes do not include unrelated staged user deletions unless separately approved.
- **Out-of-Scope**:
  - Moving `darwinSkill` package, scripts, or tests.
  - Changing import paths.
  - Refactoring framework logic.
  - Removing telemetry/dashboard surfaces.
  - Replacing `create-agents-md`.
- **Proposed-By**: Codex GPT-5
- **plan**: `plan_todo/agent_skill_library_cleanup_plan.md`
- **Cautions / Risks**:
  - Import-path migration can break a large test surface; keep review separate from migration.
  - Some planning docs may be historical but still useful for parity context.
  - Do not delete generated/cache artifacts in this review SOW unless a follow-up cleanup SOW explicitly approves it.
