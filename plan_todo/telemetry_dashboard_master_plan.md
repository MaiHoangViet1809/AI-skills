# Telemetry Dashboard Master Plan

## Goal

Build a local telemetry dashboard that boots from one script on port `9999`, uses `Vue 3 + Vite` for the frontend, uses Python + Polars for the backend/data layer, and visualizes the Codex and Claude run metrics already captured in this repo.

This document is the plan-level source of truth for the dashboard effort. Implementation should be split into 6 SOWs so each delegate slice stays narrow and reviewable.

## Current Inputs

- Telemetry run records are written under `logs_session_ai_agent/telemetry-run-<run_id>.json`
- Claude raw logs are written under `logs_session_ai_agent/claude-<session-id>.log`
- Codex rollout history is available under `~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl`
- Existing parsers already expose:
  - Codex task-local token metrics
  - Claude token and duration metrics
  - Codex and Claude tool/MCP counts
  - workflow outcome fields such as validation, fallback, repair, and scope

## Final Product Shape

- One script boots the dashboard on `http://localhost:9999`
- Backend serves API and built frontend from the same port
- Backend reads local telemetry data directly with Polars
- Frontend layout v1:
  - top row: 4-6 summary cards
  - second row:
    - left: activity chart in GitHub-like frequency style for the last 12h
    - right: task duration chart for the last 12h, with Codex and Claude token values visible per task
  - lower section:
    - run table
    - detail panel or drawer for a selected run

## Data Model For Dashboard V1

The dashboard dataset should normalize each run to one row with at least:

- identity:
  - `run_id`
  - `skill`
  - `plan`
  - `sow`
  - `task_type`
- timing:
  - `started_at`
  - `finished_at`
  - `run_duration_ms`
  - `time_to_first_usable_result_ms`
- codex:
  - `codex_session_id`
  - `codex_task_tokens`
  - `codex_cached_input_tokens`
  - `codex_fresh_input_tokens`
  - `codex_output_tokens`
  - `codex_reasoning_output_tokens`
  - `codex_turn_count`
  - `codex_avg_tokens_per_turn`
  - `codex_tool_call_count`
  - `codex_mcp_call_count`
- claude:
  - `claude_session_id`
  - `claude_total_tokens`
  - `claude_input_tokens`
  - `claude_output_tokens`
  - `claude_cache_creation_tokens`
  - `claude_cache_read_tokens`
  - `claude_duration_ms`
  - `claude_tool_call_count`
  - `claude_mcp_call_count`
- workflow:
  - `files_changed_count`
  - `repair_rounds`
  - `fallback_flag`
  - `validation_pass`
  - `success_state`
  - `scope_respected`
  - `outcome`
- derived:
  - `delegate_ratio`
  - `codex_to_claude_ratio`

## Backend And Boot Strategy

- Use Python for the dashboard server and boot script
- Use Polars for file scanning, transformation, window filtering, and summary aggregation
- Use one boot script only, for example:
  - `uv run python scripts/dashboard/run_dashboard.py`
- In v1, serve frontend static assets and API from one backend process on `:9999`
- Do not add SQLite in v1
- Do not add a separate reporting pipeline before the dashboard
- Dashboard reads local logs directly and normalizes them in memory on startup

## Frontend Layout V1

### Top Row

Show 4-6 cards for the selected window, default `12h`:

- total runs
- accepted runs or acceptance rate
- total Codex task tokens
- total Claude tokens
- average run duration
- total tool calls or fallback count

### Middle Row

Left chart:

- activity chart for the last `12h`
- visual language can resemble GitHub contribution frequency
- each bucket shows number of runs started in the bucket

Right chart:

- task duration chart for the last `12h`
- each task is one bar
- bars are ordered by start time
- tooltip includes:
  - `run_id`
  - `skill`
  - `sow`
  - `run_duration_ms`
  - `codex_task_tokens`
  - `claude_total_tokens`
  - `success_state`

### Bottom Section

V1 should include:

- a runs table with filters
- a detail panel or drawer for the selected run

The table should support at least:

- filter by time window
- filter by `skill`
- filter by `success_state`
- filter by `task_type`

## SOW Breakdown

### SOW_0021_dashboard_loader_and_schema.md

Focus:

- create `scripts/dashboard/` package skeleton
- load telemetry run JSON files with Polars
- normalize one-row-per-run dataset
- define shared backend schema/helpers

Why grouped:

- smallest stable data slice
- lowest-risk delegate start point

Good Claude delegate candidate:

- yes

### SOW_0022_dashboard_backend_summary_api.md

Focus:

- add backend app entry
- implement summary endpoint
- implement runs list endpoint
- add window and basic filter support

Why grouped:

- depends on loader
- still narrow and API-only

Good Claude delegate candidate:

- yes

### SOW_0023_dashboard_backend_detail_and_charts_api.md

Focus:

- implement run detail endpoint
- implement activity chart endpoint
- implement duration chart endpoint
- add any lightweight enrich/derived metrics needed by those endpoints

Why grouped:

- keeps chart/detail contracts together
- depends on prior API/data slices

Good Claude delegate candidate:

- yes

### SOW_0024_dashboard_frontend_shell.md

Focus:

- scaffold Vue 3 + Vite frontend
- establish dashboard shell layout
- add top summary cards row
- add shared filter and time-window state

Why grouped:

- clean UI shell slice
- minimal chart complexity

Good Claude delegate candidate:

- yes

### SOW_0025_dashboard_frontend_visuals.md

Focus:

- implement activity chart
- implement duration chart
- implement runs table
- implement run detail panel or drawer

Why grouped:

- visual layer depends on stable API and shell
- still one coherent frontend slice

Good Claude delegate candidate:

- yes

### SOW_0026_dashboard_boot_and_smoke.md

Focus:

- implement one-command boot flow on port `9999`
- serve built frontend and API from one port
- add local docs for running the dashboard
- run end-to-end smoke test against repo telemetry data

Why grouped:

- last-mile integration and acceptance belong together

Good Claude delegate candidate:

- maybe
- prefer Codex-led verification even if Claude helps with implementation

## Execution Order

1. `SOW_0021`
2. `SOW_0022`
3. `SOW_0023`
4. `SOW_0024`
5. `SOW_0025`
6. `SOW_0026`

## Delegate Notes

- Prefer delegating one SOW at a time
- Keep each delegate prompt short and let Claude read the SOW file itself
- If Claude appears to compact or stall after one narrow prompt, treat that as delegate/runtime instability rather than a signal to widen scope
- Favor fresh delegate sessions over resuming noisy ones

## Done Criteria For Whole Plan

- one script boots the dashboard at `http://localhost:9999`
- dashboard renders summary cards, 2 charts, runs table, and run detail
- dashboard reads current local telemetry logs directly with Polars
- dashboard works against current local telemetry files without requiring a DB
