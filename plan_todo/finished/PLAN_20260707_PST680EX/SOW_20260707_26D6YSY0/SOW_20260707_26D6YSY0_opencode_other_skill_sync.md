# SOW_20260707_26D6YSY0 - opencode other skill sync

- Status: completed
- Approval: approved 2026-07-07
- create_dttm: 2026-07-07T01:46:55+07:00
- create_date: 2026-07-07
- create_dttm_source: filesystem_birthtime
- create_dttm_confidence: filesystem_proxy
- create_dttm_evidence: `plan_todo/finished/SOW_20261008_VO3LKN0L/creation-date-evidence.json` (record: SOW_20260707_26D6YSY0)
- approve_dttm: unknown
- finish_dttm: unknown
- legacy_id: SOW_0064
- legacy_path: plan_todo/finished/SOW_0064_opencode_other_skill_sync.md
- migrated_dttm: 2026-10-08T12:48:51+07:00

## Preserved Contract And Historical Evidence

- **Status**: completed
- **Approval**: approved 2026-07-07
- **Completed**: 2026-07-07
- **Task**: Add OpenCode and other-agent skill sync entrypoints that copy AISkills repo skills to OpenCode native repo/user paths or explicit user-provided target roots.
- **Location**: `scripts/skills/sync_env_opencode.py`, `scripts/skills/sync_env_others.py`, shared helper files under `scripts/skills/` from SOW 0062 if needed, focused tests or verification scripts under `tests/` or `scripts/skills/`, `scripts/skills/README.md`, `plan_todo/finished/PLAN_20260707_PST680EX/PLAN_20260707_PST680EX_agent_skill_sync_refine_plan.md`, and this SOW.
- **Depends-On**: `plan_todo/finished/PLAN_20260707_PST680EX/SOW_20260707_XQ5APZF3/SOW_20260707_XQ5APZF3_core_codex_skill_sync.md`
- **Why**: The project should provide separate commands for OpenCode and future agents without silently installing to multiple agents. OpenCode has native skill destinations, while unsupported agents must stay explicit-target-only.
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
  +--> sync_env_opencode.py
  |      -> --scope repo  <target-project>/.opencode/skills/<skill>
  |      -> --scope user  $HOME/.config/opencode/skills/<skill>
  |      -> --target-root <explicit-root>
  |
  +--> sync_env_others.py
         -> --target-root <explicit-root>

No policy/rule file creation.
```
- **Deliverables**:
  - Add `scripts/skills/sync_env_opencode.py` as an OpenCode entrypoint.
  - Add `scripts/skills/sync_env_others.py` as a custom/unsupported-agent entrypoint.
  - Support OpenCode `--scope repo|user` plus `--target-root` override.
  - Require explicit `--target-root` for `sync_env_others.py`.
  - Support `--skill <name>`, `--all`, `--dry-run`, and `--overwrite`.
  - Reuse shared discovery/copy behavior from SOW 0062 where it avoids real duplication.
  - Do not support `legacy-user` or `codex-hooks` in either entrypoint.
  - Keep `--all` defined as all repo skill folders under `AISkills/skills/` that contain `SKILL.md`.
  - Add README examples showing OpenCode repo/user/custom usage and other-agent explicit target roots on macOS and Windows.
- **Done Criteria**:
  - OpenCode repo-scope dry-run shows `<target-project>/.opencode/skills/<skill-name>/`.
  - OpenCode user-scope dry-run shows `$HOME/.config/opencode/skills/<skill-name>/`.
  - OpenCode explicit target-root dry-run shows the exact destination before copying.
  - `sync_env_others.py` fails clearly without `--target-root`.
  - Both entrypoints reject or omit unsupported scope/profile options.
  - Existing overwrite safety remains opt-in.
  - Implementation uses `pathlib.Path` and supports explicit Windows-style paths without hardcoded POSIX assumptions.
  - Neither entrypoint creates `AGENTS.md`, `CLAUDE.md`, `.agents/rules`, `.claude` policy files, hooks, configs, or CLI setup.
- **Out-of-Scope**:
  - Codex and Claude default destinations.
  - Project policy/rule initialization.
  - Installing OpenCode or any other agent CLI.
  - Hybrid multi-agent sync in a single command.
- **Proposed-By**: Codex GPT-5
- **plan**: `plan_todo/finished/PLAN_20260707_PST680EX/PLAN_20260707_PST680EX_agent_skill_sync_refine_plan.md`
- **Cautions / Risks**:
  - A generic "others" command must stay explicit-target-only; otherwise it becomes an unreviewed compatibility layer.
  - Do not turn this into a policy initializer; it is only a skill copier.
