# SOW: SowDelegateFlow Advisor Session Update

- **Task**: Cập nhật skill `sow-delegate-flow` để hỗ trợ advisor loop với câu hỏi ngược từ Claude, đồng thời áp dụng rule `1 plan = 1 delegate session` và theo dõi `session_id` từ CLI output.
- **Task**: Cập nhật skill `sow-delegate-flow` để hỗ trợ advisor loop với câu hỏi ngược từ Claude, áp dụng rule `1 plan = 1 delegate session`, theo dõi `session_id` từ CLI output, và phát hiện quota/token-limit hit từ output JSON/event sau khi submit delegate call.
- **Location**: `plan_todo/SOW_sow_delegate_flow_advisor_session.md`, `/Users/maihoangviet/.codex/skills/sow-delegate-flow/SKILL.md`, `/Users/maihoangviet/.codex/skills/sow-delegate-flow/references/claude-delegate-contract.md`
- **Why**: Giảm prompt drift, giữ context theo từng plan thay vì trộn nhiều plan vào một session, và cho phép Claude escalates blocker về Codex theo kiểu advisor thay vì đoán tiếp.
- **As-Is Diagram (ASCII)**:
```text
Approved SOW
   |
   v
Codex delegates by sow_path
   |
   v
Claude returns success or failed
   |
   v
Codex reviews or falls back
```
- **To-Be Diagram (ASCII)**:
```text
New plan
   |
   v
Create fresh delegate session
   |
   v
Approved SOW -> delegate by sow_path
   |
   v
Claude returns:
  - success
  - needs_advice + open_questions
  - failed
   |
   v
Codex answers/advises and resumes same session
   |
   v
Claude reports done
   |
   v
Codex validates against SOW
   |
   +--> not good enough -> send feedback and resume same session
   |
   +--> good enough -> continue closeout
    |
    v
Validate SOW completion
   |
   +--> same plan still active -> keep session
   |
   +--> no active SOW in plan -> drop session from state

Quota/rate-limit branch:
Claude submit call
   |
   v
CLI JSON/event shows rate-limit or usage block
   |
   v
Codex stops delegating and implements locally
```
- **Deliverables**: Cập nhật ngắn gọn cho `SKILL.md`; cập nhật contract reference gồm `needs_advice`, `open_questions`, `delegate_session_id`, rule resume cùng session trong cùng plan, rule tạo session mới cho plan mới, feedback loop khi validate thất bại, và detection quota/token-limit hit từ CLI JSON/event output.
- **Done Criteria**: Skill vẫn ngắn gọn; mô tả rõ `1 plan = 1 session`; session ID được lấy từ CLI envelope thay vì hỏi model; có advisor loop rõ ràng; có validation feedback loop rõ ràng; quota/token-limit hit được mô tả theo post-submit CLI output detection thay vì percentage pre-check; validator vẫn pass.
- **Out-of-Scope**: Không thêm retention policy; không tạo script quản lý session; không đổi tên skill; không thêm parallel delegation.
- **Out-of-Scope**: Không thêm retention policy; không tạo script quản lý session; không đổi tên skill; không thêm parallel delegation; không hứa pre-check usage percentage nếu CLI không cung cấp.
- **Proposed-By**: Codex GPT-5
- **plan**: `plan_todo/SOW_sow_delegate_flow_advisor_session.md`
- **Cautions / Risks**:
  - Mô tả quá dài sẽ làm skill phình lại.
  - Nếu contract JSON quá phức tạp sẽ tăng token không cần thiết.
  - Cần nói rõ session naming chỉ là hỗ trợ debug, không phải nguồn sự thật cho session tracking.
  - Cần phân biệt rõ `delegate done` với `SOW done` để tránh đóng task sớm.
  - Cần tránh hardcode exact error string cho quota hit nếu Claude CLI có thể đổi wording giữa các version.
