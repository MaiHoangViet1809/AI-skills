- **Task**: Sửa global hook telemetry để chỉ ghi run cho isolated skill session thật, đồng thời dọn các run sai đã ghi vào global ledger.
- **Location**: `~/Projects/AISkills/scripts/telemetry/codex_hook_bridge.py`, `~/Projects/AISkills/skills/telemetry-flow/references/hook-contract.md`, `~/Projects/AISkills/skills/task-router-flow/SKILL.md`, `~/Projects/AISkills/scripts/telemetry/**`, và `~/.logs/codex/telemetry/runs/`
- **Why**: Dashboard đang có false-positive run do hook quét marker từ toàn transcript và nuốt luôn placeholder metadata từ probe/prompt không hợp lệ.
- **As-Is Diagram (ASCII)**:
```text
Stop hook
  |
  v
scan whole transcript
  |
  +--> any old marker can match
  +--> placeholder values still accepted
```
- **To-Be Diagram (ASCII)**:
```text
Stop hook
  |
  v
read first user prompt only
  |
  +--> must start with CODEX_SKILL_RUN
  +--> reject placeholder values
  +--> otherwise no-op
```
- **Deliverables**:
  - tighten marker/session boundary in `codex_hook_bridge.py`
  - reject placeholder marker values such as `<sow>` and `<task_type>`
  - cleanup script or targeted cleanup for bad global runs
  - verify dashboard no longer shows false-positive rows
- **Done Criteria**:
  - main session without first-line marker no longer emits skill telemetry
  - new isolated skill session with valid marker still emits telemetry
  - placeholder rows are removed from global ledger
  - dashboard shows only valid rows after refresh
- **Out-of-Scope**:
  - dashboard redesign
  - schema changes to run metrics
- **Proposed-By**: Codex GPT-5
- **plan**: `global cross-project skill telemetry`
- **Cautions / Risks**:
  - transcript formats may vary, so first-user-message extraction must degrade safely
  - cleanup must avoid deleting valid historical runs
