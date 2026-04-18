- **Task**: Refactor các helper/function đang bị duplicate thành shared util/common modules để telemetry, dashboard, và skill scripts dùng chung một nguồn logic.
- **Location**: `/Users/maihoangviet/Projects/AISkills/plan_todo/SOW_0037_shared_utils_dedupe.md`, `/Users/maihoangviet/Projects/AISkills/aiskills_common/telemetry/**`, `/Users/maihoangviet/Projects/AISkills/scripts/telemetry/**`, `/Users/maihoangviet/Projects/AISkills/skills/telemetry-flow/scripts/**`, `/Users/maihoangviet/Projects/AISkills/skills/sow-delegate-flow/scripts/**`, `/Users/maihoangviet/Projects/AISkills/dashboard/backend/**`, `/Users/maihoangviet/Projects/AISkills/scripts/skills/sync_environment.py`, `/Users/maihoangviet/Projects/AISkills/.codex/hooks.json.template`
- **Why**: Hiện project có nhiều helper/parser duplicate và đã bắt đầu drift logic; cần gom về nguồn dùng chung để giữ DRY/KISS/SOLID và tránh sửa một nơi hỏng nơi khác.
- **As-Is Diagram (ASCII)**:
```text
dashboard loader      telemetry hook      delegate/parser scripts
      |                    |                    |
      +--> own helper copy +--> own helper copy +--> own parser copy
                        |
                        v
                 drift / inconsistent behavior
```
- **To-Be Diagram (ASCII)**:
```text
shared util/common modules
      |
      +--> dashboard backend
      +--> telemetry hook / hook bridge
      +--> delegate/parser wrappers
      |
      v
single-source logic
```
- **Deliverables**:
  - shared util module(s) cho path/json/time/sow resolution
  - shared parser/common logic cho Codex rollout và Claude delegate logs
  - remove các duplicate helper/parser chính bằng wrapper mỏng
  - update callers hiện có sang shared modules
- **Done Criteria**:
  - `resolve_sow_file` chỉ còn 1 nguồn logic dùng chung
  - `parse_delegate_log` và `parse_codex_rollout` chỉ còn 1 nguồn implementation
  - dashboard, telemetry hook, hook bridge, và synced skill runtime vẫn chạy
  - compile/smoke checks pass
- **Out-of-Scope**:
  - dashboard redesign
  - thay đổi telemetry metric schema ngoài phần cần để dedupe
- **Proposed-By**: Codex GPT-5
- **plan**: `shared utils dedupe`
- **Cautions / Risks**:
  - cần giữ skill runtime self-contained sau khi sync sang `~/.codex`
  - không được làm vỡ hook-based telemetry global path
  - parser progress mode và telemetry mode phải vẫn phục vụ đúng use case riêng
