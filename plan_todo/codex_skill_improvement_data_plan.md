# Codex Skill Improvement Data Plan

## Goal

Build a provider-agnostic data pipeline in `darwinSkill` that can turn real agent work logs into trainable skill-improvement examples.

## Status

- completed: `SOW_0058_codex_skill_harvest_flow.md`
- completed: `SOW_0059_trainable_example_extraction_pipeline.md`

This plan is not about direct online self-modification. It is about:

- harvesting raw execution evidence from agent platforms
- normalizing it into one canonical schema
- extracting task-bounded examples from that evidence
- preparing a stable input stream for later `darwinSkill` optimization and gating

## Why This Exists

If an agent performs poorly across many real tasks, the failure signal already exists in the logs:

- user requests
- scope discussions
- tool traces
- patch history
- repair loops
- validation output
- accepted vs reopened outcomes

The missing layer is not raw data volume. The missing layer is structured conversion:

```text
provider logs
  -> canonical raw schema
  -> task/work-unit extraction
  -> trainable skill examples
  -> later darwinSkill optimization
```

## Principles

- preserve raw evidence
- separate raw evidence from judged outcome
- use provider-agnostic contracts instead of Codex-only classes
- prefer deterministic capture and normalization first
- allow LLM-assisted extraction later where judgment is needed
- allow abstain / insufficient-evidence outcomes instead of forcing low-confidence labels
- keep a path to future `train/val/test` or equivalent split discipline

## Program Shape

### Phase 1: Harvest And Canonicalize Raw Logs

Focus:

- ingest provider-native logs such as Codex session JSONL
- normalize them into one canonical raw schema
- retain provider-specific details in extensible metadata
- use historical logs as the default source first
- treat hook-based capture as later enrichment, not a prerequisite for v1
- do not collapse into positive/negative labels yet

### Phase 2: Extract Trainable Examples

Focus:

- segment raw evidence into task-bounded work units
- interpret repair loops, validation results, and acceptance/reopen signals
- produce trainable examples for skill improvement
- preserve both raw evidence refs and derived judgments in the output contract
- prefer LLM-assisted extraction for nuanced judgment, with deterministic evidence scaffolding around it

## SOW Breakdown

### SOW_0058_codex_skill_harvest_flow.md

Focus:

- harvesting from raw conversation and tool logs
- canonical raw schema
- Codex-first parser with provider-agnostic abstractions

Why grouped:

- raw data must be locked before any extraction or labeling logic
- this is the stable evidence layer every later step depends on

### SOW_0059_trainable_example_extraction_pipeline.md

Focus:

- extract trainable examples from canonical raw evidence
- combine deterministic evidence collection with LLM-assisted interpretation
- produce skill-oriented examples rather than raw turn labels

Why grouped:

- this is the first step that turns operational traces into optimization-ready data
- it needs different logic from low-level harvesting and should be reviewable on its own

## Preferred Extraction Strategy

Default bias:

- deterministic for raw capture
- deterministic for provider normalization
- LLM-assisted for work-unit interpretation and skill-example extraction

Reason:

- raw event structure should not depend on model judgment
- but deciding whether a task was shallow, incomplete, scope-missed, or successfully repaired often needs richer semantic interpretation than simple heuristics

Guardrail:

- if boundary confidence or evidence quality is too low, the pipeline should abstain or emit an explicit `insufficient_evidence` / `needs_review` style outcome instead of forcing a strong label

## Split Discipline

The pipeline should keep a clean path to later split-aware usage.

Initial bias:

- split at the work-unit or task-family level, not raw turn level
- keep related repair loops together unless there is a strong reason to separate them
- reserve a held-out slice for later validation of downstream skill updates, not just extraction smoke tests
- do not let near-duplicate continuations leak across train and validation partitions

## Acceptance

The plan is complete when:

- `darwinSkill` can ingest real provider logs into a canonical raw schema
- the pipeline can extract task-bounded, trainable skill examples from that schema
- the extraction layer can abstain when evidence is too mixed or weak
- the resulting examples are suitable as upstream input for later skill optimization runs

## Out Of Scope

- automatic online self-training during an active task
- automatic publishing into `~/.codex/skills`
- reward-model research beyond the first practical extraction pipeline
