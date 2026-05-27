- **Status**: draft
- **Approval**: pending
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
- **Out-of-Scope**:
  - slow update / meta skill epoch memory
  - provider-specific backend routing
  - benchmark-specific adapter migration
  - CLI/operator parity
- **Proposed-By**: Codex GPT-5
- **plan**: `~/Projects/AISkills/plan_todo/skill_framework_distillation_plan.md`
- **Cautions / Risks**:
  - nếu leak các internal stage contracts ra public API quá sớm, caller ergonomics sẽ xấu đi
  - nếu cố bắt parity bằng cách copy trực tiếp trainer upstream, design mới sẽ mang theo legacy coupling

