# SOW: SowDelegateFlow Skill

- **Task**: Tạo một skill global tên `SowDelegateFlow` để điều phối luồng Codex tạo SOW, chờ approve, delegate implementation sang Claude CLI bằng đường dẫn SOW, rồi fallback về Codex khi Claude lỗi hoặc hết token.
- **Location**: `plan_todo/SOW_sow_delegate_flow_skill.md`, thư mục skill global mới dưới Codex skills home, các file tối thiểu gồm `SKILL.md` và tài liệu tham chiếu nếu cần.
- **Why**: Chuẩn hóa workflow cộng tác Codex <-> Claude CLI theo SOW, giảm prompt dài, tăng khả năng tái sử dụng đa repo, và giữ SOW là nguồn sự thật duy nhất cho scope triển khai.
- **As-Is Diagram (ASCII)**:
```text
User request
   |
   v
Codex phân tích task
   |
   v
Codex tự viết prompt delegate dài hoặc tự làm
   |
   v
Claude nhận context inline, dễ drift scope
   |
   v
Codex review kết quả theo từng tình huống
```
- **To-Be Diagram (ASCII)**:
```text
User request
   |
   v
Codex đọc repo rules + tạo SOW
   |
   v
User approve SOW
   |
   v
SowDelegateFlow delegate cho Claude bằng:
  - sow_path
  - intent ngắn
  - write scope
  - JSON schema output
   |
   v
Claude tự đọc SOW file và implement
   |
   +--> success -> Codex review/test/commit
   |
   +--> fail or token exhausted -> Codex takeover
```
- **Deliverables**: Skill global `SowDelegateFlow`; `SKILL.md` mô tả trigger và workflow; tài liệu reference về contract delegate JSON và fallback rules nếu cần; một lần validation trên task nhỏ.
- **Done Criteria**: Skill trigger được cho use case phù hợp; mô tả rõ repo-aware behavior; delegate prompt chỉ dùng SOW path + intent ngắn thay vì nhét cả SOW inline; có contract JSON rõ ràng; có hướng dẫn fallback; được kiểm chứng bằng ít nhất một probe nhỏ.
- **Out-of-Scope**: Chưa tự động hóa mọi loại repo convention; chưa tích hợp sâu với CI/GitHub; chưa tạo plugin mới; chưa thay thế hoàn toàn phán đoán của Codex khi review output từ Claude.
- **Proposed-By**: Codex GPT-5
- **plan**: `plan_todo/SOW_sow_delegate_flow_skill.md`
- **Cautions / Risks**:
  - Repo khác có thể không có `AGENTS.md`, cần default behavior an toàn.
  - Claude CLI flags/model aliases có thể thay đổi theo version.
  - Nếu write scope không khóa đủ chặt, Claude có thể sửa ngoài phạm vi.
  - Fallback detection cho lỗi token/rate-limit cần được mô tả đủ thực dụng, không over-engineer.
