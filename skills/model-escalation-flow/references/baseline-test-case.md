# Model Escalation Baseline

## Status

- **State**: `verified-seed`
- **Verified**: 2026-09-20
- **Purpose**: Keep one short, public benchmark item for comparing a weak
  executor without this skill against the bounded Sol/Astra advisor path.

## User Requirement Captured

The user asked for a real online LLM benchmark item that is short, makes Luna
at maximum reasoning fail, and is solved by Sol or Astra with the smallest
practical token footprint. The item is a baseline for later comparison of
execution without the skill versus execution with this skill. Do not replace
the public item with a hand-written puzzle or claim the full skill A/B result
until the isolated retry-and-escalation path has been exercised.

## Benchmark Source

- Dataset: BIG-Bench Hard, `navigate`.
- Item: `navigate.json`, `examples[32]` (case 33 in the source file).
- Source: <https://raw.githubusercontent.com/suzgunmirac/BIG-Bench-Hard/main/bbh/navigate.json>
- Benchmark paper: <https://arxiv.org/abs/2210.09261>
- The benchmark's exact-match target is `Yes`.
- Raw benchmark input is 143 characters including its final newline; the
  expected answer is one word. This is the shortest verified failure/pass
  candidate from the checks recorded for this SOW, not a claim that it is the
  globally shortest possible benchmark item.

## Canonical Test

```text
If you follow these instructions, do you return to the starting point? Take 10 steps. Turn left. Turn left. Take 10 steps.
Options:
- Yes
- No
```

Expected output: `Yes`

## Isolated Model Evidence

Each run used a new ephemeral, read-only session with no user configuration,
no parent history, and an answer-only output contract. The direct runs did not
inject `model-escalation-flow`; they establish the baseline, not the complete
skill A/B result.

| Executor | Reasoning | Observed output | Result |
| --- | --- | --- | --- |
| `gpt-5.6-luna` | `max` | `No` | **Fail** |
| `gpt-5.6-sol` | `medium` | `Yes` | **Pass** |
| `gpt-6-astra` | `low` | `Yes` | **Pass** |

The Luna run consumed 14,003 input tokens and 47 output tokens at the Codex
CLI envelope; those figures include the model/runtime envelope and are not a
claim about the benchmark's intrinsic token length. The benchmark item itself
is intentionally kept to one short navigation question and a one-word answer.

## Future Skill A/B Protocol

1. **Without skill**: run the exact item in a fresh Luna-max session and record
   the answer, model identity, effort, and sanitized usage evidence.
2. **With skill**: give the same item to the covered lower-capability executor,
   record three materially different failed attempts if it remains wrong, then
   ask Sol-medium in a fresh native `fork_turns: "none"` context. Use Astra-low
   only if Sol is insufficient, and verify the final answer against `Yes`.
3. A valid skill-path pass requires the correct final answer, ordered tier
   evidence, no parent-context leakage, and no completion claim from advisor
   confidence alone. If the executor answers correctly before the retry gate,
   record `no escalation needed` rather than forcing a failure.
