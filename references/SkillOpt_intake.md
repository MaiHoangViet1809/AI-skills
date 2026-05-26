# SkillOpt Intake

## Source

- Upstream repo: `microsoft/SkillOpt`
- Local reference clone: `references/SkillOpt/`
- Paper link found in upstream README/project page: `https://arxiv.org/abs/2605.23904`

## Repository Shape

- `skillopt/`: core runtime package
- `scripts/`: training and eval entrypoints
- `configs/`: benchmark presets
- `docs/`: docs site source
- `skillopt_webui/`: optional monitoring UI
- `index.html`, `skillopt.html`: generated/static project pages

## Core Pipeline

The runtime is centered on `scripts/train.py` plus `skillopt.engine.trainer.ReflACTTrainer`.

Current flow:

1. Load YAML config with `_base_` inheritance and flatten it for runtime use.
2. Resolve an environment adapter from a lazy registry.
3. Build a `ReflACTTrainer(cfg, adapter)`.
4. Run the 6-stage loop:
   - rollout
   - reflect
   - aggregate
   - select
   - update
   - evaluate/gate
5. Persist outputs such as `history.json`, `runtime_state.json`, `best_skill.md`, and per-step artifacts.

## Architecture Notes

- The adapter boundary is the cleanest reusable abstraction:
  - `EnvAdapter`
  - `BaseDataLoader` / `BatchSpec`
- The current public surface is CLI-heavy:
  - `scripts/train.py` and `scripts/eval_only.py` each own large argument parsers and override mapping logic.
- Config handling is split between:
  - structured YAML in `skillopt/config.py`
  - flattening to a legacy flat runtime dict
- Backend/model routing is runtime-global and environment-variable-driven.
- Environment implementations dominate the codebase size, so a future sklearn-like rewrite should separate:
  - reusable optimization loop
  - backend/model clients
  - benchmark adapters
  - user-facing pipeline API

## LOC Baseline

Count method:

- counted tracked text files from upstream via `git ls-files`
- included: `.py`, `.md`, `.yaml`, `.yml`, `.toml`, `.txt`, `.json`, `.html`, `.css`, `.js`, `.svg`
- excluded: `.git/` internals and untracked/generated files not in Git

Totals:

- all tracked text lines: `28,554`
- Python lines only: `19,489`
- core runtime lines (`skillopt/` + `scripts/`): `20,481`

Top-level text-line distribution:

- `skillopt`: `19,536`
- `(root)`: `5,949`
- `docs`: `1,303`
- `scripts`: `945`
- `skillopt_webui`: `553`
- `configs`: `267`

Core Python distribution:

- `skillopt/envs`: `8,374`
- `skillopt/model`: `4,294`
- `skillopt/engine`: `1,921`
- `skillopt/optimizer`: `1,202`
- `scripts`: `945`
- `skillopt/gradient`: `856`
- `skillopt`: `599`
- `skillopt/datasets`: `519`
- `skillopt/evaluation`: `80`
- `skillopt/utils`: `75`

## Distillation Direction

A sklearn-like distillation should likely target a smaller API around objects such as:

- `SkillDataset`
- `SkillEnvAdapter`
- `SkillOptimizer`
- `SkillTrainer.fit()`
- `SkillTrainer.evaluate()`
- `SkillRunArtifacts`

The main cleanup opportunity is to move from:

- CLI-first orchestration
- flat config dict plumbing
- global backend state

to:

- object-first orchestration
- typed config objects
- explicit dependency injection
- stable reusable train/eval interfaces
