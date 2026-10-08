# SOW_20260425_87WNL5BL - SowDelegateFlow Session Compaction

- Status: UNKNOWN
- Approval: UNKNOWN
- create_dttm: 2026-04-25T00:36:55+07:00
- create_date: 2026-04-25
- create_dttm_source: filesystem_birthtime
- create_dttm_confidence: filesystem_proxy
- create_dttm_evidence: `plan_todo/finished/SOW_20261008_VO3LKN0L/creation-date-evidence.json` (record: SOW_20260425_87WNL5BL)
- approve_dttm: unknown
- finish_dttm: unknown
- legacy_id: SOW_0007
- legacy_path: plan_todo/finished/SOW_0007_sow_delegate_flow_session_compaction.md
- migrated_dttm: 2026-10-08T12:48:51+07:00
- legacy_title: SOW: SowDelegateFlow Session Compaction

## Preserved Contract And Historical Evidence

- **Task**: Cập nhật skill `sow-delegate-flow` để dùng policy session cost-aware: chỉ resume khi delegate session còn ngắn và sạch; nếu session đã dài/noisy thì Codex đọc transcript, compact history ngắn gọn, rồi mở session mới thay vì resume mù.
- **Location**: `plan_todo/SOW_sow_delegate_flow_session_compaction.md`, `~/.codex/skills/sow-delegate-flow/SKILL.md`, `~/.codex/skills/sow-delegate-flow/references/claude-delegate-contract.md`
- **Why**: Giảm token cost do context accumulation trong Claude Code, trong khi vẫn giữ continuity thông qua summary ngắn do Codex kiểm soát.
- **As-Is Diagram (ASCII)**:
```text
Plan with many SOWs
   |
   v
One delegate session per plan
   |
   v
Resume same session for advice/repair/follow-up
   |
   v
Context can grow noisy and expensive
```
- **To-Be Diagram (ASCII)**:
```text
Delegate session exists
   |
   v
Need follow-up?
   |
   +--> session still short/clean -> resume same session
   |
   +--> session long/noisy
          |
          v
       Codex reads transcript
          |
          v
       Codex writes compact history
          |
          v
       Start fresh session with:
         - old SOW path
         - compact history
         - new advice/feedback
         - write scope
```
- **Deliverables**: Cập nhật `SKILL.md` để mô tả resume-vs-refresh policy; cập nhật contract reference để nêu rõ transcript-based compaction, history summary shape, và việc không dùng “line count” như tín hiệu chính.
- **Done Criteria**: Skill vẫn ngắn gọn; không còn hard rule `1 plan = 1 session`; có rule rõ cho resume vs fresh session; compact history được mô tả ngắn và thực dụng; validator vẫn pass.
- **Out-of-Scope**: Không tạo script parser transcript; không tự động hóa exact message-count heuristic; không thêm retention policy; không đổi trigger multi-SOW plan.
- **Proposed-By**: Codex GPT-5
- **plan**: `plan_todo/SOW_sow_delegate_flow_session_compaction.md`
- **Cautions / Risks**:
  - Nếu compact summary kém, Claude có thể mất continuity quan trọng.
  - Nếu mô tả heuristic quá cứng, skill sẽ giòn khi CLI internals thay đổi.
  - Transcript `.jsonl` có nhiều event hệ thống nên không được dùng số dòng làm thước đo chính.
