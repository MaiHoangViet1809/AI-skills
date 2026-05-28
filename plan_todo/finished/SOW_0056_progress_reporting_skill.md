- **Status**: done
- **Approval**: approved
- **Task**: Tạo skill nội bộ trong repo để chuẩn hóa cách báo cáo tiến độ công việc theo format bảng progress ngắn gọn và summary chi tiết như workflow vừa chốt.
- **Location**: `~/Projects/AISkills/skills/progress-reporting-flow/`, `~/Projects/AISkills/plan_todo/`
- **Why**: Cách báo cáo progress vừa thử nghiệm cho thấy rõ ràng hơn, ít lặp hơn, và giúp phân biệt tốt giữa overall plan progress với SOW còn mở. Cần đóng gói nó thành skill để dùng lại nhất quán trong repo này.
- **As-Is Diagram (ASCII)**:
```text
execution work
  -> ad hoc progress wording
  -> format drift between turns
  -> easy to repeat done items
```
- **To-Be Diagram (ASCII)**:
```text
execution work
  -> progress-reporting-flow skill
  -> concise status discipline
  -> summary table for open work only
  -> detail notes only when needed
```
- **Deliverables**:
  - create `skills/progress-reporting-flow/SKILL.md`
  - add optional `references/` material only if needed to keep `SKILL.md` lean
  - encode the reporting rules we just converged on:
    - do not spam progress while still working unless there is a real decision point
    - default to progress summary after a completed step/block
    - show only open SOW items in the progress table
    - include one overall row such as `overall 4/5`
    - if a SOW is truly done and double-checked, remove it from the table
    - keep the last two columns empty for completed items if they ever need to appear in a one-off retrospective format
    - allow a short note section below the table only for non-table context
  - align wording with repo style: concise, direct, low-fluff
- **Done Criteria**:
  - repo has an importable-on-demand skill folder for progress reporting under `skills/`
  - skill instructions are specific enough that another Codex run can reproduce the same reporting behavior with low drift
  - skill scope is clearly limited to in-repo usage and not yet synced to Codex home skills
- **Progress Notes**:
  - da tao `skills/progress-reporting-flow/SKILL.md`
  - da them `skills/progress-reporting-flow/agents/openai.yaml` de dong bo voi skill metadata pattern trong repo
  - rules da chot dung behavior vua thong nhat: overall row luon co, chi hien SOW con mo, va progress chi report sau mot block co y nghia hoac tai decision point
- **Out-of-Scope**:
  - syncing the skill into `~/.codex/skills`
  - adding automation, plugins, or external tooling
  - changing unrelated existing skills unless needed for a direct cross-reference
- **Proposed-By**: Codex GPT-5
- **plan**: `~/Projects/AISkills/plan_todo/finished/SOW_0056_progress_reporting_skill.md`
- **Cautions / Risks**:
  - nếu viết quá dài, skill sẽ tốn context cho một nhu cầu khá hẹp
  - nếu rule quá cứng, skill sẽ khó dùng cho các task không có plan/SOW
  - cần tách rõ khi nào báo progress giữa chừng và khi nào chỉ báo ở cuối block
