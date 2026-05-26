- **Status**: draft
- **Approval**: pending
- **Task**: Bổ sung execution path kiểu pipeline/chain cho framework mới và thêm một demo adapter để chứng minh coexistence giữa facade API và composition API.
- **Location**: `~/Projects/AISkills/aiskills_common/skill_framework/`, `~/Projects/AISkills/tests/skill_framework/`, `~/Projects/AISkills/references/SkillOpt_intake.md`
- **Why**: Mục tiêu của framework không chỉ là bắt chước `sklearn`, mà còn phải phù hợp các project nội bộ dùng composition/chaining. Phase này reconcile hai phong cách API bằng một demo path cụ thể.
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
         demo adapter / stub backend
```
- **Deliverables**:
  - implement `SkillPipeline` hoặc equivalent composition path
  - map stages thành chainable/composable execution units
  - thêm một demo adapter hoặc stub benchmark path
  - thêm tests chứng minh facade path và pipeline path cùng dùng được core chung
  - cập nhật intake/reference note nếu cần để phản ánh mapping thiết kế
- **Done Criteria**:
  - có thể chạy một demo flow bằng `SkillPipeline.run(...)`
  - facade path và pipeline path không diverge về contract cốt lõi
  - demo adapter đủ để chứng minh embedding vào project khác
  - tests xác nhận composition path pass
- **Out-of-Scope**:
  - chưa cần nhiều benchmark adapters
  - chưa cần docs/examples polish cuối
  - chưa cần smoke integration toàn repo
- **Proposed-By**: Codex GPT-5
- **plan**: `~/Projects/AISkills/plan_todo/skill_framework_distillation_plan.md`
- **Cautions / Risks**:
  - composition layer rất dễ over-engineer
  - cần tránh tạo 2 runtime khác nhau cho facade và pipeline
