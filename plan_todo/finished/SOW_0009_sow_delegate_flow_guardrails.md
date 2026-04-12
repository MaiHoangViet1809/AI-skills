# SOW: SowDelegateFlow Guardrails

- **Task**: Cập nhật skill `sow-delegate-flow` để thêm precedence rule giữa `SOW / AGENTS.md / CLAUDE.md`, mở rộng result contract với `scope_respected` và `validation_hint`, và phân loại failure thành `infra / quality / uncertainty`.
- **Location**: `plan_todo/SOW_sow_delegate_flow_guardrails.md`, `/Users/maihoangviet/.codex/skills/sow-delegate-flow/SKILL.md`, `/Users/maihoangviet/.codex/skills/sow-delegate-flow/references/claude-delegate-contract.md`
- **Why**: Làm workflow chặt hơn trước khi dùng lâu dài: rõ precedence, dễ machine-parse hơn, và dễ tách lỗi hạ tầng khỏi lỗi chất lượng hay bất định.
- **As-Is Diagram (ASCII)**:
```text
Repo rules + approved SOW + Claude context
   |
   v
Skill uses them together
   |
   v
Precedence and failure classes are implicit
```
- **To-Be Diagram (ASCII)**:
```text
AGENTS.md / repo rules -> process constraints
Approved SOW          -> active task scope
CLAUDE.md             -> Claude-specific helper context
   |
   v
Claude returns structured result with:
  - status
  - failure_type
  - scope_respected
  - validation_hint
   |
   v
Codex routes follow-up or fallback more cleanly
```
- **Deliverables**: Cập nhật `SKILL.md` với precedence rule ngắn gọn; cập nhật contract reference với schema mới và failure taxonomy.
- **Done Criteria**: Skill vẫn ngắn gọn; precedence rule rõ; schema có `scope_respected` và `validation_hint`; failure được phân loại `infra / quality / uncertainty`; validator vẫn pass.
- **Out-of-Scope**: Không thêm sidecar memory rule; không thay đổi trigger; không thêm script mới.
- **Proposed-By**: Codex GPT-5
- **plan**: `plan_todo/SOW_sow_delegate_flow_guardrails.md`
- **Cautions / Risks**:
  - Nếu schema phình quá mức sẽ tăng token cost.
  - Failure taxonomy phải ngắn và thực dụng, không biến thành lý thuyết.
