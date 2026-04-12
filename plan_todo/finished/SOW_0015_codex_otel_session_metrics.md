# SOW: Codex OTel Session Metrics

- **Task**: Thiết lập đo usage của Codex qua OpenTelemetry theo cấp session, có timestamp, để về sau tổng hợp hiệu quả theo task/SOW và đánh giá impact của skill usage theo thời gian.
- **Location**: `plan_todo/SOW_codex_otel_session_metrics.md`, `~/.codex/config.toml`, file config OpenTelemetry Collector local, thư mục log/ledger local nếu cần dưới repo
- **Why**: Hiện chỉ có Claude usage được đo tương đối chính xác. Cần thêm session-level metrics cho Codex để so sánh cost và đánh giá hiệu quả của workflow/skills theo thời gian, nhưng không cần đo quá chi tiết từng event trong normal path.
- **As-Is Diagram (ASCII)**:
```text
Codex session
   |
   v
No local token ledger for Codex
   |
   v
Cannot compare task/SOW efficiency over time
```
- **To-Be Diagram (ASCII)**:
```text
Codex session
   |
   v
OTel export -> local collector
   |
   v
Capture response.completed token usage
   |
   v
Write session-level log/ledger with timestamp
   |
   v
Later aggregate by task/SOW to evaluate skill efficiency over time
```
- **Deliverables**:
  - Local OpenTelemetry Collector config for Codex logs
  - `~/.codex/config.toml` updated with `[otel]`
  - One tested path that captures `codex.sse_event` / `response.completed`
  - A session-level Codex ledger shape with timestamp
  - Clear note that Codex metrics are recorded per session first, then mapped to task/SOW analytically later
- **Done Criteria**:
  - Collector runs locally and accepts Codex logs
  - Codex emits telemetry locally after config update
  - At least one `response.completed` event is captured and inspected
  - Session-level token fields and timestamp are recorded in a compact local artifact
  - The design avoids over-collecting noisy event data for the normal path
- **Out-of-Scope**:
  - Historical backfill of old Codex sessions
  - Full cross-agent analytics dashboard
  - Perfect automatic task/SOW attribution for all past/future work
- **Proposed-By**: Codex GPT-5
- **plan**: `plan_todo/SOW_codex_otel_session_metrics.md`
- **Cautions / Risks**:
  - Codex OTel config may require a new session or app restart before logs appear reliably.
  - Session-level metrics are the source metric; mapping to task/SOW will be a later aggregation layer.
  - Normal-path logging should stay compact so measurement itself does not create unnecessary noise.

## Measurement Rules

- Codex should be measured at the **session** level first.
- Each recorded session metric must include a timestamp.
- The normal artifact should keep only the token fields needed to evaluate session cost/efficiency.
- Task-level or SOW-level efficiency should be computed later from session logs plus task metadata, not by forcing every Codex event into the normal read path.

## Minimum Fields To Capture

- `session_id` if exposed
- event type / completion marker proving the response completed
- timestamp
- model
- reasoning effort if exposed
- workspace / project identity
- input tokens
- output tokens
- total tokens if exposed
- any cost field if exposed
- duration or enough timing data to derive duration

## Skill Marker Requirement

The design should also evaluate a grep-friendly way to mark skill execution windows inside Codex logs so later measurement can isolate the segment related to a specific skill and SOW.

Preferred marker shape:

- `--- START SKILL <SKILL-NAME> FOR SOW <SOW-ID> ---`
- `--- FINISH SKILL <SKILL-NAME> FOR SOW <SOW-ID> ---`

The implementation should prefer the least noisy mechanism that still produces a stable marker in telemetry or local logs. If explicit assistant-text markers would pollute the user-facing conversation too much, propose or implement the cleanest alternative that still supports later filtering and performance analysis.

## Follow-On Use

These session metrics are intended to answer:

- average Codex cost per task
- average Codex cost per SOW
- before/after comparisons when a skill is introduced or refined
- whether a workflow reduces average coordinator token usage over time
