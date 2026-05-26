- **Status**: done
- **Approval**: approved
- **Task**: Clone `microsoft/SkillOpt` vào repo như một subfolder reference, đọc codebase và lập thống kê dòng code để chuẩn bị cho phase distill framework.
- **Location**: `~/Projects/AISkills/references/SkillOpt/`, `~/Projects/AISkills/plan_todo/SOW_0040_skillopt_reference_intake.md`
- **Why**: Cần một bản local reference của upstream để đánh giá kiến trúc, pipeline training skill, paper liên quan, và xác định phạm vi rút gọn thành API/pipeline kiểu `sklearn` cho các project skill AI nội bộ.
- **As-Is Diagram (ASCII)**:
```text
AISkills repo
|
+-- local skills / plans
|
+-- no SkillOpt source reference
|
+-- no baseline LOC / structure inventory
```
- **To-Be Diagram (ASCII)**:
```text
AISkills repo
|
+-- references/SkillOpt/      <- cloned upstream reference
|
+-- intake notes from code/paper
|
+-- baseline LOC + structure inventory
|
+-- input for future sklearn-like distillation SOW
```
- **Deliverables**:
  - clone upstream `microsoft/SkillOpt` vào `references/SkillOpt/`
  - xác nhận paper/tài liệu liên quan hiện có trong repo upstream
  - tóm tắt cấu trúc code chính và pipeline hiện tại
  - thống kê số dòng code theo tổng thể và theo nhóm file chính
- **Done Criteria**:
  - subfolder reference tồn tại và đọc được trong workspace
  - có thống kê LOC rõ ràng, nêu cách đếm
  - có tóm tắt ngắn về module/pipeline chính của SkillOpt
  - nêu rõ phần nào là đầu vào cho phase distill tiếp theo
- **Out-of-Scope**:
  - chưa refactor hay viết lại framework theo API kiểu `sklearn`
  - chưa nhúng SkillOpt vào code production của repo này
  - chưa benchmark, train, hoặc reproduce kết quả paper
- **Proposed-By**: Codex GPT-5
- **plan**: `skillopt intake and distillation prep`
- **Cautions / Risks**:
  - upstream có thể khá rộng, cần tách rõ code lõi với notebooks/assets để thống kê hữu ích
  - paper có thể nằm ngoài repo hoặc link ra external source, cần ghi rõ nếu chỉ xác nhận qua metadata
