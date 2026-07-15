# SOW_0072 - Remove Mandatory CodeGraph Skill Policy

- **Status**: DONE
- **Approval**: approved by user request on 2026-07-16
- **Task**: Remove mandatory CodeGraph and `code-context-search-policy` usage from AISkills-owned Codex workflows while keeping tool choice evidence-driven.
- **Location**:
  - `skills/task-execution-flow/SKILL.md`
  - `skills/task-review-investigate-compare/SKILL.md`
  - `tests/skill_feedback_cases/task-execution-flow.json`
  - `tests/skill_feedback_cases/task-review-investigate-compare.json`
  - `plan_todo/SOW_0072_remove_mandatory_codegraph_skill_policy.md`
- **Why**: CodeGraph may be unavailable or uninitialized. Requiring it adds ceremony and can interrupt normal repository inspection when `rg`, direct file reads, or another available tool is sufficient.
- **Principle**: KISS and tool neutrality. Skills define the evidence requirement, not one mandatory navigation implementation.
- **As-Is Diagram (ASCII)**:

```text
codebase task
  -> mandatory code-context-search-policy
  -> CodeGraph-first rule
  -> unavailable index can interrupt work
```

- **To-Be Diagram (ASCII)**:

```text
codebase task
  -> choose an available suitable inspection method
  -> gather sufficient evidence
  -> no mandatory CodeGraph setup or invocation
```

- **Deliverables**:
  - Remove the mandatory `code-context-search-policy` composition rule from `task-execution-flow`.
  - Remove CodeGraph-first wording from `task-review-investigate-compare`.
  - Preserve `rg` as a useful literal-text option without making one search tool universal.
  - Add positive, negative, and boundary regression scenarios for both changed skills.
  - Validate, commit, sync each changed skill individually to the Codex legacy-user environment, and verify exact parity.
- **Done Criteria**:
  - AISkills-owned skill instructions contain no mandatory CodeGraph or `code-context-search-policy` rule.
  - Reviews and execution tasks may use CodeGraph when useful and available, but never require initialization or invocation.
  - Existing evidence, authority, verification, writeback, and closeout behavior remains unchanged.
  - Both skill folders pass the available structural validator.
  - `uv run python -m unittest tests.test_skill_feedback_cases tests.test_skill_sync_scripts` passes.
  - Exact single-skill dry-run, sync, and parity verification pass for both changed skills.
- **Out-of-Scope**:
  - Modifying system, plugin-owned, or installed-only skills not registered in AISkills.
  - Removing CodeGraph tooling itself.
  - Changing task routing, review modes, verification severity, or git policy.
  - Syncing any non-Codex environment or using `--all`.
- **Proposed-By**: Codex GPT-5
- **Plan / Reference**: Standalone user-requested skill correction using `skill-evolution-flow`; related historical context: `SOW_0057_task_execution_flow_skill.md`.
- **Cautions / Risks**:
  - Removing a mandatory tool must not weaken the requirement to inspect real code and gather evidence.
  - Do not replace CodeGraph-first with an equally rigid `rg`-first rule for every question.
  - The installed-only `code-context-search-policy` skill has no AISkills registry owner and must not be edited as canonical source.

## Closeout

Definitely implemented:

- Removed mandatory `code-context-search-policy` composition from `task-execution-flow`.
- Removed CodeGraph-first evidence rules from `task-review-investigate-compare`.
- Kept CodeGraph optional when already available and useful.
- Added regression cases `optional-code-search-tool-execution-001` and
  `optional-code-search-tool-review-001`.
- Committed canonical changes as `23809c2`.
- Synced both changed skills individually to the Codex legacy-user skill root;
  exact parity passed for each.

Verification:

- Structural validation passed for both changed skill folders.
- `uv run python -m unittest tests.test_skill_feedback_cases tests.test_skill_sync_scripts` passed: 12 tests.
- `uv run python -m unittest discover -s tests` passed: 12 tests.
- `git diff --check` passed.
- Exact overwrite dry-run, sync, and parity verification passed separately for
  both skills.

Not modified or not verified:

- No isolated model forward-test ran because side-conversation subagents were
  unavailable; deterministic validation does not claim model-behavior proof.
- The installed-only `code-context-search-policy` skill still exists and still
  contains CodeGraph-first guidance. It has no AISkills registry/canonical
  source, so this SOW did not mutate or vendor it.
