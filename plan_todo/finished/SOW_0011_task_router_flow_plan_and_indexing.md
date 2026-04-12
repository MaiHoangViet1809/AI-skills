# SOW: Task Router Flow Plan And Indexing

- **Task**: Cập nhật `task-router-flow` và `references/scope-of-work.md` để ưu tiên extend plan thay vì extend SOW khi work thuộc một plan, đồng thời bắt buộc mọi SOW dùng index 4 chữ số từ `0001` đến `9999`.
- **Location**: `plan_todo/SOW_task_router_flow_plan_and_indexing.md`, `/Users/maihoangviet/.codex/skills/task-router-flow/SKILL.md`, `/Users/maihoangviet/.codex/skills/task-router-flow/references/scope-of-work.md`, và reference notes nếu cần.
- **Why**: Tránh lệch giữa plan và SOW con, đồng thời chuẩn hóa danh tính của SOW trong project bằng một index ổn định và dễ tra cứu.
- **As-Is Diagram (ASCII)**:
```text
Change touches work under a plan
   |
   v
Skill may extend the SOW directly
   |
   v
Plan and SOW can drift apart
```
- **To-Be Diagram (ASCII)**:
```text
Change touches work under a plan
   |
   v
Extend the plan first
   |
   v
Update aligned SOW under that plan

Every SOW:
  SOW_0001_...
  SOW_0002_...
  ...
```
- **Deliverables**: Skill and SOW reference updated with plan-before-SOW rule; indexed SOW naming and numbering rule documented.
- **Done Criteria**: `task-router-flow` routes scope changes under plans to plan extension first; `scope-of-work.md` states that SOWs must use 4-digit indexes and unique filenames; validator still passes.
- **Out-of-Scope**: Không tự động rename toàn bộ SOW cũ; không backfill index cho legacy files trong repo.
- **Proposed-By**: Codex GPT-5
- **plan**: `plan_todo/SOW_task_router_flow_plan_and_indexing.md`
- **Cautions / Risks**:
  - Legacy SOW files hiện tại chưa theo index mới nên cần xem rule này là forward-looking nếu chưa migrate.
  - Nếu không nói rõ cách lấy next index, người vận hành vẫn có thể tạo lệch chuẩn.
