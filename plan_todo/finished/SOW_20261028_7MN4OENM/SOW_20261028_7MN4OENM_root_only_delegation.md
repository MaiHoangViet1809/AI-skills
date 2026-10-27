# SOW_20261028_7MN4OENM — Root-only delegation, leaf-only workers

- Status: DONE
- Approval: approved by user
- create_dttm: 2026-10-28T02:27:50+07:00
- approve_dttm: 2026-10-28T02:31:15+07:00
- finish_dttm: 2026-10-28T02:35:22+07:00
- Proposed-By: Codex
- Plan / Reference: standalone; skill-evolution-flow; SOW_20261006_TXV92GQG; SOW_20261010_WU8AQ6UW

## Task

Make delegation and advisor dispatch root-coordinator-only across the four
AISkills workflow skills; every delegated worker/reviewer/advisor is a leaf
and reports oversized scope or escalation needs to its parent/main coordinator.

## Why / Evidence

- A routed worker created a nested worker during a diagnostic implementation.
  This is an observed failure, not permission to reproduce it in the active task.
- `skills/sow-delegate-flow/SKILL.md` mandates delegation for complex work but
  has no general root-only entry guard. Its failure contract says a delegate
  is not required to spawn nested children, which does not prohibit the action.
- Execution and review callers can apply their complexity gate inside a child.
- `task-escalation-flow` dispatches advisors without first excluding children.
- The Claude Code reference already has a one-level guard; generalize the
  policy without removing its transport-specific restrictions.
- Installed and canonical `sow-delegate-flow/SKILL.md` matched at inspection.
  `task-execution-flow/SKILL.md` differs due to concurrent canonical Redmine
  additions. Preserve that work; this is not evidence that it caused recursion.
- Router-generated agent prompts and runtime nesting controls are separate
  enforcement surfaces, outside this AISkills change.

## Authority / Design Principles

Repository `AGENTS.md` governs approval, surgical edits and verification.
No project concept authority or PRODUCT_PRINCIPLE_DESIGN.md was found in the
inspected repository. Apply DRY/KISS: one canonical delegation policy in
`sow-delegate-flow`, with short guards at the three dispatch decision points.
Do not add a process monitor, persistent role registry or new orchestration layer.

## As-Is Diagram (ASCII)

```text
Main -> worker -> reads complex-task / escalation rule
                 -> native child OR external agent process
                    -> possible further delegation
Claude-specific path has a guard; other paths are not uniformly guarded.
```

## To-Be Diagram (ASCII)

```text
Main/root coordinator
  |-> worker [leaf]   -- oversized/blocker + evidence --> main
  |-> reviewer [leaf] -- extra review needed ---------> main
  `-> advisor [leaf]  -- unresolved question ----------> main

Main chooses: resize scope / dispatch another bounded leaf / finish locally.
Every leaf: no native spawn, agent CLI/process, MCP/task handoff or indirect
delegation; no authority gained from naming itself a coordinator.
```

## Location / Deliverables

Allowed implementation files after approval:

- `skills/sow-delegate-flow/SKILL.md`: canonical root/leaf guard, prompt and
  result contract, prohibition of alternate-transport bypass.
- `skills/sow-delegate-flow/references/claude-code.md`: align report-to-main
  behavior while preserving existing one-level and file-tool restrictions.
- `skills/task-execution-flow/SKILL.md`: guard before automatic delegation.
- `skills/task-review-investigate-compare/SKILL.md`: guard before independent
  reviewer dispatch.
- `skills/task-escalation-flow/SKILL.md`: child requests escalation from main;
  root alone dispatches and consumes advisor passes.
- The four skills' existing `agents/openai.yaml`: change only if their
  default_prompt/discovery metadata conflicts with the corrected rule.
- `tests/skill_feedback_cases/sow-delegate-flow.json`
- `tests/skill_feedback_cases/task-execution-flow.json`
- `tests/skill_feedback_cases/task-review-investigate-compare.json`
- `tests/skill_feedback_cases/task-escalation-flow.json`
- This SOW bundle for progress and verification evidence.

No other implementation paths are authorized. Do not modify registry or sync
tooling merely because their files are nearby or currently dirty.

## Behavioral Contract

1. Check agent role before complexity/model discovery/dispatch. Reliable host
   child identity and a task explicitly assigned by a parent establish leaf
   status; do not require a fabricated API or environment variable.
2. A child never delegates, including to a stronger read-only advisor or via a
   different provider, external CLI/process, MCP or separate task/thread.
   Read-only file/search/check tools are not delegation and remain permitted.
3. A child encountering oversized scope, missing authority or a genuine blocker
   returns the exact blocker, evidence, completed scope and proposed split or
   advisor question to its parent/main through the existing authorized channel.
   This rule does not grant cross-thread messaging permission. If no channel
   exists, return the request in its result; do not create another session.
4. Stop only the blocked slice; safe independent work inside the assigned scope
   may continue. Do not silently widen scope or wait indefinitely for a child.
5. Root keeps existing approved delegation behavior, clean contexts, bounded
   ownership, verification and terminal cleanup. Root may dispatch multiple
   bounded leaves when authorized; this is not a blanket single-agent limit.
6. Every delegation prompt states leaf-only status and report-back behavior.
   Unknown role does not authorize dispatch: resolve from existing harness/task
   evidence or report uncertainty. Existing read-only work need not halt.
7. A user request reaching a child to seek more help is reported to main, not
   treated as permission for recursive delegation under this contract.
8. User-approved exception (2026-10-28): ignore the existing Haiku transport
   hop. Preserve `root -> Haiku glm-worker -> fixed glm-run -> GLM` unchanged;
   the relay forwards exactly one assigned task, cannot select further helpers
   or split scope, and GLM remains a leaf. No other child inherits this exception.

## Implementation Sequence

- T1: Before skill edits, add sanitized stable feedback cases for each affected
  skill using the existing schema: expected, negative and boundary scenarios.
- T2: Patch the canonical owner, Claude reference and the three callers in
  place; reconcile metadata only if necessary. Preserve concurrent Redmine edits.
- T3: Validate structure, feedback/sync tests, caller coverage and negative
  scenarios. Record policy evidence separately from real model/tool behavior.
- T4: Review diff and stage only task-owned changes; commit following repo
  policy. No push or installed-environment sync is authorized by this SOW.

## Done Criteria

- All four dispatch paths apply leaf exclusion before mandatory delegation or
  escalation; shared policy is referenced rather than copied wholesale.
- Expected: root can dispatch bounded leaves and verify their results.
- Negative: child facing complex work cannot spawn a native grandchild or use
  an external process/task as a bypass; advisor cannot dispatch another advisor.
- Boundary: unknown role does not assume root, root can perform sequential
  advisor tiers, child can run ordinary tools and report to parent without
  unauthorized cross-thread messaging, Claude restrictions remain intact.
- Use available skill-creator structural validator on changed skills and run
  `uv run python -m unittest tests.test_skill_feedback_cases tests.test_skill_sync_scripts`.
- Run `git diff --check`; inspect every direct dispatch caller in the declared
  four-skill scope and relevant prompt metadata.
- Existing schema/structural tests and scenario review must not be presented
  as proof that runtime physically blocks tool invocation. Live host/model
  adherence remains UNVERIFIED unless separately authorized and exercised.
- Before commit, exclude unrelated staged paths and preserve concurrent edits
  to shared files; stage only owned hunks. Do not reset or discard other work.

## Out-of-Scope

- Editing codex-router, managed agent definitions or Codex runtime/configuration.
- Runtime max-depth changes, permission changes, agent launch, live delegation
  tests, main-thread agent interruption, remote benchmark or existing-task changes.
- Installed skill sync, global installation, push, Redmine writes or task mapping.
- Changing model selection, complexity thresholds, approval gates or allowed
  root delegation transports beyond the root/leaf distinction.

## Cautions / Risks

- Prompt policy is not hard tool enforcement. Runtime/router hardening requires
  separately authorized work; the result must not claim recursive spawn is
  technically impossible after this skill-only patch.
- Clean `fork_turns: none` context does not establish root identity or grant
  delegation permission. Include explicit leaf status in the bounded prompt.
- Removing mandatory delegation globally would break legitimate root workflow;
  the correction is role-aware, not a global delegation ban.
- Installed drift and concurrent Redmine additions must not be overwritten.

## Self-review (one pass)

Completed by Codex, without sub-agents, per explicit user request and the side
conversation restriction. Review/writeback only; not implementation approval.

- Clarified that skills enforce policy, not runtime permissions; excluded
  unsupported claims of hard prevention and changes outside AISkills.
- Closed external CLI/task/advisor bypasses and unknown-role ambiguity.
- Kept valid root dispatch, child ordinary tools, safe partial progress and
  existing cross-thread authorization boundaries intact.
- Scoped deployment out; identified concurrent canonical Redmine edits for
  preservation. No remaining blocking design finding in this scoped proposal.
- Real host adherence and installed parity remain unverified, not SOW blockers
  disguised as successful tests.

## Progress

- progress_updated_dttm: 2026-10-28T02:35:22+07:00

| Item | Status | Evidence / Pending reason | Next action / Owner |
| --- | --- | --- | --- |
| P0: Draft and self-review | DONE | Four-skill rules inspected; user approved implementation and narrow Haiku exception | None |
| T1: Feedback cases | DONE | Added four stable root-only cases, each with expected/negative/boundary scenarios before skill edits; schema tests pass | None |
| T2: Skill correction | DONE | Four entrypoints, reference and prompt metadata patched; fixed Haiku relay explicitly excepted by user; Redmine WIP preserved | None |
| T3: Verification | DONE | 13 tests/four validators passed; affected feedback test and owner validator passed after exception; source double-check complete | None |
| T4: Scoped commit | DONE | Approved scope verified; closeout commit contains only owned paths/hunks; deployment excluded | No sync or push |

## Implementation Verification / Double-check

- Execution stayed in this session: side-conversation restrictions prohibit
  sub-agents and the approved scope excludes live delegation tests.
- `uv run python -m unittest tests.test_skill_feedback_cases tests.test_skill_sync_scripts`:
  13 tests PASS. These validate case schema and sync-tool contracts, not model
  compliance with the new instructions.
- skill-creator `scripts/quick_validate.py`: PASS for all four changed skills.
- `git diff --check`: PASS after the skill patch.
- Negative source review found an execution-flow shortcut lacking an explicit
  leaf branch. Patched its core rule, flow and evidence values (`leaf-local`,
  `role-unresolved`) rather than pretending leaf status means model failure.
- Cross-transport double-check found a blocking premise gap missed in the
  initial SOW review: `skills/claude-code-glm-setup/assets/glm-worker.md`
  defines a Haiku agent whose sole task is calling `glm-run`, which launches
  the GLM process. Thus the existing route is physically
  `main -> Haiku relay agent -> GLM`, despite its one-level logical label.
- Initially proposed moving the fixed relay invocation into root; user instead
  explicitly accepted the existing special Haiku branch. This supersedes that
  proposal: preserve the asset/launcher unchanged and document only the narrow
  fixed-transport exception in the shared policy and Claude reference.
- Accepted tradeoff: physical Haiku-to-GLM relay nesting remains; no evidence
  of runtime hard blocking is claimed. Autonomous recursive delegation by
  workers/reviewers/advisors remains prohibited. No general relay exception.
- After the accepted exception, reran only affected feedback schema test (one
  test PASS) and shared-owner structural validator (PASS); unchanged prior
  sync-test and other validator evidence was retained. Final source review
  confirmed no general relay exception and all three callers guard dispatch.
- Before closeout staging, fetched origin and verified HEAD equals
  origin/main (0 ahead, 0 behind). Commit staging excludes pre-existing
  Redmine additions in the mixed execution skill and all other unrelated WIP.
- No runtime/tool-permission enforcement, live model behavior or installed
  parity was verified, as explicitly excluded from acceptance. No sync, push,
  main-thread mutation or changes to the Haiku asset/launcher occurred.
