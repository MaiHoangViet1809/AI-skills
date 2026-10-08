# SOW_20260425_4NSM51RC - Telemetry Hook Skill V1

- Status: UNKNOWN
- Approval: UNKNOWN
- create_dttm: 2026-04-25T00:36:55+07:00
- create_date: 2026-04-25
- create_dttm_source: filesystem_birthtime
- create_dttm_confidence: filesystem_proxy
- create_dttm_evidence: `plan_todo/finished/SOW_20261008_VO3LKN0L/creation-date-evidence.json` (record: SOW_20260425_4NSM51RC)
- approve_dttm: unknown
- finish_dttm: unknown
- legacy_id: SOW_0019
- legacy_path: plan_todo/finished/SOW_0019_telemetry_hook_skill_v1.md
- migrated_dttm: 2026-10-08T12:48:51+07:00
- legacy_title: SOW: Telemetry Hook Skill V1

## Preserved Contract And Historical Evidence

- **Task**: Tạo một skill telemetry riêng với đúng 2 hook `start` và `finish` để capture metric run-level từ Codex rollout và Claude raw log cho việc đo hiệu quả sử dụng sau này.
- **Location**: `~/Projects/AISkills/skills/telemetry-flow/**`, `~/Projects/AISkills/scripts/telemetry/parse_codex_rollout.py`, reference telemetry liên quan, và integration tối thiểu vào `skills/sow-delegate-flow/SKILL.md`
- **Why**: Cần tách telemetry khỏi execution flow nhưng vẫn đo được token, duration, outcome, và các metric calculable khác cho từng run mà không cần LLM đánh giá.
- **As-Is Diagram (ASCII)**:
```text
Codex rollout logs     Claude raw logs
       |                    |
       v                    v
separate parsers       separate parsers
       |                    |
       +---- no stable run-level measurement ----+
```
- **To-Be Diagram (ASCII)**:
```text
telemetry start
    |
    v
create run_id + staging record + markers
    |
    +--> Codex rollout
    +--> Claude raw log
    |
    v
telemetry finish
    |
    v
parse both sides by run context
    |
    v
return normalized run metrics
```
- **Deliverables**:
  - Skill telemetry mới với 2 hooks `start` và `finish`
  - Staging record tối thiểu cho mỗi run
  - Marker convention để đối soát Codex/Claude log
  - Normalized run metrics output
  - Hook contract để `sow-delegate-flow` gọi trước/sau delegate
- **Done Criteria**:
  - Mỗi run có `run_id` riêng
  - `finish` hook trả được metric chính cho Codex, Claude, duration, outcome, và các metric calculable bổ sung
  - Metrics đều là dữ liệu parse hoặc tính trực tiếp từ log, git state, timestamp, hoặc workflow metadata
  - Có anomaly flags khi thiếu dữ liệu hoặc match không chắc chắn
  - Chưa làm report/dashboard layer
- **Out-of-Scope**:
  - Không làm report/dashboard
  - Không tổng hợp nhiều run
  - Không dùng LLM scoring
  - Không tích hợp vào mọi skill ngoài `sow-delegate-flow` trong v1
- **Proposed-By**: Codex GPT-5
- **plan**: `telemetry hook skill v1`
- **Cautions / Risks**:
  - Marker-only không đủ chắc để match run
  - Timestamp-only dễ lệch nếu không có staging record
  - Một số metric workflow cần được truyền vào `finish` hook từ local validation/result metadata
