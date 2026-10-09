# Claude Code Native GLM Role

Read this only when the active client is Claude Code. It answers one question
for the GLM gates in `sow-delegate-flow`, `task-execution-flow` and
`task-review-investigate-compare`: is the exact target natively available in
this Claude Code session, and how is it called. Those gates, their mandatory
rules and their failure rules stay authoritative.

```text
not the interactive top-level session -> native-unavailable (interface unsupported), no call
cannot tell whether it is top-level     -> native-capability-unknown, no call
interactive top-level Claude Code session
  -> glm-worker agent in the catalog?  no -> native-unavailable (exact model absent)
  -> yes (candidate only) -> one sub-agent call with a self-contained task
       -> REFUSED                              -> native-unavailable (interface unsupported)
       -> FAILED (incl. timeout), missing field,
          other model, lower effort or ok=False -> observed delegation failure
       -> model ...greennode/glm-5.3, effort=max, ok=True
                                               -> read the result file -> coordinator verifies
```

## Scope Guard: One Level Only

- Only the interactive top-level Claude Code session the user works in, on
  desktop or in a terminal, may call `glm-worker`.
- Never call `glm-worker` or its relay command from:
  - a non-interactive `claude -p` session;
  - a Claude Code process started as another coordinator's delegate, such as
    the Claude Code External Transport used by Codex;
  - any Claude sub-agent, including review or exploration sub-agents.
  In those contexts do not call; record `native-unavailable` (interface
  unsupported: the role exists but is barred at this depth) as the capability
  evidence, do the assigned work yourself and keep the selected model. If the
  session cannot tell whether it is the top-level session, record
  `native-capability-unknown` and do not call.
- This check comes first. As a backstop, the relay command (`glm-run`)
  refuses to start under a Codex process or a non-interactive Claude Code
  process and returns a `REFUSED` line. Treat that as `native-unavailable`
  (interface unsupported), not as a reason to retry.
- The GLM delegate has file tools only. It cannot run commands or start
  sub-agents, so it never delegates further.

## Identity

- `glm-worker` runs `greennode/glm-5.3` with `reasoning_effort=max` through a
  local relay. The relay uses the Claude Code CLI harness with the GLM model;
  it is this client's native GLM role, not the Claude Code External Transport,
  so that transport's eligibility guard against starting another Claude
  session from a Claude coordinator does not apply to it.
- The catalog entry and its description are only a candidate; the exact-target
  evidence is the returned status line.
- Accept a handoff only when the returned status line names
  `greennode/glm-5.3`, `effort=max` and `ok=True`. A missing field, another
  model id, a lower effort or `ok=False` is a failed handoff; aliases and
  display labels never satisfy the exact target. Such a mismatch follows the
  observed-delegation-failure rule (evidence, bounded repair), not
  `native-unavailable`.
- No `glm-worker` agent in the catalog means `native-unavailable` with reason
  `exact model absent`; continue under the calling gate's existing rule.

## Calling It

- Send one bounded task per call. The delegate starts a fresh process with no
  prior history, so the task must be self-contained: working directory, goal,
  exact files it may read or change, and done criteria.
- Mode is `read` unless the task carries an approved SOW write scope; then
  name the exact files and request `edit`. Never give overlapping write scopes
  to parallel calls.
- The agent returns the relay's final `[glm-run]` line only: the status line
  on success, or the `REFUSED` / `FAILED` line. Read GLM's original answer from
  the `result=` file the status line names; never rely on a paraphrase.
- Isolation evidence: the `result=` path lies in a run directory created for
  that call; the relay always disables session persistence, never resumes a
  session, and passes only the task text.
- For a long task, run the agent call in the background. Run directories are
  created under `glm-run/` in the system temporary directory; the newest one
  holds `progress.log` and `stream.jsonl`, written while the call runs. Read
  them to follow progress or to collect failure evidence.

## After The Call

- The result is handoff evidence, not completion. Map the required delegate
  return fields this way: model id, reasoning effort and availability come
  from the status line; transport, lifecycle and isolation from the relay's
  fresh non-persistent process; independent pass, changed files, verification
  performed, remaining risks and pending decisions come from the result file.
- Confirm changed files from the working tree yourself and run every
  verification command in the coordinator; the delegate cannot run them.
- Lifecycle: the relay bounds each call with its own timeout (540 s by
  default) and kills its whole process group when it expires; a timeout is an
  observed delegation failure. Stop a background agent call you no longer need
  with the harness's task-stop control before closeout. The delegate is one-shot: send a question answer or a
  repair round as a new call with a short self-contained handoff, never as a
  resumed session.
