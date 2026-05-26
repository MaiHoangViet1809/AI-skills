# Skill Framework Distillation Plan

## Goal

Distill `SkillOpt` thành một framework Python-native để train/evaluate AI skills bằng API importable, sạch hơn và ổn định hơn cho các project nội bộ.

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

## Final Product Shape

Framework mới nên hỗ trợ đồng thời 2 cách dùng:

- kiểu facade đơn giản:
  - `trainer = SkillTrainer(...)`
  - `trainer.fit(train_data)`
  - `trainer.evaluate(test_data)`
- kiểu composition/pipeline:
  - `pipeline = SkillPipeline([...])`
  - `pipeline.run(...)`

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
- không dùng global mutable backend state trong public API
- tách core framework khỏi benchmark-specific logic
- ưu tiên mockable/testable boundaries trước khi thêm benchmark thật
- chưa theo đuổi parity đầy đủ với toàn bộ upstream `SkillOpt`

## SOW Breakdown

### SOW_0042_skill_framework_contracts_and_skeleton.md

Focus:

- tạo package `aiskills_common/skill_framework/`
- define contracts cho `SkillTrainer`, `SkillPipeline`, `RunArtifacts`
- define typed config/object model
- define interfaces cho dataset/env/backend/stages

Why grouped:

- đây là boundary slice nhỏ nhất nhưng ảnh hưởng toàn bộ architecture
- cần chốt contracts trước khi viết runtime thật

### SOW_0043_skill_trainer_core_and_artifacts.md

Focus:

- implement trainer core tối thiểu
- implement train/eval lifecycle cơ bản
- implement artifact persistence và run state
- dùng mock backend + mock adapter để validate control flow

Why grouped:

- đây là lõi thực thi đầu tiên
- có thể kiểm chứng sớm bằng test mà chưa cần benchmark thật

### SOW_0044_skill_pipeline_and_demo_adapter.md

Focus:

- thêm composition/pipeline execution path
- map core loop vào chain/step abstraction
- thêm một demo adapter/backend stub hoặc local mock benchmark
- chứng minh coexistence giữa facade API và pipeline API

Why grouped:

- phần này là nơi reconcile giữa metaphor `sklearn` và chain ops
- nên làm sau khi core loop đã ổn định

### SOW_0045_skill_framework_examples_and_smoke.md

Focus:

- thêm scripts/examples mỏng cho usage thật
- thêm docs usage ngắn
- integration smoke tests cho facade path và pipeline path
- cleanup naming và import ergonomics

Why grouped:

- đây là last-mile usability và acceptance
- nên làm sau khi contracts và runtime đã chốt

## Execution Order

1. `SOW_0042`
2. `SOW_0043`
3. `SOW_0044`
4. `SOW_0045`

## Program-Level Acceptance

Khi toàn plan hoàn tất:

- repo có package framework importable để train/evaluate skill bằng Python API
- có cả facade path và pipeline path
- framework core không buộc người dùng phải chạy qua CLI lớn
- có mockable contracts cho adapter/backend/stage/artifacts
- có ít nhất một demo path chứng minh khả năng nhúng vào project nội bộ

## Out-of-Scope For This Plan

- parity toàn bộ benchmark upstream `SkillOpt`
- reproduction paper metrics
- web UI/dashboard cho framework mới
- migration toàn bộ project trong `~/Projects`
- integration sâu với workflow engines như Temporal

## Risks

- nếu ép chặt vào `sklearn` metaphor thì sẽ làm nghèo hóa multi-stage reflective optimization
- nếu giữ quá gần shape cũ của `SkillOpt` thì framework mới vẫn mang legacy CLI/config
- nếu generalize quá sớm trước khi có mock/demo path, contracts sẽ khó kiểm chứng
