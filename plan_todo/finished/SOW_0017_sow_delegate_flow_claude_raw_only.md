# SOW: Sow Delegate Flow Claude Raw-Only Parser

- **Task**: Đồng bộ flow Claude parser với triết lý raw-only: chỉ giữ raw log `claude-<session-id>.log`, không persist parsed artifact hoặc usage ledger, và parse on demand bằng Python khi cần.
- **Location**: `plan_todo/skills_sow/SOW_sow_delegate_flow_claude_raw_only.md`, `/Users/maihoangviet/.codex/skills/sow-delegate-flow/SKILL.md`, `/Users/maihoangviet/.codex/skills/sow-delegate-flow/references/claude-delegate-contract.md`, `/Users/maihoangviet/.codex/skills/sow-delegate-flow/references/log-parsing.md`, `/Users/maihoangviet/.codex/skills/sow-delegate-flow/scripts/parse_delegate_log.py`
- **Why**: Parser Claude hiện đang ghi thêm parsed artifact và usage ledger, trong khi raw file đã đủ làm source of truth và Python parse dưới 1 giây. Giữ thêm artifact chỉ làm tăng số file, tăng độ phức tạp, và lệch khỏi hướng rollout/raw-first hiện tại của Codex.
- **As-Is Diagram (ASCII)**:
```text
Claude raw log
   |
   v
Python parser
   |
   +--> parsed artifact file
   +--> usage ledger file
   |
   v
Coordinator reads derived files
```
- **To-Be Diagram (ASCII)**:
```text
Claude raw log
   |
   v
Python parser (on demand)
   |
   v
Print compact summary to stdout
```
- **Deliverables**:
  - Update `sow-delegate-flow` docs to make Claude raw logs the only persisted source
  - Refactor `parse_delegate_log.py` to parse and print only, without writing parsed artifact or ledger
  - Remove references to persisted parsed Claude artifacts from skill docs
- **Done Criteria**:
  - Claude side keeps only raw log files
  - Parser prints compact summary on demand
  - No parsed Claude artifact file is written by default
  - No Claude usage ledger file is written by default
  - Skill docs match the raw-only behavior
- **Out-of-Scope**:
  - Reworking Codex rollout parser
  - Deleting historical Claude parsed files automatically
- **Proposed-By**: Codex GPT-5
- **plan**: `plan_todo/skills_sow/SOW_sow_delegate_flow_claude_raw_only.md`
- **Cautions / Risks**:
  - Parser output still needs to stay compact enough that reading it remains cheaper than opening the raw log.
  - Historical parsed Claude artifacts may still exist on disk until removed manually.
