- **Status**: done
- **Approval**: approved
- **Task**: Implement trainer core tối thiểu cho framework mới, gồm `fit()` / `evaluate()`, run state, và artifact persistence cho anchor text-skill contract đã khóa ở `0042`.
- **Location**: `~/Projects/AISkills/darwinSkill/`, `~/Projects/AISkills/tests/darwinSkill/`, `~/Projects/AISkills/scripts/darwinSkill/`
- **Why**: Sau khi contracts đã chốt, cần một lõi thực thi thật để chứng minh framework không chỉ là type shell. Phase này tập trung vào control flow và persistence của trainer path trước khi thêm pipeline runtime.
- **As-Is Diagram (ASCII)**:
```text
contracts only
    |
    v
 no executable training lifecycle
```
- **To-Be Diagram (ASCII)**:
```text
SkillTrainer.fit/evaluate
          |
          v
    trainer core
      |      |
      |      +--> artifacts / run state
      v
 mock text backend + mock evaluator
```
- **Deliverables**:
  - implement trainer core tối thiểu cho `fit(...)` / `evaluate(...)` lifecycle đúng contract đã khóa ở `0042`
  - implement artifact model và persistence cơ bản theo `RunArtifacts` contract đã khóa ở `0042`
  - implement run state structure cho trainer path
  - implement mock text backend, mock evaluator, và mock text sample dataset để test control flow
  - thêm tests cho train loop, eval-only flow, artifact writes
- **Done Criteria**:
  - có thể chạy một mocked text-skill training run end-to-end qua `from darwinSkill.trainer import SkillTrainer`
  - có thể chạy một mocked evaluation run qua `SkillTrainer.evaluate(...)` và nhận `EvaluationReport`
  - artifacts được ghi và đọc lại theo contract
  - tests xác nhận lifecycle chính pass mà không cần benchmark thật
- **Out-of-Scope**:
  - chưa implement `SkillPipeline.run(...)`
  - chưa có demo text-skill path ở pipeline runtime
  - chưa có usage docs hoàn chỉnh
- **Proposed-By**: Codex GPT-5
- **plan**: `~/Projects/AISkills/plan_todo/skill_framework_distillation_plan.md`
- **Cautions / Risks**:
  - phase này dễ kéo theo benchmark-specific assumptions; cần giữ mock text-skill contract đúng mức tối thiểu
  - artifact shape phải đủ ổn định để phase sau chỉ tái dùng, không đổi contract
