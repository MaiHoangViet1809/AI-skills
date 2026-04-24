- **Task**: Cập nhật dashboard backend để luôn thấy telemetry mới bằng cách reload dữ liệu mỗi request và thêm API refresh cache thủ công.
- **Location**: `~/Projects/AISkills/plan_todo/SOW_0034_dashboard_reload_and_refresh_api.md`, `~/Projects/AISkills/dashboard/backend/app.py`, và nếu cần docs ở `~/Projects/AISkills/dashboard/README.md`
- **Why**: Dashboard đang giữ snapshot `_df` từ lúc boot nên telemetry mới đã ghi vào global ledger nhưng UI không thấy ngay.
- **As-Is Diagram (ASCII)**:
```text
global ledger updates
      |
      v
backend startup cache (_df)
      |
      v
dashboard stale until restart
```
- **To-Be Diagram (ASCII)**:
```text
global ledger updates
      |
      +--> each request reloads latest runs
      |
      +--> manual refresh API also available
      |
      v
dashboard sees new telemetry without restart
```
- **Deliverables**:
  - bỏ cache cứng `_df` ở startup
  - reload dữ liệu mới ở các API đọc
  - thêm API refresh cache/manual refresh endpoint
  - cập nhật docs ngắn nếu cần
- **Done Criteria**:
  - run mới trong `~/.logs/codex/telemetry/runs/` hiện lên mà không cần restart server
  - có endpoint refresh riêng để force reload
  - dashboard APIs vẫn hoạt động bình thường
- **Out-of-Scope**:
  - không redesign frontend
  - không đổi schema telemetry
- **Proposed-By**: Codex GPT-5
- **plan**: `dashboard telemetry freshness`
- **Cautions / Risks**:
  - reload mỗi request có thể tốn hơn nếu ledger lớn
  - cần tránh duplicate logic giữa auto-reload và manual refresh
