- **Status**: draft
- **Approval**: pending
- **Task**: Implement trainer core tối thiểu cho framework mới, gồm train/eval lifecycle cơ bản, run state, và artifact persistence với mock backend/adapter.
- **Location**: `~/Projects/AISkills/aiskills_common/skill_framework/`, `~/Projects/AISkills/tests/skill_framework/`, `~/Projects/AISkills/scripts/skill_framework/`
- **Why**: Sau khi contracts đã chốt, cần một lõi thực thi thật để chứng minh framework không chỉ là type shell. Phase này tập trung vào control flow và persistence trước khi thêm pipeline composition hay benchmark demo.
- **As-Is Diagram (ASCII)**:
```text
contracts only
    |
    v
 no executable training lifecycle
```
- **To-Be Diagram (ASCII)**:
```text
SkillTrainer.fit/evaluate
          |
          v
    trainer core
      |      |
      |      +--> artifacts / run state
      v
 mock backend + mock adapter
```
- **Deliverables**:
  - implement trainer core tối thiểu cho fit/evaluate lifecycle
  - implement artifact model và persistence cơ bản
  - implement run state/resume-friendly structures ở mức framework core nếu hợp lý
  - thêm mock backend + mock adapter để test control flow
  - thêm tests cho train loop, eval-only flow, artifact writes
- **Done Criteria**:
  - có thể chạy một mocked training run end-to-end qua Python API
  - artifacts được ghi và đọc lại theo contract
  - tests xác nhận lifecycle chính pass
  - không cần benchmark thật để validate phase này
- **Out-of-Scope**:
  - chưa có chain/pipeline composition path
  - chưa có demo adapter benchmark-facing
  - chưa có usage docs hoàn chỉnh
- **Proposed-By**: Codex GPT-5
- **plan**: `~/Projects/AISkills/plan_todo/skill_framework_distillation_plan.md`
- **Cautions / Risks**:
  - phase này dễ kéo theo benchmark-specific assumptions; cần giữ mock-first
  - artifact shape phải đủ ổn định để phase sau không phải đổi lớn
