# darwinSkill

`darwinSkill` la mot module tree Python cho skill tu tien hoa thong qua training.

Public imports v1:

```python
from darwinSkill.native import run_training, run_evaluation, run_reference_benchmark
from darwinSkill.trainer import SkillTrainer
from darwinSkill.pipeline import SkillPipeline
from darwinSkill.contracts import SkillSample, TrainingConfig, EvaluationConfig, PipelineConfig
from darwinSkill.evaluators import ExactMatchEvaluator
from darwinSkill.demo_text import DarwinMemoryBackend, demo_samples
from darwinSkill.reference_adapters import SearchQAAdapter, DocVQAAdapter, OfficeQAAdapter
```

Docs:

- [USAGE.md](/Users/maihoangviet/Projects/AISkills/darwinSkill/USAGE.md)
- [PARITY.md](/Users/maihoangviet/Projects/AISkills/darwinSkill/PARITY.md)

Philosophy v1:

- anchor la text skill
- sample contract la `prompt + expected_answer + metric`
- `SkillPipeline` chi ho tro linear stages
- trainer core dung reflective engine co gate, step artifacts, slow update, va meta skill memory
- `if/else/merge` duoc orchestration bang Python caller, khong phai graph API

Native helpers:

- `darwinSkill.native.run_training(...)`
- `darwinSkill.native.run_evaluation(...)`
- `darwinSkill.native.run_reference_benchmark(...)`
- `darwinSkill.native.run_reference_benchmark_from_path(...)`
- `darwinSkill.reference_adapters.*Adapter`
- `darwinSkill.inspection.inspect_run(...)`
- `darwinSkill.inspection.summarize_run(...)`
- `darwinSkill.inspection.load_step_record(...)`
- `darwinSkill.backends.build_spreadsheetbench_router(...)`
- `darwinSkill.backends.build_alfworld_router(...)`
- `darwinSkill.reference_adapters.build_reference_adapter(...)`
- `darwinSkill.config_loader.build_reference_adapter_from_config(...)`
- `darwinSkill.backends.build_openai_compat_backend(...)`
- `darwinSkill.backends.build_claude_compat_backend(...)`
- `darwinSkill.backends.build_qwen_compat_backend(...)`
- `darwinSkill.backends.build_codex_compat_backend(...)`
- `darwinSkill.backends.build_provider_compat_backend_for_family(...)`
- `darwinSkill.backends.build_interactive_router_for_benchmark(...)`

Benchmark-native surfaces:

- `darwinSkill.searchqa_env`
- `darwinSkill.docvqa_env`
- `darwinSkill.officeqa_env`
- `darwinSkill.alfworld_env`
- `darwinSkill.spreadsheetbench_env`
- `darwinSkill.livemathematician_env`
- `run_reference_benchmark(...)` tu auto chon evaluator benchmark-specific cho SearchQA, DocVQA, OfficeQA
- `darwinSkill.alfworld_env.run_alfworld_episode(...)` cho native Python episode/runtime loop cua ALFWorld
- `darwinSkill.alfworld_env.build_live_alfworld_environment_factory(...)` cho optional live simulator bridge cua ALFWorld
- `darwinSkill.spreadsheetbench_env.run_spreadsheet_react_session(...)` cho native Python react/tool loop cua SpreadsheetBench

Adapter-aware behavior:

- `run_with_adapter(...)` va `run_reference_adapter(...)` dung `train_samples` cho step loop
- gate/final report dung `eval_samples` neu adapter co split train/eval rieng

Run artifact layout:

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

Parity notes:

- khong co CLI va WebUI; native Python API la surface chinh
- SearchQA, DocVQA, OfficeQA da co loader + evaluator + adapter path rieng
- ALFWorld, SpreadsheetBench, LiveMathematicianBench da co benchmark-native loader/evaluator/adapter path
- SpreadsheetBench evaluator da co the chay prediction dang Python code block de sinh workbook output
- SpreadsheetBench evaluator cung hieu prediction dang JSON artifact bundle chua `solution.py` hoac `output.xlsx`
- SpreadsheetBench evaluator da ho tro them workspace bundle `files + commands`, gan hon voi react/tool orchestration
- SpreadsheetBench evaluator da ho tro them structured `tool_calls` bundle (`write_file` + `bash`)
- SpreadsheetBench evaluator da ho tro them `react transcript` bundle co assistant turns + tool_calls
- SpreadsheetBench evaluator da ho tro them upstream-style `conversation` bundle khi `conversation.json` di kem `solution.py` artifact/file
- SpreadsheetBench da co them native react runner surface de backend co the sinh `conversation + solution.py` bundle bang Python API
- ALFWorld da co them native episode runner surface de backend callback + env shim sinh runtime bundle co trajectory
- ALFWorld da co them optional live environment factory de bridge vao reference vendor simulator khi local runtime co san
- `darwinSkill.backends` da co them target-role wrappers cho `SpreadsheetBench` va `ALFWorld` de `BackendRouter` goi interactive runtime qua native Python callback
- `darwinSkill.backends` da co them provider-compat wrappers de normalize OpenAI/Claude/Qwen/Codex-style tool-call payloads vao interactive runners
- `darwinSkill.backends` da co them family-aware bootstrap helper de di tu benchmark + provider family -> interactive router gan nhu turnkey
- `darwinSkill.reference_adapters` da co registry builder de resolve benchmark aliases va dataset-backed adapters tu Python/config layer
- runtime/tool parity day du con thieu chu yeu o:
  - ALFWorld provider-bound live simulator wrappers beyond native env shim
  - production client construction va external runtime authentication/bootstrap van nam o integration layer

Run demos:

```bash
PYTHONPATH=. uv run python scripts/darwinSkill/train_demo.py
PYTHONPATH=. uv run python scripts/darwinSkill/pipeline_demo.py
```
