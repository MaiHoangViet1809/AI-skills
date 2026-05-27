# Skill Framework Distillation Plan

## Goal

Distill `SkillOpt` thành một module tree Python-native tên `darwinSkill` để train/evaluate AI skills bằng API importable qua concrete submodules, sạch hơn và ổn định hơn cho các project nội bộ.

Plan này là source of truth ở mức chương trình cho effort distillation. Thay vì giữ một SOW quá lớn, implementation sẽ được chia thành các SOW nhỏ, tuần tự, dễ review và dễ test.

## Current Inputs

- Baseline upstream đã được intake ở `references/SkillOpt/` và `references/SkillOpt_intake.md`
- `SkillOpt` hiện mạnh ở:
  - reflective optimization loop
  - env adapter boundary
  - validation gate
- `SkillOpt` hiện yếu ở:
  - CLI-first orchestration
  - flat config dict plumbing
  - global backend state
  - public API khó nhúng lại trong project khác
- Pattern tham chiếu từ các project nội bộ:
  - facade object API từ `~/Projects/nanobot/nanobot/nanobot.py`
  - compiler/executor separation từ `~/Projects/libraries/cores/workflows/common/compiler.py`
  - backend interface/registry từ `~/Projects/hybrid_brain/core/trainers/framework/backend_base.py`
- Các quyết định đã khóa cho v1:
  - anchor use case là `text skill`
  - sample/eval contract là `prompt + expected answer + metric`
  - public API khóa sớm cả `SkillTrainer` và `SkillPipeline`
  - `SkillPipeline` v1 là linear stages tuần tự
  - branching/merge không là public graph API; caller tự orchestration bằng Python ngoài pipeline
  - proof v1 chỉ cần chạy tốt trong repo này
  - source tree dùng tên `darwinSkill/`
  - không dùng `__init__.py` hay package bootstrap; imports đi qua concrete submodules

## Final Product Shape

Framework mới nên hỗ trợ đồng thời 2 cách dùng:

- kiểu facade đơn giản:
  - `from darwinSkill.trainer import SkillTrainer`
  - `trainer = SkillTrainer(...)`
  - `trainer.fit(train_data)`
  - `trainer.evaluate(test_data)`
- kiểu composition/pipeline:
  - `from darwinSkill.pipeline import SkillPipeline`
  - `pipeline = SkillPipeline([...])`
  - `pipeline.run(...)`

Composition model v1:

- `SkillPipeline` nhận danh sách stage tuần tự
- mỗi stage nhận context/artifacts hiện tại và trả về context/artifacts kế tiếp
- không có node graph, edge graph, branch DSL, hay merge DSL ở public API v1
- nếu caller cần `if/else/merge`, caller viết orchestration bằng Python ngoài `SkillPipeline`

Kiến trúc đích:

```text
project code / notebook / service
            |
            v
   SkillTrainer / SkillPipeline facade
      |                 |
      |                 +--> composed stages / chain steps
      v
 typed config + explicit dependencies
      |
      v
 trainer core -> optimizer stages -> gate/eval
      |
      +--> adapters (dataset/env/backend/artifacts)
```

## Design Constraints

- giữ framework Python-native và importable, không phụ thuộc CLI khổng lồ
- source tree là `darwinSkill/`, không tạo package với `__init__.py`
- public imports phải dùng concrete submodules, ví dụ `darwinSkill.trainer`, `darwinSkill.pipeline`
- không dùng global mutable backend state trong public API
- tách core framework khỏi benchmark-specific logic
- ưu tiên mockable/testable boundaries trước khi thêm benchmark thật
- chưa theo đuổi parity đầy đủ với toàn bộ upstream `SkillOpt`
- contract công khai phải chốt sớm và không đổi giữa `0042` đến `0045` trừ khi có SOW mới

## Public Interfaces To Lock In Phase 1

- `SkillSample`
  - typed object, không dùng raw dict ở public API
  - fields tối thiểu: `prompt`, `expected_answer`, `metadata`
- `MetricResult`
  - typed object cho kết quả một sample
  - fields tối thiểu: `score`, `passed`, `details`
- `EvaluationReport`
  - typed object cho kết quả aggregate của `evaluate(...)`
  - chứa aggregate metrics và per-sample results theo contract thống nhất
- `SkillEvaluator`
  - entrypoint tối thiểu nhận prediction + sample
  - trả về `MetricResult`
- `SkillTrainer`
  - `fit(samples: Sequence[SkillSample], ...) -> RunArtifacts`
  - `evaluate(samples: Sequence[SkillSample], ...) -> EvaluationReport`
- `SkillPipeline`
  - `run(samples: Sequence[SkillSample], ...) -> RunArtifacts`
  - linear stages only
- `SkillStage`
  - protocol cho một stage tuần tự dùng lại được giữa trainer path và pipeline path
  - stage nhận typed run context và trả về typed run context, không dùng raw dict context ở public contract
- `RunArtifacts`
  - typed object chuẩn cho outputs và persistence của train/pipeline runs

## SOW Breakdown

### SOW_0042_skill_framework_contracts_and_skeleton.md

Focus:

- tạo module tree `darwinSkill/`
- khóa contracts cho `SkillTrainer`, `SkillPipeline`, `RunArtifacts`
- khóa typed config/object model
- khóa interfaces cho sample/evaluator/backend/stages
- khóa anchor text-skill sample schema

Why grouped:

- đây là boundary slice nhỏ nhất nhưng ảnh hưởng toàn bộ architecture
- cần chốt contracts trước khi viết runtime thật

### SOW_0043_skill_trainer_core_and_artifacts.md

Focus:

- implement trainer core tối thiểu
- implement train/eval lifecycle cơ bản
- implement artifact persistence và run state
- dùng mock text backend + mock evaluator để validate control flow

Why grouped:

- đây là lõi thực thi đầu tiên
- có thể kiểm chứng sớm bằng test mà chưa cần benchmark thật

### SOW_0044_skill_pipeline_and_demo_adapter.md

Focus:

- implement runtime cho `SkillPipeline` linear stages
- map core loop vào stage abstraction đã khóa ở `0042`
- thêm demo text-skill path dựa trên `prompt + expected answer + metric`
- chứng minh coexistence giữa facade API và pipeline API mà không thêm graph semantics

Why grouped:

- phần này là nơi reconcile giữa metaphor `sklearn` và chain ops
- nên làm sau khi core loop đã ổn định

### SOW_0045_skill_framework_examples_and_smoke.md

Focus:

- thêm scripts/examples mỏng cho usage thật
- thêm docs usage ngắn
- integration smoke tests cho facade path và pipeline path
- cleanup naming và import ergonomics
- nói rõ branching/merge nằm ở Python caller, không ở pipeline core

Why grouped:

- đây là last-mile usability và acceptance
- nên làm sau khi contracts và runtime đã chốt

### SOW_0046_skill_framework_hardening_and_eval_persistence.md

Focus:

- implement eval-only artifact persistence cho trainer path
- nâng `run state` từ history tạm thành contract/persistence rõ ràng hơn
- harden import/reuse path cho examples và module consumption
- thêm failure-mode tests và contract-depth tests còn thiếu

Why grouped:

- đây là follow-up slice phát sinh từ review sau implementation đầu tiên
- gom các gap còn lại về completeness và quality bar mà không mở rộng scope sang graph API hay benchmark parity

## Execution Order

1. `SOW_0042`
2. `SOW_0043`
3. `SOW_0044`
4. `SOW_0045`
5. `SOW_0046`

## Program-Level Acceptance

Khi toàn plan hoàn tất:

- repo có module tree `darwinSkill/` importable qua concrete submodules để train/evaluate skill bằng Python API
- có cả facade path và pipeline path
- framework core không buộc người dùng phải chạy qua CLI lớn
- có mockable contracts cho adapter/backend/stage/artifacts
- có ít nhất một demo text-skill path dùng `prompt + expected answer + metric`
- public pipeline API chỉ là linear stages và được test rõ
- trainer path có eval-only persistence rõ ràng
- run state có contract/persistence rõ ràng hơn history tạm

## Out-of-Scope For This Plan

- parity toàn bộ benchmark upstream `SkillOpt`
- reproduction paper metrics
- web UI/dashboard cho framework mới
- migration toàn bộ project trong `~/Projects`
- integration sâu với workflow engines như Temporal
- public graph workflow API cho pipeline
- package bootstrap bằng `__init__.py`

## Risks

- nếu ép chặt vào `sklearn` metaphor thì sẽ làm nghèo hóa multi-stage reflective optimization
- nếu giữ quá gần shape cũ của `SkillOpt` thì framework mới vẫn mang legacy CLI/config
- nếu generalize quá sớm trước khi có mock/demo path, contracts sẽ khó kiểm chứng
- nếu đưa graph semantics vào quá sớm, phase 1 sẽ khóa nhầm API và làm tăng blast radius refactor
