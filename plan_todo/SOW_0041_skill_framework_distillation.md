- **Status**: draft
- **Approval**: pending
- **Task**: Distill `SkillOpt` thành một framework Python-native cho skill training/evaluation với API object-first kiểu `sklearn` nhưng vẫn hỗ trợ composition/pipeline chaining phù hợp các project nội bộ trong `~/Projects`.
- **Location**: `~/Projects/AISkills/aiskills_common/skill_framework/`, `~/Projects/AISkills/scripts/skill_framework/`, `~/Projects/AISkills/tests/skill_framework/`, `~/Projects/AISkills/pyproject.toml`, `~/Projects/AISkills/references/SkillOpt_intake.md`
- **Why**: `SkillOpt` có loop tối ưu skill hữu ích nhưng public surface hiện tại quá lệ thuộc CLI, flat config dict, và global backend state. Cần một framework Python-native sạch hơn để tái dùng trong các project skill AI nội bộ, đồng thời giữ được 2 phong cách sử dụng quen thuộc: facade đơn giản kiểu `fit/evaluate` và composition chain ops kiểu compiler/executor.
- **As-Is Diagram (ASCII)**:
```text
external script/CLI
        |
        v
  large flat config dict
        |
        v
 train.py / eval_only.py
        |
        v
 global backend state + env registry
        |
        v
 ReflACTTrainer + env-specific adapters

reuse in local projects:
  ad hoc
  copy/paste
  weak API boundary
```
- **To-Be Diagram (ASCII)**:
```text
project code / notebook / service
            |
            v
   SkillTrainer / SkillPipeline facade
      |                 |
      |                 +--> optional chain/step composition
      v
 typed config + explicit dependencies
      |
      v
 trainer core -> optimizer stages -> gate/eval
      |
      +--> adapters (dataset/env/backend/artifacts)

reuse in local projects:
  importable package
  stable fit/evaluate/run interfaces
  testable stage boundaries
```
- **Deliverables**:
  - tạo package framework mới dưới `aiskills_common/skill_framework/`
  - define API facade tối thiểu như `SkillTrainer`, `SkillPipeline`, `RunArtifacts`
  - tách abstraction rõ cho `dataset`, `env adapter`, `backend client`, `optimizer stage`, `gate/evaluator`
  - hỗ trợ ít nhất một execution path kiểu `trainer.fit(...)` và một composition path kiểu pipeline/chain step
  - chuyển baseline concepts từ `SkillOpt` sang typed config/object model thay cho flat dict plumbing
  - có test coverage cho lifecycle chính: build config, run train loop mock, run eval-only mock, artifact persistence
  - bổ sung script/examples tối thiểu để gọi framework mà không cần CLI khổng lồ
- **Done Criteria**:
  - repo có package importable để train/evaluate skill bằng Python API
  - public API không phụ thuộc global mutable backend state
  - một benchmark/adaptor demo có thể chạy qua framework mới với mock hoặc local stub backend
  - code tách rõ framework core khỏi benchmark-specific logic
  - có ít nhất một ví dụ usage giống `sklearn`:
    `trainer = SkillTrainer(...); trainer.fit(train_data); trainer.evaluate(test_data)`
  - có ít nhất một ví dụ usage giống chain ops/composition:
    `pipeline = SkillPipeline([...]); pipeline.run(...)`
  - test tự động bao phủ các contracts chính của framework
- **Out-of-Scope**:
  - chưa cần parity đầy đủ với toàn bộ benchmarks trong upstream `SkillOpt`
  - chưa cần reproduce paper metrics hay benchmark quality của upstream
  - chưa cần web UI/dashboard cho framework mới
  - chưa cần migration tất cả project trong `~/Projects` sang framework mới
  - chưa cần tích hợp sâu với external workflow engines như Temporal
- **Proposed-By**: Codex GPT-5
- **plan**: `skill framework distillation`
- **Cautions / Risks**:
  - nếu khóa cứng vào `sklearn` metaphor thì sẽ thiếu chỗ cho multi-stage reflective optimization; cần giữ layer composition đủ linh hoạt
  - nếu giữ quá nhiều shape của `SkillOpt` thì framework mới sẽ vẫn nặng CLI/config legacy
  - cần tránh over-generalize quá sớm; nên bắt đầu từ 1 adapter demo và 1 backend stub
  - framework này nên tham chiếu các pattern nội bộ đã có:
    - facade object API từ `~/Projects/nanobot/nanobot/nanobot.py`
    - compiler/executor separation từ `~/Projects/libraries/cores/workflows/common/compiler.py`
    - backend interface/registry từ `~/Projects/hybrid_brain/core/trainers/framework/backend_base.py`
