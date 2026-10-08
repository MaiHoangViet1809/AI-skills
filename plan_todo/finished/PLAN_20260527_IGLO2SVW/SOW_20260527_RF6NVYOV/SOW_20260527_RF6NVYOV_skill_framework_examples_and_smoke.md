# SOW_20260527_RF6NVYOV - skill framework examples and smoke

- Status: done
- Approval: approved
- create_dttm: 2026-05-27T03:11:01+07:00
- create_date: 2026-05-27
- create_dttm_source: filesystem_birthtime
- create_dttm_confidence: filesystem_proxy
- create_dttm_evidence: `plan_todo/finished/SOW_20261008_VO3LKN0L/creation-date-evidence.json` (record: SOW_20260527_RF6NVYOV)
- approve_dttm: unknown
- finish_dttm: unknown
- legacy_id: SOW_0045
- legacy_path: plan_todo/finished/SOW_0045_skill_framework_examples_and_smoke.md
- migrated_dttm: 2026-10-08T12:48:51+07:00

## Preserved Contract And Historical Evidence

- **Status**: done
- **Approval**: approved
- **Task**: Hoàn thiện usability cho framework mới bằng scripts/examples mỏng, docs usage ngắn, và integration smoke tests cho cả facade path lẫn pipeline path.
- **Location**: `~/Projects/AISkills/scripts/darwinSkill/`, `~/Projects/AISkills/tests/darwinSkill/`, `~/Projects/AISkills/darwinSkill/`
- **Why**: Sau khi framework core và composition path đã có, cần chốt cách dùng thực tế và kiểm tra last-mile để framework dùng được rõ ràng trong repo này mà không buộc người dùng phải đọc nội bộ implementation.
- **As-Is Diagram (ASCII)**:
```text
framework core exists
    |
    v
 usage examples and smoke confidence are thin
```
- **To-Be Diagram (ASCII)**:
```text
framework core
    |
    +--> thin scripts/examples
    +--> concise usage docs
    +--> integration smoke tests
```
- **Deliverables**:
  - thêm scripts/examples mỏng cho facade path và pipeline path trên anchor text skill
  - thêm docs usage ngắn trong repo
  - thêm smoke tests cho import/run path chính
  - examples dùng concrete imports từ `darwinSkill.*`, không rely vào `__init__.py`
  - nói rõ trong docs/examples rằng branching/merge được orchestration bằng Python caller, không phải graph API của `SkillPipeline`
  - cleanup naming, import ergonomics, và final acceptance gaps
- **Done Criteria**:
  - người dùng có thể nhìn vào example và chạy path cơ bản nhanh
  - smoke tests pass cho facade path và pipeline path
  - public imports và naming đủ sạch để dùng lại
- **Out-of-Scope**:
  - chưa cần benchmark parity với upstream
  - chưa cần dashboard/web UI
  - chưa cần migrate project khác sang framework mới
  - chưa cần integration proof ngoài repo này
- **Proposed-By**: Codex GPT-5
- **plan**: `plan_todo/finished/PLAN_20260527_IGLO2SVW/PLAN_20260527_IGLO2SVW_skill_framework_distillation_plan.md`
- **Cautions / Risks**:
  - nếu phase trước còn chưa ổn định, phase này dễ thành cleanup vô hạn
  - smoke tests nên giữ nhẹ để không trói chặt implementation quá sớm
