- **Status**: draft
- **Approval**: pending
- **Task**: Hoàn thiện operator experience cuối chương trình cho `darwinSkill`, gồm artifact ergonomics, compatibility docs, và parity hoặc replacement tối thiểu cho `skillopt_webui` nếu vẫn cần trong bối cảnh mới.
- **Location**: `~/Projects/AISkills/darwinSkill/`, `~/Projects/AISkills/scripts/`, `~/Projects/AISkills/plan_todo/`, `~/Projects/AISkills/references/SkillOpt/skillopt_webui/`, `~/Projects/AISkills/references/SkillOpt/docs/`
- **Why**: Sau khi core engine và benchmark surfaces đã được migrate, cần một slice cuối để chốt trải nghiệm vận hành. Original project không chỉ là library mà còn là tool mà người vận hành có thể inspect và chạy.
- **As-Is Diagram (ASCII)**:
```text
operator experience
  -> partial docs
  -> raw artifacts
  -> no parity decision yet for web UI
```
- **To-Be Diagram (ASCII)**:
```text
operator experience
  -> clear run layout
  -> parity docs / migration notes
  -> optional web UI or explicit non-UI replacement decision
  -> polished acceptance checklist
```
- **Deliverables**:
  - review and tighten output layout, artifact discoverability, and run-inspection docs
  - document parity status benchmark-by-benchmark and surface-by-surface
  - decide and implement one of:
    - minimal WebUI parity
    - explicit non-UI replacement with equivalent operator workflow
  - add final program acceptance notes tying together all prior SOWs
- **Done Criteria**:
  - operator can understand where run state, best skills, step artifacts, and epoch memory artifacts live
  - parity status is documented, not implicit
  - WebUI question is resolved by implementation or by a documented replacement decision
- **Out-of-Scope**:
  - adding new benchmark families
  - redesigning the framework public API again
  - exact visual parity with upstream site assets unless required by the chosen WebUI path
- **Proposed-By**: Codex GPT-5
- **plan**: `~/Projects/AISkills/plan_todo/skill_framework_distillation_plan.md`
- **Cautions / Risks**:
  - nếu kéo polish/UI quá sớm vào trước benchmark parity thì effort sẽ lệch hướng
  - cần chốt rõ “functional parity” ở operator layer để tránh endless cleanup
