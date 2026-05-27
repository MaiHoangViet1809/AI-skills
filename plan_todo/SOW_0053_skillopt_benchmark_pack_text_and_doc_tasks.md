- **Status**: in_progress
- **Approval**: approved
- **Task**: Migrate benchmark pack đầu tiên của reference SkillOpt gồm `SearchQA`, `DocVQA`, và `OfficeQA` vào `darwinSkill` trên nền engine/adapters/backend mới.
- **Location**: `~/Projects/AISkills/darwinSkill/`, `~/Projects/AISkills/tests/darwinSkill/`, `~/Projects/AISkills/references/SkillOpt/skillopt/envs/searchqa/`, `~/Projects/AISkills/references/SkillOpt/skillopt/envs/docvqa/`, `~/Projects/AISkills/references/SkillOpt/skillopt/envs/officeqa/`
- **Why**: Sau khi engine/platform layers ổn định, cần benchmark packs thật để chứng minh parity là functional chứ không chỉ architectural. Nhóm text/document tasks là wave phù hợp đầu tiên vì ít phụ thuộc runtime tool phức tạp hơn.
- **As-Is Diagram (ASCII)**:
```text
darwinSkill
  -> demo text backend only
  -> no migrated benchmark envs
```
- **To-Be Diagram (ASCII)**:
```text
darwinSkill benchmark pack A
  -> SearchQA adapter + dataloader + rollout/eval
  -> DocVQA adapter + dataloader + rollout/eval
  -> OfficeQA adapter + dataloader + rollout/eval
  -> smoke acceptance on migrated tasks
```
- **Deliverables**:
  - migrate benchmark-specific adapters, dataloaders, rollout/evaluator contracts for the three envs
  - port or rewrite benchmark prompt/skill assets as needed into the new layout
  - add benchmark-scoped smoke tests or replayable fixture tests
  - document any intentional deltas where the new framework keeps behavior equivalent but API/layout differs
- **Done Criteria**:
  - the three benchmark families can run through `darwinSkill` with the new engine/native Python surface
  - tests or controlled smokes prove end-to-end wiring
  - benchmark logic lives behind adapters, not in trainer core
- **Out-of-Scope**:
  - ALFWorld
  - SpreadsheetBench
  - LiveMathematicianBench
  - UI parity
- **Proposed-By**: Codex GPT-5
- **plan**: `~/Projects/AISkills/plan_todo/skill_framework_distillation_plan.md`
- **Cautions / Risks**:
  - asset/prompt migration có thể kéo theo path/layout decisions cần nhất quán với later benchmark packs
  - fixture strategy cần tránh phụ thuộc external services trong test mặc định
