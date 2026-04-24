# SOW: Global Telemetry Ledger

- **Task**: Add a global telemetry ledger at `~/.logs/codex/telemetry/runs/`, write run summaries there from the telemetry hook, backfill existing project-local run summaries from `~/Projects/*/logs_session_ai_agent/`, and make the dashboard read only from the global ledger.
- **Location**: `~/Projects/AISkills/plan_todo/SOW_0031_global_telemetry_ledger.md`, `~/Projects/AISkills/skills/telemetry-flow/scripts/telemetry_hook.py`, `~/Projects/AISkills/scripts/dashboard/**`, `~/Projects/AISkills/scripts/telemetry/**`, `~/.logs/codex/telemetry/runs/`
- **Why**: Cross-project tracking needs one shared source of truth; repo-local telemetry files are not enough for total usage tracking.
- **As-Is Diagram (ASCII)**:
```text
repo-local telemetry files
   |
   v
dashboard sees one repo at a time
```
- **To-Be Diagram (ASCII)**:
```text
repo-local telemetry summary
   |
   v
~/.logs/codex/telemetry/runs/
   |
   v
dashboard reads only global ledger
```
- **Deliverables**:
  - global run ledger directory
  - telemetry hook write-to-global behavior
  - backfill script for `~/Projects/*/logs_session_ai_agent/telemetry-run-*.json`
  - dashboard loader updated to global-only
- **Done Criteria**:
  - new runs are written to the global ledger
  - backfill collects existing runs into the global ledger
  - dashboard still works after removing project-local telemetry summaries
- **Out-of-Scope**:
  - database storage
  - cloud sync
- **Proposed-By**: Codex GPT-5
- **plan**: `global telemetry ledger`
- **Cautions / Risks**:
  - filenames must avoid collisions across projects
  - backfill should be idempotent
