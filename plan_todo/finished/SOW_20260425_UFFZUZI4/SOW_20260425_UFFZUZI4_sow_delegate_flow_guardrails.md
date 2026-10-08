# SOW_20260425_UFFZUZI4 - SowDelegateFlow Guardrails

- Status: UNKNOWN
- Approval: UNKNOWN
- create_dttm: 2026-04-25T00:36:55+07:00
- create_date: 2026-04-25
- create_dttm_source: filesystem_birthtime
- create_dttm_confidence: filesystem_proxy
- create_dttm_evidence: `plan_todo/finished/SOW_20261008_VO3LKN0L/creation-date-evidence.json` (record: SOW_20260425_UFFZUZI4)
- approve_dttm: unknown
- finish_dttm: unknown
- legacy_id: SOW_0009
- legacy_path: plan_todo/finished/SOW_0009_sow_delegate_flow_guardrails.md
- migrated_dttm: 2026-10-08T12:48:51+07:00
- legacy_title: SOW: SowDelegateFlow Guardrails

## Preserved Contract And Historical Evidence

- **Task**: Cập nhật skill `sow-delegate-flow` để thêm precedence rule giữa `SOW / AGENTS.md / CLAUDE.md`, mở rộng result contract với `scope_respected` và `validation_hint`, và phân loại failure thành `infra / quality / uncertainty`.
- **Location**: `plan_todo/SOW_sow_delegate_flow_guardrails.md`, `~/.codex/skills/sow-delegate-flow/SKILL.md`, `~/.codex/skills/sow-delegate-flow/references/claude-delegate-contract.md`
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
