# SOW: Claude Delegate Probe

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
