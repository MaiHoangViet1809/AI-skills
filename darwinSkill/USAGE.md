# darwinSkill usage guide

`darwinSkill` la native Python framework. Surface chinh la import va goi ham trong code, khong phai CLI.

## 1. Trainer path

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

Dung khi ban muon giu control tren `SkillTrainer` object.

## 2. Benchmark-backed run path

### Tu records in-memory

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

### Tu dataset path

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

Neu adapter co train/eval split rieng, `darwinSkill` se:

- dung `train_samples` cho reflective training loop
- dung `eval_samples` cho gate va final report

Cho benchmark interactive, co the wrap target runtime callback vao `BackendRouter`:

```python
from darwinSkill.backends import build_spreadsheetbench_router

router = build_spreadsheetbench_router(
    target_backend=my_chat_backend,
    optimizer_backend=my_optimizer_backend,
)
```

Hoac build adapter thang tu config:

```python
from darwinSkill.config_loader import build_reference_adapter_from_config

adapter = build_reference_adapter_from_config(
    {
        "benchmark": {"name": "office_qa"},
        "records": [{"question": "Capital of France?", "answer": "Paris"}],
    }
)
```

Neu target backend tra ve OpenAI/Claude/Qwen/Codex-style payload, co the normalize bang compat wrapper:

```python
from darwinSkill.backends import build_openai_compat_backend

target_backend = build_openai_compat_backend(my_provider_callback)
```

Hoac di thang tu benchmark + provider family:

```python
from darwinSkill.backends import build_interactive_router_for_benchmark

router = build_interactive_router_for_benchmark(
    benchmark_name="spreadsheet_bench",
    target_family="openai_chat",
    target_invoke=my_provider_callback,
    optimizer_backend=my_optimizer_backend,
)
```

## 3. Artifact inspection

```python
from darwinSkill.inspection import inspect_run, load_step_record, summarize_run

info = inspect_run(artifacts.output_dir)
summary = summarize_run(artifacts.output_dir)
step1 = load_step_record(artifacts.output_dir, 1)
```

Helper inspection nay cho phep:

- doc `summary.json`, `run_state.json`, `history.json`, `evaluations.json`
- liet ke `steps/step_XXXX/`
- liet ke `slow_update/epoch_XX/` va `meta_skill/epoch_XX/`

## 4. Current acceptance snapshot

- reflective engine core: co
- runtime state + resume + lineage: co
- benchmark pack A: co
- benchmark pack B surface: co
- `ALFWorld` native episode/runtime helper: co
- `SpreadsheetBench` native react/session helper: co
- full upstream tool-heavy runtime parity:
  - `ALFWorld` provider-specific live simulator wrappers: chua
  - `SpreadsheetBench` provider-specific live wrappers: chua
