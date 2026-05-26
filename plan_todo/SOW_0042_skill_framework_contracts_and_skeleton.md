- **Status**: draft
- **Approval**: pending
- **Task**: Tạo skeleton framework Python-native cho skill training/evaluation và chốt các contracts cốt lõi trước khi viết runtime thực thi.
- **Location**: `~/Projects/AISkills/aiskills_common/skill_framework/`, `~/Projects/AISkills/tests/skill_framework/`, `~/Projects/AISkills/pyproject.toml`
- **Why**: Phase đầu cần khóa boundary và object model để các phase sau không phải refactor lại kiến trúc nền. Đây là bước thay thế public surface CLI/dict-heavy của `SkillOpt` bằng contracts importable, typed, và rõ dependency.
- **As-Is Diagram (ASCII)**:
```text
consumer code
    |
    v
 no local skill framework package
    |
    v
 ad hoc direct scripts or future guesswork
```
- **To-Be Diagram (ASCII)**:
```text
consumer code
    |
    v
 skill_framework package
    |
    +--> SkillTrainer contract
    +--> SkillPipeline contract
    +--> typed config objects
    +--> backend/env/stage/artifact interfaces
```
- **Deliverables**:
  - tạo package `aiskills_common/skill_framework/`
  - define public contracts tối thiểu: `SkillTrainer`, `SkillPipeline`, `RunArtifacts`
  - define typed config/object model cho run/training/eval
  - define interfaces cho dataset source, env adapter, backend client, optimizer stage, gate/evaluator
  - thêm unit tests cho contract construction/import shape
  - cập nhật `pyproject.toml` nếu cần để package mới import được sạch
- **Done Criteria**:
  - package mới import được trong repo
  - public names và module boundaries rõ ràng
  - không còn phụ thuộc vào flat dict/global backend state ở API surface mới
  - tests xác nhận object creation và contract invariants pass
- **Out-of-Scope**:
  - chưa implement trainer loop hoàn chỉnh
  - chưa persistence artifacts thật
  - chưa demo adapter hay benchmark flow
- **Proposed-By**: Codex GPT-5
- **plan**: `~/Projects/AISkills/plan_todo/skill_framework_distillation_plan.md`
- **Cautions / Risks**:
  - nếu contracts quá abstract sẽ khó dùng ở phase sau
  - nếu contracts quá gần implementation thì phase đầu sẽ khóa cứng thiết kế
