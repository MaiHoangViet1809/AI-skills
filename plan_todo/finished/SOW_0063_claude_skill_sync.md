- **Status**: completed
- **Approval**: approved 2026-07-07
- **Completed**: 2026-07-07
- **Task**: Add Claude Code skill sync support as a separate public entrypoint that publishes AISkills repo skills to Claude Code repo/user skill directories.
- **Location**: `scripts/skills/sync_env_claude.py`, shared helper files under `scripts/skills/` from SOW 0062 if needed, focused tests or verification scripts under `tests/` or `scripts/skills/`, `scripts/skills/README.md`, `plan_todo/finished/agent_skill_sync_refine_plan.md`, and this SOW.
- **Depends-On**: `plan_todo/finished/SOW_0062_core_codex_skill_sync.md`
- **Why**: Claude Code uses different project/user skill locations from Codex. Its sync command must be explicit, agent-specific, and must not inherit Codex-only legacy paths or hook/config behavior.
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
  v
sync_env_claude.py
  -> --scope repo  <target-project>/.claude/skills/<skill>
  -> --scope user  $HOME/.claude/skills/<skill>

sync_env_claude.py
  -> no legacy-user scope
  -> no codex-hooks profile
  -> no AGENTS.md / CLAUDE.md / policy-rule creation
```
- **Deliverables**:
  - Add `scripts/skills/sync_env_claude.py` as a first-class entrypoint, not a hybrid Codex/Claude mode.
  - Support `--scope repo|user`, `--target-project`, `--skill <name>`, `--all`, `--target-root`, `--dry-run`, and `--overwrite`.
  - Use shared discovery/copy behavior from SOW 0062 where it avoids real duplication.
  - Resolve repo scope to `<target-project>/.claude/skills/<skill-name>/`.
  - Resolve user scope to `$HOME/.claude/skills/<skill-name>/`.
  - Reject `--scope legacy-user` clearly.
  - Reject `--profile codex-hooks` or omit `--profile` entirely for Claude.
  - Keep `--all` defined as all repo skill folders under `AISkills/skills/` that contain `SKILL.md`.
  - Add focused README examples for Claude repo/user sync on macOS and Windows path styles.
- **Done Criteria**:
  - Claude repo-scope dry-run shows `<target-project>/.claude/skills/<skill-name>/`.
  - Claude user-scope dry-run shows `$HOME/.claude/skills/<skill-name>/`.
  - `sync_env_claude.py --scope legacy-user` fails with a clear error.
  - Claude sync never writes `hooks.json`, `codex_hook_bridge.py`, `config.toml`, `AGENTS.md`, `CLAUDE.md`, `.agents/rules`, or project policy files.
  - Missing `--target-project` for repo scope fails unless `--target-root` is supplied.
  - Existing overwrite safety remains opt-in.
  - Implementation uses `pathlib.Path` and supports explicit Windows-style paths without hardcoded POSIX assumptions.
- **Out-of-Scope**:
  - Codex sync behavior except shared helper reuse.
  - OpenCode or other-agent sync.
  - Creating or modifying Claude project policy/context files.
  - Installing or configuring the Claude Code CLI.
  - Hybrid multi-agent sync in a single command.
- **Proposed-By**: Codex GPT-5
- **plan**: `plan_todo/finished/agent_skill_sync_refine_plan.md`
- **Cautions / Risks**:
  - Copying Codex hook/config behavior into Claude would mutate unrelated environment state.
  - Treating Codex legacy paths as Claude-compatible would make sync appear successful while Claude cannot discover the skill.
  - Copy the skill tree as-is, but do not assume Codex-only metadata is meaningful to Claude.
