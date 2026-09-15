---
name: "playwright-flow"
description: "Use when the task requires automating a real browser from the terminal (navigation, form filling, snapshots, screenshots, data extraction, UI-flow debugging) via `playwright-cli`, with explicit session lifecycle and cleanup."
---


# Playwright CLI Skill

Drive a real browser from the terminal using `playwright-cli`. Prefer the bundled wrapper script so the CLI works even when it is not globally installed.
Treat this skill as CLI-first automation. Do not pivot to `@playwright/test` unless the user explicitly asks for test files.
Treat browser sessions as stateful resources that must be cleaned up when the review or automation flow ends.

## Prerequisite check (required)

Before proposing commands, check whether `npx` is available (the wrapper depends on it):

```bash
command -v npx >/dev/null 2>&1
```

If it is not available, pause and ask the user to install Node.js/npm (which provides `npx`). Provide these steps verbatim:

```bash
# Verify Node/npm are installed
node --version
npm --version

# If missing, install Node.js/npm, then:
npm install -g @playwright/cli@latest
playwright-cli --help
```

Once `npx` is present, proceed with the wrapper script. A global install of `playwright-cli` is optional.

## Skill path (set once)

```bash
export CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
export PWCLI="$CODEX_HOME/skills/playwright-flow/scripts/playwright_cli.sh"
```

User-scoped skills install under `$CODEX_HOME/skills` (default: `~/.codex/skills`).

Before opening a browser, use `list` to inspect existing sessions, choose a
unique name for this task, and record its ownership. Set that name for all
commands below (replace the example if it already exists):

```bash
export PLAYWRIGHT_CLI_SESSION=task-browser-unique
```

Do not attach to a pre-existing session without explicit user authorization.

## Quick start

Use the wrapper script:

```bash
"$PWCLI" open https://playwright.dev --headed
"$PWCLI" snapshot
"$PWCLI" click e15
"$PWCLI" type "Playwright"
"$PWCLI" press Enter
"$PWCLI" screenshot
```

If the user prefers a global install, this is also valid:

```bash
npm install -g @playwright/cli@latest
playwright-cli --help
```

## Core workflow

1. Open the page.
2. Snapshot to get stable element refs.
3. Interact using refs from the latest snapshot.
4. Re-snapshot after navigation or significant DOM changes.
5. Capture artifacts (screenshot, pdf, traces) when useful.
6. Close the session when done.

Minimal loop:

```bash
"$PWCLI" open https://example.com
"$PWCLI" snapshot
"$PWCLI" click e3
"$PWCLI" snapshot
"$PWCLI" close
```

## Session lifecycle

- `open` creates or attaches to a live browser session that can persist across later commands.
- Session state lives beyond a single command; if you walk away without cleanup, stale headed browsers can accumulate.
- Use `list` to inspect active sessions before reusing or closing them.
- Use a unique task-owned named session for every task. An inherited session
  variable is not ownership evidence; check it before opening or closing.

Core lifecycle commands:

```bash
"$PWCLI" list
"$PWCLI" close
```

## When to snapshot again

Snapshot again after:

- navigation
- clicking elements that change the UI substantially
- opening/closing modals or menus
- tab switches

Refs can go stale. When a command fails due to a missing ref, snapshot again.

## Recommended patterns

### Form fill and submit

```bash
"$PWCLI" open https://example.com/form
"$PWCLI" snapshot
"$PWCLI" fill e1 "user@example.com"
"$PWCLI" fill e2 "password123"
"$PWCLI" click e3
"$PWCLI" snapshot
```

### Debug a UI flow with traces

```bash
"$PWCLI" open https://example.com --headed
"$PWCLI" tracing-start
# ...interactions...
"$PWCLI" tracing-stop
```

### Multi-tab work

```bash
"$PWCLI" tab-new https://example.com
"$PWCLI" tab-list
"$PWCLI" tab-select 0
"$PWCLI" snapshot
"$PWCLI" close
```

## Session cleanup

Default cleanup policy:

- After browser review or UI debugging ends, close only the session owned by
  this task using its explicit `--session` name or verified session variable.
- Leave all other sessions intact. If owned cleanup fails, inspect that session
  and report the remaining cleanup; a stuck browser does not authorize global kill.
- `close-all` and `kill-all` affect other sessions and require explicit user
  authorization for that global action. Never use them as automatic recovery.
- If ownership is unknown, inspect `list` and establish ownership before cleanup.
- Before starting a fresh debugging task, run `list` if you suspect old sessions may still exist.

Typical cleanup tail:

```bash
"$PWCLI" screenshot
"$PWCLI" close
```

Escalation for stale sessions:

```bash
"$PWCLI" list
"$PWCLI" --session "$PLAYWRIGHT_CLI_SESSION" close
```

## Wrapper script

The wrapper script uses `npx --package @playwright/cli playwright-cli` so the CLI can run without a global install:

```bash
"$PWCLI" --help
```

Prefer the wrapper unless the repository already standardizes on a global install.

## References

Open only what you need:

- CLI command reference: `references/cli.md`
- Practical workflows and troubleshooting: `references/workflows.md`

## Guardrails

- Always snapshot before referencing element ids like `e12`.
- Re-snapshot when refs seem stale.
- Prefer explicit commands over `eval` and `run-code` unless needed.
- When you do not have a fresh snapshot, use placeholder refs like `eX` and say why; do not bypass refs with `run-code`.
- Use `--headed` when a visual check will help.
- When capturing artifacts in this repo, use `output/playwright/` and avoid introducing new top-level artifact folders.
- Default to CLI commands and workflows, not Playwright test specs.
- Do not leave browser sessions running after the task unless the user explicitly wants to keep them open.
