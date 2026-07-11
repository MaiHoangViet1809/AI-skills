# Bug Log

## 2026-07-12 — Skill evolution overwrite preview mismatch

- **SOW**: `plan_todo/SOW_0071_skill_evolution_feedback_loop.md`, Extension 1
- **Root cause**: dry-run omitted `--overwrite`, while execution added it, so preview returned `skip` instead of previewing `replace`.
- **Fix boundary**: align preview and execution flags in `skill-evolution-flow` and add a non-mutating overwrite-preview regression test.
