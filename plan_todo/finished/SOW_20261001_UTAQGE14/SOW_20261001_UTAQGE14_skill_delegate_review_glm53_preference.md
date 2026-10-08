# SOW_20261001_UTAQGE14 - GLM-5.3-max First-Choice Delegation And Independent Review

- Status: COMPLETED
- Approval: User approved in the current task thread: "approve, làm giúp tôi cẩn thận"
- create_dttm: 2026-10-01T02:16:57+07:00
- create_date: 2026-10-01
- create_dttm_source: original_creation_datetime
- create_dttm_confidence: explicit
- create_dttm_evidence: `plan_todo/finished/SOW_20261008_VO3LKN0L/creation-date-evidence.json` (record: SOW_20261001_UTAQGE14)
- approve_dttm: 2026-10-01T02:40:07+07:00
- finish_dttm: 2026-10-01T02:42:38+07:00
- legacy_id: SOW_0095
- legacy_path: plan_todo/finished/SOW_0095_skill_delegate_review_glm53_preference.md
- migrated_dttm: 2026-10-08T12:48:51+07:00
- legacy_title: SOW_0095 - GLM-5.3-max First-Choice Delegation And Independent Review

## Preserved Contract And Historical Evidence

## Lifecycle

- **Status**: COMPLETED
- **Approval**: User approved in the current task thread: "approve, làm giúp tôi cẩn thận"
- **create_dttm**: `2026-10-01T02:16:57+07:00`
- **approve_dttm**: `2026-10-01T02:40:07+07:00`
- **finish_dttm**: `2026-10-01T02:42:38+07:00`
- **Proposed-By**: Codex
- **plan**: Standalone; follows the existing `skill-evolution-flow` workflow.

## Task

Update `sow-delegate-flow` and `task-review-investigate-compare` so that the
exact available GLM-5.3-max sub-agent is the first choice and MUST be selected
when model selection is open and an independent pass is warranted, while
preserving explicit model choice, native/custom lifecycle isolation, and
coordinator-owned verification.

## Why

The current delegation skill resolves an explicitly requested model but does
not define a first-choice ordering for GLM-5.3. The review skill has no
guidance for selecting a stronger independent sub-agent when a review benefits
from a separate pass. This can produce inconsistent model selection or make
review quality depend on whichever model happens to be chosen first.

The correction is a first-choice rule, not silent substitution: an explicit
model or transport request always wins; when the trigger is warranted and the
exact target is available, no other model is considered first; only the exact
`greennode/glm-5.3` model with `reasoning_effort=max` qualifies; variants such
as GLM-5.3 Flash or third-party aliases do not qualify; unavailability is
recorded instead of being hidden.

## Governing Rules And Baseline

- `AGENTS.md` requires canonical source edits, approved SOW coverage for
  behavior-bearing skill changes, preservation of unrelated dirty work, and
  validation at the claimed layer.
- `skills/skill-evolution-flow/SKILL.md` requires canonical ownership,
  regression evidence before patching, and no installed-copy edits as source.
- `sow-delegate-flow` already requires catalog-based model resolution,
  `fork_turns: "none"` for native children, fresh provider sessions for
  non-native agents, bounded prompts, and coordinator-owned verification.
- `task-review-investigate-compare` already stops at review/recommendation and
  does not execute the reviewed implementation.
- Current target skills are registered in `skills/registry.json` and their
  canonical folders exist.
- The current worktree contains unrelated user changes; they remain untouched.

## Location

- `skills/sow-delegate-flow/SKILL.md`
- `skills/task-review-investigate-compare/SKILL.md`
- `tests/skill_feedback_cases/sow-delegate-flow.json`
- `tests/skill_feedback_cases/task-review-investigate-compare.json`
- `plan_todo/finished/SOW_20261001_UTAQGE14/SOW_20261001_UTAQGE14_skill_delegate_review_glm53_preference.md`

No installed Codex/Claude copy, provider configuration, project code, shared
fixture schema, or unrelated skill is in scope. Sync is a separate explicit
deployment action after canonical validation and commit.

## Plan / Reference

- `skills/skill-evolution-flow/SKILL.md`
- `skills/sow-delegate-flow/SKILL.md`
- `skills/task-review-investigate-compare/SKILL.md`
- `plan_todo/finished/SOW_20260928_41N2XGU5/SOW_20260928_41N2XGU5_sow_delegate_native_context_isolation.md`
- Three read-only reviews on `2026-10-01`: two GLM-5.3-max passes and one
  Luna-max pass; all recommended `revise` before approval.

## As-Is Diagram (ASCII)

```text
delegate/review request
  -> resolve explicit model when named
  -> otherwise no shared GLM-5.3 preference
  -> native or custom lifecycle rules
  -> coordinator review / recommendation
```

## To-Be Diagram (ASCII)

```text
delegate or independent-review request
  -> classify intent: explicit delegation or optional independent review
  -> resolve explicit model/transport, if supplied
       exact and compatible -> use it
       unavailable/incompatible -> stop and ask; no substitution
  -> selection open and independent pass warranted?
       no  -> coordinator-only review/execution
       yes -> inspect current catalog for exact greennode/glm-5.3 + max
                 available -> MUST select that exact target as first choice
                 unavailable ->
                   explicit delegation: stop and ask
                   optional review: report unavailable, continue locally only
  -> native: fork_turns none
  -> non-native: brand-new provider session, no history
  -> bounded prompt -> coordinator independently verifies/synthesizes
```

## Exact Model And Trigger Contract

- The first-choice target is exact model id `greennode/glm-5.3` with
  `reasoning_effort=max`. When selection is open and the independent-pass
  trigger is warranted, the coordinator MUST select this exact target before
  considering any other model. `greennode/glm-5.3-flash-thirdparty`, GLM-5.3
  Flash, aliases, stale role names, and other providers are not an exact match.
- Resolve availability from the current native catalog or the provider's
  documented transport at the time of delegation. Never infer availability
  from a display name or an earlier task.
- Use a sub-agent only for an explicit independent-review request, a
  behavior-bearing or high-risk contract review, or a task whose ambiguity or
  blast radius makes a second bounded pass materially useful. Do not spawn one
  for a simple status, editorial clarification, or routine local check.
- If multiple exact transports are available and the user did not select one,
  stop and ask rather than inventing a pairing.

## Contract Changes

1. **Explicit choice wins**: a user-named model or transport is authoritative;
   the GLM-5.3 first-choice rule must not override it. If explicitly selected model
   and transport are incompatible, stop and ask.
2. **First-choice rule**: when model selection is open and the exact trigger
   contract says an independent pass is warranted, the coordinator MUST select
   exact GLM-5.3-max first when it is available; no alternate model may be
   selected before it.
3. **No invented availability**: never hardcode a role name or claim exact
   GLM-5.3-max is available without current catalog/transport evidence.
4. **No silent fallback**: explicit delegation with an open model choice stops
   and asks when exact GLM-5.3-max is unavailable. An optional independent
   review may report `unavailable` and continue coordinator-only, but it may
   not silently select another model.
5. **Isolation remains mandatory**: native GLM-5.3 uses the native lifecycle
   with `fork_turns: "none"`; a non-native GLM-5.3 transport starts a fresh
   provider-owned session with no prior task history.
6. **Review remains advisory**: delegated findings are evidence only; the
   coordinator owns synthesis, writeback, verification, and closeout.
7. **Evidence is reported**: both delegation and review closeout record
   selected model, exact model identity, transport, availability evidence,
   lifecycle state, isolation status, and whether an independent pass ran.
8. **Review output is explicit**: the review skill reports the same evidence
   fields and discards delegate findings when isolation cannot be proven.

## Deliverables

1. Add the exact GLM-5.3-max first-choice priority, trigger, identity,
   compatibility, and unavailable branches to `sow-delegate-flow`.
2. Add a bounded independent-review rule and evidence fields to
   `task-review-investigate-compare`.
3. Add one sanitized regression fixture to each target skill with expected,
   negative, and boundary scenarios covering exact match, explicit override,
   unavailable target, native isolation, and optional-review behavior.
4. Keep existing fresh-session, approval, scope, and coordinator-verification
   rules intact without duplicating the full delegation workflow in the review
   skill.

## Done Criteria

1. Both target skills state exact `greennode/glm-5.3` plus `max` reasoning as
   the first choice when available and the trigger is warranted; variants and
   aliases do not satisfy the match.
2. Explicit model/transport choice, incompatible pairings, multiple exact
   matches, and unavailable exact targets have deterministic stop/ask behavior.
3. The preference is limited to independent-review or materially risky,
   ambiguous, behavior-bearing work; simple status/editorial work remains
   coordinator-only.
4. Native/custom classification and context isolation remain explicit, with no
   `fork_turns: "all"` path introduced.
5. Explicit delegation never becomes local execution silently; optional review
   may continue coordinator-only only after recording exact-target unavailability.
6. Review delegation remains read-only and coordinator-owned; the review skill
   does not execute implementation work.
7. Review/closeout output records model id, reasoning effort, transport,
   availability evidence, lifecycle, isolation status, and independent-pass
   result.
8. Each fixture follows the existing envelope with unique `id`, sanitized
   feedback metadata, and `scenarios[].kind` values `expected`, `negative`,
   and `boundary`; cases cover every branch in the contract.
9. `uv run python "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" skills/sow-delegate-flow`
   and the same command for `task-review-investigate-compare` pass.
10. `uv run python -m unittest tests.test_skill_feedback_cases
    tests.test_skill_sync_scripts` passes.
11. Targeted content assertions and `git diff --check` pass; only SOW-owned
    files are staged and committed after approval and verification.
12. Forward tests, if a clean isolated context and exact GLM-5.3-max transport
    are available, record actual model/transport evidence separately from
    deterministic fixture validation; otherwise closeout marks them unverified.

## Out Of Scope

- Changing the provider catalog, Codex router, Claude CLI, or model credentials.
- Making GLM-5.3 a hard requirement for every review or delegation; this does
  not weaken the first-choice rule when the exact target is available and the
  trigger is warranted.
- Replacing an explicit user-selected model with GLM-5.3.
- Changing native/non-native session semantics or allowing inherited history.
- Pushing or syncing installed copies; commit is a required post-approval
  closeout action unless the user explicitly defers it.
- Modifying `task-router-flow`, other skills, project code, or shared test
  infrastructure.

## Cautions / Risks

- Catalog names and provider transports can drift; availability evidence must
  be current and exact, not inferred from a display label.
- Independent sub-agent passes add latency and token cost; the trigger must
  remain bounded to material review value.
- Fixture and structural checks cannot prove model behavior; forward tests may
  remain unverified when clean transport isolation is unavailable.
- A failed isolation check invalidates delegate findings and must not be
  converted into coordinator conclusions.
- A user-selected model or transport must never be replaced by the preference.

## Review Writeback

The three independent reviews identified, and the approved implementation now
addresses: the duplicate
SOW id, exact model/transport identity, explicit GLM-5.3-max first-choice
priority, explicit delegation versus optional review behavior when the exact
target is unavailable, bounded trigger criteria, incompatible or multiple exact
transports, review evidence fields, fixture semantics, exact validation
commands, commit authority, and required risks. The approved implementation
updated both target skills and added one sanitized regression case to each
target fixture; no installed copy, provider configuration, or unrelated skill
was edited.

## Implementation Verification

- **Skill validation**: both target directories passed the bundled
  `quick_validate.py` structural validator.
- **Fixture validation**: both new JSON cases parsed successfully and the
  repository feedback-case contract passed with expected, negative, and
  boundary scenarios.
- **Repository tests**: `uv run python -m unittest
  tests.test_skill_feedback_cases tests.test_skill_sync_scripts` passed
  (`13` tests).
- **Content assertions**: exact `greennode/glm-5.3` plus
  `reasoning_effort=max`, first-choice `MUST` rule, explicit override,
  unavailable branches, fresh-session isolation, and evidence fields were
  confirmed in both skills.
- **Scope checks**: `git diff --check` passed; only the two target skills,
  their two feedback fixtures, and this SOW are task-owned changes. Existing
  unrelated worktree changes were preserved.
- **Behavioral boundary**: no clean GLM-5.3-max provider forward-test was run;
  model behavior and transport availability remain unverified beyond the
  deterministic skill and fixture checks.

## SOW Vs Implementation Comparison

| SOW requirement | Implementation evidence | Result |
| --- | --- | --- |
| GLM-5.3-max is first choice for warranted independent passes | Both target skills require exact `greennode/glm-5.3` with `reasoning_effort=max` and `MUST select` before alternates | PASS |
| Explicit choices, incompatible transports, and unavailable targets are deterministic | Both skills preserve explicit override and stop/ask or coordinator-only unavailable branches | PASS |
| Native and non-native context remains isolated | `fork_turns: "none"`, fresh provider-owned session, no-history and discard-on-failure rules are explicit | PASS |
| Review remains advisory and reports evidence | Review skill records model, reasoning, transport, availability, lifecycle, isolation, and pass result | PASS |
| Regression coverage uses the existing fixture envelope | One new sanitized expected/negative/boundary case was added to each target fixture | PASS |
| Runtime model behavior is proven | No clean isolated provider forward-test was available in this execution | UNVERIFIED |

## Approval And Closeout

User approval is recorded above. The approved implementation and deterministic
verification are complete; this SOW is moved to `plan_todo/finished/` before
commit. Push and installed-copy sync remain separate authorization gates and
were not performed.
