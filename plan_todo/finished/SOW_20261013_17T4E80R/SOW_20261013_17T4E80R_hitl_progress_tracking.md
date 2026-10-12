# SOW_20261013_17T4E80R - HITL Progress Tracking

- Status: COMPLETED
- Approval: APPROVED by user; implement, double-check, commit, push and sync Codex/Claude.
- Proposed-By: Codex
- create_dttm: 2026-10-13T04:56:48+07:00
- approve_dttm: 2026-10-13T05:27:30+07:00
- finish_dttm: 2026-10-13T05:41:04+07:00
- plan: None; bounded standalone skill-contract change.

## Task / Why

Require persisted SOW/Plan progress before ending a turn that hands control
to a human. Show what is done, current status, why anything is pending and
the exact next action, instead of relying on chat-only summaries.

## Location

- `skills/task-router-flow/SKILL.md` and
  `references/{scope-of-work,plan}.md` in that skill.
- `skills/task-execution-flow/SKILL.md`.
- `skills/task-review-investigate-compare/SKILL.md`.
- `skills/task-progress-report/SKILL.md`.
- `skills/sow-delegate-flow/SKILL.md` (coordinator writeback ownership only).
- Corresponding five `agents/openai.yaml` files only if discovery wording changes.
- Corresponding five `tests/skill_feedback_cases/*.json` files;
  `tests/test_hitl_progress_contract.py` for focused contract checks.
- This SOW's lifecycle, progress and verification evidence.

## Preflight / Principles

- Inspected current templates and routing/execution/review/reporting rules.
  Plan updates sequence/acceptance after each SOW; SOW records lifecycle;
  execution calls progress reporting once at final closeout by default.
  None establishes a mandatory persisted progress gate before every HITL turn.
- This is a contract gap, not proof that a model failed to load a skill.
- No root principle document or declared concept authority found. Apply
  DRY/SOLID/KISS: one canonical progress contract in the SOW reference,
  linked by consuming skills; no external tracker or duplicate status store.
- Preserve concurrent dirty router/template/execution/registry/policy edits.

## As-Is / To-Be (ASCII)

```text
As-Is: work -> chat handoff -> human -> recover status from chat/files
To-Be: work -> reconcile owned progress + evidence -> save SOW/Plan
           -> concise handoff + requested decision -> human
           -> reread saved state before resuming
```

## Deliverables / Behavior Locks

1. SOW/EXT owns a compact current-state table, keyed to existing deliverables
   or done criteria, not tool calls. Respect a target project's declared
   progress contract first; the following is the packaged default, not authority
   to replace existing project statuses/trackers. Proposed minimum:

   | Item | Status | Evidence / Pending reason | Next action / Owner |
   | --- | --- | --- | --- |
   | <stable key: deliverable/check> | <state> | <proof or exact reason> | <action / role> |

   Record `progress_updated_dttm` with seconds and numeric timezone offset.
   Completed rows remain visible in the owning document; this does not change
   the chat report's open-items-only rule. Reuse an existing deliverable/check
   ID, or assign a unique document-local key in Item once; never renumber on
   reorder or reuse a key. The coordinator owns key allocation and writeback.
   Base SOW owns base rows; each EXT owns its delta rows. Parent/Plan aggregate
   rows link their evidence instead of duplicating detail. Draft EXT tracking
   does not amend approved base scope or reopen completed parents.
   Do not invent percentage estimates or derive task completion from row counts;
   chat percentages need a declared evidence-based denominator, otherwise N/A.
2. Item states: `PENDING`, `IN_PROGRESS`, `AWAITING_VERIFICATION`, `DONE`,
   `BLOCKED`, `WAITING_HITL`. Implementation without required verification is
   `AWAITING_VERIFICATION`, never `DONE`. Each non-done row states the actual
   reason and next action/owner; done rows link adequate completion evidence.
   PENDING means not started; IN_PROGRESS means active work; BLOCKED means an
   external/dependency impediment. Required human input/decision means
   WAITING_HITL, including when an external blocker also exists (record both
   in the reason). User-requested pause maps to WAITING_HITL with reason
   user-paused and next action user resume; stop the affected work, do not
   repeatedly prompt or silently resume. No new PAUSED lifecycle state.
   These item states neither replace lifecycle Status nor
   grant approval. DONE proves only that row's completion criteria, not
   aggregate SOW/Plan completion.
3. Before any HITL handoff turn (approval, scope decision, clarification,
   blocker requiring human input, review verdict awaiting decision, or final
   acceptance), reconcile and persist affected owning active records, including
   draft/pending records, completed work and requested human action. Draft SOWs
   must be updated before requesting approval. Record `WAITING_HITL` only for
   the item actually awaiting a human; retain independent work's truthful state. A review can be
   done while implementation remains pending approval. Never claim approval
   or completion from silence, a percentage, or a sub-agent's assertion.
   If readback/reconciliation confirms the existing progress, evidence and
   requested human action are current, the gate passes with no file change;
   update progress_updated_dttm only when persisted progress changes. At final
   closeout, save final progress before the existing lifecycle move; read the
   destination to verify it. Do not reopen finished history just for tracking.
4. Before resuming, reread the owning record and approval state. Delegates
   return item-level evidence; coordinator verifies and owns final writeback.
   Reread the document immediately before writeback; match its stable row key
   and expected prior content, patch only owned rows and
   preserve concurrent edits. If the owned row changed, reread and reconcile
   against current evidence; do not overwrite a stale snapshot. Unresolved
   ownership/conflicts abort writeback as UNSAVED. If documents cannot
   be safely written, report progress as UNSAVED plus reason and exact pending
   action; do not claim the persistence gate passed. UNSAVED is a handoff
   persistence outcome, not an item state; retain the actual work state.
   Read back the saved rows before claiming persistence. This is bounded
   conflict detection, not a guarantee of atomic writes or a new locking system.
   Locate the canonical contract through the harness/project authority; if
   missing, report dependent tracking unverified rather than inventing a
   contract, installing a skill or blocking unrelated exempt work.
5. Optional Plan reuses its SOW Sequence and Acceptance tables: add one
   `Pending reason / Next action / Owner` column to SOW Sequence; refresh affected
   SOW state and aggregate evidence in Acceptance's existing Result / Gap; link child
   evidence rather than copy child task lists. Child completion does not prove
   Plan completion. Record the Plan's progress_updated_dttm too. Do not create
   a Plan just for progress reporting.
6. New records receive the section; existing active records touched by a
   consuming agent receive it lazily with stable row keys. No rewriting
   finished history. No SOW is created solely for progress on an exempt task;
   use its existing authorized work record or a brief chat status when none.
7. Separate mandatory file writeback from `task-progress-report` invocation:
   preserve one default report at final closeout. HITL responses briefly show
   changed status, pending reason and human decision; no report per tool call
   or artificial turn, and no requirement to repeat unchanged tables in chat.

## Done Criteria

- Add sanitized expected/negative/boundary fixtures before skill edits:
  partial implementation + approval handoff; verified completion; review-only
  verdict; blocked dependency; no-SOW route; Plan aggregate partial completion;
  delegate evidence not yet verified; unwritable/concurrently edited record;
  user pause; dependency vs human wait; unchanged handoff; base vs draft EXT;
  missing contract and final progress preserved through the lifecycle move.
- Contract tests assert canonical ownership, state distinctions, mandatory
  pre-HITL persistence, pending reason/next action, resume reread, optional Plan
  preservation and one-default-report behavior. Skill validators and targeted
  tests pass; run the full available suite and inspect scoped mixed diffs.
- One isolated forward simulation from raw scenarios when native GLM-5.3-max
  is available; distinguish simulated adherence from actual host behavior.
- Negative check: handoff with stale persisted progress must not count as
  ready; implementation-only must not become DONE; no new approval inferred.
- Gap check and evidence recorded before closing. No unresolved blocking gap.

## Out Of Scope / Risks

- No historical migration, new Plan, runtime tracker, telemetry, MCP, Redmine
  writes, CLI, dependencies or changes to approval/delegation/lifecycle rules.
- Delivery authorization: scoped commit, push and sync the five changed skills
  to Codex and Claude after verification and double-check; no broader sync.
- Main risks: duplicated trackers, fake DONE, noisy reporting, concurrent
  overwrite. Mitigate with canonical contract, evidence gates, bounded owned
  writeback and separate document/chat semantics.
- Instructions and static tests cannot guarantee host/model adherence;
  behavior remains unverified without an exercised relevant path.

## Progress

- progress_updated_dttm: 2026-10-13T05:41:04+07:00

| Item | Status | Evidence / Pending reason | Next action / Owner |
| --- | --- | --- | --- |
| T1: Scope draft | DONE | Current contract inspected; scope and behavior locks recorded above. | None |
| T2: Draft review | DONE | Initial review plus two independent native GLM-5.3-max passes; resolutions below checked by coordinator. | None |
| T3: Skill implementation | DONE | Canonical contract and five consumers pass scoped verification below. | None |
| T4: Verification | DONE | 52 tests, five validators, three negative mutations and eight-case independent simulation pass; gap check found none. | None |
| T5: Delivery | DONE | Implementation commit pushed; five committed skills synced to Codex and Claude, 10/10 parity PASS. Delivery evidence below. | None |

## Draft Review / Baseline Evidence

- Isolated native GLM-5.3-max reviewed this draft without inherited chat;
  no source edits, nested delegation or runtime claims. Coordinator patched:
  explicit Plan column, draft-record HITL coverage and stale-write protection.
- `uv run --no-sync --offline python -m unittest discover -s tests -q`:
  47/47 PASS on the existing baseline, not verification of proposed skills.
  Whitespace check passed. Approval/implementation/behavior tests remain pending.

### Two Additional Independent Reviews

- Each pass ran in a fresh native GLM-5.3-max context with fork_turns:none,
  read-only ownership and no nested delegation. They reviewed the same draft
  independently; coordinator consolidated and patched their findings.
- Pass 1: stable row key/prior-content conflict check, UNSAVED as persistence
  outcome, human-vs-external blocker precedence, evidence-based chat percentages.
- Pass 2: user-pause mapping, base/EXT delta ownership, unchanged-handoff no-op.
  Human-vs-external blocker finding overlapped pass 1 and was resolved once.
- Coordinator additionally clarified target-project authority, lazy adoption,
  Plan timestamp, missing contract and final-move ordering. Updated Done Criteria
  carries these cases; no new runtime tracker/locking system or lifecycle state.
- Post-patch contract inspection and whitespace check passed; no remaining
  actionable blocker found in this review scope. This is approval-readiness
  review, not verification of implemented skill behavior. Still DRAFT/PENDING.

## Execution Evidence

- User approved exact scope and both sync targets; delivery follows verified
  source commit, push and committed-source sync. Approval above supersedes the
  historical draft-review state, not its evidence.
- Native GLM-5.3-max with fork_turns:none owned five fixtures and focused tests;
  fixtures-ready preceded all skill edits. Coordinator implemented the canonical
  gate and five callers, then strengthened checks for readback/row keys/unknown
  contracts and aggregate semantics. No nested delegation or shared write scope.
- Clean HEAD-based candidate excludes pre-existing Redmine/policy changes;
  `uv run --project <repo> --no-sync --offline python -m unittest discover -s tests -q`:
  52/52 PASS. All five skill structural validators PASS. Whitespace check PASS.
- Three normalized negative mutations reject missing persistence/readback,
  missing prior-row comparison, and chat-only completion. The initial mutation
  probe did not normalize wrapped text; corrected probe rejects all 3/3.
- Registry, policy/docs and untracked Redmine reference match pre-task snapshots.
  Discovery metadata remains accurate; no metadata or registry changes required.
- Independent native GLM-5.3-max raw-scenario simulation used a fresh context
  and task-only candidate without fixtures/goldens. Eight traces matched locks:
  draft approval, missing runtime environment, partial Plan integration, user
  pause/draft EXT, unchanged handoff, conflicting row, exempt/missing-contract
  routes, and unverified delegate -> verified bundle closeout. No actionable
  findings found. Coordinator checked final source/caller coverage and evidence.
- Gap checklist: contract/caller coverage complete; required edge cases and
  preservation covered; concurrency is explicitly best-effort, not atomic.
  No new runtime, dependencies, performance path or cleanup/logging ownership.
  No blocking gap. Actual weak-model/Claude-host adherence remains unverified;
  simulations and textual tests establish contract scope, not a universal
  adherence guarantee. Delivery evidence below closes the remaining owned work.

## Delivery / Closeout

- Implementation commit: `8e39f4599cc35790e998612c496b2c21e74252c8`, pushed
  successfully to origin/main. Actual staged allowlist was 13 source/test files
  plus this SOW; implementation bytes matched the tested clean candidate.
- Exported that committed revision, previewed only the five approved skills
  for both authorized targets, backed up installed copies, then used existing
  skill_sync_common.copy_skill and verify_skill_copy.compare_skill.
  Codex 5/5 and Claude 5/5 copies have no missing/extra/changed files.
- All progress rows are verified DONE; preserve final progress through the
  standalone bundle move to finished and read back the destination. Closeout
  documentation commit follows actual sync evidence, not a predicted result.
- Unrelated policy/Redmine/registry work remains unstaged and unchanged.
  No other installed skill was synced. Remaining limitation: actual host/weak
  model adherence is unverified; the approved contract/packaging checks passed.
