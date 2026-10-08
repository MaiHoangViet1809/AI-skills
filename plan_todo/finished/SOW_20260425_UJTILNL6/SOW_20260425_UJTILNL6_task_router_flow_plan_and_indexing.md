# SOW_20260425_UJTILNL6 - Task Router Flow Plan And Indexing

- Status: UNKNOWN
- Approval: UNKNOWN
- create_dttm: 2026-04-25T00:36:55+07:00
- create_date: 2026-04-25
- create_dttm_source: filesystem_birthtime
- create_dttm_confidence: filesystem_proxy
- create_dttm_evidence: `plan_todo/finished/SOW_20261008_VO3LKN0L/creation-date-evidence.json` (record: SOW_20260425_UJTILNL6)
- approve_dttm: unknown
- finish_dttm: unknown
- legacy_id: SOW_0011
- legacy_path: plan_todo/finished/SOW_0011_task_router_flow_plan_and_indexing.md
- migrated_dttm: 2026-10-08T12:48:51+07:00
- legacy_title: SOW: Task Router Flow Plan And Indexing

## Preserved Contract And Historical Evidence

- **Task**: Cập nhật `task-router-flow` và `references/scope-of-work.md` để ưu tiên extend plan thay vì extend SOW khi work thuộc một plan, đồng thời bắt buộc mọi SOW dùng index 4 chữ số từ `0001` đến `9999`.
- **Location**: `plan_todo/SOW_task_router_flow_plan_and_indexing.md`, `~/.codex/skills/task-router-flow/SKILL.md`, `~/.codex/skills/task-router-flow/references/scope-of-work.md`, và reference notes nếu cần.
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
