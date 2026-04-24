# SOW: SowDelegateFlow Wording Trim

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
