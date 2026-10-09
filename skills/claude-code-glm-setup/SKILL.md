---
name: claude-code-glm-setup
description: Set up GreenNode GLM-5.3 through codex-router as a one-level glm-worker sub-agent for Claude Code desktop, with a verification check per phase. Use when a user asks to connect GLM, codex-router or GreenNode to Claude Code, or to reproduce this setup on another machine. Claude Code on macOS only.
---

# Claude Code GLM Setup

Connect GreenNode GLM-5.3 (max effort) to Claude Code desktop through a local
codex-router, as a sub-agent the top-level session can call one level deep.

```text
Claude Code desktop (top-level, Claude subscription)
  -> glm-worker agent (thin relay)          ~/.claude/agents/glm-worker.md
       -> glm-run (depth guard, evidence)   ~/.local/bin/glm-run
            -> claude-router -p --model codex_router/anthropic/greennode/glm-5.3 --effort max
                 -> codex-router (local) -> GreenNode GLM-5.3
  <- one status line + result.md            coordinator reads and verifies
```

## Rules

- Run the phases in order. Each phase ends with a check; if it fails, stop,
  report the evidence and fix the cause before continuing. Do not skip a
  phase because an earlier attempt probably worked.
- Credentials never pass through chat, command arguments or files you write.
  The user enters the GreenNode key in the router's private prompt or Control
  Center. If a key was pasted into chat anyway, do not use or repeat it and
  advise rotating it. Endpoint URLs come from the user; never guess one.
- Ask before changing the user's codex-router checkout, `~/.claude`,
  `~/.local/bin` or any service, and say exactly what will change.
- One level only: just the interactive top-level session calls `glm-worker`.
  Never call it from `claude -p`, from a Codex delegate or from a sub-agent.
- Leave Codex configuration and Codex skills untouched unless the user asks.
- If anything below disagrees with what you observe, trust the observation,
  stop and report; see [troubleshooting](references/troubleshooting.md).

## P0 Preflight

Check, do not install:

- macOS (`sw_vers`), `python3`, `node`.
- Claude Code CLI on `PATH` (`claude --version`; verified with 2.1.289) and
  the desktop app in use.
- The relay model works:
  `claude -p "Reply exactly OK" --model claude-haiku-5-5 --effort max --tools "" --no-session-persistence`
  prints `OK`. If that model is unavailable to the account, plan to change
  only the `model:` line of `glm-worker.md` in P4 and tell the user.
- codex-router checkout path from the user (run router commands from its
  root), router service running
  (`launchctl print gui/$(id -u)/io.github.codex-router` shows `state = running`),
  and Claude target support (README section "Make models appear in Claude
  Code" exists and `./bin/model-router claude status` runs).
- The user has their own GreenNode endpoint URL and API key ready, and is on
  the network or VPN the endpoint needs.

Check: every item confirmed; otherwise stop with the missing item.

## P1 GreenNode Provider

If the checkout already ships a built-in `greennode` provider (a fork), use
its own setup and skip to the check. Otherwise, from the checkout root, give
the user these commands to run in their own terminal:

```bash
./bin/model-router codex providers generic add greennode --name "GreenNode" --base-url <ENDPOINT_BASE_URL> --adapter openai-chat
```

```bash
./bin/model-router codex providers generic credential greennode set
```

```bash
./bin/model-router codex providers generic add-model greennode glm-5.3 --json
```

- Add `--allow-private` to the first command only when the endpoint resolves
  to a private address (company network or VPN).
- The credential command prompts privately; the key never appears in chat.
- `providers generic test greennode` checks reachability and the key.

Check: `add-model` prints `"slug": "greennode/glm-5.3"` (upstream publishes
`<provider id>/<model id>`), and `test` succeeds. Any other id will not be
accepted by the delegation skills, so stop.

## P2 Claude Code Target

Ask first: it adds the `~/.local/bin/claude-router` launcher, publishes the
routed models for Claude Code in the router's state and refreshes the router
service; it does not edit Claude Code settings or login. Undo with
`./bin/model-router claude disable`.

```bash
./bin/model-router claude enable
```

Check: its output lists `codex_router/anthropic/greennode/glm-5.3` and the
launcher `~/.local/bin/claude-router`. Then, from a scratch directory:

```bash
claude-router -p "Reply exactly: ROUTER_OK" --model codex_router/anthropic/greennode/glm-5.3 --output-format json --no-session-persistence
```

Check: the result is `ROUTER_OK` and `modelUsage` names only the routed id.
The `[claude-code:unrecognized_model]` stderr line is harmless.

## P3 Stream Probe

Run the probe in [stream-prefix-fix.md](references/stream-prefix-fix.md)
three times from the checkout root.

Check: `PASS` all three times. On `TRUNCATED`, show the evidence, ask the user
to approve the fix in their checkout, apply it as described there, restart
the router service (`launchctl kickstart -k gui/$(id -u)/io.github.codex-router`,
after asking), and rerun the probe until it passes.

## P4 Relay

Install the bundled [glm-run](scripts/glm-run) and
[glm-worker.md](assets/glm-worker.md) after the user agrees:

- With an AISkills clone, symlink them so updates flow:
  `~/.local/bin/glm-run` -> `<clone>/skills/claude-code-glm-setup/scripts/glm-run`,
  `~/.claude/agents/glm-worker.md` -> `<clone>/skills/claude-code-glm-setup/assets/glm-worker.md`.
- Otherwise copy them from the installed skill
  (`~/.claude/skills/claude-code-glm-setup/scripts/glm-run` and
  `.../assets/glm-worker.md`), then `chmod +x ~/.local/bin/glm-run`.
- Create `~/.local/bin` and `~/.claude/agents` first if missing, and confirm
  `~/.local/bin` is on `PATH` (`command -v glm-run`).

If `glm-worker` is not in the agent list, start a new Claude Code session.
Then call the `glm-worker` agent with a small self-contained read task, for
example "Working directory: <scratch dir>. Read-only. Reply exactly:
RELAY_OK".

Check: the agent returns one line
`[glm-run] model=codex_router/anthropic/greennode/glm-5.3 effort=max mode=read ok=True ... result=<path>`
and that `result.md` contains `RELAY_OK`.

## P5 Guards

From the interactive top-level session that passed P4 (its Bash tool), in a
scratch directory:

```bash
mkdir -p fake && ln -sf /bin/bash fake/claude && ln -sf /bin/bash fake/codex
fake/claude -p -c 'echo task | glm-run --mode read --cwd /tmp'
fake/codex -c 'echo task | glm-run --mode read --cwd /tmp'
echo "Read every file here and summarize each in detail." | glm-run --mode read --cwd <any repo> --timeout 15
```

Check: the first two print `REFUSED nested delegation`; the third prints
`FAILED timeout after 15s run_dir=<dir>`, that directory holds a non-empty
`stream.jsonl` and a `progress.log` (empty if GLM had not called a tool yet),
and no `claude-router` process from it
remains (`pgrep -fl "Read every file here"` prints nothing).

## P6 Delegation Rules

Install `sow-delegate-flow`, `task-execution-flow` and
`task-review-investigate-compare` for Claude Code, following
`INSTALL_FOR_AGENTS.md` in https://github.com/MaiHoangViet1809/AI-skills
(installs from GitHub without a clone), or from a clean clone of it:

```bash
uv run python scripts/skills/sync_env_claude.py --scope user --skill sow-delegate-flow --overwrite
```

Repeat for the other two skills; never sync from a tree with uncommitted
edits.

Check: `~/.claude/skills/sow-delegate-flow/references/claude-code.md` exists;
on the clone path `scripts/skills/verify_skill_copy.py --skill <name>
--target-root ~/.claude/skills` reports parity for each skill. Codex skills
are untouched unless the user asked.

## P7 Handoff

Tell the user, briefly:

- In Claude Code desktop, the delegation skills now call GLM when their gates
  require it, and the user can ask directly ("use glm-worker to review X").
- GLM gets file tools only (no shell); Claude reads `result.md` and runs
  every verification itself. Long calls can run in the background with
  progress in the newest `glm-run/` run directory under the system temp dir.
- Cost: each call runs the relay model once (about $0.15 at max effort,
  measured 2026-10-10) plus GreenNode usage.
- Residual risks: in-session sub-agents are kept from calling `glm-worker`
  by instruction only; the first real task is the acceptance test for P1.

## Verification Summary

Report one row per phase with the evidence seen (command and key output).
Separate what was verified from what was skipped, and why.
