# SOW_20260425_VJ86J7C3 - SowDelegateFlow Refinements

- Status: UNKNOWN
- Approval: UNKNOWN
- create_dttm: 2026-04-25T00:36:55+07:00
- create_date: 2026-04-25
- create_dttm_source: filesystem_birthtime
- create_dttm_confidence: filesystem_proxy
- create_dttm_evidence: `plan_todo/finished/SOW_20261008_VO3LKN0L/creation-date-evidence.json` (record: SOW_20260425_VJ86J7C3)
- approve_dttm: unknown
- finish_dttm: unknown
- legacy_id: SOW_0018
- legacy_path: plan_todo/finished/SOW_0018_sow_delegate_flow_refinements.md
- migrated_dttm: 2026-10-08T12:48:51+07:00
- legacy_title: SOW: SowDelegateFlow Refinements

## Preserved Contract And Historical Evidence

- **Task**: Cập nhật skill `sow-delegate-flow` để thêm validation matrix theo loại SOW, termination policy ngắn gọn, và final review note template; đồng thời gom toàn bộ SOW liên quan tới skill vào `plan_todo/`.
- **Location**: `plan_todo/SOW_sow_delegate_flow_refinements.md`, `~/.codex/skills/sow-delegate-flow/SKILL.md`, `~/.codex/skills/sow-delegate-flow/references/claude-delegate-contract.md`, các file SOW liên quan dưới `plan_todo/finished/`
- **Why**: Giảm operator judgment, làm flow bớt ceremonial, và tách tài liệu refine skill khỏi tài liệu đặc thù project.
- **As-Is Diagram (ASCII)**:
```text
Multi-SOW plan
   |
   v
Delegate and review loop works
   |
   v
Validation depth and stop conditions still depend on operator judgment
```
- **To-Be Diagram (ASCII)**:
```text
Multi-SOW plan
   |
   v
Delegate and review loop works
   |
   +--> validation matrix suggests minimum check by SOW type
   |
   +--> termination policy limits repair/advice loops
   |
   +--> final review note gives a standard closeout shape
```
- **Deliverables**: Cập nhật ngắn gọn cho skill và reference contract; thư mục `plan_todo/finished/` chứa các SOW refinement của skill.
- **Done Criteria**: Skill vẫn ngắn gọn; có validation matrix hữu ích; có termination policy thực dụng; có final review note template; validator vẫn pass; SOW skill được dời khỏi `plan_todo/finished/`.
- **Out-of-Scope**: Không thêm sidecar memory rule; không thay đổi trigger multi-SOW plan; không tự động hóa exact command discovery cho mọi repo.
- **Proposed-By**: Codex GPT-5
- **plan**: `plan_todo/SOW_sow_delegate_flow_refinements.md`
- **Cautions / Risks**:
  - Validation matrix quá chi tiết sẽ làm skill phình ra.
  - Termination policy quá cứng có thể cắt ngắn một vòng repair đáng ra nên làm tiếp.
