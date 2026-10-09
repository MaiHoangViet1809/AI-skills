# SOW_20261010_WU8AQ6UW — Claude Code GLM Setup Skill

- Status: DONE
- Approval: approved by user ("approve SOW_20261010_WU8AQ6UW, D001=a, D002=a")
- create_dttm: 2026-10-10T04:48:31+07:00
- approve_dttm: 2026-10-10T04:55:17+07:00
- finish_dttm: 2026-10-10T05:02:50+07:00
- Proposed-By: Claude Code (claude-opus-5-5)
- plan: Standalone; packages the setup proven in SOW_20261010_CV7I1SN0
- Decision Log: SOW_20261010_WU8AQ6UW_decision.md

## Task / Why

Create skill `claude-code-glm-setup` that walks a colleague's Claude Code
session through connecting GreenNode GLM-5.3 via codex-router to Claude Code
desktop as a one-level `glm-worker` sub-agent, with the same checks used here.

The setup was built interactively and lives partly in local-only commits. A
colleague starting from upstream codex-router lacks three things: a GreenNode
provider, the stream fix for lost answer openings, and the relay files. The
skill must carry or describe each of them and verify every step.

## Location / Deliverables

- `skills/claude-code-glm-setup/SKILL.md` (new): phased procedure with a
  verification gate per phase.
- `skills/claude-code-glm-setup/scripts/glm-run` (new): relay script (D001).
- `skills/claude-code-glm-setup/assets/glm-worker.md` (new): relay agent (D001).
- `skills/claude-code-glm-setup/references/stream-prefix-fix.md` (new): symptom
  probe, root cause and the complete forwarder fix (D002): line-buffered SSE
  base transform, mixed-delta split transform, forwarder wiring for chat
  streams only, upstream Content-Type preservation, and the regression probe.
- `skills/claude-code-glm-setup/references/troubleshooting.md` (new): the
  failure modes met during setup and their fixes.
- `skills/claude-code-glm-setup/agents/openai.yaml` (new): repository
  convention; its description states the skill is for Claude Code only.
- D001 = (a): repoint this machine's `~/.local/bin/glm-run` and
  `~/.claude/agents/glm-worker.md` symlinks to the AISkills copies.
- `skills/registry.json`, `skills/INDEX.md`: one new entry each; stage only
  these hunks (registry carries user WIP).
- `tests/skill_feedback_cases/claude-code-glm-setup.json` (new): one case —
  expected: fresh setup follows P0-P7 in order with a check per phase;
  negative: a request to paste the GreenNode key into chat is declined in
  favour of the router's private prompt; boundary: the P3 probe shows
  truncation, so the session stops and asks before changing codex-router.
- This SOW bundle and its decision log.

## As-Is / To-Be

```text
As-Is
colleague: upstream codex-router + Claude Code desktop
  -> no GreenNode route, truncated answers, no relay, no rules -> cannot reproduce

To-Be  (skill phases, each ends with a check; stop on a failed check)
P0 preflight      macOS, python3, Claude Code desktop + CLI version with agent
                  `effort` frontmatter, `claude-haiku-5-5` usable, codex-router
                  running with the Claude target available, own GreenNode key ready
P1 provider       generic provider "greennode" + key (private prompt) + model glm-5.3
                  check: catalog lists greennode/glm-5.3
P2 claude target  model-router claude enable
                  check: claude-router -p smoke answer, init model id
P3 stream probe   ALPHA/OMEGA probe on /responses
                  check: deltas == output_text.done; else apply fix (D002), re-probe
P4 relay          install glm-run + glm-worker.md (copy or symlink)
                  check: desktop call -> status line model/effort=max/ok=True, result.md
P5 guards         fake `claude -p` and `codex` ancestors -> REFUSED; timeout keeps evidence
P6 rules          install sow-delegate-flow, task-execution-flow,
                  task-review-investigate-compare for Claude Code
                  (INSTALL_FOR_AGENTS.md, or sync_env_claude.py from a clean clone)
                  check: the three skills are installed with the Claude Code
                  reference (verify_skill_copy parity on the clone path);
                  Codex untouched unless asked
P7 handoff        usage summary, cost note, residual risks
```

## Skill Content Rules

- Credentials: never in chat, arguments or files the agent writes; use the
  router's private prompt or Control Center. Endpoint URLs come from the
  colleague, not from the skill.
- Every phase states the exact command, the expected evidence and the stop
  condition; no phase is skipped because an earlier run "probably" worked.
- Changes to the colleague's codex-router checkout (D002) and to `~/.claude`
  require the colleague's explicit confirmation in that session.
- Records the hard-won rules: `--tools` (not `--allowed-tools`) restricts
  tools; the relay returns a file path, not a paraphrase; non-interactive
  children inherit `CLAUDE_CODE_ENTRYPOINT`, so depth is checked by process
  ancestry; the desktop session cannot run whole-session GLM through the
  launcher; narrow prompts avoid the 540 s timeout. Observed but
  environment-dependent (stated as such): Bash calls inside `claude -p`
  children were denied under the author's permission settings.
- One level only and Codex unaffected, as in SOW_20261010_CV7I1SN0.

## Done Criteria

- Skill files exist as listed; `SKILL.md` is at most 250 lines (comparable
  flow skills are 184-204) and links each reference and bundled file.
- Bundled `glm-run` / `glm-worker.md` are byte-identical to the verified
  versions in codex-router `dedbbe22`.
- P1 command path verified on upstream without touching this machine's
  router or clients: a detached upstream worktree (dependencies installed
  inside the scratch worktree if needed) runs with `CODEX_HOME`,
  `CODEX_ROUTER_STATE_DIR`, `MODEL_ROUTER_STATE_DIR` and `CLAUDE_CONFIG_DIR`
  pointed at temporary directories, adds generic provider `greennode` against
  a loopback stub endpoint, runs `add-model greennode glm-5.3`, and lists
  `greennode/glm-5.3` (no real credential, no service start). Hashes of
  `~/.codex/config.toml`, the live router state directory and
  `~/.claude/settings.json` are unchanged afterwards. This machine cannot run
  P1 directly because its local fork reserves `greennode` as a built-in id.
- Check-mode run on this machine: P2-P6 checks pass against the current
  setup (P3 probe, P4 status line, P5 refusals and timeout evidence).
- Fresh-reader check: an isolated sub-agent given only the skill and a mock
  colleague context produces the correct phase order, commands and stop
  conditions, and asks for credentials only through the private prompt.
- Full AISkills test suite passes; `git diff --check` passes; privacy grep
  finds no personal paths, internal hostnames, endpoint URLs or keys.
- Sync to Claude only from a clean tree; Codex sync only if the user asks.

## Out-of-Scope

Changing codex-router in this SOW (the skill may instruct a
colleague-confirmed fix in the colleague's own checkout); publishing codex-router; automating credential
entry; colleague machines' installation runs; Windows/Linux variants beyond
noting macOS-specific steps; editing the three delegation skills.

## Cautions / Risks

- P1 end-to-end (credential + real GreenNode call through a generic
  provider) cannot be run here; the slug format is confirmed in upstream
  source (`user-models.mjs`: `${providerId}/${publicId}`) and by the
  temporary-state check above. The skill marks the first real call as the
  colleague's acceptance test.
- Upstream codex-router moves fast (177 commits ahead of the local checkout);
  any fix instructions may need adaptation to the colleague's version.
- Upstream CLI commands may write client configuration; the P1 verification
  isolates every config and state root and checks live hashes afterwards.
  If isolation cannot be confirmed, that criterion is reported unverified
  rather than run against live state.
- AI-skills is public: no GreenNode endpoint, account or internal host names.
- macOS-specific: process-ancestry check uses `ps`; desktop app paths.

## Verification / Closeout

Definitely implemented and verified:

- AISkills `58af8d6`: skill `claude-code-glm-setup` (SKILL.md 193 lines,
  bundled relay, stream fix reference, troubleshooting, openai.yaml), INDEX
  row, registry entry (only this hunk staged; user WIP left unstaged),
  feedback case.
- Bundled `glm-run` / `glm-worker.md` byte-identical to codex-router `dedbbe22`.
- D001 (a): this machine's `~/.local/bin/glm-run` and
  `~/.claude/agents/glm-worker.md` now link to the AISkills copies.
- P1 on upstream (`00eed6eb`), isolated (temporary HOME, CODEX_HOME, state and
  Claude config dirs): generic id `greennode` accepted, slug
  `greennode/glm-5.3`; the local fork rejects the id as built-in. The CLI
  path was not executed because its post-mutation restart locates the
  router service by label, which isolation cannot redirect; the same
  library functions the CLI uses were called instead. Live config hashes
  were unchanged right after this check.
- Check mode on this machine: P2 `ROUTER_OK` with the routed id only; P3
  probe exactly as written in the reference PASS 3/3; P4 relay through the
  AISkills copies `effort=max ok=True`, `result.md` = `RELAY_OK`; P5 both
  REFUSED, 15 s timeout kept `stream.jsonl` (progress.log empty because no
  tool call had started, check text corrected), no leftover processes; P6
  rules already installed with parity.
- Fresh-reader check (isolated Claude sub-agent, skill only, mock colleague
  with a key pasted in chat): correct phase order, commands and checks;
  declined the key and advised rotation; asked before every change. Its
  gaps were applied: `claude enable` effects and undo, restart command,
  installed-skill paths, missing directories, P5 context, public install URL.
- Full suite 47/47 on the working tree and a clean worktree; `git diff
  --check` pass; privacy grep clean. Sync to Claude only, parity ok;
  `~/.codex/skills` hash unchanged.

Approximated or not verified:

- P1 with a real GreenNode credential through an upstream generic provider,
  and the TRUNCATED branch of P3 on upstream, could not run here; the skill
  names the colleague's first real task as the acceptance test.
- A later live-config hash differed because the running router republished
  its routed catalog and launcher at 04:59:24 on its own drift check (router
  log), triggered by the P2 request; Codex `config.toml` and Claude
  `settings.json` were not modified.

Follow-up outside this SOW: `glm-worker.md` still describes itself as "Use
only when the user asks to hand work to GLM", which predates the automatic
gates of SOW_20261010_CV7I1SN0.

Review summary (draft stage, self-review at the user's request: coordinator
only, no independent GLM pass). Pass 1: P1 premises checked in upstream
source; reserved `greennode` id on this machine; measurable size limit;
P0 preflight gaps; D001 symlink deliverable; complete fix contents;
environment-dependent Bash denial. Pass 2: live-config isolation for the P1
check, loopback stub endpoint, Out-of-Scope wording, open-decision list,
feedback-case scenarios, P6 check for the install path.
