# SOW_0091 - Model Escalation Advisor Flow

## Lifecycle

- **Status**: COMPLETED
- **Approval**: approved by user in the current task on 2026-09-20; the same approval extends source-executor coverage to GLM-family high-reasoning models, Claude Sonnet/Haiku, and the public benchmark baseline recorded below
- **create_dttm**: 2026-09-20T05:10:20+07:00
- **approve_dttm**: 2026-09-20T05:17:50+07:00
- **finish_dttm**: 2026-09-20T06:25:32+07:00
- **Implementation State**: skill, metadata, fixture, and benchmark baseline are implemented and verified in the working tree; full skill-path A/B remains an explicitly recorded follow-up runtime check
- **Proposed-By**: Codex
- **plan**: N/A; standalone skill addition

## Task

Add `model-escalation-flow` to guide a lower-capability executor such as OpenAI
Luna, a GLM-family model running at high reasoning, or Claude Sonnet/Haiku
through a bounded advisor escalation: record three to five meaningful failed
attempts, ask `gpt-5.6-sol` at medium reasoning first, then ask `gpt-6-astra`
at low reasoning only when Sol is insufficient, and preserve context isolation,
SOW authority, verification, and explicit stop conditions. Record one short
public LLM benchmark item as a reproducible baseline for later no-skill versus
skill-path checks.

## Why

Repeated retries by a lower-capability executor can become a no-evidence loop
or a panic response, whether the executor is OpenAI, GLM, or Claude. The skill
supplies an advisor/executor pattern without silently delegating implementation,
bypassing approval, leaking parent conversation history, or claiming completion
from advisor confidence alone.

## Scope Boundary

This SOW documents the already-created skill and its distribution metadata, and
the approved source-executor coverage extension. It does not authorize
product-code changes, provider configuration, automatic model switching,
telemetry, transcript persistence, or installed-environment sync. The advisor
is read-only by default; implementation remains governed by an approved SOW and
`task-execution-flow`. The current closeout request separately authorizes
distribution of this verified skill to the requested Codex and Claude targets.

## Location

- `skills/model-escalation-flow/SKILL.md`
- `skills/model-escalation-flow/agents/openai.yaml`
- `skills/model-escalation-flow/references/baseline-test-case.md`
- `skills/INDEX.md`
- `skills/registry.json`
- `tests/skill_feedback_cases/model-escalation-flow.json`
- `plan_todo/SOW_0091_model_escalation_advisor_flow.md`

No other files are in scope. Existing dirty changes in `INSTALL_FOR_AGENTS.md`,
`README.md`, `plan_todo/skill_design_decisions.md`, `sow-delegate-flow`,
`task-router-flow`, their feedback fixtures, `SOW_0056`, `SOW_0089`, and
other concurrent untracked SOW files remain outside this SOW and must not be
staged or rewritten by it.

## As-Is Diagram (ASCII)

```text
lower-capability executor
  -> OpenAI Luna | GLM family at high reasoning | Claude Sonnet/Haiku
  -> difficult or stateful task
  -> repeated retry / contradictory reasoning / no safe next experiment
  -> no explicit evidence gate for asking a stronger advisor
  -> risk of endless loop, arbitrary model substitution, or context leakage
```

## To-Be Diagram (ASCII)

```text
lower-capability executor
  -> record meaningful attempts and evidence
  -> after 3 failed attempts (maximum 5) start isolated Sol-medium advisor pass
  -> apply and verify one bounded recommendation
  -> if still unresolved, start isolated Astra-low advisor pass once
  -> repair and verify locally, ask for authority, or stop unresolved
```

## Deliverables

1. A discoverable `model-escalation-flow` skill with:
   - explicit trigger and retry gate;
   - source-executor coverage for OpenAI Luna, GLM-family high reasoning, and
     Claude Sonnet/Haiku without treating family name alone as failure evidence;
   - ordered Sol-medium then Astra-low escalation ladder;
   - read-only advisor boundary and no-silent-substitution rule;
   - native `fork_turns: "none"` and fresh external-session isolation;
   - self-contained advisor handoff and evidence-return contract;
   - coordinator loop, stop conditions, and final response contract.
2. Codex interface metadata in `agents/openai.yaml`.
3. Registry and human index entries with exact file parity.
4. A sanitized feedback fixture covering expected, negative, and boundary
   escalation behavior.
5. A public benchmark baseline with exact prompt, canonical answer, isolated
   Luna-max failure, and Sol-medium/Astra-low pass evidence.
6. Verification evidence recorded below without claiming model behavior from
   text or structural checks alone.

## Done Criteria

1. The skill frontmatter and body describe the bounded Sol-to-Astra ladder with
   the requested reasoning levels, source-executor family coverage, and no
   silent provider/model substitution.
2. Escalation requires concrete retry evidence; duplicate retries and missing
   authority do not count as panic evidence.
3. Advisor prompts are task-local and context-isolated; parent history is not
   passed through `fork_turns: "all"` by default.
4. The advisor remains read-only unless explicit delegation and an approved SOW
   authorize implementation writes.
5. Stop conditions prevent escalation loops and preserve `implemented but not
   fully verified` when required runtime evidence is unavailable.
6. The registry entry lists every file in the skill folder and no extra file.
7. `quick_validate.py`, feedback fixture validation, registry/sync tests, JSON
   parsing, and whitespace checks pass for the task-owned changes.
8. The benchmark baseline records the exact public source, answer contract,
   model identity, reasoning effort, and observed outputs.
9. The final SOW-vs-implementation comparison below has no untracked scope gap.

## Out-of-Scope

- Editing product code, tests outside the feedback fixture, scripts, runtime
  configuration, provider routing, model catalog, telemetry, or hooks.
- Automatic escalation without the retry/evidence gate.
- Persisting full prompts, historical transcripts, secrets, or credential data.
- Reusing a parent conversation or old provider session for a new advisor task.
- Full no-skill versus skill-path orchestration beyond the isolated baseline
  runs below.
- Commit, push, or changes to unrelated dirty files unless separately requested.
- Treating this skill text or advisor output as proof of actual cross-model
  dispatch behavior.

## Cautions / Risks

- Model IDs and reasoning labels are catalog-dependent; resolve the current
  catalog/transport for OpenAI, GLM, and Claude and stop if the requested tier
  is unavailable.
- `fork_turns: "none"` is an orchestration guard, not proof that an external
  provider created a fresh session; external transport evidence is still
  required.
- Structural validation proves packaging and wording only. The direct baseline
  model runs below do not prove the complete retry-and-escalation orchestration
  or native context isolation.
- The skill must not turn a missing SOW, missing runtime contract, or destructive
  operation into a retry count; those are authority or safety stops.

## Implementation Verification

- `uv run /Users/maihoangviet/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/model-escalation-flow`: passed.
- `uv run python tests/test_skill_feedback_cases.py`: passed (`1` test).
- `uv run python tests/test_skill_sync_scripts.py`: passed (`12` tests).
- `uv run python -m json.tool skills/registry.json`: passed.
- `uv run python -m json.tool tests/skill_feedback_cases/model-escalation-flow.json`: passed.
- Registry parity check for the new skill: passed; three listed files equal
  three actual files.
- `git diff --check` for tracked task-owned edits: passed.
- Trailing-whitespace check for the new skill files, fixture, and this untracked
  SOW: passed.
- Post-approval source-family check: passed; Luna, GLM-high, Sonnet, and Haiku
  appear in the skill trigger, metadata, index/registry description, and
  regression fixture.
- Public baseline source check: passed; BBH `navigate`, case 33, is recorded
  with its raw source URL, exact prompt, expected `Yes`, and answer-only
  contract.
- Isolated baseline model check: passed as differentiated evidence;
  `gpt-5.6-luna` at `max` returned `No`, while `gpt-5.6-sol` at `medium` and
  `gpt-6-astra` at `low` returned `Yes` on fresh sessions.
- Full no-skill versus skill-path A/B: not run; the baseline reference states
  the required retry, `fork_turns: "none"`, and evidence contract without
  claiming that orchestration result.

## SOW Vs Implementation Comparison

| SOW requirement | Implementation evidence | Result |
| --- | --- | --- |
| New skill with retry gate and Sol-to-Astra ladder | `skills/model-escalation-flow/SKILL.md` defines 3 meaningful attempts, maximum 5, Sol `medium`, then Astra `low` | Matched |
| Source executor family coverage | Skill trigger and source-family section cover OpenAI Luna, GLM-family high reasoning, and Claude Sonnet/Haiku | Matched after approved scope extension |
| Evidence-backed advisor handoff | `Advisor Handoff Contract` and `Final Response Contract` sections | Matched |
| Clean context for native and external advisors | `Context Isolation` requires `fork_turns: "none"` and fresh external sessions | Matched in text; runtime isolation unverified |
| Read-only and SOW authority boundary | `Trigger`, `Escalation Ladder`, and `Coordinator Loop` sections | Matched |
| Registry/index/metadata distribution | `SKILL.md`, `agents/openai.yaml`, `skills/INDEX.md`, and `skills/registry.json` | Matched |
| Regression coverage | `tests/skill_feedback_cases/model-escalation-flow.json` with expected/negative/boundary scenarios | Matched structurally |
| Short public model-escalation baseline | `skills/model-escalation-flow/references/baseline-test-case.md` records BBH navigate case 33 and isolated Luna/Sol/Astra outputs | Matched; full skill-path A/B remains unverified |
| No unrelated implementation changes | Current worktree contains unrelated pre-existing dirty files; task-owned new files are isolated in Location | No SOW scope gap found |

## Review Summary

Four review rounds were performed after capturing the SOW. The user then
approved the source-family scope extension on 2026-09-20; a targeted
post-approval implementation check now confirms the added family coverage.

1. **Round 1 - contract completeness:** checked lifecycle, Task, Why, Location,
   diagrams, Deliverables, Done Criteria, Out-of-Scope, risks, and evidence.
   No blocking SOW gap found.
2. **Round 2 - adversarial boundary:** checked retry counting, escalation order,
   unavailable tiers, context isolation, approval/SOW authority, stop states,
   and no-silent-substitution behavior. No blocking SOW gap found.
3. **Round 3 - implementation comparison:** compared every Location and Done
   Criteria item with the actual skill, metadata, registry, index, fixture, and
   validation output. No untracked scope gap found; provider behavior remains
   explicitly unverified.
4. **Round 4 - baseline evidence:** checked that the public prompt, canonical
   answer, isolated model IDs/efforts, and observed outputs are recorded without
   overclaiming a complete skill-path A/B result. No actionable finding found.

**Review conclusion:** No actionable SOW findings found. The implementation and
short public baseline are present and aligned; the only residual gap is the
unrun full retry-and-escalation skill-path A/B check.

## Approval Gate

This SOW records the implementation, the user-approved source-family extension,
and the user-approved public baseline. The current user request separately
authorizes repository closeout, commit/push, and Codex/Claude sync for this
skill. Do not treat the direct baseline model runs as proof of the full
retry-and-escalation orchestration; run that isolated A/B check separately.
