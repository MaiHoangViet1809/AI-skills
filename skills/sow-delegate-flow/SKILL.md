---
name: sow-delegate-flow
description: Use when a task is being executed as a plan with multiple sequential SOWs. Keep each approved SOW as the source of truth, delegate implementation to Claude Code CLI by SOW path, and manage cost by resuming only short, clean delegate sessions while compacting long ones into a fresh session. Handle review, advice, repair feedback, and local fallback when Claude fails, hits limits, or drifts outside scope.
---

# Sow Delegate Flow

Use this skill for multi-SOW plans that run as Codex -> SOW -> approval -> Claude -> review -> feedback/advice -> fallback.

## Precedence

- `AGENTS.md` and repo rules define process constraints and guardrails.
- The approved SOW defines the active task scope and deliverables.
- `CLAUDE.md` adds Claude-specific helper context but does not override repo rules or the approved SOW.

## Rules

- Keep the approved SOW as the source of truth for the current implementation.
- Do not delegate before approval.
- Track `session_id` from CLI output, not from model text.
- Delegate with `sow_path`, short intent, write scope, and structured output.
- Tell Claude to read the SOW file itself.
- Read local repo rules first, especially `AGENTS.md` and `CLAUDE.md`.
- Review changed files and run one relevant local check.
- If Claude asks a good question, answer it and continue.
- If Claude says done but validation fails, send repair feedback and continue.
- Resume only when the current delegate session is still short and clean.
- If the current delegate session is long or noisy, read its transcript, compact the useful history, and continue in a fresh session.
- Take over locally if Claude fails, drifts, or the CLI output shows usage or rate-limit blocking.
- Use `json` output by default.
- Switch to `stream-json` only when you need deeper delegate debugging because the delegate output is poor, abnormal, or blocked in a way that needs event-level inspection.
- Capture Claude output to a raw log file first, then parse it on demand and read the parser output by default.
- Open the raw log only when the parser reports an anomaly or the flow explicitly needs deep debugging.
- If `telemetry-flow` is available, start a telemetry run before the first delegate call and finish it once the workflow reaches a terminal outcome.

## Flow

1. Read workspace rules.
2. Create or update the SOW.
3. Wait for approval.
4. If run telemetry is needed, start a `telemetry-flow` run and keep the `run_id`.
5. Start a delegate session or decide whether to resume the current one.
6. Delegate by SOW path, not by pasting the full SOW.
7. Write raw delegate output to `logs_session_ai_agent/`, parse it with the helper script, and read the parser output.
8. If Claude returns `needs_advice`, answer and continue in the current or a refreshed session.
9. If Claude returns done, review files and validate.
10. If validation fails, send feedback and continue in the current or a refreshed session.
11. Once the workflow reaches a terminal outcome, finish the telemetry run before closeout or commit.
12. If validation passes, close the SOW.
13. Drop the session from active state when the plan has no active SOW left.

## Validation Matrix

Use repo-specific commands when available. Otherwise apply these minimum checks:

- `docs-only`: `git diff --check` plus one focused cross-reference or grep check
- `frontend`: targeted build, test, or route/component check for the touched surface
- `backend`: targeted module test or `uv run pytest ...` for the changed area
- `migration`: backward-compat check plus one scan for legacy markers or old paths

## Termination Policy

- `quality`: allow up to 2 repair rounds, then finish locally or stop
- `infra`: if scope is already clear, finish locally instead of waiting on delegate recovery
- `uncertainty`: answer once; if the task is still ambiguous, stop and escalate
- `rate-limit`: if the partial diff is usable and scope is clear, finish locally

See [claude-delegate-contract.md](references/claude-delegate-contract.md) for the prompt shape, result contract, transcript compaction, validation guidance, termination policy, and limit handling.

See [output-filtering.md](references/output-filtering.md) for the mandatory default filtering policy for captured delegate output.

See [log-parsing.md](references/log-parsing.md) for the raw-log-first capture flow, parser contract, and parser output shape.

See [../telemetry-flow/references/hook-contract.md](../telemetry-flow/references/hook-contract.md) for the start/finish telemetry hook contract used around delegate runs.

## Defaults

- Prefer the user's normal Claude profile when known.
- Default to `--model sonnet --effort medium` when no override exists.
- Use `json` as the default output mode.
- Use `stream-json` only for delegate debugging.
- Filter captured output by default, dropping `system`-typed noise unless the flow or user explicitly requires it.
- Use parser output as the normal read path. Open raw logs only on anomaly or explicit deep-debug flows.
- Use CLI output or events to detect limit hits after submit. Do not assume percentage prechecks are available.
- Poll or re-check long-running delegate calls at roughly 30 second intervals by default.
- Prefer a fresh session over resuming a long, noisy one.
- If repo rules are missing, keep scope narrow and verify locally before closing.
