- **Task**: Chuẩn hóa telemetry hook architecture thành global cross-project flow, cập nhật skill specs để mọi project gọi skill đều ghi telemetry đúng theo project/session hiện tại, rồi sync toàn bộ spec vào Codex environment.
- **Location**: `~/Projects/AISkills/plan_todo/SOW_0035_global_cross_project_skill_telemetry.md`, `~/Projects/AISkills/skills/telemetry-flow/**`, `~/Projects/AISkills/skills/task-router-flow/**`, `~/Projects/AISkills/skills/sow-delegate-flow/**`, `~/Projects/AISkills/scripts/telemetry/**`, `~/Projects/AISkills/scripts/skills/**`, `~/Projects/AISkills/.codex/**`, và target sync files trong `~/.codex/**`
- **Why**: Telemetry hiện mới là pilot gắn với `AISkills`; cần biến thành kiến trúc global thật để session từ project khác vẫn ghi đúng skill/project metadata và hiện lên dashboard tổng.
- **As-Is Diagram (ASCII)**:
```text
global codex hooks
      |
      v
AISkills-owned bridge
      |
      +--> hardcoded repo + pilot assumptions
      +--> project khác không ghi đúng run
```
- **To-Be Diagram (ASCII)**:
```text
global codex hooks
      |
      v
global bridge + generic skill contract
      |
      +--> resolve current project from cwd/session
      +--> resolve skill metadata from marker/transcript
      +--> write global ledger for any project
```
- **Deliverables**:
  - `SOW_0035`
  - refactor hook bridge thành cross-project global flow
  - cập nhật `telemetry-flow` spec thành global contract
  - cập nhật `task-router-flow` và `sow-delegate-flow` specs cho marker/hook behavior thống nhất
  - sync scripts/hook assets sang Codex env theo global layout
- **Done Criteria**:
  - run từ project khác ghi vào `~/.logs/codex/telemetry/runs/` với `project_name/project_path` đúng
  - skills synced vào `~/.codex` dùng được cho project khác
  - dashboard tổng thấy telemetry cross-project
  - không còn hardcode repo `AISkills` trong runtime bridge path
- **Out-of-Scope**:
  - redesign dashboard
  - migrate tất cả tool/plugin skills ngoài repo này
- **Proposed-By**: Codex GPT-5
- **plan**: `global cross-project skill telemetry`
- **Cautions / Risks**:
  - cần tránh double-count với explicit telemetry path của `sow-delegate-flow`
  - project khác có thể không có SOW path giống AISkills nên resolver phải degrade gracefully
  - sync sang `~/.codex` không được làm vỡ config khác
