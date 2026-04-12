# SOW: Sow Delegate Flow Json First

- **Task**: Cập nhật `sow-delegate-flow` để dùng `json` làm output mode mặc định, chỉ bật `stream-json` khi cần debug sâu hơn delegate behavior, và ghi rõ rằng stream capture nên lọc bỏ `system` noise thay vì thay đổi runtime environment của Claude.
- **Location**: `plan_todo/SOW_sow_delegate_flow_json_first.md`, `/Users/maihoangviet/.codex/skills/sow-delegate-flow/SKILL.md`, `/Users/maihoangviet/.codex/skills/sow-delegate-flow/references/claude-delegate-contract.md`
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
