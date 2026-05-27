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
- `darwinSkill.reference_adapters.*Adapter`

Benchmark-native surfaces:

- `darwinSkill.searchqa_env`
- `darwinSkill.docvqa_env`
- `darwinSkill.officeqa_env`
- `darwinSkill.alfworld_env`
- `darwinSkill.spreadsheetbench_env`
- `darwinSkill.livemathematician_env`
- `run_reference_benchmark(...)` tu auto chon evaluator benchmark-specific cho SearchQA, DocVQA, OfficeQA

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
- runtime/tool parity day du cho ALFWorld simulator va SpreadsheetBench codegen/react van con la phan can dao sau them

Run demos:

```bash
PYTHONPATH=. uv run python scripts/darwinSkill/train_demo.py
PYTHONPATH=. uv run python scripts/darwinSkill/pipeline_demo.py
```
