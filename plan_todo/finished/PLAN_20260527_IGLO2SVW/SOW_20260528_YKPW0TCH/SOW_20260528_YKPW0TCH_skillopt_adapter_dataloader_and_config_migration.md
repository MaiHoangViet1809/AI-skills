# SOW_20260528_YKPW0TCH - skillopt adapter dataloader and config migration

- Status: completed
- Approval: approved
- create_dttm: 2026-05-28T01:05:05+07:00
- create_date: 2026-05-28
- create_dttm_source: filesystem_birthtime
- create_dttm_confidence: filesystem_proxy
- create_dttm_evidence: `plan_todo/finished/SOW_20261008_VO3LKN0L/creation-date-evidence.json` (record: SOW_20260528_YKPW0TCH)
- approve_dttm: unknown
- finish_dttm: unknown
- legacy_id: SOW_0051
- legacy_path: plan_todo/SOW_0051_skillopt_adapter_dataloader_and_config_migration.md
- migrated_dttm: 2026-10-08T12:48:51+07:00

## Preserved Contract And Historical Evidence

- **Status**: completed
- **Approval**: approved
- **Task**: Xây adapter, dataloader, batch spec, và config migration layer cho `darwinSkill` để benchmark/runtime có thể chạy trên framework mới qua native Python API mà không quay lại CLI-first architecture.
- **Location**: `~/Projects/AISkills/darwinSkill/`, `~/Projects/AISkills/tests/darwinSkill/`, `~/Projects/AISkills/references/SkillOpt/skillopt/envs/`, `~/Projects/AISkills/references/SkillOpt/skillopt/datasets/`, `~/Projects/AISkills/references/SkillOpt/skillopt/config.py`
- **Why**: Benchmark parity phụ thuộc trực tiếp vào cách original SkillOpt build batches, splits, eval envs, và config resolution. Nếu không tái tạo lớp này, các SOW benchmark sau sẽ phải nhét logic benchmark vào trainer core.
- **As-Is Diagram (ASCII)**:
```text
caller provides list[SkillSample]
  -> trainer/pipeline runs directly
```
- **To-Be Diagram (ASCII)**:
```text
config loader / builder
  -> adapter registry
  -> dataloader / batch spec
  -> train batch / eval batch builders
  -> trainer engine
```
- **Deliverables**:
  - define importable adapter and dataloader interfaces for train/eval split construction
  - create typed batch spec objects for rollout and evaluation
  - add config loading layer that can:
    - read structured configs
    - map compatibility fields from legacy-style settings
    - hand resolved objects into native Python API helpers and framework objects
  - add tests for:
    - adapter registry resolution
    - split/batch creation contracts
    - structured config mapping
    - legacy-compat override translation
- **Done Criteria**:
  - benchmark adapters can plug into framework through explicit contracts instead of ad hoc caller wiring
  - config loading is usable from Python without requiring CLI wrappers
  - trainer no longer assumes raw sample lists are the only input path
- **Progress Notes**:
  - benchmark dataset loaders/evaluators da duoc map vao `darwinSkill.benchmarks`
  - `run_with_adapter(...)` va `run_reference_adapter(...)` da dung `eval_samples` rieng cho gate/final report thay vi collapse ve train split
  - da co adapter registry/builder cho benchmark aliases (`records` hoac `path`) va config-driven resolution qua `build_reference_adapter_from_config(...)`
  - typed benchmark spec, alias resolution, va adapter/config contracts da du cho benchmark-backed train/eval paths ma khong can quay lai CLI-first architecture
- **Out-of-Scope**:
  - provider execution internals
  - actual migration of each benchmark implementation
  - UI layer
- **Proposed-By**: Codex GPT-5
- **plan**: `plan_todo/finished/PLAN_20260527_IGLO2SVW/PLAN_20260527_IGLO2SVW_skill_framework_distillation_plan.md`
- **Cautions / Risks**:
  - config compatibility layer dễ phình thành flat-dict legacy nếu không siết object boundaries
  - adapter contracts phải đủ giàu cho interactive envs, không chỉ text QA
