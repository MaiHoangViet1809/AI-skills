# SOW_20261001_ZJDHWCVU_EXT_U8XRPS06 - Mandatory Available GLM-5.3-max Delegation

- Status: COMPLETED
- Approval: APPROVED by user
- create_dttm: 2026-10-05T01:57:59+07:00
- approve_dttm: 2026-10-05T02:45:09+07:00
- finish_dttm: 2026-10-05T02:58:16+07:00
- legacy_id: SOW_0096_EXT_01
- legacy_path: plan_todo/finished/SOW_0096_EXT_01_mandatory_glm53_delegation.md
- migrated_dttm: 2026-10-08T12:48:51+07:00
- legacy_title: SOW_0096 EXT_01 - Mandatory Available GLM-5.3-max Delegation
- Parent: [SOW_20261001_ZJDHWCVU](SOW_20261001_ZJDHWCVU_task_execution_delegate_preference.md)

## Preserved Contract And Historical Evidence

- **Status**: COMPLETED
- **Approval**: APPROVED by user
- **create_dttm**: 2026-10-05T01:57:59+07:00
- **approve_dttm**: 2026-10-05T02:45:09+07:00
- **finish_dttm**: 2026-10-05T02:58:16+07:00
- **Proposed-By**: Codex
- **plan**: None; bounded extension of SOW_0096
- **Parent**: [SOW_0096](SOW_20261001_ZJDHWCVU_task_execution_delegate_preference.md)

## Task

Replace optional delegation/suitability skipping with mandatory delegation to
available exact `greennode/glm-5.3` at `reasoning_effort=max` in execution and
review flows. Local fallback is permitted only for confirmed unavailability
or an actual delegation failure, with evidence.

## Why / Baseline

The user clarified that seeing GLM-5.3-max in the current model catalog must
cause delegation, not merely model priority after an optional suitability gate.
Current execution instructions and metadata allow local work for simple or
unsuitable tasks; review permits skipping routine independent passes. These
are canonical contract gaps, not installed-copy drift.

Follow `AGENTS.md` and `skill-evolution-flow`: explicit approval before
behavior-bearing edits, DRY/KISS, isolated bounded ownership, scoped commits,
and evidence-labelled verification. No concept authority is declared here.

## Location

- `skills/task-execution-flow/SKILL.md` and `agents/openai.yaml`
- `skills/sow-delegate-flow/SKILL.md` and `agents/openai.yaml`
- `skills/task-review-investigate-compare/SKILL.md` and `agents/openai.yaml`
- Matching three files under `tests/skill_feedback_cases/`
- `tests/test_mandatory_delegation_contract.py` (new)
- This extension and its parent SOW_0096, including lifecycle/reference updates

## As-Is Diagram (ASCII)

```text
task -> optional suitability / independent-pass trigger
     -> skip as simple/unsuitable -> local
     -> choose delegation -> available GLM-5.3-max first
```

## To-Be Diagram (ASCII)

```text
task -> scope/authority preflight -> current exact-model availability
     -> available -> bounded isolated GLM-5.3-max delegation
                    -> success -> coordinator verifies and closes
                    -> actual failure -> evidence -> local fallback
     -> unavailable -> evidence -> local fallback
```

## Deliverables / Behavior Locks

1. For a task entering execution or review, the main coordinator MUST delegate
   a meaningful bounded task/review slice when exact GLM-5.3-max is available.
   Simplicity, mechanical edits, suitability, token/latency cost, or an optional
   independent-pass trigger are not reasons to skip. Do not fabricate a trivial
   handoff merely to claim compliance while doing the delegated work locally.
2. Check the current native catalog/list-models or documented provider catalog
   for exact model and supported `max` effort. Flash/third-party variants,
   aliases and historical availability do not qualify. Use the native role
   when registered; otherwise use an available documented transport, not a
   guessed CLI or invented provider setup.
3. Only confirmed target unavailability or an observed delegation failure
   permits automatic local fallback. A delegation failure means a confirmed
   launch, transport, session, or isolation error; terminal child failure; or
   delegate output that fails the bounded task/evidence contract after the
   allowed repair rounds. Record the failed stage, concrete error or capability
   evidence, task impact, and fallback decision. A blocked transport or failed
   isolation preflight is a failure only when a concrete check establishes it;
   never turn suitability judgement into an invented failure. If coordinator
   verification is missing because an external runtime/evidence path is
   unavailable, keep the task unverified and stop rather than silently execute
   locally. Clean up failed task-owned sessions and discard invalid output.
   Existing bounded repair/wait rules remain, without unbounded retries.
4. Keep approval, secret-safety, exact scope, non-overlapping ownership, native
   `fork_turns: none`, fresh external sessions and coordinator verification.
   Shape a safe bounded slice rather than skip delegation. If no safe authorized
   slice exists, stop for scope/authority clarification; do not leak context or
   call this a successful delegation/local fallback. Reviews may delegate
   read-only before implementation approval. Children are not required to
   spawn nested children; this decision belongs to the main coordinator.
5. A later explicit human instruction selecting another model/transport or
   local-only execution supersedes the default for that named task. Record it
   as a user override, never as an agent-chosen third fallback exception.
   Explicit delegation requests still stop/ask on failure unless the user
   authorizes fallback; do not silently replace the requested transport/model.
6. Keep one owner: execution/review decide and invoke; `sow-delegate-flow`
   owns transport, prompts, isolation and cleanup. Coordinator preflight,
   verification, writeback, approval handling and commit remain local duties,
   not reasons to bypass the required delegated slice. No delegate per tool
   call, overlapping workers, provider/config changes or new orchestration.
7. Align discovery metadata and existing fixtures in place. Remove conflicting
   effective optional/suitability/skip assertions rather than append a
   contradictory MUST section. Preserve unrelated optional-plan contracts.

## Done Criteria

- Completion is canonical-only: verified repository changes, not installed
  runtime adoption. Do not claim Codex/Claude active copies use the new rule
  until a separately user-authorized sync and installed parity check complete.
- All three skills and metadata consistently require delegation when the exact
  target is available; no autonomous simple/routine/suitability skip remains.
- Expected/negative/boundary cases cover: available trivial task and review;
  missing model; Flash-only catalog; real launch/runtime/isolation failure;
  invalid delegate output or failed coordinator verification; user override;
  unapproved implementation; unsafe context; no nested support;
  successful handoff followed by failed coordinator verification.
- Deterministic tests assert the branch/exception/metadata contract and existing
  fixture schema. Run all three structural validators and
  `uv run python -m unittest tests.test_mandatory_delegation_contract
  tests.test_plan_contract_integration tests.test_skill_feedback_cases
  tests.test_skill_sync_scripts`; JSON/YAML parsing and diff checks pass.
- Exercise one actual bounded read-only GLM-5.3-max delegation when available;
  record exact role/model/effort, fresh context, result, coordinator verification
  and cleanup. Live availability absence is recorded, not simulated as live
  success. Unavailable/error branch fixtures are deterministic evidence only;
  one successful run does not prove universal model adherence.
- Gap-check the final diff against this extension, remove conflicting old
  assertions, preserve unrelated work, and commit only verified scoped changes.
- Only after explicit extension approval, reopen the parent to active status
  and clear its top-level `finish_dttm`; preserve base approval and historical
  evidence. At verified completion, finish extension and parent, move this
  extension to matching `finished/`, and repair references.

## Verification Evidence

- **Structural checks** (`2026-10-05T02:57:14+07:00`): `uv run --no-sync
  --offline python -m unittest tests.test_mandatory_delegation_contract
  tests.test_plan_contract_integration tests.test_skill_feedback_cases
  tests.test_skill_sync_scripts` passed with `25` tests; JSON/YAML parsing and
  `git diff --check` passed.
- **Actual delegation**: a bounded implementation slice and a separate
  read-only closeout review used native exact `greennode/glm-5.3` with
  `reasoning_effort=max` and `fork_turns: "none"`; both used clean task-local
  prompts, returned scoped evidence, and were cleaned up by the coordinator.
- **Gap finding and repair**: the read-only review found one Medium fixture
  wording gap; it was repaired before closeout.

| Severity | Finding | Impact | Solution |
| --- | --- | --- | --- |
| Medium | `automatic-execution-delegation-001` still used `suitability reason` and `suitability decision`. | The fixture retained legacy optional/suitability language and the contract test could miss that drift. | Replace both phrases with availability/mandatory-decision wording and assert both legacy phrases are rejected. |

- **Post-implementation gap check**: contract complete; expected, negative, and
  boundary fixtures cover availability, Flash-only, failure, invalid output,
  coordinator verification, user override, unsafe/unapproved scope, isolation,
  cleanup, read-only review, and no nested delegation. No remaining actionable
  gaps found.
- **Negative check**: a stale optional/suitability phrase or missing exact-model
  effort would fail the deterministic contract test; installed Codex/Claude
  adoption remains intentionally unverified because sync is out of scope.

## Out Of Scope

- Implementation before extension approval; this request authorizes drafting.
- Global Codex/Claude sync, push, provider installs/catalog/config changes,
  credentials, new transports, nested-agent workarounds or benchmarks.
  Sync requires a separate explicit deployment request; this extension does
  not grant installation authority or require a new SOW merely for that sync.
- Changes to SOW/optional-plan policy, verification or safety gates, project
  code, unrelated dirty files, or rewriting completed SOW_0095 history.
  The mandatory rule does not apply when the exact target is unavailable or no
  safe authorized slice can be defined; those cases stop or use only the
  evidence-backed fallback defined above.

## Cautions / Risks

- Mandatory delegation costs tokens/latency even for small tasks; that tradeoff
  is requested, not an autonomous reason to revert to preference.
- SOW_0096's original approved preference remains historical. This approved
  extension supersedes it; old timestamps are not authority for the new
  contract. The parent was reopened for this extension and the canonical
  implementation and verification evidence are now recorded here.
- Avoid moving policy ownership into multiple copied workflows. State the
  mandatory gate briefly and reuse the existing delegate lifecycle.
- Guardrails cannot be waived by model availability. A safety stop is not an
  undocumented permission to execute locally or a fake provider failure.

## Plan / Reference

- [Parent SOW_0096](SOW_20261001_ZJDHWCVU_task_execution_delegate_preference.md)
- [Prior model/isolation contract](../SOW_20261001_UTAQGE14/SOW_20261001_UTAQGE14_skill_delegate_review_glm53_preference.md)
- [Execution skill](../../../skills/task-execution-flow/SKILL.md)
- [Delegate skill](../../../skills/sow-delegate-flow/SKILL.md)
- [Review skill](../../../skills/task-review-investigate-compare/SKILL.md)

## Decision

Extend SOW_0096 rather than create unrelated scope. Model availability now
drives a mandatory task-level handoff, not an optional suitability preference.
Use the existing three skills and regression mechanisms; no new framework.
