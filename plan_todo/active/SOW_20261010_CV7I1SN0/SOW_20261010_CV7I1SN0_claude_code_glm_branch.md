# SOW_20261010_CV7I1SN0 — Claude Code GLM Branch For Delegation Skills

- Status: APPROVED
- Approval: approved by user ("approve, làm giúp tôi cẩn thận"); D002 decided by user: automatic, one level only
- create_dttm: 2026-10-10T03:38:24+07:00
- approve_dttm: 2026-10-10T04:13:38+07:00
- finish_dttm: null
- Proposed-By: Claude Code (claude-opus-5-5)
- plan: Standalone; follows local glm-worker setup verified 2026-10-10
- Decision Log: SOW_20261010_CV7I1SN0_decision.md

## Task / Why

Add an additive Claude Code client branch to `sow-delegate-flow`,
`task-execution-flow` and `task-review-investigate-compare` so a top-level
Claude Code session treats a locally installed `glm-worker` agent as its native
`greennode/glm-5.3` max-effort role, one level deep only, while every Codex
path stays byte-identical.

Claude Code desktop can delegate to GLM-5.3 at max effort through a user-level
`glm-worker` relay agent, but the three skills that own GLM decisions only
inspect the native catalog and have no rule mapping that agent to the exact
target, so Claude Code keeps all work local. The user decided (D002) that
Claude Code uses it automatically under the existing gates, and only as a
single-level sub-agent of the top-level session.

## Prerequisites (relay, outside this repository)

- P1 effort evidence: the relay status line reports `effort=max`; without it
  the role is `native-unavailable` with reason `max effort unsupported` (D003).
- P2 depth guard: the relay refuses to run when any ancestor process is a
  Codex process or a non-interactive Claude Code process (`-p` / `--print`).
  A refusal is reported as `native-unavailable` (interface unsupported) and the
  caller works itself (D004).
- P3 progress evidence: the relay prints its run directory first and writes the
  event stream and a progress log incrementally, so timeouts keep evidence.

P1-P3 are made and verified in the relay's own repository before
implementation here, following that repository's rules (changelog fragment,
scoped commit).

## Location / Deliverables

- `skills/sow-delegate-flow/SKILL.md`: add one `## Client Branch` section only.
- `skills/sow-delegate-flow/references/claude-code.md` (new): the single
  Claude Code reference used by all three skills.
- Each pointer only routes ("Claude Code: see ...") and makes no availability
  claim; availability is decided by the reference's status-line evidence, so
  the existing anti-alias lines in those sections stay authoritative.
- Pointer wording in both gates follows the existing cross-skill pattern:
  locate `sow-delegate-flow` through the harness's supplied skill
  location/catalog and read `references/claude-code.md`; if it cannot be
  located, the gate keeps its current Claude Code behaviour.
- `skills/task-execution-flow/SKILL.md`: add one short Claude Code pointer in
  the Mandatory GLM-5.3-max Delegation Gate only (file carries user WIP; stage
  only this hunk).
- `skills/task-review-investigate-compare/SKILL.md`: add one short Claude Code
  pointer in the Mandatory Review Contract only.
- `tests/skill_feedback_cases/sow-delegate-flow.json`,
  `task-execution-flow.json`, `task-review-investigate-compare.json`: one new
  case each (expected / negative / boundary).
- `skills/registry.json`: add the new reference file entry; stage only this hunk.
- This SOW bundle and its decision log.

No existing line in any of the three skills is edited or removed.

## As-Is / To-Be

```text
As-Is
Claude Code -> any GLM gate -> catalog lists "glm-worker"
            -> no rule maps it to greennode/glm-5.3 max -> coordinator-only work

To-Be
client -> GLM gate (execution / review / explicit delegation) -> Client Branch
  Codex       -> existing lines byte-identical; Codex behaviour unchanged
  Claude Code -> read sow-delegate-flow/references/claude-code.md
    top-level session?  no (delegate of Codex or of another Claude) -> work itself
    glm-worker in catalog?  no -> native-unavailable -> local, as today
    yes -> one-level sub-agent call: self-contained task, read | edit (approved scope)
        relay (P2): ancestor is Codex or `claude -p`?  yes -> refused -> local
        status line: model=...greennode/glm-5.3, effort=max, ok=True ?
          no  -> delegation failure -> existing failure/fallback rules
          yes -> read result file -> coordinator verifies (delegate has no shell)

Allowed:   Claude Code (top-level) -> glm-worker -> GLM (file tools only)
Forbidden: Codex -> claude -p -> glm-worker ; Claude sub-agent -> glm-worker ;
           GLM -> any further delegation
```

## Reference Content (claude-code.md)

- Scope guard: applies only to the interactive top-level Claude Code session
  the user works in (desktop or terminal). A non-interactive `claude -p`
  session, a Claude Code process started as another coordinator's delegate
  (for example Codex's documented `claude -p` transport) and any Claude
  sub-agent never call `glm-worker` or the relay directly; they do the
  assigned work themselves. The relay's P2 guard enforces this
  deterministically for separate processes. In-session sub-agents share the
  session's process tree and environment (verified 2026-10-10), so for them
  the rule is instruction-level only.
- Identification: the `glm-worker` agent type is in the Claude Code agent
  catalog. Acceptance requires the returned status line to name
  `greennode/glm-5.3`, `effort=max` and `ok=True`; any mismatch or missing
  field is a failed handoff, never an alias match. Catalog absence or a P2
  refusal is `native-unavailable`.
- Not a Claude delegation: the relay runs the Claude Code CLI harness with the
  GLM model. It is the native GLM role, not the Claude External Transport, so
  the Claude self-delegation guard (no new Claude-model session from a Claude
  coordinator) does not block it; the one-level scope guard above does.
- Gates: the existing execution gate, review independent pass and explicit
  delegation rules apply unchanged; this reference only answers "is the exact
  target natively available in Claude Code, and how is it called".
- Delegate return fields (sow-delegate-flow SKILL.md:315-319): model id,
  reasoning effort and availability come from the status line; transport,
  lifecycle and isolation from the relay's fresh non-persistent process;
  independent pass, changed files, verification performed, remaining risks and
  pending decisions come from the result file, with changed files and
  verification confirmed by the coordinator (working-tree diff and its own checks).
- Isolation: each call is a fresh non-interactive process with no history; the
  prompt is self-contained (working directory, goal, allowed files, done criteria).
- Modes: `read` by default; `edit` only for an approved SOW write scope. The
  delegate has file tools only (no shell, no sub-agents), so verification
  commands always run in the coordinator.
- Result: the relay returns one status line; the coordinator reads GLM's
  original answer from the named result file and treats it as handoff
  evidence, not completion. Long calls may run in the background and be
  followed through the relay's progress log (P3).
- Parallelism: non-overlapping write scopes only, as in the existing rules.

## Done Criteria

- P1-P3 verified in the relay: status line shows `effort=max`; a run from the
  desktop session is accepted; a run under `claude -p` and a run with a Codex
  ancestor are refused; a forced timeout leaves `stream.jsonl` and the
  progress log on disk.
- Each of the three `SKILL.md` diffs is additive only.
- Negative checks: the Codex arm of the Client Branch states "no change" and
  does not name `references/claude-code.md`; the two pointers mention only
  Claude Code; the Codex-to-Claude transport section is unchanged.
- Delegate-context probe: Codex's documented read-only Claude command
  (sow-delegate-flow SKILL.md:160-162) with a delegation-shaped review task,
  run after the Claude sync, produces no `glm-worker` / Task call and is
  answered by the selected Claude model.
- In-session probe: a Claude sub-agent given a delegation-shaped task in a
  synced top-level session does not call `glm-worker` or the relay.
- New text avoids the forbidden phrases in
  `tests/test_mandatory_delegation_contract.py:38-41` and stale wording
  ("optional", "when suitable") for GLM-5.3 cases; feedback cases follow
  `tests/test_skill_feedback_cases.py` with no private paths.
- `test_mandatory_delegation_contract.py`, `test_skill_feedback_cases.py`,
  `test_skill_sync_scripts.py`, `test_plan_contract_integration.py` pass.
- Sync only to Claude: `sync_env_claude.py` with `--overwrite` for the three
  skills; `verify_skill_copy.py` against `~/.claude/skills` passes.
- `sync_env_codex.py` is not run; `~/.codex/skills` is unchanged (hash before/after).
- `git diff --check` passes; commit contains only this SOW's files and hunks.

## Out-of-Scope

Existing lines of the three skills; any `agents/openai.yaml`;
`task-router-flow` and other user WIP; `~/.codex/**`; the relay beyond P1-P3;
installation of `glm-worker` on other machines.

## Cautions / Risks

- Native-only enforcement is preserved: `glm-worker` is part of Claude Code's
  own agent catalog, so no external router, CLI or credential is searched.
- The existing gates are mandatory, not discretionary: once the exact target
  is available, Claude Code must delegate every safe bounded slice and run the
  review independent pass. Each call costs one relay run plus GLM time
  (a review pass took about 2.5 to 4 minutes; one timed out at 540 s).
- In-session nesting (top-level -> Claude sub-agent -> `glm-worker`) has no
  deterministic guard: sub-agents have the Agent and Bash tools and the same
  environment as the top-level session (verified 2026-10-10). The scope guard
  and the in-session probe are the controls.
- P2 relies on process ancestry; a new launcher that hides `-p` or the Codex
  process name would bypass it. The instruction-level scope guard remains the
  second layer, and the delegate-context probe checks both.
- Codex receives the additive sections and the inert reference on its next
  manual sync; the Codex arm must read as "no change".
- AI-skills is a public repository: the reference names no personal paths,
  internal hostnames, account names, secrets, relay topology or prices.
- `task-execution-flow/SKILL.md` and `skills/registry.json` carry uncommitted
  user work; stage only this SOW's hunks.
- Machines without `glm-worker` fall back to the current coordinator-only
  behaviour.

## Verification / Closeout

Pending implementation.

Review summary (draft stage): two independent reviews by native GLM-5.3 max
through the relay, each a fresh process with no prior history, plus a
coordinator check of every cited line. Pass 1: needs-changes (scope coverage,
effort evidence, Codex negative check, field shape); fixes produced D002, D003
and P1. Pass 2: approve-ready pending D002, three Low findings, two applied;
combined Task/Why and Location/Deliverables headings match approved SOWs here.
The first pass-2 attempt timed out at 540 s; a narrower retry completed.
Final Codex-impact review found the indirect Codex -> `claude -p` ->
`glm-worker` path (D004). The user then decided D002 (automatic, one level
only), which added the two gate pointers and the P2 depth guard (D004); P3
progress evidence is recorded in D005. Final review (native GLM-5.3 max via
the relay): one Medium (in-session sub-agent path) and four Low wording and
traceability findings, all applied.
