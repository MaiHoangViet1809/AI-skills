# SOW: Code Context Benchmark

- **Task**: Benchmark ba phương án lấy code context cho workflow agentic coding trên cùng một prompt truy vấn: native tool, `cocoindex-code`, và `cased/kit`.
- **Location**: `plan_todo/SOW_code_context_benchmark.md`, file kết quả benchmark trong `plan_todo/`
- **Why**: Xác định phương án nào cho ra context hữu ích nhất với chi phí thấp nhất trước khi cân nhắc tích hợp vào workflow `sow-delegate-flow`.
- **As-Is Diagram (ASCII)**:
```text
Need code context
   |
   v
Unclear whether native search or indexing tools are better
   |
   v
Decision would be based on anecdotes
```
- **To-Be Diagram (ASCII)**:
```text
One benchmark prompt
   |
   +--> native tool
   +--> cocoindex-code
   +--> cased/kit
   |
   v
Compare outputs with same rubric
   |
   v
Choose the best workflow fit
```
- **Deliverables**: Một benchmark report trong `plan_todo/` so sánh 3 phương án; rubric chấm rõ ràng; kết luận có nên dùng công cụ ngoài native tool hay không.
- **Done Criteria**: Cùng một prompt được chạy qua cả 3 phương án; đo được ít nhất các metric `files_returned`, `latency`, `raw_output_tokens`, `usable_output_tokens`; tôi chấm thêm `file_quality`, `detail_quality`, `next_step_readiness`, `follow_up_read_cost` theo rubric 1-5; có recommendation cuối cùng.
- **Out-of-Scope**: Không tích hợp tool thắng cuộc vào skill ngay; không benchmark nhiều prompt; không tối ưu production setup.
- **Proposed-By**: Codex GPT-5
- **plan**: `plan_todo/SOW_code_context_benchmark.md`
- **Cautions / Risks**:
  - Chấm quality vẫn có yếu tố chủ quan, nên phải giữ rubric cố định.
  - Tool setup friction có thể ảnh hưởng latency nhưng vẫn là dữ liệu hữu ích.
  - Một prompt duy nhất không phản ánh mọi loại truy vấn, nên kết luận chỉ nên ở mức thực dụng, không tuyệt đối.
