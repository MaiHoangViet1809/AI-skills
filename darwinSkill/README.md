# darwinSkill

`darwinSkill` is a Python-native module tree for evolving AI skills through training.

It distills the core mechanics of `SkillOpt` into a cleaner API that can be embedded into other projects without relying on a CLI or WebUI.

## Public Imports

```python
from darwinSkill.src.native import run_training, run_evaluation, run_reference_benchmark
from darwinSkill.src.trainer import SkillTrainer
from darwinSkill.src.pipeline import SkillPipeline
from darwinSkill.src.contracts import SkillSample, TrainingConfig, EvaluationConfig, PipelineConfig
from darwinSkill.src.evaluators import ExactMatchEvaluator
from darwinSkill.src.demo_text import DarwinMemoryBackend, demo_samples
from darwinSkill.src.reference_adapters import SearchQAAdapter, DocVQAAdapter, OfficeQAAdapter
from darwinSkill.src.provider_logs import load_codex_session, read_provider_session, write_provider_session
from darwinSkill.src.extraction import build_trainable_examples, segment_session_into_work_units
```

## Main Docs

- [AGENT_GUIDE.md](/Users/maihoangviet/Projects/AISkills/darwinSkill/AGENT_GUIDE.md)
- [USAGE.md](/Users/maihoangviet/Projects/AISkills/darwinSkill/USAGE.md)
- [PARITY.md](/Users/maihoangviet/Projects/AISkills/darwinSkill/PARITY.md)

## Design Summary

- The anchor use case is a text skill.
- The default sample contract is `prompt + expected_answer + metric`.
- `SkillPipeline` is intentionally linear-only.
- The trainer core uses a reflective engine with gate, step artifacts, slow update, and meta-skill memory.
- Branching and merge orchestration belong in caller Python code, not in a public graph API.

## Native Python Entry Points

- `darwinSkill.src.native.run_training(...)`
- `darwinSkill.src.native.run_evaluation(...)`
- `darwinSkill.src.native.run_reference_benchmark(...)`
- `darwinSkill.src.native.run_reference_benchmark_from_path(...)`
- `darwinSkill.src.native.run_reference_adapter(...)`
- `darwinSkill.src.inspection.inspect_run(...)`
- `darwinSkill.src.inspection.summarize_run(...)`
- `darwinSkill.src.inspection.load_step_record(...)`

## Skill Improvement Data Pipeline

`darwinSkill` also includes a provider-agnostic evidence pipeline for skill improvement:

```text
provider-native logs
  -> canonical raw schema
  -> work-unit extraction
  -> trainable skill examples
```

Main modules:

- `darwinSkill.src.provider_logs`
- `darwinSkill.src.extraction`

Main scripts:

- `PYTHONPATH=. uv run python darwinSkill/scripts/harvest_provider_logs.py --provider codex --input /abs/path/to/session.jsonl --output /abs/path/to/canonical.json`
- `PYTHONPATH=. uv run python darwinSkill/scripts/extract_skill_examples.py --input /abs/path/to/canonical.json --output /abs/path/to/examples.json --skill-name task-execution-flow`

Default behavior:

- harvesting is deterministic and evidence-preserving
- extraction is deterministic around the evidence bundle
- interpretation defaults to heuristics, but callers can inject an LLM-backed interpreter through `CallbackEvidenceInterpreter`

## Backend And Integration Helpers

- `darwinSkill.src.backends.build_spreadsheetbench_router(...)`
- `darwinSkill.src.backends.build_alfworld_router(...)`
- `darwinSkill.src.backends.build_openai_compat_backend(...)`
- `darwinSkill.src.backends.build_claude_compat_backend(...)`
- `darwinSkill.src.backends.build_qwen_compat_backend(...)`
- `darwinSkill.src.backends.build_codex_compat_backend(...)`
- `darwinSkill.src.backends.build_provider_compat_backend_for_family(...)`
- `darwinSkill.src.backends.build_interactive_router_for_benchmark(...)`
- `darwinSkill.src.reference_adapters.build_reference_adapter(...)`
- `darwinSkill.src.config_loader.build_reference_adapter_from_config(...)`

## Benchmark-Native Surfaces

- `darwinSkill.src.searchqa_env`
- `darwinSkill.src.docvqa_env`
- `darwinSkill.src.officeqa_env`
- `darwinSkill.src.alfworld_env`
- `darwinSkill.src.spreadsheetbench_env`
- `darwinSkill.src.livemathematician_env`

Useful runtime helpers:

- `run_reference_benchmark(...)` auto-resolves benchmark-specific evaluators for SearchQA, DocVQA, and OfficeQA.
- `darwinSkill.src.alfworld_env.run_alfworld_episode(...)` runs a native Python ALFWorld episode/runtime loop.
- `darwinSkill.src.alfworld_env.build_live_alfworld_environment_factory(...)` provides an optional bridge to the reference ALFWorld simulator.
- `darwinSkill.src.spreadsheetbench_env.run_spreadsheet_react_session(...)` runs a native Python react/tool loop for SpreadsheetBench.

## Adapter-Aware Behavior

- `run_with_adapter(...)` and `run_reference_adapter(...)` use `train_samples` for the reflective training loop.
- Gate and final evaluation use `eval_samples` when an adapter exposes separate train/eval splits.

## Run Artifact Layout

- `summary.json`
- `history.json`
- `run_state.json`
- `evaluations.json`
- `best_skill.md`
- `final_skill.txt`
- `steps/step_XXXX/`
- `skills/skill_vXXXX.md`
- `slow_update/epoch_XX/`
- `meta_skill/epoch_XX/`

## Parity Notes

- There is no CLI or WebUI. The native Python API is the primary surface.
- SearchQA, DocVQA, and OfficeQA have dedicated loader, evaluator, and adapter paths.
- ALFWorld, SpreadsheetBench, and LiveMathematicianBench have benchmark-native loader, evaluator, and adapter paths.
- SpreadsheetBench supports Python code predictions, JSON artifact bundles, workspace bundles, structured tool calls, react transcripts, and upstream-style conversation replay bundles.
- ALFWorld supports a native episode runner and an optional live environment factory when local dependencies are available.
- `darwinSkill.src.backends` includes target-role wrappers for SpreadsheetBench and ALFWorld, plus provider-compat payload normalizers and family-aware router bootstrap helpers.
- `darwinSkill.src.reference_adapters` includes a registry builder for benchmark aliases and dataset-backed adapters from Python/config inputs.

Current remaining integration gaps are mostly outside the framework core:

- provider-bound live simulator wrappers beyond the native ALFWorld env shim
- production client construction
- external runtime authentication/bootstrap

## Demo Scripts

```bash
PYTHONPATH=. uv run python darwinSkill/scripts/train_demo.py
PYTHONPATH=. uv run python darwinSkill/scripts/pipeline_demo.py
```
