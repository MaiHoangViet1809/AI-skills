# Skill Framework Distillation Plan

## Goal

Distill `SkillOpt` thành một module tree Python-native tên `darwinSkill` để train/evaluate AI skills bằng API importable qua concrete submodules, nhưng vẫn tái tạo lại đầy đủ chức năng cốt lõi và các bề mặt vận hành chính của original project.

Plan này là source of truth ở mức chương trình cho effort distillation. Mục tiêu không chỉ là một v1 skeleton dễ nhúng, mà là một framework sạch hơn về API nhưng vẫn đạt functional parity với snapshot `references/SkillOpt/` ở các lớp: optimizer engine, runtime state, backend routing, adapter/config layer, benchmark surfaces, và native Python usage surfaces.

## Current Inputs

- Baseline upstream đã được intake ở `references/SkillOpt/` và `references/SkillOpt_intake.md`
- `SkillOpt` hiện mạnh ở:
  - reflective optimization loop
  - env adapter boundary
  - validation gate
  - epoch-boundary memory mechanisms như slow update và meta skill
  - multi-backend execution routing
  - benchmark-specific adapters/dataloaders đủ giàu để chạy end-to-end
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
- Thực tế implementation hiện tại mới hoàn thành phase v1 skeleton:
  - facade API đã có
  - linear pipeline đã có
  - demo text-skill path đã có
  - nhưng mechanics của original SkillOpt mới chỉ được tái hiện một phần nhỏ

## Program Principle

Nguyên tắc kiến trúc của phase tiếp theo:

- không đổi hướng API sạch để lấy parity
- không chấp nhận giữ v1 mỏng như trạng thái cuối
- public API có thể vẫn nhỏ, nhưng internal engine phải mở rộng để mang lại chức năng tương đương upstream
- nếu original có một mechanics lõi, ưu tiên tái tạo nó trong internal engine hoặc native Python helper layer, không đẩy trách nhiệm đó ra caller code trừ khi có lý do rõ ràng
- parity ở đây là functional parity, không phải copy nguyên xi cấu trúc file hay implementation detail của upstream

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

Kiến trúc đích sau parity reconstruction:

```text
project code / service / notebook
                |
                v
    clean darwinSkill public API surface
    - SkillTrainer.fit/evaluate
    - SkillPipeline.run
    - helper builders for native Python orchestration
                |
                v
      internal reflective optimization engine
      - rollout
      - reflect
      - aggregate
      - select
      - update
      - gate
      - slow update
      - meta skill
                |
                v
   explicit backends + adapters + dataloaders + config loader
                |
                v
   benchmark modules / artifact persistence / parity docs
```

## Design Constraints

- giữ framework Python-native và importable, không phụ thuộc CLI
- source tree là `darwinSkill/`, không tạo package với `__init__.py`
- public imports phải dùng concrete submodules, ví dụ `darwinSkill.trainer`, `darwinSkill.pipeline`
- không dùng global mutable backend state trong public API; nếu cần compatibility internals thì phải được bọc lại phía sau object boundary
- CLI wrappers và WebUI là out-of-scope cho plan này
- tách core framework khỏi benchmark-specific logic
- ưu tiên mockable/testable boundaries trước khi thêm benchmark thật
- contract công khai phải giữ ổn định càng nhiều càng tốt; parity expansion nên đi vào internal engine trước
- parity với upstream phải được chia nhỏ thành nhiều SOW độc lập để không trượt thành một mega-change khó review
- benchmark parity chỉ tính trên snapshot `references/SkillOpt/` đang có trong repo này

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

### SOW_0047_skillopt_reflective_engine_parity.md

Focus:

- tách `improve` đơn giản hiện tại thành reflective optimization engine có các internal stages tương ứng upstream:
  - rollout
  - reflect
  - aggregate
  - select
  - update
  - gate
- thiết kế typed contracts cho patch candidates, selected edits, candidate skill, và gate decision
- giữ facade API gọn nhưng cho phép trainer path chạy một step loop giàu hơn thay vì `predict -> evaluate -> improve` đơn giản

Why grouped:

- đây là chênh lệch lớn nhất giữa v1 skeleton và original SkillOpt
- nếu không làm slice này trước, các slice parity khác sẽ không có engine đúng để bám vào

### SOW_0048_skillopt_runtime_state_resume_and_artifact_lineage.md

Focus:

- mở rộng artifact model để lưu state theo step/epoch thay vì chỉ final summary
- thêm runtime state rõ ràng cho resume, current skill, best skill, selected candidate lineage, và step records
- chuẩn hóa skill versioning, per-step directories, trajectory/step digests, và artifact readback contracts

Why grouped:

- original SkillOpt không chỉ có loop giàu, mà còn có persistence đủ sâu để inspect và resume
- đây là lớp hạ tầng bắt buộc để các mechanics như gate, slow update, meta skill có thể vận hành đúng

### SOW_0049_skillopt_epoch_memory_parity.md

Focus:

- tái tạo `slow update` và `meta skill` như epoch-boundary mechanisms
- thêm longitudinal comparison pairs, changed/regressed/stable categorizations, và injected guidance/memory flow
- lưu artifact riêng cho `slow_update/` và `meta_skill/` theo epoch

Why grouped:

- đây là mechanics lõi được paper/original dùng để chống quên và tích lũy chiến lược
- tách riêng giúp review rõ memory logic mà không lẫn với step engine

### SOW_0050_skillopt_backend_router_and_dual_role_execution.md

Focus:

- đưa vào model/backend layer có phân vai rõ optimizer backend và target backend
- hỗ trợ backend routing/config compatibility cho các provider chính trong original snapshot:
  - Azure/OpenAI-style chat
  - Codex exec-style target path
  - Claude code/chat-style path
  - Qwen chat-style path
- bọc compatibility state để caller vẫn inject dependencies rõ ràng qua Python API

Why grouped:

- original project phụ thuộc mạnh vào dual-role execution, không chỉ một backend `predict/improve`
- tách slice này khỏi engine core giúp cô lập rủi ro provider/runtime

### SOW_0051_skillopt_adapter_dataloader_and_config_migration.md

Focus:

- tái tạo adapter boundary theo hướng importable:
  - env adapter
  - dataloader/batch spec
  - eval/train split builders
- thêm config loader/mapping layer để đọc structured config nhưng vẫn phục vụ native Python API
- giữ bridge cho legacy-style config semantics của upstream ở internal compatibility layer, không đẩy người dùng về CLI

Why grouped:

- original SkillOpt gắn chặt engine vào adapter+dataloader+config semantics
- nếu thiếu lớp này thì parity benchmark chỉ là danh nghĩa

### SOW_0052_skillopt_native_python_run_and_eval_surface.md

Focus:

- dựng run/eval orchestration helpers thuần Python trên nền API mới
- đảm bảo train/eval parity được truy cập qua native Python API, không qua CLI
- expose config resolution, registry wiring, và eval-only artifact parity cho code caller sử dụng trực tiếp

Why grouped:

- mục tiêu parity không chỉ là import được class, mà còn là có bề mặt Python đủ hoàn chỉnh để chạy end-to-end
- tách slice này giúp giải bài toán usability mà không kéo framework quay lại CLI-first

### SOW_0053_skillopt_benchmark_pack_text_and_doc_tasks.md

Focus:

- migrate và chuẩn hóa benchmark pack cho các env dạng text/document QA trong reference snapshot:
  - SearchQA
  - DocVQA
  - OfficeQA
- map prompts, rollout/evaluator/dataloader contracts vào engine mới
- thêm smoke/integration coverage cho các benchmark ít phụ thuộc tool runtime hơn

Why grouped:

- đây là benchmark family có giá trị parity cao nhưng blast radius vừa phải
- phù hợp làm wave benchmark đầu tiên sau khi engine/platform layers đã sẵn sàng

Current status:

- completed
- benchmark-native modules da co cho `SearchQA`, `DocVQA`, `OfficeQA`
- native benchmark helpers da auto resolve evaluator cho 3 env nay

### SOW_0054_skillopt_benchmark_pack_interactive_and_tool_tasks.md

Focus:

- migrate benchmark pack còn lại trong reference snapshot:
  - ALFWorld
  - SpreadsheetBench
  - LiveMathematicianBench
- hỗ trợ các runtime/tool-specific needs, trajectory capture, và evaluator contracts phức tạp hơn
- thêm acceptance tests/instructions cho các path có phụ thuộc nặng

Why grouped:

- đây là phần benchmark khó nhất và gần nhất với original behavior complexity
- cần làm sau khi backend, adapter, và artifact layers đã ổn định

Current status:

- in progress
- benchmark-native loader/evaluator/adapter path da co cho `ALFWorld`, `SpreadsheetBench`, `LiveMathematicianBench`
- full upstream runtime parity cho simulator/codegen/react path van la phan con lai

### SOW_0055_skillopt_api_ergonomics_and_parity_docs.md

Focus:

- rà lại experience cuối chương trình ở mức native Python API:
  - output layout
  - run inspection ergonomics
  - compatibility docs
  - parity docs và usage docs cho native Python integration
- chốt docs acceptance cho parity phase

Why grouped:

- original project có thêm vận hành phụ, nhưng ở framework mới phần cần giữ lại là inspectability và docs chứ không phải UI riêng
- slice cuối này gom phần polish và documentation mà không làm nhiễu các SOW core trước đó

Current status:

- completed
- co native inspection helpers cho run artifacts
- co docs usage/parity cho trainer, benchmark-backed runs, va artifact inspection

## Execution Order

1. `SOW_0042`
2. `SOW_0043`
3. `SOW_0044`
4. `SOW_0045`
5. `SOW_0046`
6. `SOW_0047`
7. `SOW_0048`
8. `SOW_0049`
9. `SOW_0050`
10. `SOW_0051`
11. `SOW_0052`
12. `SOW_0053`
13. `SOW_0054`
14. `SOW_0055`

## Program-Level Acceptance

Khi toàn plan hoàn tất:

- repo có module tree `darwinSkill/` importable qua concrete submodules để train/evaluate skill bằng Python API
- có cả facade path và pipeline path
- framework được dùng end-to-end qua native Python API, không cần CLI hay WebUI
- có mockable contracts cho adapter/backend/stage/artifacts
- có ít nhất một demo text-skill path dùng `prompt + expected answer + metric`
- public pipeline API chỉ là linear stages và được test rõ
- trainer path có eval-only persistence rõ ràng
- run state có contract/persistence rõ ràng hơn history tạm
- internal engine tái tạo được các mechanics chính của original SkillOpt:
  - rollout
  - reflect
  - aggregate
  - select
  - update
  - gate
  - slow update
  - meta skill
- framework hỗ trợ dual-role backend execution tương đương optimizer/target split
- adapter/dataloader/config layer đủ để chạy lại benchmark packs trong reference snapshot
- có benchmark migration coverage cho các env trong `references/SkillOpt/skillopt/envs/`
- artifact layout đủ sâu để inspect, compare, và resume runs theo step/epoch
- parity ở đây là functional parity trên snapshot reference, không yêu cầu clone nguyên implementation upstream

## Out-of-Scope For This Plan

- reproduction paper metrics
- migration toàn bộ project trong `~/Projects`
- integration sâu với workflow engines như Temporal
- public graph workflow API cho pipeline
- package bootstrap bằng `__init__.py`
- CLI wrappers cho train/eval
- WebUI hoặc dashboard riêng cho framework mới
- bit-for-bit source parity với upstream
- hỗ trợ những benchmark/env không tồn tại trong snapshot `references/SkillOpt/`

## Risks

- nếu ép chặt vào `sklearn` metaphor thì sẽ làm nghèo hóa multi-stage reflective optimization
- nếu giữ quá gần shape cũ của `SkillOpt` thì framework mới vẫn mang legacy CLI/config mindset vào public surface
- nếu parity bị hiểu thành copy nguyên xi thay vì tái cấu trúc đúng lớp, code sẽ bị lẫn giữa adapter/framework/operator concerns
- nếu migrate benchmark quá sớm trước khi engine/runtime state ổn định, acceptance sẽ rất nhiễu và khó debug
- nếu trì hoãn backend/router quá lâu, reflective engine parity sẽ bị giả lập bằng mocks quá nhiều
- nếu trộn usability với UI surface quá sớm, effort sẽ lệch khỏi engine/platform parity cốt lõi
