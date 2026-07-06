- **Status**: draft
- **Approval**: pending
- **Task**: Add guarded OpenCode and other-agent skill sync entrypoints that copy AISkills repo skills only to explicit user-provided target roots.
- **Location**: `scripts/skills/sync_env_opencode.py`, `scripts/skills/sync_env_others.py`, shared helper files under `scripts/skills/` from SOW 0062 if needed, focused tests or verification scripts under `tests/` or `scripts/skills/`, `scripts/skills/README.md`, `plan_todo/agent_skill_sync_refine_plan.md`, and this SOW.
- **Depends-On**: `plan_todo/SOW_0062_core_codex_skill_sync.md`
- **Why**: The project should provide separate commands for OpenCode and future agents without guessing undocumented skill destinations or silently installing to multiple agents.
- **As-Is Diagram (ASCII)**:
```text
AISkills/skills/<skill>
  |
  v
Codex-centric sync only
```
- **To-Be Diagram (ASCII)**:
```text
AISkills/skills/<skill>
  |
  +--> sync_env_opencode.py --target-root <explicit-root>
  |
  +--> sync_env_others.py   --target-root <explicit-root>

No default OpenCode repo/user destination until verified.
No policy/rule file creation.
```
- **Deliverables**:
  - Add `scripts/skills/sync_env_opencode.py` as a guarded OpenCode entrypoint.
  - Add `scripts/skills/sync_env_others.py` as a custom/unsupported-agent entrypoint.
  - Require explicit `--target-root` for both entrypoints.
  - Support `--skill <name>`, `--all`, `--dry-run`, and `--overwrite`.
  - Reuse shared discovery/copy behavior from SOW 0062 where it avoids real duplication.
  - Do not implement OpenCode default repo/user destinations until verified and captured in a later SOW.
  - Do not support `legacy-user` or `codex-hooks` in either entrypoint.
  - Keep `--all` defined as all repo skill folders under `AISkills/skills/` that contain `SKILL.md`.
  - Add README examples showing guarded OpenCode/custom usage with explicit target roots on macOS and Windows.
- **Done Criteria**:
  - `sync_env_opencode.py` fails clearly without `--target-root`.
  - `sync_env_others.py` fails clearly without `--target-root`.
  - Explicit target-root dry-runs show the exact destination before copying.
  - Both entrypoints reject or omit unsupported scope/profile options.
  - Existing overwrite safety remains opt-in.
  - Implementation uses `pathlib.Path` and supports explicit Windows-style paths without hardcoded POSIX assumptions.
  - Neither entrypoint creates `AGENTS.md`, `CLAUDE.md`, `.agents/rules`, `.claude` policy files, hooks, configs, or CLI setup.
- **Out-of-Scope**:
  - Verifying or implementing OpenCode default skill destinations.
  - Codex and Claude default destinations.
  - Project policy/rule initialization.
  - Installing OpenCode or any other agent CLI.
  - Hybrid multi-agent sync in a single command.
- **Proposed-By**: Codex GPT-5
- **plan**: `plan_todo/agent_skill_sync_refine_plan.md`
- **Cautions / Risks**:
  - Guessing OpenCode destinations can create silent dead installs or leak skills into the wrong project.
  - A generic "others" command must stay explicit-target-only; otherwise it becomes an unreviewed compatibility layer.
  - Do not turn this into a policy initializer; it is only a skill copier.
