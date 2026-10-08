# Bug Log

## 2026-07-12 — Skill evolution overwrite preview mismatch

- **SOW**: [SOW_20260712_TNK5SBDC](finished/SOW_20260712_TNK5SBDC/SOW_20260712_TNK5SBDC_skill_evolution_feedback_loop.md), [Extension 1](finished/SOW_20260712_TNK5SBDC/SOW_20260712_TNK5SBDC_EXT_O80EDZRT_historical_extension.md)
- **Root cause**: dry-run omitted `--overwrite`, while execution added it, so preview returned `skip` instead of previewing `replace`.
- **Fix boundary**: align preview and execution flags in `skill-evolution-flow` and add a non-mutating overwrite-preview regression test.
