# SOW_20260425_NOOXZ8GY - playwright skill cleanup lifecycle

- Status: UNKNOWN
- Approval: UNKNOWN
- create_dttm: 2026-04-25T00:36:55+07:00
- create_date: 2026-04-25
- create_dttm_source: filesystem_birthtime
- create_dttm_confidence: filesystem_proxy
- create_dttm_evidence: `plan_todo/finished/SOW_20261008_VO3LKN0L/creation-date-evidence.json` (record: SOW_20260425_NOOXZ8GY)
- approve_dttm: unknown
- finish_dttm: unknown
- legacy_id: SOW_0039
- legacy_path: plan_todo/finished/SOW_0039_playwright_skill_cleanup_lifecycle.md
- migrated_dttm: 2026-10-08T12:48:51+07:00

## Preserved Contract And Historical Evidence

- **Task**: Import skill Playwright vào repo dưới tên `playwright-flow` và bổ sung session lifecycle/cleanup guardrails để tránh để lại browser sessions sống dai.
- **Location**: `~/Projects/AISkills/skills/playwright-flow/`, `~/Projects/AISkills/scripts/skills/sync_environment.py`
- **Why**: Skill Playwright hiện tại dạy cách mở và dùng browser, nhưng chưa nhấn mạnh cleanup lifecycle như `list`, `close`, `close-all`, `kill-all`, nên dễ để lại session stale sau khi debug UI.
- **As-Is Diagram (ASCII)**:
```text
open -> snapshot -> click -> screenshot
         |
         v
      cleanup not explicit
```
- **To-Be Diagram (ASCII)**:
```text
open -> snapshot -> interact -> capture
                           |
                           v
                 list/close/close-all/kill-all
```
- **Deliverables**:
  - import skill vào repo dưới tên `playwright-flow`
  - thêm section `Session Lifecycle`
  - thêm section `Session Cleanup`
  - cập nhật references với cleanup commands
  - sync skill mới sang `~/.codex`
- **Done Criteria**:
  - repo có skill `playwright-flow`
  - skill nêu rõ `open` tạo session sống qua nhiều lệnh
  - mặc định close session sau khi xong
  - `kill-all` được nhắc cho session stale/headed bị treo
  - sync sang Codex env thành công
- **Out-of-Scope**:
  - không sửa upstream skill gốc
  - không đổi wrapper script logic nếu chưa cần
- **Proposed-By**: Codex GPT-5
- **plan**: `playwright skill cleanup lifecycle`
- **Cautions / Risks**:
  - cần giữ skill ngắn gọn, không biến thành full CLI manual
