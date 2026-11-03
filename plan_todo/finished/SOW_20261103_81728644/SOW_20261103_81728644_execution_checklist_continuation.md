# SOW_20261103_81728644 — Checklist rõ ràng, tiếp tục làm đến khi xong

- **Status**: DONE
- **Approval**: approved by user
- **create_dttm**: 2026-11-03T10:36:56+07:00
- **approve_dttm**: 2026-11-03T10:43:18+07:00
- **finish_dttm**: 2026-11-03T11:01:35+07:00
- **Task**: Bổ sung checklist cập nhật theo tiến độ và quy tắc tiếp tục thực thi, không dừng chỉ để báo cáo.
- **Why**: User phải nhắc tiếp tục nhiều lần dù việc đã được duyệt còn dang dở; checklist cần cho thấy đang làm gì và còn gì.
- **Proposed-By**: Codex
- **Plan / Reference**: Standalone; kế thừa HITL Progress và SOW_20261102_14C42EC0, không thay thế journal hiện có.
- **Extensions**: 1. EXT_3AF67539 — DONE, full checklist snapshot; lần đóng trước: 2026-11-03T10:45:39+07:00, commit `44ac22a`.

## Location

- `skills/task-execution-flow/SKILL.md`: quy trình thực thi.
- `skills/task-router-flow/references/scope-of-work.md`: liên kết checklist với Progress hiện có.
- `TEMPLATE_AGENTS.md`: nguyên tắc dùng chung cho project.
- `AGENTS.md`: nguyên tắc tương ứng cho chính AISkills.
- `tests/skill_feedback_cases/task-execution-flow.json`: tình huống kiểm chứng.
- Bundle SOW này: tiến độ và evidence.

## As-Is Diagram (ASCII)

```text
Việc đã duyệt -> làm một phần -> báo tiến độ -> kết thúc lượt
                                              |
                                   user phải nhắc tiếp tục
```

Skill đã yêu cầu mini-task, verification và Progress/HITL, nhưng chưa bắt buộc checklist hiển thị và bước tiếp tục sau mỗi mục. Đây là thiếu sót quy trình; chưa chứng minh là nguyên nhân duy nhất khiến Agent dừng.

## To-Be Diagram (ASCII)

```text
Mục tiêu + checklist [ ] -> làm -> kiểm chứng -> [x] -> mục tiếp theo
                              |
                     phát sinh trong scope -> thêm [ ]
                              |
                     cần quyết định/blocker -> báo đúng việc bị chặn
```

## Contract

1. Với task nhiều bước, trước khi làm nêu mục tiêu ngắn và checklist `[ ]`. Task một bước không cần checklist hình thức.
2. Mỗi mục có ID ổn định. Chỉ đổi `[ ]` thành `[x]` khi đạt kiểm chứng của mục đó; đang làm/chờ verify vẫn `[ ]`, kèm trạng thái ngắn.
3. Việc phát sinh trong scope: thêm dòng mới rồi tiếp tục. Việc ngoài scope chỉ ghi đề xuất/chờ duyệt; thêm checklist không cấp quyền làm. Giữ các mục đã xong, không đánh lại số hoặc xóa lịch sử. Nếu evidence mất hiệu lực, mở lại đúng mục và ghi lý do.
4. Dùng Progress hiện có làm nguồn trạng thái. Khi bắt đầu, tại mốc tiến độ và khi kết thúc, hiện toàn bộ checklist cùng ID/tên; chỉ đổi trạng thái hoặc thêm mục mới. Không gửi từng mảnh buộc user ghép lịch sử; không lặp mỗi tool call. Task miễn SOW chỉ theo dõi trong chat.
5. Sau mỗi mục hoặc finding trong scope, làm tiếp việc an toàn kế tiếp. Commentary, mini-task PASS hoặc kết quả delegate không tự thành điểm kết thúc lượt.
6. Chỉ dừng khi hoàn tất phạm vi yêu cầu hiện tại, user yêu cầu, hết khả năng công cụ thực tế, hoặc có blocker/decision cần bên ngoài. Nêu evidence, việc bị chặn và điều cần giải quyết; tiếp tục phần độc lập còn làm được. Không hỏi lại quyền đã có, không retry vô hạn. Yêu cầu chỉ review/tạo SOW kết thúc ở bàn giao đó, không tự triển khai.
7. `TEMPLATE_AGENTS.md` và `AGENTS.md` chỉ giữ nguyên tắc ngắn về checklist và tiếp tục trong scope; chi tiết nằm trong skill. Không sao chép cả workflow sang policy.

## Deliverables

- Sửa tại điểm bắt đầu, sau mini-task và trước handoff; làm rõ câu hiện tại nói skill không quản lý progress format.
- Làm rõ Hard Gates: `implemented but not fully verified` là trạng thái chưa xong, không phải lệnh kết thúc lượt khi còn kiểm chứng hoặc sửa lỗi an toàn có thể làm tiếp.
- Thêm feedback case đã khử thông tin riêng tư trước khi sửa skill; dùng `skill-creator` cho thay đổi canonical.
- Giữ nguyên approval, verification, delegation, an toàn Git và quyền user dừng.

## Done Criteria

- [x] DC1: Policy ngắn; skill mô tả checklist, cập nhật và tiếp tục, không trùng toàn bộ quy trình.
- [x] DC2: Progress/checklist dùng cùng ID và evidence; không thay thế contract project hay tạo thêm state store.
- [x] DC3: Scenario review bao phủ làm tiếp sau PASS/finding và khi còn verification khả thi; việc phát sinh trong/ngoài scope; evidence bị vô hiệu; task một bước; user stop; blocker một phần; scope chưa duyệt; giới hạn công cụ.
- [x] DC4: Validator của `skill-creator` và `uv run python -m unittest tests.test_skill_feedback_cases tests.test_skill_sync_scripts tests.test_planning_bundle_contract` PASS.
- [x] DC5: Phân biệt test cấu trúc/scenario review với hành vi Agent thật; không tuyên bố chữa dứt điểm nếu chưa có behavioral evidence.
- [x] DC6: Review diff, chỉ commit thay đổi thuộc SOW sau verification; giữ nguyên dirty work khác, không push.

## Out-of-Scope

- Không sửa project khác hoặc installed skills; không sync/deploy khi chưa chọn và duyệt target.
- Không đổi model/delegation, thêm telemetry, timer, dịch vụ hoặc cơ chế tự chạy ngoài lượt.
- Không bỏ approval, điều kiện an toàn hay ép hoàn thành khi evidence chưa đủ.

## Cautions / Risks

- Checklist không bảo đảm Agent tuân thủ. Quy tắc phải đặt ở điểm quyết định làm tiếp, không chỉ tăng chữ MUST.
- Skill execution và router reference đang có thay đổi chưa commit; đọc lại và sửa đúng hunk, không ghi đè/gộp phần khác.
- Checklist user thấy là cách trình bày Progress, không phải workflow/state machine thứ hai.

## Review hiện tại

- EXT_3AF67539 thay rule chỉ báo phần thay đổi bằng snapshot đầy đủ; các ranh giới miễn SOW, approval và verification giữ nguyên.
- Đã đối chiếu canonical execution skill, HITL Progress, policy template và journal contract; không đổi approval hoặc tạo state store thứ hai. Hành vi Agent sau sửa chưa được kiểm chứng.

## Progress

- **progress_updated_dttm**: 2026-11-03T11:01:35+07:00

| Item | Status | Evidence / Pending reason | Next action / Owner |
| --- | --- | --- | --- |
| T1: Khảo sát và tạo SOW | DONE | Đã đọc policy, canonical skill, Progress contract và journal SOW cũ | Không còn |
| T2: Self-review và review cuối | DONE | Đã sửa các điểm dễ hiểu sai; user đã duyệt | Không còn |
| T3: Implement và verify | DONE | Canonical skill/policy đã sửa; validator và 21 tests PASS | Không còn |
| T4: Double-check và scoped delivery | DONE | Đã sửa điểm dễ hiểu sai về user Stop; commit riêng hunk thuộc SOW, giữ nguyên Redmine | Không còn; không sync/push |
| EXT_3AF67539 | DONE | Full snapshot rule và case đã sửa; validator + 21 tests PASS, double-check | Không còn; xem EXT |

## Verification / Delivery

- `skill-creator/scripts/quick_validate.py skills/task-execution-flow`: PASS.
- `uv run python -m unittest tests.test_skill_feedback_cases tests.test_skill_sync_scripts tests.test_planning_bundle_contract`: 21 tests PASS.
- Case `execution-checklist-continuation-001`: expected/negative/boundary đã review; đây là fixture/scenario coverage, không phải model behavioral test.
- Double-check một lần: policy và skill phân biệt partial blocker với user Stop; không có scope bypass hay state store mới. Kiểm tra whitespace PASS.
- Fetch/compare: main đồng bộ `origin/main` trước commit; chỉ stage hunk thuộc SOW, giữ nguyên Redmine và dirty work khác.
- Chỉ thay canonical source; chưa sync installed skills/project khác. Chưa chứng minh Agent thực tế hết dừng sớm.
