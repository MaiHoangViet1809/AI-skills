# SOW_20260425_HP5K09Z0 - dashboard reload and refresh api

- Status: UNKNOWN
- Approval: UNKNOWN
- create_dttm: 2026-04-25T00:36:55+07:00
- create_date: 2026-04-25
- create_dttm_source: filesystem_birthtime
- create_dttm_confidence: filesystem_proxy
- create_dttm_evidence: `plan_todo/finished/SOW_20261008_VO3LKN0L/creation-date-evidence.json` (record: SOW_20260425_HP5K09Z0)
- approve_dttm: unknown
- finish_dttm: unknown
- legacy_id: SOW_0034
- legacy_path: plan_todo/finished/SOW_0034_dashboard_reload_and_refresh_api.md
- migrated_dttm: 2026-10-08T12:48:51+07:00

## Preserved Contract And Historical Evidence

- **Task**: Cập nhật dashboard backend để luôn thấy telemetry mới bằng cách reload dữ liệu mỗi request và thêm API refresh cache thủ công.
- **Location**: `plan_todo/SOW_0034_dashboard_reload_and_refresh_api.md`, `~/Projects/AISkills/dashboard/backend/app.py`, và nếu cần docs ở `~/Projects/AISkills/dashboard/README.md`
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
