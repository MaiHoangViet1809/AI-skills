# SOW: Task Router Flow Skill

- **Task**: Tạo skill mới `task-router-flow` để làm front-door workflow cho request mới: phân nhánh request theo loại công việc, draft hoặc extend SOW khi cần, xử lý nhánh debug/docs đúng quy ước hiện tại, tách định nghĩa SOW ra reference file riêng, rồi hand off sang bước thực thi tiếp theo.
- **Location**: `plan_todo/skills_sow/SOW_task_router_flow_skill.md`, thư mục skill global mới dưới Codex skills home, các file skill liên quan gồm `SKILL.md` và `references/scope-of-work.md`, và cập nhật tối thiểu vào `AGENTS.md` nếu cần để chuyển hướng sang skill.
- **Why**: Workflow thực tế hiện tại không chỉ là “viết SOW”, mà là quyết định nhánh xử lý đầu vào của request. Tách workflow này ra thành skill sẽ gọn hơn trong `AGENTS.md` và tái sử dụng được.
- **As-Is Diagram (ASCII)**:
```text
User request
   |
   v
Agent reads AGENTS.md and decides ad hoc:
  - new SOW
  - extend old SOW
  - debug flow
  - docs/plan flow
```
- **To-Be Diagram (ASCII)**:
```text
User request
   |
   v
Use task-router-flow
   |
   +--> new code change
   |      draft SOW -> revise -> wait approve -> hand off
   |
   +--> existing SOW change
   |      extend SOW -> wait approve -> hand off
   |
   +--> debug request
   |      find root cause -> confirm intent if needed ->
   |      extend SOW if big -> continue -> note fix_bug.md
   |
   +--> docs / SOW / plan only
   |      no new SOW -> show plan -> wait approve -> edit
   |
   v
Final check -> summary -> commit -> user summary
```
- **Deliverables**: Skill global `task-router-flow`; `SKILL.md` mô tả trigger `Use this skill when the user makes a work request that may require creating a new SOW, extending an existing SOW, debugging toward a fix, or editing docs/plan files, and the correct workflow branch has not yet been chosen.`; 4 workflow branches; reference files cho decision table và định nghĩa SOW; cập nhật nhẹ `AGENTS.md` nếu cần để giảm phần inline và chuyển hướng sang skill.
- **Done Criteria**: Skill chọn đúng một trong bốn nhánh chính; draft/extend SOW theo template hiện có khi cần; định nghĩa SOW nằm trong reference file riêng thay vì nhét vào `SKILL.md`; biết khi nào không tạo SOW mới; biết ghi vào `plan_todo/fix_bug.md` cho nhánh debug; biết closeout bằng final check + summary + commit; validator vẫn pass.
- **Out-of-Scope**: Không refactor hết mọi repo rule khác trong `AGENTS.md`; không thay đổi `sow-delegate-flow`; không tự động migrate toàn bộ tài liệu cũ.
- **Proposed-By**: Codex GPT-5
- **plan**: `plan_todo/skills_sow/SOW_task_router_flow_skill.md`
- **Cautions / Risks**:
  - Nếu branch rules không đủ rõ, skill sẽ chồng lấn với `sow-delegate-flow`.
  - Nếu mô tả quá chi tiết, skill sẽ thành ceremonial và tốn context.
  - Nhánh debug cần giữ quyền hỏi lại user khi root cause cho thấy ambiguity thật sự, không phải hỏi theo quán tính.
