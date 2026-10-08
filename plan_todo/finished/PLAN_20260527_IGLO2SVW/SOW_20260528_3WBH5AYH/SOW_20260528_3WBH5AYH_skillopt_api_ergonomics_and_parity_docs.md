# SOW_20260528_3WBH5AYH - skillopt api ergonomics and parity docs

- Status: completed
- Approval: approved
- create_dttm: 2026-05-28T02:21:49+07:00
- create_date: 2026-05-28
- create_dttm_source: filesystem_birthtime
- create_dttm_confidence: filesystem_proxy
- create_dttm_evidence: `plan_todo/finished/SOW_20261008_VO3LKN0L/creation-date-evidence.json` (record: SOW_20260528_3WBH5AYH)
- approve_dttm: unknown
- finish_dttm: unknown
- legacy_id: SOW_0055
- legacy_path: plan_todo/SOW_0055_skillopt_api_ergonomics_and_parity_docs.md
- migrated_dttm: 2026-10-08T12:48:51+07:00

## Preserved Contract And Historical Evidence

- **Status**: completed
- **Approval**: approved
- **Task**: Hoàn thiện API ergonomics, artifact inspection docs, và parity documentation cuối chương trình cho `darwinSkill` theo hướng native Python API.
- **Location**: `~/Projects/AISkills/darwinSkill/`, `~/Projects/AISkills/plan_todo/`, `~/Projects/AISkills/references/SkillOpt/docs/`
- **Why**: Sau khi core engine và benchmark surfaces đã được migrate, cần một slice cuối để chốt trải nghiệm dùng framework qua Python API. Original project có thêm lớp vận hành bằng UI/CLI, nhưng với hướng mới thứ cần giữ lại là inspectability và tài liệu parity.
- **As-Is Diagram (ASCII)**:
```text
Python API experience
  -> partial docs
  -> raw artifacts
  -> parity story chưa được chốt rõ
```
- **To-Be Diagram (ASCII)**:
```text
Python API experience
  -> clear run layout
  -> parity docs / migration notes
  -> artifact inspection guide
  -> polished acceptance checklist
```
- **Deliverables**:
  - review and tighten output layout, artifact discoverability, and run-inspection docs
  - document parity status benchmark-by-benchmark and surface-by-surface
  - document native Python usage patterns for:
    - trainer path
    - pipeline path
    - benchmark-backed run path
  - add final program acceptance notes tying together all prior SOWs
- **Done Criteria**:
  - người dùng Python API có thể hiểu rõ nơi lưu run state, best skills, step artifacts, và epoch memory artifacts
  - parity status is documented, not implicit
  - không còn dependency hay dangling scope nào tới WebUI/CLI trong parity plan
- **Completion Notes**:
  - added native inspection helpers:
    - `darwinSkill.inspection.inspect_run(...)`
    - `darwinSkill.inspection.summarize_run(...)`
    - `darwinSkill.inspection.load_step_record(...)`
  - added benchmark path helper:
    - `darwinSkill.native.run_reference_benchmark_from_path(...)`
  - finalized user-facing docs:
    - `darwinSkill/README.md`
    - `darwinSkill/USAGE.md`
    - `darwinSkill/PARITY.md`
- **Out-of-Scope**:
  - adding new benchmark families
  - redesigning the framework public API again
  - UI riêng hoặc visual parity với upstream site assets
- **Proposed-By**: Codex GPT-5
- **plan**: `plan_todo/finished/PLAN_20260527_IGLO2SVW/PLAN_20260527_IGLO2SVW_skill_framework_distillation_plan.md`
- **Cautions / Risks**:
  - nếu kéo polish docs quá sớm vào trước benchmark parity thì effort sẽ lệch hướng
  - cần chốt rõ “functional parity” ở native Python API layer để tránh endless cleanup
