- **Status**: draft
- **Approval**: pending
- **Task**: Tái tạo các mechanics cuối epoch của SkillOpt gồm `slow update`, longitudinal comparison, và `meta skill` memory trong `darwinSkill`.
- **Location**: `~/Projects/AISkills/darwinSkill/`, `~/Projects/AISkills/tests/darwinSkill/`, `~/Projects/AISkills/references/SkillOpt/skillopt/optimizer/`, `~/Projects/AISkills/references/SkillOpt/skillopt/engine/trainer.py`
- **Why**: Đây là phần giúp original SkillOpt chống catastrophic forgetting và duy trì optimizer memory giữa các epoch. Nếu bỏ phần này thì engine parity chỉ mới ngang step loop chứ chưa đạt learning dynamics của original project.
- **As-Is Diagram (ASCII)**:
```text
epoch N
  -> finish batches
  -> move on
```
- **To-Be Diagram (ASCII)**:
```text
epoch N
  -> step loop complete
  -> longitudinal compare(prev vs curr)
  -> slow update guidance injection
  -> meta skill memory write
  -> epoch N+1 reflect uses accumulated memory
```
- **Deliverables**:
  - add epoch-boundary hooks for:
    - longitudinal comparison pair building
    - pair categorization: improved / regressed / persistent_fail / stable_success
    - slow update guidance generation and injection
    - meta skill memory generation and reuse
  - persist artifacts under dedicated epoch directories such as:
    - `slow_update/epoch_XX/`
    - `meta_skill/epoch_XX/`
  - define typed contracts for comparison pairs, slow update result, and meta skill content
  - add tests for:
    - first epoch placeholder or skip semantics
    - later epoch comparison flow
    - memory reuse in the next epoch
    - missing comparison data fallback behavior
- **Done Criteria**:
  - epoch-boundary mechanisms exist as first-class runtime behavior
  - slow update and meta skill artifacts are persisted and inspectable
  - trainer can carry strategy memory from prior epochs into later reflective steps
  - tests prove non-trivial epoch-to-epoch behavior rather than single-epoch only
- **Out-of-Scope**:
  - provider-specific prompting quality
  - full benchmark migration
  - WebUI visualization of slow-update/meta-skill artifacts
- **Proposed-By**: Codex GPT-5
- **plan**: `~/Projects/AISkills/plan_todo/skill_framework_distillation_plan.md`
- **Cautions / Risks**:
  - nếu comparison-pair schema không ổn định, benchmark adapters sẽ phải rewrite nhiều lần
  - memory injection cần tránh làm bẩn public trainer API

