# SOW_20260425_TZNXOS70 - Dashboard Loader And Schema

- Status: UNKNOWN
- Approval: UNKNOWN
- create_dttm: 2026-04-25T00:36:55+07:00
- create_date: 2026-04-25
- create_dttm_source: filesystem_birthtime
- create_dttm_confidence: filesystem_proxy
- create_dttm_evidence: `plan_todo/finished/SOW_20261008_VO3LKN0L/creation-date-evidence.json` (record: SOW_20260425_TZNXOS70)
- approve_dttm: unknown
- finish_dttm: unknown
- legacy_id: SOW_0021
- legacy_path: plan_todo/finished/SOW_0021_dashboard_loader_and_schema.md
- migrated_dttm: 2026-10-08T12:48:51+07:00
- legacy_title: SOW: Dashboard Loader And Schema

## Preserved Contract And Historical Evidence

- **Task**: Xây slice loader/schema cho telemetry dashboard bằng Python + Polars để đọc local telemetry logs và chuẩn hóa dataset one-row-per-run dùng chung cho các SOW backend sau.
- **Location**: `plan_todo/SOW_0021_dashboard_loader_and_schema.md`, `~/Projects/AISkills/scripts/dashboard/**`, và file cấu hình Python liên quan nếu cần.
- **Why**: Lần delegate trước scope backend/data/API quá rộng. Slice này thu hẹp còn loader + schema để Claude xử lý gọn hơn.
- **As-Is Diagram (ASCII)**:
```text
telemetry logs + parsers
        |
        v
manual local inspection only
        |
        v
no normalized dashboard dataset
```
- **To-Be Diagram (ASCII)**:
```text
telemetry logs
    |
    v
Polars loader
    |
    v
normalized run dataset
    |
    +--> reused by later backend APIs
```
- **Deliverables**:
  - Python dashboard package or scripts under `scripts/dashboard/`
  - Polars-based loader over telemetry run records
  - normalized one-row-per-run dataset/schema helpers
  - small local smoke entry or test helper for loading current repo data
- **Done Criteria**:
  - current local telemetry files load into a normalized dataset
  - data layer is reusable by later API SOWs
  - no HTTP API is added in this SOW
  - scope stays loader/schema only
- **Out-of-Scope**:
  - summary/runs/detail/charts endpoints
  - Vue frontend
  - single-port boot and static asset serving
  - dashboard layout polish
- **Proposed-By**: Codex GPT-5
- **plan**: `plan_todo/telemetry_dashboard_master_plan.md`
- **Cautions / Risks**:
  - avoid eager rescans of raw Claude/Codex artifacts when telemetry run JSON already has enough fields
  - keep schema explicit so later SOWs do not drift
