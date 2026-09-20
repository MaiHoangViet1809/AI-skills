# Model Escalation Baseline

## Status

- **State**: `verified-seed-and-recovery`
- **Verified**: 2026-09-20
- **Purpose**: Keep short, public benchmark items for comparing a weak
  executor without this skill against the bounded Sol/Astra advisor path.

## User Requirement Captured

The user asked for a real online LLM benchmark item that is short, makes Luna
at maximum reasoning fail, and is solved by Sol or Astra with the smallest
practical token footprint. The item is a baseline for later comparison of
execution without the skill versus execution with this skill. Do not replace
the public items with hand-written puzzles or claim a statistical Luna failure
rate from one run. The controlled recovery below is behavioral evidence for
one concrete failure-to-advisor path.

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

## Controlled Failure-to-Advisor Check

The final closeout check uses BrainBench v3 Q31 because its public analysis
lists it as a universally hard item (`0%` mean accuracy across the evaluated
models) and the prompt is only 90 characters. BrainBench evaluates each item
over ten runs per model, but it does not publish a per-item `gpt-5.6-luna`
result; the Luna result here is a fresh local observation.

- Source: <https://raw.githubusercontent.com/Lomnus-ai/BrainBench/main/data/brainteasers.json>
- Analysis: <https://raw.githubusercontent.com/Lomnus-ai/BrainBench/main/results/analysis.md>
- Prompt: `A store sign says 'Buy one, get one free.' I only want one item. Is there any deal for me?`
- Contract: `A = Yes, there is a deal`; `B = No, there is no deal`.

| Stage | Executor | Expected | Observed | Result |
| --- | --- | --- | --- | --- |
| Fresh baseline without skill | `gpt-5.6-luna` / `max` | `A` | `B` | **Fail** |
| One isolated advisor pass | `gpt-5.6-sol` / `medium` | `A` | `A` | **Pass** |

The Luna CLI envelope reported 1,048 tokens and the Sol envelope 19,330
tokens. These include the Codex runtime envelope, not just the 90-character
benchmark. The handoff contained only the task, acceptance contract, and the
sanitized wrong result; no parent history or files were passed. Sol resolved
the item, so Astra was not invoked and the check stopped after one advisor
pass.

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

The controlled BrainBench Q31 check above satisfies one explicit failure-to-Sol
recovery case. It does not replace the retry gate for real implementation work
or establish a fixed Luna failure percentage.
