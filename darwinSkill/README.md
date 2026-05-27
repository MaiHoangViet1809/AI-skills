# darwinSkill

`darwinSkill` la mot module tree Python cho skill tu tien hoa thong qua training.

Public imports v1:

```python
from darwinSkill.trainer import SkillTrainer
from darwinSkill.pipeline import SkillPipeline
from darwinSkill.contracts import SkillSample, TrainingConfig, EvaluationConfig, PipelineConfig
from darwinSkill.evaluators import ExactMatchEvaluator
from darwinSkill.demo_text import DarwinMemoryBackend, demo_samples
```

Philosophy v1:

- anchor la text skill
- sample contract la `prompt + expected_answer + metric`
- `SkillPipeline` chi ho tro linear stages
- `if/else/merge` duoc orchestration bang Python caller, khong phai graph API

Run demos:

```bash
PYTHONPATH=. uv run python scripts/darwinSkill/train_demo.py
PYTHONPATH=. uv run python scripts/darwinSkill/pipeline_demo.py
```
