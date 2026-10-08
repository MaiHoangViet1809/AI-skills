# SOW_20260425_L1VYWH14 - SowDelegateFlow Wording Trim

- Status: UNKNOWN
- Approval: UNKNOWN
- create_dttm: 2026-04-25T00:36:55+07:00
- create_date: 2026-04-25
- create_dttm_source: filesystem_birthtime
- create_dttm_confidence: filesystem_proxy
- create_dttm_evidence: `plan_todo/finished/SOW_20261008_VO3LKN0L/creation-date-evidence.json` (record: SOW_20260425_L1VYWH14)
- approve_dttm: unknown
- finish_dttm: unknown
- legacy_id: SOW_0005
- legacy_path: plan_todo/finished/SOW_0005_sow_delegate_flow_wording_trim.md
- migrated_dttm: 2026-10-08T12:48:51+07:00
- legacy_title: SOW: SowDelegateFlow Wording Trim

## Preserved Contract And Historical Evidence

- **Task**: Rút gọn câu chữ của skill `sow-delegate-flow` để giảm context/token cost nhưng vẫn giữ đủ trigger, workflow, và fallback contract.
- **Location**: `plan_todo/SOW_sow_delegate_flow_wording_trim.md`, `~/.codex/skills/sow-delegate-flow/SKILL.md`, `~/.codex/skills/sow-delegate-flow/references/claude-delegate-contract.md`
- **Why**: Skill này là orchestration layer nên cần cực ngắn, dễ scan, và ít token khi được load.
- **As-Is Diagram (ASCII)**:
```text
Trigger skill
   |
   v
Load SKILL.md
   |
   v
Read workflow + contract
   |
   v
Nội dung đúng nhưng còn dài hơn mức cần thiết
```
- **To-Be Diagram (ASCII)**:
```text
Trigger skill
   |
   v
Load shorter SKILL.md
   |
   v
Read compact workflow + contract links
   |
   v
Same behavior, lower token cost
```
- **Deliverables**: Bản rút gọn của `SKILL.md`; reference contract ngắn hơn nếu cần; không đổi behavior cốt lõi của skill.
- **Done Criteria**: Nội dung ngắn hơn rõ rệt; vẫn giữ trigger description hữu ích; vẫn mô tả được approval, delegate-by-path, JSON output, review, và fallback; validator vẫn pass.
- **Out-of-Scope**: Không đổi tên skill; không đổi metadata UI; không thêm script mới; không đổi workflow logic.
- **Proposed-By**: Codex GPT-5
- **plan**: `plan_todo/SOW_sow_delegate_flow_wording_trim.md`
- **Cautions / Risks**:
  - Rút quá mạnh có thể làm trigger description yếu đi.
  - Bỏ chi tiết sai chỗ có thể làm skill khó dùng hơn.
