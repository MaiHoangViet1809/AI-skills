# darwinSkill Scripts

- `PYTHONPATH=. uv run python darwinSkill/scripts/train_demo.py`
- `PYTHONPATH=. uv run python darwinSkill/scripts/pipeline_demo.py`
- `PYTHONPATH=. uv run python darwinSkill/scripts/harvest_provider_logs.py --provider codex --input /abs/path/to/session.jsonl --output /abs/path/to/canonical.json`
- `PYTHONPATH=. uv run python darwinSkill/scripts/extract_skill_examples.py --input /abs/path/to/canonical.json --output /abs/path/to/examples.json --skill-name task-execution-flow`

Branching and merge behavior should stay in caller Python code when needed. It is not part of the public `SkillPipeline` API.
