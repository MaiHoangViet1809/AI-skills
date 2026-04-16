- **Task**: Pilot hook-based telemetry cho `task-router-flow` bằng Codex hooks để một skill-run/session tự start/finish telemetry và trả summary ngắn về main session, không làm vỡ flow telemetry hiện tại của `sow-delegate-flow`.
- **Location**: `/Users/maihoangviet/Projects/AISkills/plan_todo/SOW_0033_task_router_hooked_subagent_telemetry_pilot.md`, `/Users/maihoangviet/Projects/AISkills/skills/task-router-flow/**`, `/Users/maihoangviet/Projects/AISkills/skills/telemetry-flow/**`, `/Users/maihoangviet/Projects/AISkills/scripts/telemetry/**`, `/Users/maihoangviet/Projects/AISkills/.codex/**`, `/Users/maihoangviet/Projects/AISkills/scripts/skills/sync_environment.py`
- **Why**: Cần kiểm chứng kiến trúc skill/session riêng cho `task-router-flow` có thể tự emit telemetry qua Codex hooks, giữ main session sạch hơn, trong khi không đụng path cũ của `sow-delegate-flow`.
- **As-Is Diagram (ASCII)**:
```text
main session
   |
   +--> task-router-flow inline
   +--> telemetry-flow gọi theo process thường
   |
   +--> sow-delegate-flow vẫn dùng start/finish cũ
```
- **To-Be Diagram (ASCII)**:
```text
main session
   |
   +--> task-router-flow session/subagent
           |
           +--> Codex SessionStart anchors telemetry time
           +--> task-router work
           +--> Codex Stop resolves prompt marker and finishes telemetry
           +--> return brief summary to main session
   |
   +--> sow-delegate-flow path cũ giữ nguyên
```
- **Deliverables**:
  - file `SOW_0033`
  - hook bridge script cho Codex events
  - repo-owned hook config template + sync sang `~/.codex`
  - docs/pilot instructions cho `task-router-flow` và `telemetry-flow`
  - smoke test chứng minh hook pipeline tự ghi telemetry run
- **Done Criteria**:
  - bật được `codex_hooks` qua sync/config
  - hook pipeline tự tạo telemetry run cho pilot `task-router-flow`
  - global ledger có run mới từ pilot
  - `sow-delegate-flow` vẫn dùng path cũ, không regression
- **Out-of-Scope**:
  - migrate all skills sang hook path
  - bỏ flow telemetry hiện tại
  - hook telemetry cho Claude
- **Proposed-By**: Codex GPT-5
- **plan**: `subagent telemetry pilot`
- **Cautions / Risks**:
- hooks còn experimental
- `Stop` không support matcher, script phải tự filter
- skill metadata phải được hydrate lại từ transcript tại `Stop`
- cần tránh double-count nếu sau này parent cũng emit telemetry
