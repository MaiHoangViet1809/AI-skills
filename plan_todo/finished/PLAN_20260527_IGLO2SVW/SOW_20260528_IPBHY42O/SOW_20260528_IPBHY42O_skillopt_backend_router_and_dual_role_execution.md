# SOW_20260528_IPBHY42O - skillopt backend router and dual role execution

- Status: completed
- Approval: approved
- create_dttm: 2026-05-28T01:05:05+07:00
- create_date: 2026-05-28
- create_dttm_source: filesystem_birthtime
- create_dttm_confidence: filesystem_proxy
- create_dttm_evidence: `plan_todo/finished/SOW_20261008_VO3LKN0L/creation-date-evidence.json` (record: SOW_20260528_IPBHY42O)
- approve_dttm: unknown
- finish_dttm: unknown
- legacy_id: SOW_0050
- legacy_path: plan_todo/SOW_0050_skillopt_backend_router_and_dual_role_execution.md
- migrated_dttm: 2026-10-08T12:48:51+07:00

## Preserved Contract And Historical Evidence

- **Status**: completed
- **Approval**: approved
- **Task**: Thiết kế lại backend/model layer của `darwinSkill` để hỗ trợ dual-role execution tương đương original SkillOpt, gồm optimizer backend và target backend với routing rõ ràng.
- **Location**: `~/Projects/AISkills/darwinSkill/`, `~/Projects/AISkills/tests/darwinSkill/`, `~/Projects/AISkills/references/SkillOpt/skillopt/model/`
- **Why**: Original SkillOpt dùng các runtime và provider khác nhau cho optimizer path và target path. Một `SkillBackend.predict/improve_skill` đơn giản không đủ để tái tạo execution semantics này trên các benchmark thật.
- **As-Is Diagram (ASCII)**:
```text
SkillBackend
  -> predict(skill, sample)
  -> improve_skill(skill, feedback)
```
- **To-Be Diagram (ASCII)**:
```text
BackendRouter
  -> target backend executes rollout/eval path
  -> optimizer backend executes reflect/update/memory path
  -> compatibility config resolves provider/runtime specifics
```
- **Deliverables**:
  - introduce explicit optimizer-role and target-role backend interfaces
  - create routing/config objects for provider selection and execution options
  - support compatibility paths for provider/runtime families present in the reference snapshot:
    - Azure/OpenAI-style chat
    - Codex exec-style runtime
    - Claude chat/code-exec style runtime
    - Qwen chat style runtime
  - preserve Python-native dependency injection for callers that want direct backend construction
  - add tests and smoke adapters for:
    - optimizer/target role separation
    - routing resolution
    - incompatible config detection
    - fallback/default provider mapping
- **Done Criteria**:
  - trainer engine can use distinct backends for reflection/update and rollout/evaluation
  - backend routing lives behind explicit objects rather than process-global public assumptions
  - compatibility behavior is testable from native Python call sites
- **Progress Notes**:
  - `BackendRouter`, `RoutingConfig`, va `BackendRuntimeConfig` da cover role split + family mapping
  - da co target-role wrappers cho `SpreadsheetBench` va `ALFWorld` de interactive runtimes di qua `BackendRouter`
  - da co provider-compat wrappers cho OpenAI/Claude/Qwen/Codex-style tool-call payloads
  - da co family-aware bootstrap helper de di tu benchmark + provider family -> interactive router
  - done criteria da duoc dat o framework core; production client construction/auth bootstrap duoc giu la integration concern ngoai native Python API core
- **Out-of-Scope**:
  - migrating every benchmark adapter
  - UI integration
  - exact token accounting parity with every provider
- **Proposed-By**: Codex GPT-5
- **plan**: `plan_todo/finished/PLAN_20260527_IGLO2SVW/PLAN_20260527_IGLO2SVW_skill_framework_distillation_plan.md`
- **Cautions / Risks**:
  - provider abstractions quá chung sẽ làm mất capability-specific knobs
  - provider compatibility nên được giữ ở internal/operator layer, không tràn vào public trainer constructor vô tổ chức
