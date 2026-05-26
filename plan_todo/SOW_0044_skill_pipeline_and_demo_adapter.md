- **Status**: draft
- **Approval**: pending
- **Task**: Implement runtime cho `SkillPipeline.run(...)` theo linear-stage public contract đã khóa ở `0042` và thêm một demo text-skill path dùng `prompt + expected answer + metric`.
- **Location**: `~/Projects/AISkills/darwinSkill/`, `~/Projects/AISkills/tests/darwinSkill/`, `~/Projects/AISkills/references/SkillOpt_intake.md`
- **Why**: Mục tiêu của framework không chỉ là bắt chước `sklearn`, mà còn phải phù hợp các project nội bộ dùng composition/chaining. Phase này implement composition path công khai nhưng giữ semantics hẹp ở linear stages để tránh khóa nhầm graph API.
- **As-Is Diagram (ASCII)**:
```text
SkillTrainer facade
    |
    v
 core lifecycle works

SkillPipeline path
    |
    v
 missing
```
- **To-Be Diagram (ASCII)**:
```text
 facade path              pipeline path
 SkillTrainer             SkillPipeline
     |                        |
     +-----------+------------+
                 |
                 v
          shared framework core
                 |
                 v
       demo text-skill stage path
```
- **Deliverables**:
  - implement `SkillPipeline.run(...)` đúng public contract đã khóa ở `0042`
  - implement linear `SkillStage` runtime cho pipeline path
  - map trainer-core stages thành execution units tái dùng được trong pipeline path
  - thêm demo text-skill path dựa trên `SkillSample(prompt, expected_answer, metadata)` và evaluator metric contract
  - thêm tests chứng minh facade path và pipeline path cùng dùng được core chung
  - cập nhật intake/reference note để phản ánh mapping thiết kế từ SkillOpt sang framework mới
- **Done Criteria**:
  - có thể chạy một demo flow bằng `from darwinSkill.pipeline import SkillPipeline` rồi `SkillPipeline.run(...)` và nhận `RunArtifacts`
  - pipeline path chỉ hỗ trợ linear stages và điều này được test rõ
  - facade path và pipeline path không diverge về sample/evaluator/artifact contract cốt lõi
  - demo text-skill path chạy được với metric evaluator
  - tests xác nhận composition path pass
- **Out-of-Scope**:
  - chưa hỗ trợ graph pipeline, branch pipeline, hay merge pipeline ở public API
  - chưa cần nhiều benchmark adapters
  - chưa cần docs/examples polish cuối
  - chưa cần smoke integration toàn repo
- **Proposed-By**: Codex GPT-5
- **plan**: `~/Projects/AISkills/plan_todo/skill_framework_distillation_plan.md`
- **Cautions / Risks**:
  - composition layer rất dễ over-engineer
  - cần tránh tạo 2 runtime khác nhau cho facade và pipeline
  - cần giữ branching/merge hoàn toàn ngoài public pipeline API v1
