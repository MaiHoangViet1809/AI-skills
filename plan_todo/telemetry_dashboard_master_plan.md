# Telemetry Dashboard Master Plan

## Goal

Build a local telemetry dashboard that boots from one script on port `9999`, uses `Vue 3 + Vite` for the frontend, uses Python + Polars for the backend/data layer, and visualizes the Codex and Claude run metrics already captured in this repo.

This document is the plan-level source of truth for the dashboard effort. Implementation should be split into at most 4 SOWs so the work can be delegated in smaller, safer chunks.

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

Keep the work in 4 SOWs maximum.

### SOW_0021_dashboard_data_backend.md

Focus:

- create dashboard backend package or scripts
- implement Polars loader for telemetry run records
- enrich runs from Claude raw logs and Codex rollout only where needed
- define API response shapes for summary, runs list, run detail, and charts

Why grouped:

- this is one coherent data and API slice
- it can be delegated independently with low UI coupling

Good Claude delegate candidate:

- yes

### SOW_0022_dashboard_frontend_shell.md

Focus:

- scaffold Vue 3 + Vite frontend
- establish dashboard layout shell
- implement top summary cards row
- implement global time window and filter state
- connect frontend to backend summary and runs endpoints

Why grouped:

- this is the stable UI shell and state-management slice
- can move in parallel once API contract is known

Good Claude delegate candidate:

- yes

### SOW_0023_dashboard_charts_and_detail.md

Focus:

- implement activity chart
- implement task duration chart
- implement runs table
- implement run detail panel or drawer
- wire tokens, duration, tool counts, and status fields into visual components

Why grouped:

- charts and detail views depend on the frontend shell
- still one cohesive visualization slice

Good Claude delegate candidate:

- yes

### SOW_0024_dashboard_boot_and_finish.md

Focus:

- implement one-command boot flow on port `9999`
- serve built frontend and API from one port
- add local docs for running the dashboard
- perform end-to-end smoke test against real telemetry data in this repo

Why grouped:

- boot, packaging, and final integration belong together
- this is the risky last-mile slice and should stay narrow

Good Claude delegate candidate:

- maybe
- use Claude for implementation if the prior 3 SOWs are stable
- keep final verification and acceptance in Codex

## Delegation Strategy

- Prefer delegating `SOW_0021`, `SOW_0022`, and `SOW_0023` separately
- Keep `SOW_0024` smaller and review-heavy
- Do not delegate all 4 at once unless API and UI contracts are already frozen
- Recommended sequence:
  1. `SOW_0021`
  2. `SOW_0022`
  3. `SOW_0023`
  4. `SOW_0024`

## Acceptance Criteria For The Whole Plan

- one script boots the dashboard at `http://localhost:9999`
- dashboard renders summary cards, 2 charts, runs table, and run detail
- metrics shown come from the current telemetry system, not hardcoded fixtures
- Codex metrics use task-local tokens, not accumulated session-gross values
- Claude and Codex tool/MCP metrics are visible somewhere in the detail view
- dashboard works against current local telemetry files without requiring a DB

## Risks

- direct log reads may become slow if local history grows a lot
- rollout enrichment may be expensive if run matching is too broad
- serving Vue build from one Python process needs a clean dev/prod story
- chart design can sprawl if the bottom section is not kept tight in v1
