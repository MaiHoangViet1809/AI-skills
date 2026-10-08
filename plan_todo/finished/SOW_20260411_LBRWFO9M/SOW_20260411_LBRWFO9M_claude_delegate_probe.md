# SOW_20260411_LBRWFO9M - Claude Delegate Probe

- Status: UNKNOWN
- Approval: UNKNOWN
- create_dttm: 2026-04-11T03:01:41+07:00
- create_date: 2026-04-11
- create_dttm_source: filesystem_birthtime
- create_dttm_confidence: filesystem_proxy
- create_dttm_evidence: `plan_todo/finished/SOW_20261008_VO3LKN0L/creation-date-evidence.json` (record: SOW_20260411_LBRWFO9M)
- approve_dttm: unknown
- finish_dttm: unknown
- legacy_id: SOW_0003
- legacy_path: plan_todo/finished/SOW_0003_claude_delegate_probe.md
- migrated_dttm: 2026-10-08T12:48:51+07:00
- legacy_title: SOW: Claude Delegate Probe

## Preserved Contract And Historical Evidence

- **Task**: Thử delegate một tác vụ Python tối thiểu cho Claude CLI, yêu cầu trả metadata dạng JSON để Codex kiểm tra và rút ra contract phối hợp.
- **Location**: `plan_todo/SOW_claude_delegate_probe.md`, `test_claude_cli.py`
- **Why**: Xác minh luồng cộng tác Codex -> Claude CLI trong repo này trước khi đóng gói thành skill orchestration lớn hơn.
- **As-Is Diagram (ASCII)**:
```text
User request
   |
   v
Codex tự làm hoặc mô tả ý tưởng
   |
   v
Chưa có contract delegate Claude CLI được kiểm chứng
```
- **To-Be Diagram (ASCII)**:
```text
User request
   |
   v
Codex tạo SOW và được approve
   |
   v
Codex gọi Claude CLI non-interactive
   |
   v
Claude tạo test_claude_cli.py + trả JSON status
   |
   v
Codex đọc JSON, review file, xác nhận contract/fallback
```
- **Deliverables**: `test_claude_cli.py` chứa hàm `sum_float(*args)`; một lần chạy delegate Claude CLI với output JSON; tóm tắt contract phối hợp thực tế.
- **Done Criteria**: Claude CLI chạy được ở chế độ non-interactive; JSON output parse được; file Python được tạo đúng scope; Codex đọc lại file và xác nhận nội dung cơ bản.
- **Out-of-Scope**: Chưa tạo skill hoàn chỉnh; chưa refactor repo; chưa thêm test framework; chưa thay đổi workflow commit rộng hơn ngoài phạm vi probe này.
- **Proposed-By**: Codex GPT-5
- **plan**: `plan_todo/SOW_claude_delegate_probe.md`
- **Cautions / Risks**:
  - Claude CLI có thể hết token hoặc trả output không đúng schema.
  - Claude có thể chạm ngoài phạm vi nếu prompt không khóa đủ chặt.
  - Repo hiện có thay đổi cục bộ ở `.claude/launch.json`, không được đụng vào.
