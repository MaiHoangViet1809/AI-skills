# SOW: Sow Delegate Flow Output Filtering

- **Task**: Cập nhật `sow-delegate-flow` để tách output filtering thành reference file riêng có ví dụ, làm rõ rằng `json` là mode mặc định đồng thời output filtering là bắt buộc mặc định: phải lọc bỏ `system`-typed messages khỏi captured output trừ khi flow hoặc user yêu cầu giữ lại, và bổ sung code samples shell cụ thể để operator không phải tự đoán cách filter.
- **Location**: `plan_todo/skills_sow/SOW_sow_delegate_flow_output_filtering.md`, `/Users/maihoangviet/.codex/skills/sow-delegate-flow/SKILL.md`, `/Users/maihoangviet/.codex/skills/sow-delegate-flow/references/claude-delegate-contract.md`, reference file mới trong `references/`
- **Why**: Cụm “filter captured system noise” hiện quá chung chung. Cần mô tả riêng, có ví dụ, và chốt rõ cách hiểu `json default` để giảm operator ambiguity và context waste.
- **As-Is Diagram (ASCII)**:
```text
Delegate output
   |
   v
json-first policy exists
   |
   v
Filtering guidance is still generic
```
- **To-Be Diagram (ASCII)**:
```text
Delegate output
   |
   +--> json default
   |      keep useful final result
   |      drop system-typed message noise by default
   |
   +--> stream-json debug
          keep only useful events
          drop system noise by explicit filter examples
```
- **Deliverables**: Cập nhật `SKILL.md`; cập nhật contract reference; thêm reference file riêng mô tả output filtering với ví dụ cụ thể và code samples shell.
- **Done Criteria**: Skill vẫn ngắn gọn; filtering logic không còn chung chung; có reference riêng với examples; `json` default được giải thích rõ; output filtering là default bắt buộc trừ khi flow hoặc user yêu cầu khác; có code samples shell cho `json` và `stream-json`; validator vẫn pass.
- **Out-of-Scope**: Không đổi trigger của skill; không thêm wrapper script; không đổi runtime environment của Claude.
- **Proposed-By**: Codex GPT-5
- **plan**: `plan_todo/skills_sow/SOW_sow_delegate_flow_output_filtering.md`
- **Cautions / Risks**:
  - Nếu mô tả filtering quá dài sẽ làm reference phình ra.
  - Nếu ví dụ không đủ rõ thì operator vẫn có thể capture sai output.
