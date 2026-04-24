# Claude Delegate Contract

## Prompt Template

```text
You are working in <workspace>.

Read this approved SOW:
- <absolute_sow_path>

Intent:
- <one short sentence>

Write scope:
- <absolute file or directory path>

Rules:
- Implement only the approved SOW.
- Do not modify files outside the write scope.
- Read the SOW file for details.
- Return structured output only.
```

## Session Policy

- Start a fresh session for a new delegate thread.
- Resume only while the current delegate session is still short and clean.
- If the session gets long or noisy, compact the useful history and continue in a fresh session.
- Use `--name` only as a debug aid.
- Treat CLI `session_id` as the source of truth.
- Do not use transcript line count as the main threshold; transcript files include system events.

## Transcript Compaction

When refreshing a session, read the transcript and carry forward only the state Claude still needs:

```text
Previous delegate summary:
- SOW: <path>
- Goal: <one line>
- Done: <2-4 bullets>
- Remaining: <2-4 bullets>
- Constraints: <1-3 bullets>
- Advice or feedback: <1-3 bullets>
```

Then start a fresh session with:
- the same SOW path
- the compact summary
- the latest advice or repair feedback
- the write scope

## CLI Shape

Use `stream-json` by default so the coordinator can parse progress from the raw log while Claude is still running.

Capture raw CLI output to a file first, then parse it on demand before the coordinator reads it.

```bash
tmp_log="$HOME/.logs/codex/telemetry/claude/<project>/claude-$(date +%s)-tmp.log"
claude -p \
  --output-format stream-json \
  --json-schema '<schema-json>' \
  --model sonnet \
  --effort medium \
  --permission-mode bypassPermissions \
  "<prompt>" > "$tmp_log"

python ~/.codex/skills/sow-delegate-flow/scripts/parse_delegate_log.py \
  --raw-log "$tmp_log" \
  --mode stream-json \
  --repo-root "$REPO"
```

Normal polling:

- let Claude run
- re-check the parsed log summary at the configured poll interval
- use parsed progress, not raw file size, as the signal
- stay in the coordinator loop until a real decision point appears

Follow-up turns:

```bash
tmp_log="$HOME/.logs/codex/telemetry/claude/<project>/claude-$(date +%s)-tmp.log"
claude -p \
  --resume <session-id> \
  --output-format stream-json \
  --json-schema '<schema-json>' \
  "<prompt>" > "$tmp_log"

python ~/.codex/skills/sow-delegate-flow/scripts/parse_delegate_log.py \
  --raw-log "$tmp_log" \
  --mode stream-json \
  --repo-root "$REPO"
```

Fresh-session follow-up after compaction:

```bash
tmp_log="$HOME/.logs/codex/telemetry/claude/<project>/claude-$(date +%s)-tmp.log"
claude -p \
  --output-format stream-json \
  --json-schema '<schema-json>' \
  "<prompt with compact history>" > "$tmp_log"

python ~/.codex/skills/sow-delegate-flow/scripts/parse_delegate_log.py \
  --raw-log "$tmp_log" \
  --mode stream-json \
  --repo-root "$REPO"
```

Normal read path:

- run the parser against the raw log first
- during execution, use the parser output as a compact progress view
- read the parser output first
- read the raw log only if the parser reports an anomaly or the flow explicitly needs deep debugging

Coordinator loop:

- keep polling and re-reading parser output in the same execution path
- do not stop after one or two polls unless there is a terminal or actionable state
- actionable states are:
  - terminal success/failure result
  - `needs_advice`
  - likely stall by difficulty threshold
  - explicit infra or rate-limit block

## Result Schema

```json
{
  "type": "object",
  "properties": {
    "status": { "type": "string", "enum": ["success", "needs_advice", "failed"] },
    "failure_type": { "type": "string", "enum": ["infra", "quality", "uncertainty"] },
    "changed_files": { "type": "array", "items": { "type": "string" } },
    "summary": { "type": "string" },
    "open_questions": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "question": { "type": "string" },
          "why": { "type": "string" },
          "recommended": { "type": "string" }
        },
        "required": ["question", "why", "recommended"],
        "additionalProperties": false
      }
    },
    "scope_respected": { "type": "boolean" },
    "validation_hint": { "type": "string" },
    "fallback_needed": { "type": "boolean" }
  },
  "required": [
    "status",
    "failure_type",
    "changed_files",
    "summary",
    "open_questions",
    "scope_respected",
    "validation_hint",
    "fallback_needed"
  ],
  "additionalProperties": false
}
```

## Validation Guidance

Choose the smallest useful local check that matches the SOW type:

- `docs-only`: `git diff --check` plus a focused cross-reference or grep check
- `frontend`: targeted build, test, or route/component check
- `backend`: targeted module test or `uv run pytest ...`
- `migration`: backward-compat check plus a scan for legacy markers

Use `validation_hint` as a suggestion from Claude, not as proof.

## Failure Types

- `infra`: quota, CLI failure, tool failure, environment block
- `quality`: implementation ran but did not meet the SOW or failed validation
- `uncertainty`: delegate is blocked by ambiguity and needs advice

## Termination Policy

- `quality`: allow up to 2 repair rounds, then finish locally or stop
- `infra`: if scope is clear, prefer local finish over waiting for delegate recovery
- `uncertainty`: answer once; if it remains ambiguous, stop and escalate
- `rate-limit`: if the partial diff is usable and scope is clear, finish locally

## Control Logic

- `success`: review and validate locally.
- `needs_advice`: answer the questions, then resume or refresh the session.
- `failed` + `infra`: fall back locally unless infrastructure is intentionally fixed first.
- `failed` + `quality`: send repair feedback or take over locally.
- `failed` + `uncertainty`: answer or escalate the question, then continue.
- If `scope_respected` is false, treat the delegate result as unsafe by default.

## Final Review Note

Use this compact closeout shape after review:

```text
Delegate status: <success | needs_advice | failed>
Files changed: <paths or count>
Validation run: <command or focused check>
Issues found: <none or short list>
Final disposition: <accept | repair | local finish | stop>
```

## Limit Handling

- Prefer detecting limit hits from the parser output built from streamed events first.
- Treat usage or rate-limit blocking as fallback triggers.
- Do not rely on exact error strings or percentage prechecks.
- If overage is unavailable or rejected and Claude is blocked, continue locally.

See [log-parsing.md](log-parsing.md) for the canonical raw-log path, parser output shape, and extraction rules.

## Polling

- Use polling backoff instead of eager fixed-interval checks.
- Start around 30 second intervals, then back off while the run still looks active.
- Classify the task before waiting:
  - `easy`: simple docs or very small isolated edit
  - `medium`: normal implementation slice
  - `hard`: larger refactor, broad implementation, or infra-heavy task
- Do not treat an empty or unchanged log during early polling as a stall by itself.
- Only treat a delegate run as likely stalled near these no-progress thresholds:
  - `easy`: 5 minutes
  - `medium`: 10 minutes
  - `hard`: 15 minutes
- Check faster only when the result is on the critical path and you expect a short run.
- Keep the loop alive until one of those thresholds or another real decision point is reached.
