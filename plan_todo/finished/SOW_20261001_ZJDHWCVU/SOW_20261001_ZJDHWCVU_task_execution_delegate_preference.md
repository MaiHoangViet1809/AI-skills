# SOW_20261001_ZJDHWCVU - Task Execution Delegation Preference

- Status: COMPLETED
- Approval: User approved in the current task thread: "patch giúp tôi, sau đó implement, rồi commit, push"
- create_dttm: 2026-10-01T03:23:09+07:00
- create_date: 2026-10-01
- create_dttm_source: original_creation_datetime
- create_dttm_confidence: explicit
- create_dttm_evidence: `plan_todo/finished/SOW_20261008_VO3LKN0L/creation-date-evidence.json` (record: SOW_20261001_ZJDHWCVU)
- approve_dttm: 2026-10-01T03:47:20+07:00
- finish_dttm: 2026-10-05T02:58:16+07:00
- legacy_id: SOW_0096
- legacy_path: plan_todo/finished/SOW_0096_task_execution_delegate_preference.md
- migrated_dttm: 2026-10-08T12:48:51+07:00
- legacy_title: SOW_0096 - Task Execution Delegation Preference
- Extension order (historical; no new approval):
  1. [SOW_20261001_ZJDHWCVU_EXT_U8XRPS06](SOW_20261001_ZJDHWCVU_EXT_U8XRPS06_mandatory_glm53_delegation.md); retain recorded scope/dependencies.

## Preserved Contract And Historical Evidence

Approved [EXT_01](SOW_20261001_ZJDHWCVU_EXT_U8XRPS06_mandatory_glm53_delegation.md) replaces
optional delegation with mandatory available GLM-5.3-max delegation. The
parent was reopened for the approved extension and is now closed again after
canonical verification; base approval history remains unchanged.

## Lifecycle

- **Status**: COMPLETED
- **Approval**: User approved in the current task thread: "patch giúp tôi, sau đó implement, rồi commit, push"
- **create_dttm**: `2026-10-01T03:23:09+07:00`
- **approve_dttm**: `2026-10-01T03:47:20+07:00`
- **finish_dttm**: `2026-10-05T02:58:16+07:00`
- **Proposed-By**: Codex
- **plan**: Standalone; follows `skill-evolution-flow` and extends the approved
  delegation contract from SOW_0095.

## Task

Update `task-execution-flow` so that, after scope approval and before local
implementation, it evaluates whether the next bounded slice should be
delegated first. When suitable, delegation is the default path through an
explicit internal `automatic-execution-delegation` mode of
`sow-delegate-flow`; when model selection is open, the exact available
GLM-5.3-max target is first choice. Explicit local-only or model choices win,
and unsuitable or unavailable automatic delegation falls back to
coordinator-owned local execution only after recording the reason. Explicit
user delegation retains stop/ask behavior and never silently falls back.

## Why

The execution flow currently moves from approved scope to local mini-task
implementation without a clear delegation decision point. This makes use of
available sub-agents inconsistent and can encourage either unnecessary local
work or unsafe broad handoffs. The change must prefer delegation where a
bounded, isolated slice is genuinely suitable without making delegation a
hard gate or weakening local verification.

## Governing Rules And Baseline

- `AGENTS.md` requires approved SOW coverage for behavior-bearing skill edits,
  preservation of unrelated work, scoped commits, and verification at the
  claimed layer.
- `skills/skill-evolution-flow/SKILL.md` requires canonical ownership,
  sanitized regression evidence, and no installed-copy edits as source.
- `task-execution-flow` already owns execution gates, repair loops,
  implementation verification, gap-finding, and closeout.
- `sow-delegate-flow` already owns model/transport resolution, bounded
  ownership, native `fork_turns: "none"`, fresh non-native sessions, and
  coordinator verification.
- SOW_0095 established exact `greennode/glm-5.3` plus
  `reasoning_effort=max` as the first choice for an open model selection when
  an independent pass is warranted. This SOW explicitly extends that same
  exact identity and isolation rule to the approved internal automatic
  execution-delegation mode; it does not alter provider catalogs.

## Location

- `skills/task-execution-flow/SKILL.md`
- `skills/task-execution-flow/agents/openai.yaml`
- `skills/sow-delegate-flow/SKILL.md`
- `tests/skill_feedback_cases/task-execution-flow.json`
- `tests/skill_feedback_cases/sow-delegate-flow.json`
- `plan_todo/finished/SOW_20261001_ZJDHWCVU/SOW_20261001_ZJDHWCVU_task_execution_delegate_preference.md`

No installed Codex/Claude copies, provider catalog, router, credentials,
`task-router-flow`, project code, or shared fixture schema are in scope. Sync
is a separate explicit deployment action after canonical validation and
commit.

## Plan / Reference

- `skills/task-execution-flow/SKILL.md`
- `skills/sow-delegate-flow/SKILL.md`
- `skills/skill-evolution-flow/SKILL.md`
- `plan_todo/finished/SOW_20261001_UTAQGE14/SOW_20261001_UTAQGE14_skill_delegate_review_glm53_preference.md`
- Existing `tests/skill_feedback_cases/task-execution-flow.json` and
  `sow-delegate-flow.json` contracts.

## As-Is Diagram (ASCII)

```text
approved SOW
  -> gather context and split mini-tasks
  -> local implementation
  -> coordinator verification and gap-finding
  -> closeout
```

## To-Be Diagram (ASCII)

```text
approved SOW
  -> gather context and split one bounded slice
  -> delegation suitability gate
       explicit local-only or unsuitable -> local implementation
       explicit user delegation -> sow-delegate-flow explicit mode
       suitable automatic slice -> sow-delegate-flow internal mode
                    open model -> exact GLM-5.3-max first when available
                    unavailable/isolation failure -> record and continue local-only
  -> coordinator verification and gap-finding in either path
  -> closeout with delegation decision evidence
```

## Delegation Preference Contract

- `task-execution-flow` owns the automatic suitability gate. It may enter
  `sow-delegate-flow` only with the explicit internal mode
  `automatic-execution-delegation`; this is not a user-facing trigger and does
  not broaden ordinary single-agent activation.
- `sow-delegate-flow` remains the sole owner of model/transport resolution,
  bounded prompt construction, context isolation, session lifecycle, and
  delegate cleanup. Its explicit user-delegation path is unchanged.
- Evaluate delegation only after an approved SOW is confirmed and before the
  next implementation slice. Do not delegate unapproved implementation,
  unbounded architecture decisions, or work that lacks a bounded owner and
  verifiable result.
- Prefer one automatic delegated slice when it is non-trivial,
  independently bounded, context-isolatable, and locally verifiable. Keep
  simple mechanical edits, secret-bearing work, interactive operator actions,
  and tasks requiring unavailable local state coordinator-owned.
- An explicit user request for local execution or a named model/transport wins.
  Explicit delegation that cannot satisfy model, transport, or isolation
  requirements stops and asks; it never silently falls back.
- In either independent-review or approved automatic-execution-delegation mode,
  open model selection uses exact `greennode/glm-5.3` with
  `reasoning_effort=max` as first choice when current catalog or documented
  transport evidence confirms availability. Variants, stale aliases, and
  guessed availability do not qualify.
- Automatic preference may continue coordinator-only after recording whether
  exact model, compatible transport, fresh-session guarantee, or isolation
  evidence was unavailable. It must not silently select another model.
- The coordinator delegates at most one non-overlapping slice at a time and
  remains responsible for approval, scope, verification, repair, and closeout.
- Record whether the slice was delegated or local, the suitability decision
  and reason, selected model/transport and availability evidence when
  delegated, lifecycle and isolation status, and resulting verification.

## Deliverables

1. Add a delegation-suitability gate and bounded first-delegate decision point
   to `task-execution-flow` without duplicating the full delegate workflow.
2. Add the internal `automatic-execution-delegation` composition trigger to
   `sow-delegate-flow`; preserve its explicit user-delegation behavior.
3. Extend the exact GLM-5.3-max first-choice and explicit-override rules to
   the approved automatic mode without changing provider catalogs.
4. Add delegation decision and evidence requirements to execution verification
   and closeout.
5. Update the skill's discovery metadata so its default prompt mentions the
   delegation preference without implying mandatory delegation.
6. Add one sanitized regression case to each affected fixture with expected,
   negative, and boundary scenarios covering automatic composition, explicit
   override, unsafe/unapproved local handling, unavailable target, and
   isolation fallback.

## Done Criteria

1. The execution flow evaluates delegation only after approved scope and before
   the next implementation slice.
2. Suitable bounded slices enter `sow-delegate-flow` only through the named
   internal automatic mode; unsuitable, secret, interactive, unbounded, or
   unverifiable work remains coordinator-owned.
3. Explicit local-only and explicit model/transport choices always win.
4. Open model selection in both independent-review and automatic modes uses
   exact GLM-5.3-max first-choice semantics without inventing availability or
   silently substituting another model.
5. Automatic preference records which model, transport, fresh-session, or
   isolation check failed and may continue local; explicit delegation still
   follows stop/ask behavior from `sow-delegate-flow`.
6. Native/non-native isolation and coordinator verification remain mandatory;
   delegate completion alone cannot close the task.
7. Closeout evidence records delegation decision, reason, model/transport when
   applicable, isolation, verification, and residual risks.
8. The two new fixture cases follow the existing envelope with unique `id`,
   sanitized metadata, exactly `expected`, `negative`, and `boundary`
   scenarios, and explicit branch assertions: automatic approved slice,
   explicit local/model override, unsafe or unapproved local path, unavailable
   exact target, variant rejection, and isolation failure.
9. `uv run python "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" skills/task-execution-flow` and the same command for `skills/sow-delegate-flow` pass.
10. `uv run python -m unittest tests.test_skill_feedback_cases tests.test_skill_sync_scripts` passes.
11. Targeted assertions explicitly check: approved-scope gate before automatic
    mode; explicit local/model precedence; internal trigger composition;
    exact-model and documented-availability checks; no silent alternate;
    automatic local fallback versus explicit stop/ask; fresh-session and
    isolation requirements; and closeout evidence fields.
12. Metadata parsing confirms the task-execution default prompt describes
    optional delegation and does not make it mandatory; JSON parsing and
    `git diff --check` pass.
13. Only SOW-owned files are staged and committed after verification, then the
    requested push targets the commit containing the verified scope.

## Out Of Scope

- Changing the provider model/transport catalog, credentials, or adding a new
  transport. The bounded internal trigger and wording change to
  `sow-delegate-flow` are explicitly in scope.
- Making delegation mandatory for every task or blocking local execution when
  the preference is unsuitable or unavailable.
- Changing SOW approval, verification, repair, gap-finding, or closeout gates.
- Syncing installed Codex/Claude copies; that remains a separate authorization
  gate. The user explicitly authorizes the repository push in this SOW's
  approval request.
- Modifying `task-router-flow`, project code, or shared test infrastructure.

## Cautions / Risks

- Delegation adds setup latency and token cost; the suitability gate must avoid
  delegating trivial work.
- A broad or secret-dependent prompt can violate context isolation; such work
  must stay local or stop for explicit authorization.
- A missing provider/catalog entry must not become a guessed model selection.
- Local fallback after automatic preference failure is valid only when the
  reason and unverified delegation scope are recorded.
- Composition drift between the two skills can reintroduce implicit fallback;
  the internal mode name and branch-specific fixture coverage are required.
- Fixture and structural tests prove contract wording, not provider behavior.

## Review Writeback

The three independent reviews found and this patch addresses: the missing
composition contract between automatic execution preference and
`sow-delegate-flow`; explicit delegation stop/ask versus automatic local
fallback; exact model and documented-transport evidence; metadata validation;
branch-specific fixture assertions; and the final SOW path/commit boundary.

## Implementation Verification

- **Skill validation**: `quick_validate.py` passed for both
  `task-execution-flow` and `sow-delegate-flow`.
- **Fixture and metadata validation**: both JSON fixtures parsed, the feedback
  contract passed, the new expected/negative/boundary cases passed targeted
  branch assertions, and `task-execution-flow/agents/openai.yaml` parsed with
  optional delegation wording.
- **Repository tests**: `uv run python -m unittest
  tests.test_skill_feedback_cases tests.test_skill_sync_scripts` passed
  (`13` tests).
- **Content assertions**: approved-scope ordering, internal composition mode,
  explicit local/model precedence, exact GLM-5.3-max identity, documented
  availability, automatic local fallback, explicit stop/ask, isolation, and
  closeout evidence fields were all confirmed.
- **Diff checks**: `git diff --check` passed and unrelated dirty worktree
  changes were preserved.
- **Behavioral boundary**: no live provider delegation forward-test was run;
  model/transport behavior remains unverified beyond deterministic skill,
  fixture, metadata, and repository checks.

## SOW Vs Implementation Comparison

| SOW requirement | Implementation evidence | Result |
| --- | --- | --- |
| Execution flow evaluates delegation before each implementation slice | `Delegation Suitability Gate` is placed after approved scope and before implementation | PASS |
| Automatic and explicit delegation compose without fallback drift | Named `automatic-execution-delegation` mode is accepted only from task execution; explicit user delegation still stops/asks | PASS |
| GLM-5.3-max remains exact first choice | Both skills require exact `greennode/glm-5.3` plus `reasoning_effort=max` with current availability evidence | PASS |
| Unsafe or unavailable automatic work remains local | Secret, interactive, unbounded, unavailable, and unisolated branches record the reason and continue coordinator-only | PASS |
| Evidence and regression coverage are auditable | Metadata assertion, two sanitized fixture cases, targeted branch checks, validators, and 13 tests pass | PASS |
| Live provider behavior is proven | No clean provider forward-test was run | UNVERIFIED |

## Approval And Closeout

User approval is recorded above. Implementation and deterministic verification
are complete; this SOW is moved to `plan_todo/finished/` before the scoped
commit and requested push. Installed Codex/Claude sync remains separate.
