# Claude Code Native GLM Role

Read this only when the active client is Claude Code. It answers one question
for the GLM gates in `sow-delegate-flow`, `task-execution-flow` and
`task-review-investigate-compare`: is the exact target natively available in
this Claude Code session, and how is it called. Those gates, their mandatory
rules and their failure rules stay authoritative.

```text
interactive top-level Claude Code session
  -> glm-worker agent in the catalog?  no -> native-unavailable (exact model absent)
  -> yes -> one sub-agent call with a self-contained task
       -> status line: model ...greennode/glm-5.3, effort=max, ok=True ?
            no / REFUSED / FAILED -> observed delegation failure or native-unavailable
            yes -> read the result file -> coordinator review and verification
```

## Scope Guard: One Level Only

- Only the interactive top-level Claude Code session the user works in, on
  desktop or in a terminal, may call `glm-worker`.
- Never call `glm-worker` or its relay command from:
  - a non-interactive `claude -p` session;
  - a Claude Code process started as another coordinator's delegate, such as
    the Claude Code External Transport used by Codex;
  - any Claude sub-agent, including review or exploration sub-agents.
  In those contexts do the assigned work yourself and keep the selected model.
- The relay refuses to start under a Codex process or a non-interactive
  Claude Code process and prints `REFUSED`. Treat that as
  `native-unavailable` (interface unsupported), not as a reason to retry.
- The GLM delegate has file tools only. It cannot run commands or start
  sub-agents, so it never delegates further.

## Identity

- `glm-worker` runs `greennode/glm-5.3` with `reasoning_effort=max` through a
  local relay. The relay uses the Claude Code CLI harness with the GLM model;
  it is this client's native GLM role, not the Claude External Transport, so
  the Claude self-delegation guard does not apply to it.
- Accept a handoff only when the returned status line names
  `greennode/glm-5.3`, `effort=max` and `ok=True`. A missing field, another
  model id, a lower effort or `ok=False` is a failed handoff; aliases and
  display labels never satisfy the exact target.
- No `glm-worker` agent in the catalog means `native-unavailable` with reason
  `exact model absent`; continue under the calling gate's existing rule.

## Calling It

- Send one bounded task per call. The delegate starts a fresh process with no
  prior history, so the task must be self-contained: working directory, goal,
  exact files it may read or change, and done criteria.
- Mode is `read` unless the task carries an approved SOW write scope; then
  name the exact files and request `edit`. Never give overlapping write scopes
  to parallel calls.
- The agent returns one status line. Read GLM's original answer from the
  `result=` file it names; never rely on a paraphrase.
- For a long task, run the call in the background. The relay prints its run
  directory first and writes `progress.log` and `stream.jsonl` there while it
  runs; read them to follow progress or to collect failure evidence.

## After The Call

- The result is handoff evidence, not completion. Map the required delegate
  return fields this way: model id, reasoning effort and availability come
  from the status line; transport, lifecycle and isolation from the relay's
  fresh non-persistent process; independent pass, changed files, verification
  performed, remaining risks and pending decisions come from the result file.
- Confirm changed files from the working tree yourself and run every
  verification command in the coordinator; the delegate cannot run them.
