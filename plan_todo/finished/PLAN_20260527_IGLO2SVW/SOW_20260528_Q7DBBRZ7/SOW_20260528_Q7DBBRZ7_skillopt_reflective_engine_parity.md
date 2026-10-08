# SOW_20260528_Q7DBBRZ7 - skillopt reflective engine parity

- Status: completed
- Approval: approved
- create_dttm: 2026-05-28T01:05:05+07:00
- create_date: 2026-05-28
- create_dttm_source: filesystem_birthtime
- create_dttm_confidence: filesystem_proxy
- create_dttm_evidence: `plan_todo/finished/SOW_20261008_VO3LKN0L/creation-date-evidence.json` (record: SOW_20260528_Q7DBBRZ7)
- approve_dttm: unknown
- finish_dttm: unknown
- legacy_id: SOW_0047
- legacy_path: plan_todo/SOW_0047_skillopt_reflective_engine_parity.md
- migrated_dttm: 2026-10-08T12:48:51+07:00

## Preserved Contract And Historical Evidence

- **Status**: completed
- **Approval**: approved
- **Task**: Mở rộng `darwinSkill` từ loop `predict -> evaluate -> improve` hiện tại thành reflective optimization engine có các internal stages tương ứng core training loop của original SkillOpt.
- **Location**: `~/Projects/AISkills/darwinSkill/`, `~/Projects/AISkills/tests/darwinSkill/`, `~/Projects/AISkills/references/SkillOpt/skillopt/engine/`, `~/Projects/AISkills/references/SkillOpt/docs/guide/training-loop.md`
- **Why**: Đây là chênh lệch lớn nhất giữa refactor hiện tại và mục tiêu ban đầu. Nếu không tái tạo `rollout -> reflect -> aggregate -> select -> update -> gate`, framework mới chỉ là trainer đơn giản chứ chưa phải distillation đúng nghĩa của SkillOpt.
- **As-Is Diagram (ASCII)**:
```text
SkillTrainer.fit()
  -> batch loop
     -> Predict
     -> Evaluate
     -> Improve
  -> final Predict
  -> final Evaluate
  -> persist
```
- **To-Be Diagram (ASCII)**:
```text
SkillTrainer.fit()
  -> epoch loop
     -> step loop
        -> Rollout
        -> Reflect
        -> Aggregate
        -> Select
        -> Update
        -> Gate
  -> persist step/epoch/final state
```
- **Deliverables**:
  - introduce internal stage model for:
    - rollout
    - reflect
    - aggregate
    - select
    - update
    - gate
  - define typed contracts for:
    - rollout results
    - reflection outputs / patch candidates
    - aggregated candidate groups
    - selected edits
    - candidate skill artifacts
    - gate decision results
  - refactor trainer path so public `SkillTrainer.fit(...)` stays stable while internal control flow becomes multi-stage
  - preserve compatibility path for current simple text demo, either through a trivial adapter or simplified default stage implementations
  - add engine-level tests proving:
    - stage ordering
    - gate can reject candidate updates
    - aggregate/select/update can be stubbed independently
    - final persisted skill is the accepted skill, not simply the latest candidate
- **Done Criteria**:
  - `darwinSkill` can execute an end-to-end reflective step loop with explicit gate behavior
  - the internal engine no longer collapses all optimization logic into one `improve_skill(...)` call
  - public `SkillTrainer` surface remains importable and coherent
  - tests cover accept and reject paths across the new reflective engine
- **Progress Notes**:
  - reflective engine da co cac stage `rollout -> reflect -> aggregate -> select -> update -> gate`
  - da co typed contracts cho patch/group/select/gate payloads trong engine/contracts layer
  - `SkillTrainer.fit(...)` giu public surface gon trong khi noi bo chay reflective step loop
  - da co test cho persist step/epoch artifacts va gate reject path
- **Out-of-Scope**:
  - slow update / meta skill epoch memory
  - provider-specific backend routing
  - benchmark-specific adapter migration
  - usability helpers ngoài native Python API core
- **Proposed-By**: Codex GPT-5
- **plan**: `plan_todo/finished/PLAN_20260527_IGLO2SVW/PLAN_20260527_IGLO2SVW_skill_framework_distillation_plan.md`
- **Cautions / Risks**:
  - nếu leak các internal stage contracts ra public API quá sớm, caller ergonomics sẽ xấu đi
  - nếu cố bắt parity bằng cách copy trực tiếp trainer upstream, design mới sẽ mang theo legacy coupling
