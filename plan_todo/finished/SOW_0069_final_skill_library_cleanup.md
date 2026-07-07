- **Status**: complete
- **Approval**: approved 2026-07-08
- **Task**: Run the final library cleanup and verification pass after telemetry removal, GitHub install-guide replacement, and `darwinSkill` regroup review.
- **Location**: root `README.md`, `INSTALL_FOR_AGENTS.md`, `skills/`, `scripts/skills/`, `tests/`, `plan_todo/skill_design_decisions.md`, and `plan_todo/agent_skill_library_cleanup_plan.md`.
- **Why**: After the focused SOWs land, the repo needs one final consistency pass so active docs, skill manifests, local sync scripts, and planning decisions all present AISkills as a portable skill library.
- **Depends-On**: `plan_todo/SOW_0066_remove_telemetry_dashboard.md`, `plan_todo/SOW_0067_review_darwinskill_regroup.md`, and `plan_todo/SOW_0068_agent_github_install_guide.md`
- **As-Is Diagram (ASCII)**:
```text
focused SOWs
  -> remove telemetry/dashboard
  -> review darwinSkill
  -> add GitHub install guide

remaining risk
  -> stale docs
  -> stale skill registry
  -> stale design decisions
```
- **To-Be Diagram (ASCII)**:
```text
AISkills
  -> active skills are supported
  -> install guide is primary agent path
  -> local sync scripts are optional clone path
  -> docs match actual repo state
  -> completed plan/SOWs moved to finished/
```
- **Deliverables**:
  - Re-run active owned-path scans for deleted telemetry/dashboard/create-agents surfaces, treating `references/` and `plan_todo/finished/` as historical context rather than active product surface.
  - Update `plan_todo/skill_design_decisions.md` with the new distribution decision.
  - Ensure active skill list and registry contain only supported skills.
  - Ensure root README presents AISkills as a portable skill library.
  - Ensure `scripts/skills/README.md` presents Python sync scripts as optional cloned-repo convenience.
  - Verify install docs against Codex, Claude Code, OpenCode, and other-agent target-root paths.
  - Move completed plan/SOW files to `plan_todo/finished/` when the whole cleanup plan is complete.
- **Done Criteria**:
  - No active docs claim telemetry/dashboard is maintained in this repo.
  - No active docs claim `create-agents-md` exists.
  - `INSTALL_FOR_AGENTS.md` is the primary agent-facing install path.
  - Local cloned-repo sync scripts are documented as optional convenience commands.
  - Registry/manifest validation passes.
  - Skill sync tests pass.
  - Worktree changes do not include unrelated staged user deletions unless separately approved.
- **Out-of-Scope**:
  - New feature work beyond cleanup consistency.
  - Implementing the `darwinSkill` move if SOW 0067 recommends one.
  - Installing or validating external OSS telemetry tooling.
- **Proposed-By**: Codex GPT-5
- **plan**: `plan_todo/agent_skill_library_cleanup_plan.md`
- **Cautions / Risks**:
  - Final cleanup can become a grab bag; keep it limited to consistency and verification.
  - Finished historical planning docs may still mention removed systems; distinguish historical records from active docs.
