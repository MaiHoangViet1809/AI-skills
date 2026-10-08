# SOW_20260425_KQ138ZHE - Sow Delegate Flow Json First

- Status: UNKNOWN
- Approval: UNKNOWN
- create_dttm: 2026-04-25T00:36:55+07:00
- create_date: 2026-04-25
- create_dttm_source: filesystem_birthtime
- create_dttm_confidence: filesystem_proxy
- create_dttm_evidence: `plan_todo/finished/SOW_20261008_VO3LKN0L/creation-date-evidence.json` (record: SOW_20260425_KQ138ZHE)
- approve_dttm: unknown
- finish_dttm: unknown
- legacy_id: SOW_0012
- legacy_path: plan_todo/finished/SOW_0012_sow_delegate_flow_json_first.md
- migrated_dttm: 2026-10-08T12:48:51+07:00
- legacy_title: SOW: Sow Delegate Flow Json First

## Preserved Contract And Historical Evidence

- **Task**: Cập nhật `sow-delegate-flow` để dùng `json` làm output mode mặc định, chỉ bật `stream-json` khi cần debug sâu hơn delegate behavior, và ghi rõ rằng stream capture nên lọc bỏ `system` noise thay vì thay đổi runtime environment của Claude.
- **Location**: `plan_todo/SOW_sow_delegate_flow_json_first.md`, `~/.codex/skills/sow-delegate-flow/SKILL.md`, `~/.codex/skills/sow-delegate-flow/references/claude-delegate-contract.md`
- **Why**: Giảm log bloat và context cost cho coordinator, trong khi vẫn giữ khả năng chuyển sang `stream-json` khi cần debug delegate failures hoặc output bất thường.
- **As-Is Diagram (ASCII)**:
```text
Delegate call
   |
   v
Often described with stream-first handling
   |
   v
Coordinator may read too much event noise
```
- **To-Be Diagram (ASCII)**:
```text
Delegate call
   |
   +--> normal path -> json
   |
   +--> deep delegate debugging -> stream-json
            |
            v
         filter captured stream
         keep useful events only
```
- **Deliverables**: Cập nhật ngắn gọn cho `SKILL.md`; cập nhật contract reference cho `json-first`, `stream-json` only for delegate debugging, `system` event filtering at capture layer, và polling default 30s.
- **Done Criteria**: Skill vẫn ngắn gọn; `json` là default mode; `stream-json` được mô tả như debug tool; có note rõ không đổi Claude runtime environment; có note poll/check mặc định 30s; validator vẫn pass.
- **Out-of-Scope**: Không thay đổi runtime capabilities của Claude bằng `--bare`; không thêm script wrapper; không thay đổi trigger của skill.
- **Proposed-By**: Codex GPT-5
- **plan**: `plan_todo/SOW_sow_delegate_flow_json_first.md`
- **Cautions / Risks**:
  - Nếu mô tả stream debug quá sơ sài thì operator có thể không biết khi nào nên bật nó.
  - Nếu lọc stream quá mạnh thì có thể mất một số tín hiệu debug hữu ích.
