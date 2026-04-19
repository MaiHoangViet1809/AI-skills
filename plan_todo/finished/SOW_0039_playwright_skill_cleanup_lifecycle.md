- **Task**: Import skill Playwright vào repo dưới tên `playwright-flow` và bổ sung session lifecycle/cleanup guardrails để tránh để lại browser sessions sống dai.
- **Location**: `/Users/maihoangviet/Projects/AISkills/skills/playwright-flow/`, `/Users/maihoangviet/Projects/AISkills/scripts/skills/sync_environment.py`
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
