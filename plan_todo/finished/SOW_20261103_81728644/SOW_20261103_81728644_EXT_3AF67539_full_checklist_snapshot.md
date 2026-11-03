# EXT 3AF67539 — Checklist đầy đủ ở mỗi mốc

- **Parent**: SOW_20261103_81728644
- **Status**: DONE
- **Approval**: approved by user
- **create_dttm**: 2026-11-03T10:58:53+07:00
- **approve_dttm**: 2026-11-03T10:58:53+07:00
- **finish_dttm**: 2026-11-03T11:01:35+07:00
- **Task / Why**: Sửa rule do SOW trước tạo ra: checklist bị chia mảnh, final đổi tên task khiến user phải ghép lịch sử.
- **Location**: Các skill/policy/feedback paths trong SOW gốc và bundle này.
- **Dependencies**: SOW gốc; giữ approval, verification và delegation.
- **Scope delta / Deliverables**: Snapshot đầy đủ ở mỗi mốc/final, giữ ID/tên, append mục mới; dùng Progress hiện có, không tạo store hay sửa chat cũ.

## As-Is / To-Be

```text
As-Is: checklist đầu -> update rời -> final đổi tên
To-Be: cùng checklist đầy đủ -> cập nhật trạng thái -> final cùng ID/tên
```

## Acceptance

- [x] A1: Skill, Progress reference và policy nhất quán; checklist đầy đủ ở mỗi mốc/final, không lặp mỗi tool call.
- [x] A2: Feedback case không còn bắt báo từng mảnh; giữ user Stop và scope gate.
- [x] A3: Validator + 21 tests theo SOW PASS; double-check không còn rule trái chiều.
- [x] A4: Scoped staging loại hunk Redmine; local commit, giữ dirty work khác; không sync/push.

## Out-of-Scope / Risks

- Không sync installed skills/project khác hoặc sửa renderer chat. Snapshot mới không thay tin cũ.
- Chỉ gửi snapshot tại mốc có thay đổi; test cấu trúc không chứng minh Agent tuân thủ.

## Progress

- **progress_updated_dttm**: 2026-11-03T11:01:35+07:00

| Item | Status | Evidence / Pending reason | Next action / Owner |
| --- | --- | --- | --- |
| T1: Rà hiện trạng, ghi phạm vi sửa | DONE | Đối chiếu screenshot, canonical rule và feedback; simple-main, sửa hẹp wording | Không còn |
| T2: Sửa skill/guardrail và feedback case | DONE | Full snapshot ở milestone/final, giữ ID/tên; case cập nhật trước skill | Không còn |
| T3: Kiểm chứng, double-check và commit | DONE | Validator + 21 tests PASS; double-check, whitespace và staged diff PASS | Không sync/push |

## Evidence

- `uv run python .../skill-creator/scripts/quick_validate.py skills/task-execution-flow`: PASS.
- `uv run python -m unittest tests.test_skill_feedback_cases tests.test_skill_sync_scripts tests.test_planning_bundle_contract`: 21 tests PASS.
- Double-check: bỏ rule changed-only trong skill/case và open-only cho execution checklist trong Progress reference. Policy/template thống nhất; giữ permission và user Stop. Không có finding còn mở.
- Đây là structural tests và scenario review, chưa phải independent model behavioral test; installed skills vẫn chưa sync.
