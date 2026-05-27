- **Status**: in_progress
- **Approval**: approved
- **Task**: Xây adapter, dataloader, batch spec, và config migration layer cho `darwinSkill` để benchmark/runtime có thể chạy trên framework mới qua native Python API mà không quay lại CLI-first architecture.
- **Location**: `~/Projects/AISkills/darwinSkill/`, `~/Projects/AISkills/tests/darwinSkill/`, `~/Projects/AISkills/references/SkillOpt/skillopt/envs/`, `~/Projects/AISkills/references/SkillOpt/skillopt/datasets/`, `~/Projects/AISkills/references/SkillOpt/skillopt/config.py`
- **Why**: Benchmark parity phụ thuộc trực tiếp vào cách original SkillOpt build batches, splits, eval envs, và config resolution. Nếu không tái tạo lớp này, các SOW benchmark sau sẽ phải nhét logic benchmark vào trainer core.
- **As-Is Diagram (ASCII)**:
```text
caller provides list[SkillSample]
  -> trainer/pipeline runs directly
```
- **To-Be Diagram (ASCII)**:
```text
config loader / builder
  -> adapter registry
  -> dataloader / batch spec
  -> train batch / eval batch builders
  -> trainer engine
```
- **Deliverables**:
  - define importable adapter and dataloader interfaces for train/eval split construction
  - create typed batch spec objects for rollout and evaluation
  - add config loading layer that can:
    - read structured configs
    - map compatibility fields from legacy-style settings
    - hand resolved objects into native Python API helpers and framework objects
  - add tests for:
    - adapter registry resolution
    - split/batch creation contracts
    - structured config mapping
    - legacy-compat override translation
- **Done Criteria**:
  - benchmark adapters can plug into framework through explicit contracts instead of ad hoc caller wiring
  - config loading is usable from Python without requiring CLI wrappers
  - trainer no longer assumes raw sample lists are the only input path
- **Out-of-Scope**:
  - provider execution internals
  - actual migration of each benchmark implementation
  - UI layer
- **Proposed-By**: Codex GPT-5
- **plan**: `~/Projects/AISkills/plan_todo/skill_framework_distillation_plan.md`
- **Cautions / Risks**:
  - config compatibility layer dễ phình thành flat-dict legacy nếu không siết object boundaries
  - adapter contracts phải đủ giàu cho interactive envs, không chỉ text QA
