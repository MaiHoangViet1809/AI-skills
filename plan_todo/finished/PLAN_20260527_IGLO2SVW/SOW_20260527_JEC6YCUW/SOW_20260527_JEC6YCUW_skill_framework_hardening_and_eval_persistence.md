# SOW_20260527_JEC6YCUW - skill framework hardening and eval persistence

- Status: done
- Approval: approved
- create_dttm: 2026-05-27T14:34:13+07:00
- create_date: 2026-05-27
- create_dttm_source: filesystem_birthtime
- create_dttm_confidence: filesystem_proxy
- create_dttm_evidence: `plan_todo/finished/SOW_20261008_VO3LKN0L/creation-date-evidence.json` (record: SOW_20260527_JEC6YCUW)
- approve_dttm: unknown
- finish_dttm: unknown
- legacy_id: SOW_0046
- legacy_path: plan_todo/finished/SOW_0046_skill_framework_hardening_and_eval_persistence.md
- migrated_dttm: 2026-10-08T12:48:51+07:00

## Preserved Contract And Historical Evidence

- **Status**: done
- **Approval**: approved
- **Task**: Hoàn thiện các gap còn lại của `darwinSkill` bằng cách thêm eval-only artifact persistence, siết `run state`, harden import/reuse path, và mở rộng test coverage cho failure modes và contract depth.
- **Location**: `~/Projects/AISkills/darwinSkill/`, `~/Projects/AISkills/tests/darwinSkill/`, `~/Projects/AISkills/scripts/darwinSkill/`, `plan_todo/finished/PLAN_20260527_IGLO2SVW/PLAN_20260527_IGLO2SVW_skill_framework_distillation_plan.md`
- **Why**: Review sau implementation đầu tiên cho thấy framework đã chạy được nhưng chưa đủ sâu ở 4 điểm: `SkillTrainer.evaluate(...)` chưa persist artifacts, `run state` mới chỉ là history tạm, examples còn phụ thuộc path bootstrapping ad hoc, và tests chưa bao phủ failure modes chính. Slice này đóng các gap đó mà không đổi hướng kiến trúc đã khóa.
- **As-Is Diagram (ASCII)**:
```text
SkillTrainer.fit() -> persisted artifacts
SkillTrainer.evaluate() -> in-memory report only

run state -> transient history list

examples -> direct sys.path bootstrapping

tests -> mostly happy path
```
- **To-Be Diagram (ASCII)**:
```text
SkillTrainer.fit()      -> persisted artifacts
SkillTrainer.evaluate() -> persisted artifacts + report

run state -> typed state contract + persisted state file

examples -> cleaner module consumption path

tests -> happy path + failure modes + persistence checks
```
- **Deliverables**:
  - implement eval-only artifact persistence for `SkillTrainer.evaluate(...)`
  - define and persist a clearer run-state contract beyond ad hoc history-only tracking
  - update trainer-path persistence so eval runs can be inspected/read back like train runs
  - reduce ad hoc import bootstrapping in examples/scripts as far as repo constraints allow, while preserving the no-`__init__.py` decision
  - add tests for:
    - eval-only artifact writes
    - run-state persistence/readback
    - missing or invalid pipeline stage sequencing
    - empty samples and invalid config edge cases
    - failing evaluator/backend behavior where contract checks should raise
  - update docs/examples if import/reuse behavior changes
- **Done Criteria**:
  - `SkillTrainer.evaluate(...)` writes a reviewable artifact bundle or equivalent persisted eval output under the existing artifact model
  - framework exposes a clearer persisted run-state artifact than a transient in-memory history list
  - examples remain runnable and cleaner with respect to module consumption assumptions
  - tests cover both happy path and the main failure modes identified in review
  - no change to the previously locked public scope of linear-only `SkillPipeline`
- **Out-of-Scope**:
  - không thêm graph/branch/merge pipeline API
  - không theo đuổi benchmark parity với upstream SkillOpt
  - không đổi anchor khỏi `text skill`
  - không mở rộng sang cross-project integration proof ngoài repo này
- **Proposed-By**: Codex GPT-5
- **plan**: `plan_todo/finished/PLAN_20260527_IGLO2SVW/PLAN_20260527_IGLO2SVW_skill_framework_distillation_plan.md`
- **Cautions / Risks**:
  - cần giữ slice này là hardening của scope cũ, không để trượt thành redesign mới
  - run-state contract phải đủ rõ để hữu ích nhưng không nên phình thành resume engine đầy đủ nếu plan chưa yêu cầu
