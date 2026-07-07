# DarwinSkill Regroup Review

- **Date**: 2026-07-08
- **Scope**: Review current `darwinSkill` placement and recommend regrouping direction.
- **SOW**: `SOW_0067_review_darwinskill_regroup.md`

## Inventory

| Surface | Current path | Role | Review |
| --- | --- | --- | --- |
| Library code | `darwinSkill/*.py` | Runtime, pipeline, adapters, providers, benchmarks, reference envs | Cohesive package root; many modules, but not actually scattered across repo. |
| Library docs | `darwinSkill/README.md`, `AGENT_GUIDE.md`, `USAGE.md`, `PARITY.md` | User and agent guidance | Correctly colocated with package. |
| Utility scripts | `scripts/darwinSkill/*.py` | Demos, harvesting, extraction, training helpers | Conventional script split, but discoverability depends on `scripts/darwinSkill/README.md`. |
| Tests | `tests/darwinSkill/test_*.py` | Package validation | Conventional test split; mirrors package boundary. |
| Planning history | `plan_todo/SOW_0047...SOW_0055...` | Implementation lineage | Correctly kept in planning, not runtime. |
| External reference | `references/SkillOpt/` | Source/reference material | Correctly outside runtime package. |

Exact owned paths reviewed:

- `darwinSkill/AGENT_GUIDE.md`
- `darwinSkill/PARITY.md`
- `darwinSkill/README.md`
- `darwinSkill/USAGE.md`
- `darwinSkill/*.py`
- `scripts/darwinSkill/README.md`
- `scripts/darwinSkill/*.py`
- `tests/darwinSkill/test_*.py`
- `plan_todo/SOW_0047_skillopt_reflective_engine_parity.md`
- `plan_todo/SOW_0048_skillopt_runtime_state_resume_and_artifact_lineage.md`
- `plan_todo/SOW_0049_skillopt_epoch_memory_parity.md`
- `plan_todo/SOW_0050_skillopt_backend_router_and_dual_role_execution.md`
- `plan_todo/SOW_0051_skillopt_adapter_dataloader_and_config_migration.md`
- `plan_todo/SOW_0052_skillopt_native_python_run_and_eval_surface.md`
- `plan_todo/SOW_0053_skillopt_benchmark_pack_text_and_doc_tasks.md`
- `plan_todo/SOW_0054_skillopt_benchmark_pack_interactive_and_tool_tasks.md`
- `plan_todo/SOW_0055_skillopt_api_ergonomics_and_parity_docs.md`
- `references/SkillOpt/`

## Finding

`darwinSkill` feels spread out because it spans package code, scripts, tests,
planning, and references. That spread is mostly a normal Python repo layout, not
a broken ownership boundary.

The risky move would be a mechanical directory migration just to make the tree
look grouped. That would change import paths, test paths, docs links, and script
assumptions without improving runtime behavior.

No tracked `__pycache__` or `.pyc` artifacts were found under `darwinSkill/`,
`scripts/darwinSkill/`, or `tests/darwinSkill/`.

## Planning Disposition

| SOW | Status in file | Review disposition |
| --- | --- | --- |
| `SOW_0047_skillopt_reflective_engine_parity.md` | `completed` | Historical implementation record; eligible to move to `plan_todo/finished/` in a planning cleanup. |
| `SOW_0048_skillopt_runtime_state_resume_and_artifact_lineage.md` | `completed` | Historical implementation record; eligible to move to `plan_todo/finished/` in a planning cleanup. |
| `SOW_0049_skillopt_epoch_memory_parity.md` | `completed` | Historical implementation record; eligible to move to `plan_todo/finished/` in a planning cleanup. |
| `SOW_0050_skillopt_backend_router_and_dual_role_execution.md` | `completed` | Historical implementation record; eligible to move to `plan_todo/finished/` in a planning cleanup. |
| `SOW_0051_skillopt_adapter_dataloader_and_config_migration.md` | `completed` | Historical implementation record; eligible to move to `plan_todo/finished/` in a planning cleanup. |
| `SOW_0052_skillopt_native_python_run_and_eval_surface.md` | `completed` | Historical implementation record; eligible to move to `plan_todo/finished/` in a planning cleanup. |
| `SOW_0053_skillopt_benchmark_pack_text_and_doc_tasks.md` | `completed` | Historical implementation record; eligible to move to `plan_todo/finished/` in a planning cleanup. |
| `SOW_0054_skillopt_benchmark_pack_interactive_and_tool_tasks.md` | `completed` | Historical implementation record; eligible to move to `plan_todo/finished/` in a planning cleanup. |
| `SOW_0055_skillopt_api_ergonomics_and_parity_docs.md` | `completed` | Historical implementation record; eligible to move to `plan_todo/finished/` in a planning cleanup. |

This SOW does not move those files. The regroup review is advisory; moving old
planning records should be a separate low-risk docs cleanup so it does not hide
the framework-layout decision.

## Layout Options

| Option | Verdict | Reason |
| --- | --- | --- |
| Keep current Python convention: `darwinSkill/`, `scripts/darwinSkill/`, `tests/darwinSkill/` | Recommended now | Lowest risk, import paths stay stable, test layout stays conventional. |
| Move package to `src/darwinSkill/` | Defer | Useful only if packaging/import isolation becomes a concrete requirement. |
| Group everything under `projects/darwinSkill/` | Reject for now | Makes the repo look grouped, but forces broad path churn across imports, scripts, tests, and docs. |
| Create `darwinSkill_workspace/` | Reject | Adds a new ownership concept without solving runtime or packaging issues. |

## Recommendation

Use a soft regroup first:

- Keep runtime code in `darwinSkill/`.
- Keep tests in `tests/darwinSkill/`.
- Keep utility scripts in `scripts/darwinSkill/`.
- Add or maintain a short ownership map in `darwinSkill/README.md` if future
  work needs better navigation.
- Only open a migration SOW if there is a concrete packaging target, such as
  moving to `src/darwinSkill/` or publishing the package.

## Future Migration Trigger

Open a separate SOW only if one of these becomes true:

- packaging requires `src/` layout
- imports become ambiguous
- script entry points need packaging as console commands
- tests need strict package-install validation

Until then, avoid moving files.
