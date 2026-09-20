# SOW_0091 - Model Escalation Advisor Flow

## Lifecycle

- **Status**: COMPLETED
- **Approval**: approved by user in the current task on 2026-09-20; the same approval extends source-executor coverage to GLM-family high-reasoning models, Claude Sonnet/Haiku, and the public benchmark baseline recorded below
- **create_dttm**: 2026-09-20T05:10:20+07:00
- **approve_dttm**: 2026-09-20T05:17:50+07:00
- **finish_dttm**: 2026-09-20T22:26:10+07:00
- **Implementation State**: skill, metadata, fixture, benchmark baselines, and one controlled failure-to-advisor runtime check are implemented and verified; the SOW-owned closeout has no remaining required gap
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
- `plan_todo/finished/SOW_0091_model_escalation_advisor_flow.md`

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
- Statistical benchmark sweeps or a claim that Luna fails a fixed percentage of
  runs; the closeout records one observed failure and one bounded recovery.
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
- Controlled failure-to-advisor runtime check: passed. A fresh
  `gpt-5.6-luna` `max` session returned `B` for BrainBench Q31 where `A` is
  canonical; one fresh `gpt-5.6-sol` `medium` advisor session received only a
  compact sanitized handoff and returned `A`. The Luna CLI envelope reported
  1,048 tokens and the Sol envelope reported 19,330 tokens; these include the
  runtime envelope and are not intrinsic prompt cost.
- The Sol pass was sufficient, so Astra was not run. No parent history, files,
  or repository changes were passed to either process. This proves one
  bounded weak-executor recovery path, not a deterministic Luna failure rate or
  universal success across all weak-model families.

## Closeout Runtime Finding

The final runtime finding uses BrainBench v3 Q31 because the public analysis
identifies it as a universally hard item (`0%` mean accuracy across the
evaluated models) and the prompt is only 90 characters. The public report
evaluated each question across ten runs per model, but it does not publish a
per-item `gpt-5.6-luna` result; the Luna failure below is therefore local
runtime evidence rather than an extrapolated benchmark statistic.

- **Source**: <https://raw.githubusercontent.com/Lomnus-ai/BrainBench/main/data/brainteasers.json>
- **Analysis**: <https://raw.githubusercontent.com/Lomnus-ai/BrainBench/main/results/analysis.md>
- **Question**: `A store sign says 'Buy one, get one free.' I only want one item. Is there any deal for me?`
- **Answer contract**: `A = Yes, there is a deal`; `B = No, there is no deal`.

| Stage | Model / effort | Expected | Observed | Status |
| --- | --- | --- | --- | --- |
| Baseline, no skill | `gpt-5.6-luna` / `max` | `A` | `B` | **not-ok** |
| Isolated advisor | `gpt-5.6-sol` / `medium` | `A` | `A` | **ok** |

**Finding:** `model-escalation-flow` can recover a concrete wrong answer from a
covered weak executor through a fresh, read-only Sol advisor handoff. The check
stopped after Sol resolved the item; no repeated skill run or Astra pass was
needed. This is behavioral evidence that the strategy supports an unresolved
weak-model case, while leaving statistical failure-rate claims explicitly out
of scope.

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
| Short public model-escalation baseline | `skills/model-escalation-flow/references/baseline-test-case.md` records the initial BBH seed and the BrainBench Q31 failure-to-Sol recovery | Matched; one bounded runtime recovery verified, no statistical failure-rate claim |
| No unrelated implementation changes | Current worktree contains unrelated pre-existing dirty files; task-owned new files are isolated in Location | No SOW scope gap found |

## Review Summary

Five review rounds were performed after capturing the SOW. The user then
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
   validation output. No untracked scope gap found; native or external
   provider behavior outside this CLI check remains explicitly unverified.
4. **Round 4 - baseline evidence:** checked that the public prompt, canonical
   answer, isolated model IDs/efforts, and observed outputs are recorded without
   overclaiming a deterministic Luna failure rate. No actionable finding found.
5. **Round 5 - controlled recovery evidence:** ran one fresh Luna-max baseline
   on the shorter BrainBench Q31 item, captured the wrong `B` result, and sent
   only the sanitized failure evidence to one fresh Sol-medium process. Sol
   returned the canonical `A`; Astra was correctly not invoked. No actionable
   finding found.

**Review conclusion:** No actionable SOW findings found. The implementation,
public baseline, and one controlled weak-executor recovery are present and
aligned. Statistical Luna failure-rate measurement remains intentionally out of
scope and is not required to close this SOW.

## Approval Gate

This SOW records the implementation, the user-approved source-family extension,
the public benchmark baseline, and the controlled failure-to-Sol runtime
finding. The SOW is closed. The evidence supports the claim that the skill can
recover one wrong answer from a covered weak executor; it does not claim a
fixed Luna failure rate, universal model-family coverage, or automatic
completion from advisor confidence.
