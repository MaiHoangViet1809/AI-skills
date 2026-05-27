- **Status**: draft
- **Approval**: pending
- **Task**: Dựng thin CLI/operator surfaces cho `darwinSkill` để cung cấp train/eval entrypoints tương đương original SkillOpt mà không kéo framework quay lại CLI-first.
- **Location**: `~/Projects/AISkills/scripts/`, `~/Projects/AISkills/darwinSkill/`, `~/Projects/AISkills/tests/darwinSkill/`, `~/Projects/AISkills/references/SkillOpt/scripts/`
- **Why**: Functional parity không dừng ở import API. Original project có `train.py` và `eval_only.py` để operator chạy thực tế. Bản refactor cần có surface tương đương, nhưng chỉ là wrapper mỏng trên engine và config/adapters mới.
- **As-Is Diagram (ASCII)**:
```text
scripts/darwinSkill/*.py
  -> demo only
  -> sys.path bootstrapping
  -> not operator-grade
```
- **To-Be Diagram (ASCII)**:
```text
thin train CLI
thin eval-only CLI
  -> config resolution
  -> adapter/backend wiring
  -> SkillTrainer / engine
  -> rich artifact outputs
```
- **Deliverables**:
  - implement train and eval-only operator scripts on top of the new API/config layer
  - support practical override flow and resolved-run output paths
  - persist eval-only artifacts with parity-minded layout
  - upgrade examples/docs from demo-only scripts to operator-aware usage
  - add smoke tests for CLI entrypoints and eval-only flow
- **Done Criteria**:
  - users can launch training and eval-only runs without writing custom Python bootstrap
  - CLI wrappers are measurably thinner than original `scripts/train.py`
  - eval-only path produces inspectable artifacts rather than just in-memory reports
- **Out-of-Scope**:
  - benchmark migration completeness by itself
  - WebUI
  - full command-line flag parity for every legacy flag in one shot unless needed for the migrated benchmarks
- **Proposed-By**: Codex GPT-5
- **plan**: `~/Projects/AISkills/plan_todo/skill_framework_distillation_plan.md`
- **Cautions / Risks**:
  - CLI wrapper dễ phình lại thành orchestration layer nếu config/adapters chưa chốt
  - cần giữ path này là operator surface, không phải public API trung tâm

