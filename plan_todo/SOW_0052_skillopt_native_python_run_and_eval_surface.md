- **Status**: draft
- **Approval**: pending
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
- **Out-of-Scope**:
  - benchmark migration completeness by itself
  - CLI wrappers
  - WebUI
  - command-line flag parity
- **Proposed-By**: Codex GPT-5
- **plan**: `~/Projects/AISkills/plan_todo/skill_framework_distillation_plan.md`
- **Cautions / Risks**:
  - nếu helper layer bị thiết kế như mini-CLI trong Python, API sẽ bị rối
  - cần giữ path này là native Python usability layer, không phải orchestration abstraction dư thừa
