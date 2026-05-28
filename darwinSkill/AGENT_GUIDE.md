# darwinSkill Agent Guide

This guide is for AI agents that need to use `darwinSkill` correctly with minimal ramp-up.

## What `darwinSkill` Is

`darwinSkill` is a Python-native framework for training and evaluating evolving AI skills.

It provides:

- a reflective training engine
- artifact persistence and resume state
- benchmark adapters and evaluators
- backend routing for optimizer-role vs target-role execution
- native Python entry points for training and evaluation
- provider-log harvesting into a canonical raw schema
- work-unit extraction into trainable skill-improvement examples

It does not provide:

- a CLI-first workflow
- a WebUI
- a public graph pipeline API
- production-ready provider auth/bootstrap for every runtime

## Choose The Right Entry Point

Use `SkillTrainer` when:

- you want direct control over the trainer object
- you already have `SkillSample` inputs
- you already know which backend and evaluator to use

Use `SkillPipeline` when:

- you want an explicit linear sequence of stages
- your flow fits a stage-based pipeline
- you do not need branching/merge graph semantics

Use `darwinSkill.native.run_*` helpers when:

- you want the shortest path to a working train/eval flow
- you want benchmark-backed runs
- you want less manual wiring in caller code

Short rule:

- lowest-level control: `SkillTrainer`
- linear staged orchestration: `SkillPipeline`
- fastest usable API: `darwinSkill.native`

Use `darwinSkill.provider_logs` when:

- you need to harvest provider-native transcripts into a stable raw schema
- you want Codex historical session logs as input evidence
- you need a provider-agnostic artifact before any task judgment

Use `darwinSkill.extraction` when:

- you already have canonical raw evidence
- you need task-bounded work units
- you want trainable examples for later skill optimization

## Minimum Input Contract

The base public sample type is:

```python
from darwinSkill.contracts import SkillSample

sample = SkillSample(
    prompt="Capital of France?",
    expected_answer="Paris",
    metadata={},
)
```

The default mental model is:

- input: `prompt`
- target: `expected_answer`
- scoring: provided by a `SkillEvaluator`

Training config:

```python
from darwinSkill.contracts import TrainingConfig

config = TrainingConfig(
    num_epochs=2,
    batch_size=1,
    edit_budget=4,
    initial_skill="",
    run_name="my-run",
)
```

Evaluation config:

```python
from darwinSkill.contracts import EvaluationConfig

config = EvaluationConfig(
    skill_text="current skill text",
    run_name="my-eval",
)
```

## What The Caller Must Supply

At minimum, caller code must supply:

- a `SkillBackend`
- a `SkillEvaluator`
- either raw `SkillSample` inputs or an adapter/benchmark source

Typical backend responsibility:

- produce predictions from `skill_text + sample`
- optionally improve or reflect skill content when used in training

Typical evaluator responsibility:

- score one prediction against one sample
- return a `MetricResult`

Optional caller-side wiring:

- dataset adapters
- benchmark routers
- provider compat wrappers
- live runtime bootstrap for interactive benchmarks

## Output And Artifacts

After a training run, the most important outputs are:

- `summary.json`
- `run_state.json`
- `evaluations.json`
- `best_skill.md`
- `final_skill.txt`
- `steps/step_XXXX/`
- `skills/skill_vXXXX.md`

If epoch memory is enabled, also inspect:

- `slow_update/epoch_XX/`
- `meta_skill/epoch_XX/`

Use:

```python
from darwinSkill.inspection import inspect_run, summarize_run, load_step_record
```

to inspect run artifacts programmatically.

For skill-improvement data runs, the important outputs are:

- canonical raw session artifacts written by `write_provider_session(...)`
- `WorkUnit` records from `segment_session_into_work_units(...)`
- `TrainableSkillExample` records from `build_trainable_examples(...)`

## Integration Boundary

`darwinSkill` covers framework behavior, not full production integration.

Framework-owned:

- reflective engine
- gate and best-skill tracking
- resume state and artifact lineage
- benchmark loaders/evaluators/adapters
- benchmark-native Python helpers
- provider payload normalization and router composition

Caller-owned or integration-layer-owned:

- provider client construction
- auth and secret management
- network/process bootstrap
- production runtime environment setup
- service/job orchestration around the framework
- any LLM-backed interpretation policy layered on top of the extraction contracts

For tool-heavy benchmarks such as `ALFWorld` and `SpreadsheetBench`, assume the framework gives you the execution surface, but your project may still need to wire runtime dependencies.

## Copy-Paste Recipes

### 1. Simple Trainer Run

```python
from darwinSkill.contracts import TrainingConfig
from darwinSkill.demo_text import DarwinMemoryBackend, demo_samples
from darwinSkill.evaluators import ExactMatchEvaluator
from darwinSkill.trainer import SkillTrainer

trainer = SkillTrainer(
    backend=DarwinMemoryBackend(),
    evaluator=ExactMatchEvaluator(),
    config=TrainingConfig(num_epochs=2, batch_size=1, run_name="demo-train"),
)

artifacts = trainer.fit(demo_samples())
```

### 2. Benchmark Run From Dataset Path

```python
from darwinSkill.contracts import TrainingConfig
from darwinSkill.demo_text import DarwinMemoryBackend
from darwinSkill.native import run_reference_benchmark_from_path

artifacts = run_reference_benchmark_from_path(
    name="officeqa",
    path="/abs/path/to/dataset_or_split_dir",
    backend=DarwinMemoryBackend(),
    config=TrainingConfig(run_name="officeqa-run"),
)
```

### 3. Interactive Benchmark Router

```python
from darwinSkill.backends import build_interactive_router_for_benchmark

router = build_interactive_router_for_benchmark(
    benchmark_name="spreadsheet_bench",
    target_family="openai_chat",
    target_invoke=my_provider_callback,
    optimizer_backend=my_optimizer_backend,
)
```

Use this when the target runtime is interactive or tool-driven.

### 4. Skill Improvement Data Extraction

```python
from pathlib import Path

from darwinSkill.extraction import CallbackEvidenceInterpreter, build_trainable_examples
from darwinSkill.provider_logs import load_codex_session

session = load_codex_session(Path("/abs/path/to/codex-session.jsonl"))
examples = build_trainable_examples(session, skill_name="task-execution-flow")

llm_interpreter = CallbackEvidenceInterpreter(my_judge_callback)
judged_examples = build_trainable_examples(
    session,
    skill_name="task-execution-flow",
    interpreter=llm_interpreter,
)
```

Use the default path first. Add an LLM-backed interpreter only when you need subtler judgments than the heuristic baseline can support.

## Recommended Operating Pattern

1. Start with `darwinSkill.native.run_*` unless you need lower-level control.
2. Use benchmark helpers when your task already matches an existing benchmark surface.
3. Drop to `SkillTrainer` when you need custom evaluator or backend behavior.
4. Use `SkillPipeline` only when a linear stage sequence is the right abstraction.
5. Inspect artifacts after every meaningful training or extraction run before assuming the output is good.

## Common Mistakes

- expecting a CLI workflow instead of importing Python modules
- expecting `SkillPipeline` to support graph branching
- treating provider compat wrappers as full production clients
- ignoring `eval_samples` vs `train_samples` split behavior
- declaring success without inspecting `best_skill.md`, `summary.json`, or step artifacts

## If You Are Unsure

- read [README.md](/Users/maihoangviet/Projects/AISkills/darwinSkill/README.md) for the high-level surface
- read [USAGE.md](/Users/maihoangviet/Projects/AISkills/darwinSkill/USAGE.md) for examples
- read [PARITY.md](/Users/maihoangviet/Projects/AISkills/darwinSkill/PARITY.md) for boundaries and remaining gaps

Default bias:

- use the simplest native Python surface that solves the task
- keep provider/runtime wiring outside the framework core
