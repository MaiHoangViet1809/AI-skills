---
name: telemetry-flow
description: Use when you need run-level telemetry around an execution workflow. Start a telemetry run before execution to create a run record and markers, then finish it after execution to parse Codex rollout and Claude raw logs into one normalized metrics summary.
---

# Telemetry Flow

Use this skill to capture calculable run-level telemetry without mixing reporting into the execution skill itself.

## Rules

- Use exactly two hooks: `start` before execution and `finish` after execution.
- Use the staging record as the source of truth for run identity.
- Use marker text only as a cross-check and debug aid.
- Capture only metrics that can be parsed or calculated from logs and workflow metadata.
- Finish the telemetry run before commit so `files_changed_count` can be computed from the current worktree.

## Flow

1. Run the `start` hook with `skill`, `plan`, `sow`, `intent`, and `task_type`.
2. Keep the returned `run_id` and staging path for the rest of the workflow.
3. If stronger Codex-side correlation is needed, emit the returned start marker as a short commentary line.
4. Run the actual workflow.
5. Run the `finish` hook with the `run_id`, Claude raw log paths, and workflow outcome metadata.
6. If a finish marker is being used, emit it around closeout so rollout parsing can cross-check the run window.

## Global Hook Contract

Codex hooks may trigger telemetry around an isolated skill session automatically.

Rules:
- treat the isolated skill session as the telemetry boundary
- let global Codex hooks own that boundary, with `SessionStart` anchoring time and `Stop` reading the session transcript to hydrate skill metadata
- resolve the current project from the session `cwd`
- keep `sow-delegate-flow` on the existing explicit `start/finish` path unless it is intentionally run as its own skill session
- the isolated skill session should return a brief summary back to the parent or main session

## Metrics

The finish hook should return:

- Codex task-local token usage from rollout history
- Claude totals from raw delegate logs
- Codex and Claude tool or MCP call counts from event-level logs
- run-level duration and first usable result timing
- workflow outcome metadata such as validation, repairs, fallback, and scope
- per-task ratios and turn metrics that are purely arithmetic on captured metrics

See [hook-contract.md](references/hook-contract.md) for the command shape, staging record fields, marker format, metric definitions, and normalized output.
