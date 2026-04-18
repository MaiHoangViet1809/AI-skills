- **Task**: Chuyển toàn bộ telemetry writes từ `logs_session_ai_agent` trong từng project sang global telemetry paths dưới `~/.logs/codex/telemetry/`.
- **Location**: `/Users/maihoangviet/Projects/AISkills/plan_todo/SOW_0038_move_all_telemetry_logs_global.md`, `/Users/maihoangviet/Projects/AISkills/aiskills_common/telemetry/**`, `/Users/maihoangviet/Projects/AISkills/skills/telemetry-flow/scripts/**`, `/Users/maihoangviet/Projects/AISkills/skills/sow-delegate-flow/scripts/**`, `/Users/maihoangviet/Projects/AISkills/scripts/telemetry/**`, và docs/reference telemetry liên quan
- **Why**: Dashboard đã đọc global ledger, nhưng raw/staging telemetry vẫn còn write local theo từng repo; điều này đi ngược mục tiêu centralized telemetry.
- **As-Is Diagram (ASCII)**:
```text
repo/logs_session_ai_agent/
  -> telemetry-run-*.json
  -> claude-*.log

~/.logs/codex/telemetry/runs/
  -> normalized run summaries
```
- **To-Be Diagram (ASCII)**:
```text
~/.logs/codex/telemetry/
  -> runs/
  -> staging/
  -> claude/
  -> hook-debug/
  -> hook-state/

no telemetry writes into repo-local logs_session_ai_agent/
```
- **Deliverables**:
  - shared global path helpers cho `runs`, `staging`, `claude`
  - update telemetry hook / delegate parser / related scripts sang global paths
  - update docs/contracts đang còn nói `logs_session_ai_agent`
  - verify dashboard + telemetry flow vẫn hoạt động
- **Done Criteria**:
  - run staging không còn write vào project-local `logs_session_ai_agent`
  - Claude raw logs không còn write vào project-local `logs_session_ai_agent`
  - global ledger và parser paths vẫn chạy đúng
  - docs khớp với global-only telemetry storage
- **Out-of-Scope**:
  - dashboard redesign
  - thay đổi metric schema
- **Proposed-By**: Codex GPT-5
- **plan**: `global telemetry storage`
- **Cautions / Risks**:
  - cần naming/path đủ ổn để tránh collision cross-project
  - parser và backfill cũ phải chịu được dữ liệu lịch sử
  - không được làm vỡ hook/runtime sync sang `~/.codex`
