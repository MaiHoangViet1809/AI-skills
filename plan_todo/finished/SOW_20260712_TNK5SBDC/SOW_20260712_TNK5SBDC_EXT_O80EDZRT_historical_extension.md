# SOW_20260712_TNK5SBDC_EXT_O80EDZRT - Extension 1: Overwrite Dry-Run Parity

- Status: done
- Approval: approved by user on 2026-07-12
- create_dttm: unknown
- approve_dttm: unknown
- finish_dttm: unknown
- legacy_id: SOW_0071_EXT_1
- legacy_path: plan_todo/finished/SOW_0071_skill_evolution_feedback_loop.md
- migrated_dttm: 2026-10-08T12:48:51+07:00
- Parent: [SOW_20260712_TNK5SBDC](SOW_20260712_TNK5SBDC_skill_evolution_feedback_loop.md)

## Preserved Contract And Historical Evidence

## Extension 1: Overwrite Dry-Run Parity

- **Status**: done
- **Approval**: approved by user on 2026-07-12
- **Finding**: The workflow previews an existing target without `--overwrite`, so dry-run reports `skip` while execution uses `--overwrite` and performs `replace`.
- **Location**: `skills/skill-evolution-flow/SKILL.md`, `scripts/skills/README.md`, `tests/test_skill_sync_scripts.py`, `plan_todo/fix_bug.md`, and this SOW.
- **Change**:
  - require preview and execution to use the same agent, scope, target, skill, and overwrite flags;
  - preview adds `--dry-run`; execution removes only `--dry-run`;
  - add a regression test proving overwrite dry-run reports `replace` without mutating the existing target.
- **Done Criteria**:
  - an existing target preview reports `replace`, not `skip`;
  - preview leaves stale target content unchanged;
  - the corresponding execution replaces only the selected skill;
  - structural validation, full tests, exact-skill sync, and installed parity pass.
- **Out-of-Scope**: changing sync command semantics, adding multi-skill sync, or modifying unrelated skills.
- **Verification**:
  - overwrite preview reported `replace` and did not mutate the target;
  - full suite passed, 12 tests;
  - canonical fix commit: `1674b60`;
  - exact Codex legacy-user overwrite sync and source/install parity passed.
