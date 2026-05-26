- **Status**: draft
- **Approval**: pending
- **Task**: Hoàn thiện usability cho framework mới bằng scripts/examples mỏng, docs usage ngắn, và integration smoke tests cho cả facade path lẫn pipeline path.
- **Location**: `~/Projects/AISkills/scripts/skill_framework/`, `~/Projects/AISkills/tests/skill_framework/`, `~/Projects/AISkills/aiskills_common/skill_framework/`, `~/Projects/AISkills/pyproject.toml`
- **Why**: Sau khi framework core và composition path đã có, cần chốt cách dùng thực tế và kiểm tra last-mile để framework sẵn sàng nhúng vào project khác mà không cần đọc nội bộ implementation.
- **As-Is Diagram (ASCII)**:
```text
framework core exists
    |
    v
 usage examples and smoke confidence are thin
```
- **To-Be Diagram (ASCII)**:
```text
framework core
    |
    +--> thin scripts/examples
    +--> concise usage docs
    +--> integration smoke tests
```
- **Deliverables**:
  - thêm scripts/examples mỏng cho facade path và pipeline path
  - thêm docs usage ngắn trong repo
  - thêm smoke tests cho import/run path chính
  - cleanup naming, import ergonomics, và final acceptance gaps
- **Done Criteria**:
  - người dùng có thể nhìn vào example và chạy path cơ bản nhanh
  - smoke tests pass cho facade path và pipeline path
  - public imports và naming đủ sạch để dùng lại
- **Out-of-Scope**:
  - chưa cần benchmark parity với upstream
  - chưa cần dashboard/web UI
  - chưa cần migrate project khác sang framework mới
- **Proposed-By**: Codex GPT-5
- **plan**: `~/Projects/AISkills/plan_todo/skill_framework_distillation_plan.md`
- **Cautions / Risks**:
  - nếu phase trước còn chưa ổn định, phase này dễ thành cleanup vô hạn
  - smoke tests nên giữ nhẹ để không trói chặt implementation quá sớm
