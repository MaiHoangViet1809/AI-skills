- **Status**: draft
- **Approval**: pending
- **Task**: Tạo skeleton framework Python-native cho text-skill training/evaluation và khóa các public contracts cốt lõi, gồm cả `SkillTrainer` và `SkillPipeline`, trước khi viết runtime thực thi.
- **Location**: `~/Projects/AISkills/darwinSkill/`, `~/Projects/AISkills/tests/darwinSkill/`, `~/Projects/AISkills/scripts/darwinSkill/`
- **Why**: Phase đầu cần khóa boundary và object model để các phase sau không phải refactor lại kiến trúc nền. Đây là bước thay thế public surface CLI/dict-heavy của `SkillOpt` bằng contracts importable, typed, và rõ dependency, đồng thời khóa sớm linear-pipeline API để tránh drift giữa facade path và pipeline path.
- **As-Is Diagram (ASCII)**:
```text
consumer code
    |
    v
 no local darwinSkill module tree
    |
    v
 ad hoc direct scripts or future guesswork
```
- **To-Be Diagram (ASCII)**:
```text
consumer code
    |
    v
 darwinSkill module tree
    |
    +--> SkillTrainer contract
    +--> SkillPipeline contract
    +--> SkillStage contract
    +--> SkillSample / SkillEvaluator contract
    +--> typed config objects
    +--> backend/artifact interfaces
```
- **Deliverables**:
  - tạo module tree `darwinSkill/` không dùng `__init__.py`
  - define public contracts cố định: `SkillTrainer`, `SkillPipeline`, `SkillStage`, `RunArtifacts`, `SkillSample`, `SkillEvaluator`, `MetricResult`, `EvaluationReport`
  - define typed config/object model cho run/training/eval của anchor `text skill`
  - define `SkillPipeline` là linear stages tuần tự; không có graph DSL, branch DSL, hay merge DSL
  - define sample schema v1 gồm `prompt`, `expected_answer`, và `metadata`
  - define `MetricResult` với fields tối thiểu `score`, `passed`, `details`
  - define `EvaluationReport` cho aggregate output của `SkillTrainer.evaluate(...)`
  - define evaluator contract v1 nhận prediction + sample và trả về `MetricResult`
  - define `SkillTrainer.fit(samples, ...) -> RunArtifacts`
  - define `SkillTrainer.evaluate(samples, ...) -> EvaluationReport`
  - define `SkillPipeline.run(samples, ...) -> RunArtifacts`
  - define `SkillStage` nhận/trả về typed run context thay vì raw dict context
  - chốt concrete import paths qua submodules, ví dụ `darwinSkill.trainer` và `darwinSkill.pipeline`
  - define backend client interface và artifact interface dùng chung cho trainer path và pipeline path
  - thêm unit tests cho contract construction/import shape
  - thêm test-level usage examples chứng minh shape của `SkillTrainer.fit/evaluate` và `SkillPipeline.run`
- **Done Criteria**:
  - module tree `darwinSkill/` import được trong repo qua concrete submodules
  - public names, sample schema, metric/evaluation shapes, và module boundaries rõ ràng
  - không còn phụ thuộc vào flat dict/global backend state ở API surface mới
  - tests xác nhận object creation, pipeline linear-stage invariants, và evaluator contract pass
- **Out-of-Scope**:
  - chưa implement trainer loop hoàn chỉnh
  - chưa persistence artifacts thật
  - chưa chạy benchmark/demo flow
  - chưa hỗ trợ branching/merge ở public pipeline API
- **Proposed-By**: Codex GPT-5
- **plan**: `~/Projects/AISkills/plan_todo/skill_framework_distillation_plan.md`
- **Cautions / Risks**:
  - nếu contracts quá abstract sẽ khó dùng ở phase sau
  - nếu pipeline contract ôm nhiều semantics hơn linear stages, phase đầu sẽ khóa sai API
  - nếu vô tình quay lại pattern package bootstrap, source layout sẽ lệch khỏi constraint đã chốt
