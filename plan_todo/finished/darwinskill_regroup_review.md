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

## Finding

`darwinSkill` feels spread out because it spans package code, scripts, tests,
planning, and references. That spread is mostly a normal Python repo layout, not
a broken ownership boundary.

The risky move would be a mechanical directory migration just to make the tree
look grouped. That would change import paths, test paths, docs links, and script
assumptions without improving runtime behavior.

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
