# SOW_0094 - Default Native Delegation Context Isolation

- **Status**: DONE
- **Completed**: 2026-09-28
- **Approval**: User explicitly authorized committing, pushing, and syncing the
  previously identified `sow-delegate-flow` change on 2026-09-28.
- **Task**: Make native delegation guidance explicitly pass `fork_turns: "none"`
  by default, cover expected/negative/boundary cases, and deploy only this skill
  to the Codex legacy user skill directory.
- **Location**:
  - `skills/sow-delegate-flow/SKILL.md`
  - `tests/skill_feedback_cases/sow-delegate-flow.json`
  - `plan_todo/finished/SOW_0094_sow_delegate_native_context_isolation.md`
- **Why**: The native spawn tool defaults to inherited turns when the option is
  omitted. Delegation should start from a self-contained task prompt and avoid
  unrelated parent history unless the user explicitly requests it.
- **As-Is Diagram (ASCII)**:

```text
delegate task
  -> fork_turns omitted or inherited context used
  -> child may receive unrelated parent history
```

- **To-Be Diagram (ASCII)**:

```text
delegate task
  -> explicitly pass fork_turns="none"
  -> send a self-contained bounded prompt
  -> child starts without parent turns
```

- **Decision**: This changes AISkills guidance and its regression fixture only;
  it does not change the Codex tool schema/default. Passing `fork_turns="all"`
  is allowed only after the user explicitly requests inherited history.
- **Deliverables**: Canonical skill guidance, sanitized expected/negative/
  boundary regression coverage, scoped commit, push, and one-skill Codex sync
  with source/install parity verification.
- **Done Criteria**:
  - `sow-delegate-flow` remains registered in `skills/registry.json`.
  - Skill structural validation and focused feedback/sync tests pass.
  - The feedback fixture contains expected, negative, and boundary coverage.
  - Exact scoped diff was committed as `f26bc0c` and pushed to `origin/main`.
  - The exact skill was synced to `~/.codex/skills` and parity verification passed.
  - Isolated model forward-test status is reported separately; deterministic
    checks must not be presented as proof of model behavior.
- **Out-of-Scope**: Changing Codex's native `spawn_agent` schema/default,
  changing other skills or dirty files, syncing other skills/environments, or
  delegating a live task as a behavior test.
- **Proposed-By**: Codex
- **Cautions / Risks**: The host tool default remains unchanged; callers must
  follow the skill and explicitly pass `fork_turns="none"`.

## Verification

- `scripts/quick_validate.py skills/sow-delegate-flow/`: passed.
- `uv run python -m unittest tests.test_skill_feedback_cases tests.test_skill_sync_scripts`:
  passed, 13 tests.
- `git diff --check`: passed.
- Isolated model forward-test: not run; this side conversation does not use
  sub-agents, so model behavior remains unverified.
- Sync dry-run: replaced only `sow-delegate-flow` at `~/.codex/skills`.
- Codex skill sync: passed after canonical push.
- Source/install parity: passed for `~/.codex/skills/sow-delegate-flow`.
