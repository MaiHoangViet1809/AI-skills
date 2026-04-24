# SOW: Telemetry Delegate Smoke Test

- **Task**: Chạy một smoke test end-to-end cho `telemetry-flow` và `sow-delegate-flow` bằng cách delegate một tác vụ Python rất nhỏ cho Claude rồi kiểm tra metrics output thực tế.
- **Location**: `~/Projects/AISkills/plan_todo/finished/SOW_0020_telemetry_delegate_smoke_test.md`, `~/Projects/AISkills/telemetry_smoke_math.py`, và `~/Projects/AISkills/logs_session_ai_agent/`
- **Why**: Cần xác nhận telemetry hook chạy được với một lần delegate thực tế, không chỉ với synthetic log.
- **As-Is Diagram (ASCII)**:
```text
telemetry-flow exists
    |
    v
verified with local parser checks only
```
- **To-Be Diagram (ASCII)**:
```text
approved SOW
    |
    v
telemetry start
    |
    v
delegate small Python task
    |
    v
telemetry finish
    |
    v
inspect real metrics output
```
- **Deliverables**:
  - Một lần chạy delegate thực tế cho task Python nhỏ
  - File Python nhỏ do Claude tạo hoặc sửa
  - Một lần chạy `telemetry-flow` start/finish với output metrics thực
  - Tóm tắt rõ telemetry hoạt động hay fail ở bước nào
- **Done Criteria**:
  - Claude delegate được gọi thực tế hoặc fail với tín hiệu rõ ràng
  - `telemetry-flow finish` trả JSON metrics thực
  - Kết quả được review và commit theo scope của smoke test
- **Out-of-Scope**:
  - Không mở rộng kiến trúc telemetry
  - Không làm report/dashboard
  - Không benchmark nhiều task
- **Proposed-By**: Codex GPT-5
- **plan**: `telemetry delegate smoke test`
- **Cautions / Risks**:
  - Claude CLI có thể rate-limit hoặc lỗi runtime ngoài scope test
  - Codex-side match có thể degraded nếu marker không xuất hiện đúng window
