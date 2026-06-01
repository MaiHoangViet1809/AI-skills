- **Status**: done
- **Approval**: approved
- **Task**: Đổi tên skill nội bộ `progress-reporting-flow` thành `task-progress-report`, cập nhật các tham chiếu hiện hành trong repo, xóa skill cũ ở production, và sync lại 2 skill đích vào `~/.codex/skills`.
- **Location**: `~/Projects/AISkills/skills/`, `~/Projects/AISkills/scripts/skills/`, `~/Projects/AISkills/plan_todo/`, `~/.codex/skills/`
- **Why**: Tên skill hiện tại mô tả chức năng nhưng chưa khớp naming intent mới. Việc đổi sang `task-progress-report` sẽ làm tên ngắn hơn, trực tiếp hơn, và dễ áp dụng nhất quán hơn khi skill được gọi từ các skill khác hoặc khi sync sang Codex. Vì production hiện vẫn còn skill cũ nên cần xóa bản cũ và sync lại đúng bộ skill đang dùng để tránh drift giữa repo và `~/.codex/skills`.
- **As-Is Diagram (ASCII)**:
```text
task execution flow
  -> references progress-reporting-flow

skills/
  -> progress-reporting-flow/
     -> SKILL.md
     -> agents/openai.yaml

~/.codex/skills/
  -> progress-reporting-flow/
  -> task-execution-flow/
```
- **To-Be Diagram (ASCII)**:
```text
task execution flow
  -> references task-progress-report

skills/
  -> task-progress-report/
     -> SKILL.md
     -> agents/openai.yaml

~/.codex/skills/
  -> task-progress-report/
  -> task-execution-flow/
  -> progress-reporting-flow removed
```
- **Deliverables**:
  - rename `skills/progress-reporting-flow/` to `skills/task-progress-report/`
  - update skill metadata in the renamed skill to use `task-progress-report`
  - update current repo references that should point to the new skill name
  - remove `~/.codex/skills/progress-reporting-flow/`
  - sync `task-progress-report` and `task-execution-flow` into `~/.codex/skills/`
  - keep historical completed SOW records unchanged unless they are needed for active runtime references
- **Done Criteria**:
  - repo no longer has active runtime/current-doc references to `progress-reporting-flow` where they should now use `task-progress-report`
  - renamed skill folder still contains the expected skill files and remains installable by the repo scripts
  - direct cross-references from other active skills use `task-progress-report`
  - `~/.codex/skills/progress-reporting-flow/` no longer exists
  - `~/.codex/skills/task-progress-report/` and `~/.codex/skills/task-execution-flow/` reflect the repo versions after sync
- **Out-of-Scope**:
  - rewriting historical finished SOW documents only for naming normalization
  - changing the behavior of the progress reporting skill beyond the rename
- **Proposed-By**: Codex GPT-5
- **plan**: `~/Projects/AISkills/plan_todo/finished/SOW_0060_task_progress_report_rename.md`
- **Cautions / Risks**:
  - rename drift nếu còn sót tham chiếu tên cũ trong skill khác
  - historical SOW docs sẽ còn giữ tên cũ theo chủ đích unless explicitly normalized later
  - cần giữ install/discovery behavior không bị gãy sau khi đổi tên thư mục
  - cần tránh để production giữ đồng thời cả tên cũ và tên mới sau khi sync
