# darwinSkill Usage Guide

`darwinSkill` is a native Python framework. The main surface is importing and calling it from code, not using a CLI.

## 1. Trainer Path

Use this when you want direct control over the `SkillTrainer` object.

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

## 2. Benchmark-Backed Run Path

### From In-Memory Records

```python
from darwinSkill.contracts import TrainingConfig
from darwinSkill.demo_text import DarwinMemoryBackend
from darwinSkill.native import run_reference_benchmark

artifacts = run_reference_benchmark(
    name="searchqa",
    backend=DarwinMemoryBackend(),
    records=[
        {"question": "Capital of France?", "answers": ["Paris"]},
    ],
    config=TrainingConfig(run_name="searchqa-inline"),
)
```

### From A Dataset Path

```python
from darwinSkill.contracts import TrainingConfig
from darwinSkill.demo_text import DarwinMemoryBackend
from darwinSkill.native import run_reference_benchmark_from_path

artifacts = run_reference_benchmark_from_path(
    name="officeqa",
    path="/abs/path/to/split_dir_or_dataset",
    backend=DarwinMemoryBackend(),
    config=TrainingConfig(run_name="officeqa-path"),
)
```

If an adapter exposes separate train/eval splits, `darwinSkill` will:

- use `train_samples` for the reflective training loop
- use `eval_samples` for gate decisions and the final report

## 3. Interactive Benchmark Routing

For interactive benchmarks, wrap the target runtime callback through `BackendRouter`.

```python
from darwinSkill.backends import build_spreadsheetbench_router

router = build_spreadsheetbench_router(
    target_backend=my_chat_backend,
    optimizer_backend=my_optimizer_backend,
)
```

You can also build an adapter directly from config:

```python
from darwinSkill.config_loader import build_reference_adapter_from_config

adapter = build_reference_adapter_from_config(
    {
        "benchmark": {"name": "office_qa"},
        "records": [{"question": "Capital of France?", "answer": "Paris"}],
    }
)
```

If the target backend returns OpenAI/Claude/Qwen/Codex-style payloads, normalize them with a compat wrapper:

```python
from darwinSkill.backends import build_openai_compat_backend

target_backend = build_openai_compat_backend(my_provider_callback)
```

Or bootstrap directly from benchmark name plus provider family:

```python
from darwinSkill.backends import build_interactive_router_for_benchmark

router = build_interactive_router_for_benchmark(
    benchmark_name="spreadsheet_bench",
    target_family="openai_chat",
    target_invoke=my_provider_callback,
    optimizer_backend=my_optimizer_backend,
)
```

For `ALFWorld`, if local dependencies and the reference snapshot are available, the router can use the default live environment factory automatically:

```python
router = build_interactive_router_for_benchmark(
    benchmark_name="alfworld",
    target_family="claude_chat",
    target_invoke=my_provider_callback,
    optimizer_backend=my_optimizer_backend,
)
```

## 4. Artifact Inspection

```python
from darwinSkill.inspection import inspect_run, load_step_record, summarize_run

info = inspect_run(artifacts.output_dir)
summary = summarize_run(artifacts.output_dir)
step1 = load_step_record(artifacts.output_dir, 1)
```

These helpers let you:

- read `summary.json`, `run_state.json`, `history.json`, and `evaluations.json`
- inspect `steps/step_XXXX/`
- inspect `slow_update/epoch_XX/` and `meta_skill/epoch_XX/`

## 5. Current Acceptance Snapshot

- reflective engine core: available
- runtime state + resume + lineage: available
- benchmark pack A: available
- benchmark pack B surface: available
- `ALFWorld` native episode/runtime helper: available
- `SpreadsheetBench` native react/session helper: available

Still left to project-side integration:

- `ALFWorld` provider-specific live simulator wrappers
- `SpreadsheetBench` provider-specific live wrappers

## 6. Provider Log Harvesting

Use this when you want to turn provider-native logs into a canonical raw artifact:

```python
from pathlib import Path

from darwinSkill.provider_logs import load_codex_session, write_provider_session

session = load_codex_session(Path("/abs/path/to/codex-session.jsonl"))
write_provider_session(Path("/abs/path/to/canonical-session.json"), session)
```

Command form:

```bash
PYTHONPATH=. uv run python scripts/darwinSkill/harvest_provider_logs.py \
  --provider codex \
  --input /abs/path/to/codex-session.jsonl \
  --output /abs/path/to/canonical-session.json
```

Current v1 behavior:

- historical Codex session JSONL is the default source
- provider-specific details are preserved in metadata
- raw evidence stays separate from later judgments

## 7. Trainable Example Extraction

Use this when you already have canonical raw evidence and want task-bounded skill-improvement examples:

```python
from pathlib import Path

from darwinSkill.extraction import CallbackEvidenceInterpreter, build_trainable_examples
from darwinSkill.provider_logs import read_provider_session

session = read_provider_session(Path("/abs/path/to/canonical-session.json"))
examples = build_trainable_examples(session, skill_name="task-execution-flow")

llm_interpreter = CallbackEvidenceInterpreter(my_judge_callback)
judged_examples = build_trainable_examples(
    session,
    skill_name="task-execution-flow",
    interpreter=llm_interpreter,
)
```

Command form:

```bash
PYTHONPATH=. uv run python scripts/darwinSkill/extract_skill_examples.py \
  --input /abs/path/to/canonical-session.json \
  --output /abs/path/to/examples.json \
  --skill-name task-execution-flow
```

Output characteristics:

- work-unit segmentation includes boundary confidence, mixed-context flags, and continuation links
- examples preserve raw evidence references separately from derived reasoning
- low-confidence or mixed-context work units can abstain instead of forcing a label
- callers can swap in an LLM-backed interpreter without changing the canonical evidence layer
