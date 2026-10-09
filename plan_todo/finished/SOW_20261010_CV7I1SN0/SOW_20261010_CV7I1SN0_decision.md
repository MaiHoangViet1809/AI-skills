# SOW_20261010_CV7I1SN0 — Decisions

- Parent: SOW_20261010_CV7I1SN0_claude_code_glm_branch.md

## D001 — Client branch plus Claude-only reference

- Date: 2026-10-10T03:38:24+07:00
- Status / Owner: proposed; user selected "branch in skill, or split and read the matching copy"; Claude Code
- Context: Skill sync copies identical content to every client. The user
  requires the Claude Code guidance to leave the Codex side untouched.
- Options: (1) edit `sow-delegate-flow` rules in place; (2) separate
  Claude-only skill; (3) two full copies of the skill; (4) additive client
  branch in `SKILL.md` that routes Claude Code to `references/claude-code.md`.
- Chosen: (4). Codex text stays byte-identical, the Claude rules live in one
  reference, and shared rules are not duplicated.
- Tradeoffs / Risks: Codex still receives the small branch section and the
  inert reference on its next sync. Option (3) would duplicate about 370 lines
  that drift; option (2) would split delegation authority across two skills.
- Evidence: local verification 2026-10-10 — the relay agent ran in Claude Code
  desktop and returned GLM-5.3 output; registry parity tests require the new
  reference to be registered.
- Supersedes: None.

## D002 — Coverage of the other native GLM gates

- Date: 2026-10-10T03:47:00+07:00 (decided 2026-10-10T04:20:00+07:00)
- Status / Owner: decided by user; Claude Code
- Context: Review pass 1 found that `task-execution-flow` (SKILL.md:272-287)
  decides whether `automatic-execution-delegation` is entered and
  `task-review-investigate-compare` (SKILL.md:109-129) owns the independent
  review pass; both check the native catalog themselves. Changing only
  `sow-delegate-flow` leaves both coordinator-only in Claude Code.
- Options: (a) explicit delegation only; (b) add the Claude Code pointer to
  both gates in this SOW; (c) a follow-up SOW for (b).
- Chosen: (b). User: "tự động làm khi cần, và chỉ được phép kích hoạt dưới dạng
  sub-agent 1 level, không được nested delegate, không được codex > claude -p >
  glm". The existing mandatory gates apply unchanged once the exact target is
  available.
- Tradeoffs / Risks: widens the change to two more shared skills (additive
  pointers only; `task-execution-flow` carries user WIP, so only this hunk is
  staged) and makes GLM calls mandatory for safe slices and review passes in
  Claude Code, with their time and relay cost.
- Evidence: review pass 1 plus coordinator check of the cited lines; user decision.
- Supersedes: None.


## D003 — Effort evidence as a prerequisite

- Date: 2026-10-10T03:47:00+07:00
- Status / Owner: proposed; Claude Code
- Context: The exact target is `greennode/glm-5.3` at max effort, and the
  Failure Evidence Contract (SKILL.md:310-315) requires the delegate to return
  its reasoning effort. The relay status line reports model and result but not
  effort.
- Options: treat effort as an installation detail; require the status line to
  report it.
- Chosen: require `effort=max` in the status line (prerequisite P1, made in the
  relay outside this repository); missing evidence is `native-unavailable`
  with reason `max effort unsupported`.
- Tradeoffs / Risks: adds one small change outside this repository before
  implementation.
- Evidence: review pass 1 finding; SKILL.md:75 and 310-315.
- Supersedes: None.

## D004 — One-level delegation only; no GLM from delegated processes

- Date: 2026-10-10T04:05:00+07:00 (revised 2026-10-10T04:20:00+07:00)
- Status / Owner: proposed; constraint set by user in D002; Claude Code
- Context: Codex delegates to Claude Code through a fresh `claude -p` process
  (sow-delegate-flow SKILL.md:139-162). A probe with Codex's read-only flags
  showed the child has the Task tool and the `glm-worker` agent, so Codex's
  explicitly selected Claude work could be re-delegated to GLM. The user
  forbids any nesting, including Codex -> `claude -p` -> GLM.
- Options: (1) instruction-level guard only; (2) relay refusal by
  `CLAUDE_CODE_ENTRYPOINT`; (3) relay refusal by process ancestry plus the
  instruction-level guard.
- Chosen: (3). Probe 2026-10-10: a `claude -p` child inherited
  `CLAUDE_CODE_ENTRYPOINT=claude-desktop`, so (2) cannot tell the cases apart.
  The desktop session's ancestors are `claude --input-format stream-json`
  (no `-p`) and the Claude app; a Codex delegate has a `claude -p` and a Codex
  process above it. The relay refuses on either signal (prerequisite P2).
- Tradeoffs / Risks: ancestry can be bypassed by a launcher that hides `-p`
  or the Codex process name; the instruction guard and the delegate-context
  probe remain as second layers. Non-interactive `claude -p` sessions started
  by the user can no longer use the relay.
- Evidence: probe outputs above; GLM delegate already restricted to file
  tools, so it cannot recurse.
- Supersedes: earlier D004 text (instruction-level guard only).

## D005 — Relay progress evidence (P3)

- Date: 2026-10-10T04:20:00+07:00
- Status / Owner: approved with the SOW; Claude Code
- Context: The relay wrote its event stream only after the delegate finished,
  so the 540 s timeout during draft review left no evidence, and the parent
  could not see progress during long calls. Printing progress to stdout does
  not help: tool output reaches the parent only after the command ends, and
  extra text invites the relay agent to paraphrase.
- Options: progress on stdout; progress written to files during the run.
- Chosen: files. The relay prints its run directory first, writes
  `stream.jsonl` and a per-tool-call `progress.log` incrementally, and kills
  the whole delegate process group on timeout.
- Tradeoffs / Risks: one more stdout line for the relay agent to ignore.
- Evidence: timed-out pass-2 attempt; user question on progress visibility.
- Supersedes: None.
