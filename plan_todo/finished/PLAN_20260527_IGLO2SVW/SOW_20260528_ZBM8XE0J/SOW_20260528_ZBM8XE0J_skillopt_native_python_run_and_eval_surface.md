# SOW_20260528_ZBM8XE0J - skillopt native python run and eval surface

- Status: completed
- Approval: approved
- create_dttm: 2026-05-28T02:21:49+07:00
- create_date: 2026-05-28
- create_dttm_source: filesystem_birthtime
- create_dttm_confidence: filesystem_proxy
- create_dttm_evidence: `plan_todo/finished/SOW_20261008_VO3LKN0L/creation-date-evidence.json` (record: SOW_20260528_ZBM8XE0J)
- approve_dttm: unknown
- finish_dttm: unknown
- legacy_id: SOW_0052
- legacy_path: plan_todo/SOW_0052_skillopt_native_python_run_and_eval_surface.md
- migrated_dttm: 2026-10-08T12:48:51+07:00

## Preserved Contract And Historical Evidence

- **Status**: completed
- **Approval**: approved
- **Task**: Dựng native Python run/eval surface cho `darwinSkill` để cung cấp train/eval orchestration tương đương original SkillOpt mà không kéo framework quay lại CLI-first.
- **Location**: `~/Projects/AISkills/darwinSkill/`, `~/Projects/AISkills/tests/darwinSkill/`, `~/Projects/AISkills/references/SkillOpt/scripts/`
- **Why**: Functional parity không dừng ở import được vài class. Original project có `train.py` và `eval_only.py` để chạy end-to-end; ở framework mới, phần tương đương cần được hấp thụ vào bề mặt native Python API thay vì giữ lại CLI wrapper.
- **As-Is Diagram (ASCII)**:
```text
Python API usage
  -> low-level trainer/pipeline objects
  -> demo-only helpers
  -> chưa có run/eval helper đầy đủ cho parity
```
- **To-Be Diagram (ASCII)**:
```text
native Python run helper
native Python eval helper
  -> config resolution
  -> adapter/backend wiring
  -> SkillTrainer / engine
  -> rich artifact outputs
```
- **Deliverables**:
  - implement train and eval-only orchestration helpers on top of the new API/config layer
  - support practical Python-side override flow and resolved-run output paths
  - persist eval-only artifacts with parity-minded layout
  - upgrade examples/docs from demo-only usage to parity-minded native Python usage
  - add smoke tests for native Python train/eval helper flows
- **Done Criteria**:
  - users can launch training and eval-only runs from native Python without hand-wiring low-level internals
  - parity run/eval flows are reachable without introducing CLI wrappers
  - eval-only path produces inspectable artifacts rather than just in-memory reports
- **Progress Notes**:
  - da co `run_training(...)`, `run_evaluation(...)`, `run_with_adapter(...)`, `run_reference_benchmark(...)`, `run_reference_benchmark_from_path(...)`, va `run_reference_adapter(...)`
  - config resolution, adapter/backend wiring, va benchmark-aware evaluator resolution da di qua native Python helpers
  - eval/train flows da persist artifact layout inspectable thay vi chi tra in-memory report
  - README/USAGE/PARITY va smoke tests da cover native Python train/eval helper surfaces
- **Out-of-Scope**:
  - benchmark migration completeness by itself
  - CLI wrappers
  - WebUI
  - command-line flag parity
- **Proposed-By**: Codex GPT-5
- **plan**: `plan_todo/finished/PLAN_20260527_IGLO2SVW/PLAN_20260527_IGLO2SVW_skill_framework_distillation_plan.md`
- **Cautions / Risks**:
  - nếu helper layer bị thiết kế như mini-CLI trong Python, API sẽ bị rối
  - cần giữ path này là native Python usability layer, không phải orchestration abstraction dư thừa
