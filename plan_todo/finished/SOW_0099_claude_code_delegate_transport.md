# SOW_0099 - Claude Code Delegate Transport Contract

- **Status**: COMPLETED
- **Approval**: APPROVED by user
- **create_dttm**: 2026-10-06
- **approve_dttm**: 2026-10-06T05:08:47+07:00
- **finish_dttm**: 2026-10-06T05:12:42+07:00
- **Proposed-By**: Codex
- **plan**: None; bounded skill-contract update

## Task

Document and integrate the supported Claude Code CLI delegation path so agents
can delegate isolated review/research/brainstorm work to the Claude `opus`
alias at High effort and code implementation work to the Claude `sonnet` alias
at High effort without guessing the
CLI syntax, session mode, or safety boundary.

## Why / Baseline

The delegate skill documents native Codex and external-agent boundaries but does
not contain the verified Claude Code invocation used for the recent review.
Agents may therefore try interactive or stateful syntax, omit fresh-session
handling, or select an unsuitable model for the task type.

The current exact invocation is:

```bash
claude -p \
  --model opus \
  --effort high \
  --output-format stream-json \
  --no-session-persistence \
  --permission-mode plan \
  --permission-prompts none \
  --allowed-tools Read,Glob,Grep \
  <<'EOF'
Review the specified files read-only.
Do not edit, commit, push, or deploy.
Return a concise JSON-like report with verdict, findings, evidence, and recommendations.
EOF
```

Claude is an external transport. Existing exact GLM-5.3-max rules remain the
default when model selection is open; this SOW adds Claude as an explicit,
documented transport/model choice and does not silently replace GLM policy.

## Location

- `skills/sow-delegate-flow/SKILL.md`
- `skills/task-review-investigate-compare/SKILL.md`
- `skills/task-execution-flow/SKILL.md`
- `skills/task-router-flow/SKILL.md`
- Corresponding feedback fixtures under `tests/skill_feedback_cases/`
- This SOW, including its eventual move to `plan_todo/finished/`

## As-Is Diagram (ASCII)

```text
review / execute / route
          |
          v
   mention external delegate
          |
          +--> Claude CLI syntax/model/session details are implicit
          `--> agent guesses transport or mode
```

## To-Be Diagram (ASCII)

```text
review / research / brainstorm / investigate ----> `opus` + high
implementation code ----------------------------> `sonnet` + high
                                                     |
                                                     v
     fresh `claude -p` session + stream-json + no persistence
                          |
                          v
               coordinator reviews and verifies
```

## Deliverables / Behavior Locks

1. Add one canonical Claude Code external-transport section to
   `sow-delegate-flow`. It MUST document `claude -p`, exact model/effort
   mapping, `--output-format stream-json`, `--no-session-persistence`,
   `--permission-mode plan` for read-only review, `--permission-prompts none`,
   and bounded `--allowed-tools` usage.
2. Use `opus` with `--effort high` for review, brainstorm, research, and
   investigation. Use `sonnet` with `--effort high` for approved code
   implementation. These are Claude CLI aliases that resolve to the current
   corresponding model; verify the resolved model in the init event before
   launch is accepted, and never silently substitute another model.
3. Preserve external-agent isolation: every logical task starts fresh, receives
   a self-contained prompt, contains no parent transcript, and explicitly
   forbids edits for read-only work. `stream-json` is an event transport, not
   proof that the delegate is correct; the coordinator remains responsible for
   review, diff, tests, and closeout.
4. Add short cross-references:
   - `task-review-investigate-compare` delegates independent Claude review
     through `sow-delegate-flow`; the review skill owns the question and verdict.
   - `task-execution-flow` delegates approved Claude implementation slices
     through `sow-delegate-flow`; execution owns SOW scope and verification.
   - `task-router-flow` routes explicit Claude delegation to
     `sow-delegate-flow` without creating a second transport contract.
5. Add sanitized expected, negative, and boundary feedback scenarios covering:
   read-only Opus review, Sonnet implementation under an approved SOW, missing
   model/CLI, explicit user-selected model override, stale-session rejection,
   destructive-operation safety, and coordinator verification after a valid
   `stream-json` response.
6. Do not change native GLM-5.3-max availability rules, SOW approval gates,
   execution ownership, or installed copies in this SOW.

## Done Criteria

- One canonical Claude Code syntax exists in `sow-delegate-flow`; no duplicate
  transport command is added to the three consumer skills.
- The four skills explicitly reference the delegate skill at their delegation
  decision point and retain their current ownership boundaries.
- Opus/Sonnet routing, fresh-session requirements, read-only mode, and
  coordinator verification are unambiguous and do not silently override the
  existing GLM-5.3-max policy.
- Feedback fixtures parse and cover expected, negative, and boundary behavior.
- Run the available skill validator, targeted feedback/sync tests, JSON parsing,
  and `git diff --check`.
- Perform one negative check: a stale session, unavailable requested model, or
  invalid delegate result must not be reported as a successful Claude handoff.
- Canonical implementation and deterministic checks are complete before any
  optional installed-skill sync.

## Out Of Scope

- Replacing the exact GLM-5.3-max mandatory delegation policy.
- Adding a new provider SDK, MCP server, auth flow, session store, retry
  service, orchestration layer, or wrapper around Claude Code.
- Automatic model substitution, global default changes, or background sessions.
- Product/runtime code, project-specific SOW execution, or production deploy.
- Syncing `~/.codex/skills/` or any Claude installation without a separate
  explicit deployment request.
- Rewriting completed SOW history or unrelated dirty/untracked files.

## Verification / Closeout

- Implemented the canonical Claude Code transport section in
  `sow-delegate-flow`; consumer skills reference it without duplicating the
  command contract.
- Added expected/negative/boundary cases to the delegate, review, execution
  and router fixtures. All JSON fixtures parse and case IDs remain unique.
- Structural validators passed for all four changed skills.
- `uv run --no-sync --offline python -m unittest
  tests.test_skill_feedback_cases tests.test_skill_sync_scripts` passed 13
  tests; `git diff --check` passed.
- Runtime alias probes confirmed `opus` resolves to `claude-opus-5-5` and
  `sonnet` resolves to `claude-sonnet-5-5`. The `opus-latest` and
  `sonnet-latest` aliases were rejected and are not documented.
- Negative checks cover unavailable/mismatched model, stale session, invalid
  stream result, unapproved implementation, duplicate transport contracts and
  destructive-operation safety.
- Not exercised: a real Claude code-edit session under an approved SOW. The
  implementation contract remains constrained to `acceptEdits` plus approved
  file tools; coordinator verification remains mandatory.
- Installed skill sync and push are intentionally outside this SOW.

## Cautions / Risks

- `opus` and `sonnet` must be confirmed against the installed CLI and their
  resolved model IDs inspected in the init event before launch is accepted; a
  display label or remembered alias is not proof.
- Plan mode and restricted tools express the requested read-only boundary, but
  the coordinator MUST still inspect process output, diff, and repository state.
- `stream-json` may contain intermediate events; only the completed result plus
  coordinator verification counts as handoff evidence.
- A user-selected Claude model/transport wins for that named task; absent such
  a selection, existing exact GLM-5.3-max policy remains authoritative.

## Plan / Reference

- `sow-delegate-flow`
- `task-review-investigate-compare`
- `task-execution-flow`
- `task-router-flow`
- `SOW_0096_EXT_01_mandatory_glm53_delegation`

## Decision

Approved by the user. Use one canonical Claude CLI contract in
`sow-delegate-flow`; consumer skills reference it but do not duplicate it.
Claude is an explicit transport/model choice, with `opus` for thinking/review
and `sonnet` for approved implementation; GLM-5.3-max remains the open-choice
default.
