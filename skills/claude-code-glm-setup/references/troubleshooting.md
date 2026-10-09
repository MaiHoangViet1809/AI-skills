# Troubleshooting

Each entry was met while building this setup. Fix the cause; do not work
around a failed check.

| Symptom | Cause | Fix |
| --- | --- | --- |
| GLM answers start mid-sentence | Mixed reasoning+content chunk dropped by LiteLLM's Chat-to-Responses bridge | [stream-prefix-fix.md](stream-prefix-fix.md) |
| The GLM delegate ran a shell command although only file tools were allowed | `--allowed-tools` only auto-approves; settings-allowed tools still run | Restrict with `--tools` (the bundled relay passes both) |
| The relay agent's answer is a summary or a translation, not GLM's text | Relay models paraphrase long outputs | The relay writes GLM's answer to `result.md` and returns one status line; read the file |
| `glm-worker` prints `REFUSED nested delegation` | Called under a Codex process or a non-interactive `claude -p` | Intended. Only the interactive top-level session may delegate; do the work in the caller |
| Relay times out after 540 s with no evidence | Old relay wrote the stream only at exit; the launcher's CLI child held stdout open after kill | Bundled relay writes `stream.jsonl` / `progress.log` live and kills the process group; narrow the prompt to the files it must read |
| A detection idea based on `CLAUDE_CODE_ENTRYPOINT` misfires | Non-interactive children inherit the parent's value (for example `claude-desktop`) | Use process ancestry, as the relay does |
| `claude-router` works in a terminal but the desktop app still uses Claude | The launcher configures only the process it starts | Expected. Desktop uses GLM through `glm-worker`; whole-session GLM needs a terminal `claude-router` |
| `--model sonnet` under `claude-router` still runs GLM | The launcher points every Claude alias at the routed model | Expected. Claude main plus GLM worker needs the desktop session and `glm-worker` |
| `[claude-code:unrecognized_model]` on stderr | Routed ids are not in Claude Code's built-in catalog | Harmless when the init event names the routed model |
| Bash calls inside a `claude -p` child are denied | Observed under the author's permission settings; environment-dependent | Do not rely on Bash in probes run through `claude -p`; probe from the top-level session |
| `generic add greennode` fails with "already used by the built-in registry" | The checkout is a fork that ships GreenNode built in | Use that fork's GreenNode provider; the published id is still `greennode/glm-5.3` |
| The GreenNode endpoint resolves to a private address | Endpoint reachable only on a company network or VPN | Add the provider with `--allow-private`, and connect the VPN before tests |
| `glm-worker` missing from the agent list in an open session | The session has not picked up the new agent file | Start a new Claude Code session |
| Router answers `authentication_error` to a direct request | The local router requires its caller capability | Use `claude-router` or the router's own helpers (the probe reads its caller secret) |
