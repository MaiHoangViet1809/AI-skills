- **Status**: complete
- **Approval**: approved 2026-07-08
- **Task**: Migrate `darwinSkill` into a self-contained mini project inside AISkills while preserving the public Python package import name `darwinSkill`.
- **Location**: `darwinSkill/`, `scripts/darwinSkill/`, `tests/darwinSkill/`, `references/SkillOpt/`, `plan_todo/SOW_0047_*.md` through `plan_todo/SOW_0055_*.md`, `plan_todo/skill_framework_distillation_plan.md`, `plan_todo/codex_skill_improvement_data_plan.md`, root `pyproject.toml`, and docs that mention these paths.
- **Why**: `darwinSkill` has grown into a framework-like mini project. Keeping code, scripts, tests, references, and historical planning spread across the parent AISkills repo makes ownership harder to scan. A self-contained `darwinSkill/` boundary makes it clear this is a separate project inside the skill library repo without case-sensitive path ambiguity.
- **Depends-On**: `plan_todo/finished/SOW_0067_review_darwinskill_regroup.md`

## As-Is Diagram

```text
AISkills/
  darwinSkill/                 package code + docs
  scripts/darwinSkill/         demo/extraction/training scripts
  tests/darwinSkill/           tests
  references/SkillOpt/         upstream reference snapshot
  plan_todo/SOW_0047-0055      DarwinSkill implementation history
```

## To-Be Diagram

```text
AISkills/
  darwinSkill/
    README.md
    AGENT_GUIDE.md
    USAGE.md
    PARITY.md
    src/
      *.py
    scripts/
      README.md
      *.py
    tests/
      test_*.py
    references/
      SkillOpt/
```

## Deliverables

- Keep the `darwinSkill/` project boundary as the mini-project root.
- Move runtime package files from root `darwinSkill/*.py` to `darwinSkill/src/*.py`.
- Keep `darwinSkill/README.md`, `AGENT_GUIDE.md`, `USAGE.md`, and `PARITY.md` at the mini-project root.
- Move utility scripts from `scripts/darwinSkill/` to `darwinSkill/scripts/`.
- Move tests from `tests/darwinSkill/` to `darwinSkill/tests/`.
- Move `references/SkillOpt/` to `darwinSkill/references/SkillOpt/`.
- Update imports, test configuration, script paths, and docs so supported imports use `darwinSkill.src.*`.
- Remove all `__init__.py`, `__pycache__`, and `.pyc` files from the DarwinSkill tree.
- Keep AISkills `skills/` registry/install docs unchanged unless a path reference truly points to old DarwinSkill locations.

## Done Criteria

- `import darwinSkill` works through Python namespace package behavior from repo root.
- DarwinSkill tests run from the new boundary: `uv run python -m unittest discover -s darwinSkill/tests`.
- Root skill sync tests still pass: `uv run python -m unittest tests/test_skill_sync_scripts.py`.
- `rg -n "scripts/darwinSkill|tests/darwinSkill|references/SkillOpt" README.md plan_todo scripts skills darwinSkill -g '!darwinSkill/references/SkillOpt/**'` shows only intentional historical notes or updated paths.
- No runtime code remains directly under root `darwinSkill/`.
- No DarwinSkill scripts remain under root `scripts/darwinSkill/`.
- No DarwinSkill tests remain under root `tests/darwinSkill/`.
- No tracked generated cache files are introduced.
- The migration commit does not modify unrelated skill-library files beyond necessary path/docs/config updates.

## Out-of-Scope

- Refactoring DarwinSkill behavior.
- Renaming the Python package import from `darwinSkill` to `DarwinSkill`.
- Changing benchmark semantics.
- Removing or rewriting SkillOpt reference content beyond moving it under `darwinSkill/references/`.
- Changing AISkills agent install-guide behavior unless a stale path reference requires it.

## Cautions / Risks

- Removing `__init__.py` means imports rely on Python namespace package behavior.
- `uv` and test discovery may need config changes if root `pyproject.toml` assumes package files at repo root.
- Scripts may use relative paths that break after moving under `darwinSkill/scripts/`.
- References in historical SOWs can stay historical, but active docs should point to new paths.
- Do not silently flatten `references/SkillOpt/`; keep it as a reference snapshot.

## Verification

- `uv run python -m unittest discover -s darwinSkill/tests`
- `uv run python -m unittest tests/test_skill_sync_scripts.py`
- `git diff --check`
- stale path scan for old DarwinSkill paths
