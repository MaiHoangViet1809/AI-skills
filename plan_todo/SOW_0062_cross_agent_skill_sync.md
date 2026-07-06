- **Status**: draft
- **Approval**: pending
- **Task**: Refine AISkills skill installer/synchronizer so repo-owned skills can be installed for Codex and Claude Code on macOS and Windows 10/11, with explicit repo-scope and user-scope targets.
- **Location**: `scripts/skills/install_skills.py`, `scripts/skills/sync_environment.py`, `scripts/skills/README.md`, `plan_todo/agent_skill_sync_refine_plan.md`, `plan_todo/SOW_0062_cross_agent_skill_sync.md`, and focused tests or verification scripts if needed under `tests/` or `scripts/skills/`
- **Why**: Current sync tooling is designed around Codex local setup and `~/.codex/skills`. The user needs a repeatable way to sync AISkills skills for Codex and Claude Code across macOS and Windows machines, while keeping project-specific rules inside each target project instead of globalizing them accidentally.
- **As-Is Diagram (ASCII)**:
```text
AISkills/skills/<skill>
  |
  v
install_skills.py
  -> ~/.codex/skills/<skill>

sync_environment.py --target codex
  -> ~/.codex/skills/<selected>
  -> ~/.codex/hooks.json
  -> ~/.codex/config.toml
```
- **To-Be Diagram (ASCII)**:
```text
AISkills/skills/<skill>
  |
  v
sync_environment.py
  -> --agent codex --scope repo --target-project <repo>
       <repo>/.agents/skills/<skill>
  -> --agent codex --scope user
       $HOME/.agents/skills/<skill>
  -> --agent codex --scope legacy-user
       $HOME/.codex/skills/<skill>
  -> --agent claude --scope repo --target-project <repo>
       <repo>/.claude/skills/<skill>
  -> --agent claude --scope user
       $HOME/.claude/skills/<skill>

sync_environment.py --profile skills
  -> skill directories only

sync_environment.py --profile codex-hooks
  -> explicit Codex hook/config sync only

init-agent-env skill
  -> owns AGENTS.md / CLAUDE.md / .agents/rules creation
  -> not owned by sync_environment.py
```
- **Deliverables**:
  - Update `scripts/skills/sync_environment.py` to support:
    - `--agent codex|claude|both`
    - `--scope repo|user|legacy-user`
    - `--profile skills|codex-hooks`, with `skills` as the default and no hook/config mutation unless `codex-hooks` is explicit
    - `--target-project <path>` for repo-scoped installs
    - `--skill <name>` and `--all`
    - `--target-root <path>` override
    - `--dry-run`
    - `--overwrite`
  - Preserve or adapt `scripts/skills/install_skills.py` as the low-level skill copier, or fold its behavior into `sync_environment.py` only if that reduces duplication without creating a facade/wrapper split.
  - Define target validation rules:
    - `legacy-user` is valid only for `--agent codex`
    - `--agent both --scope legacy-user` must fail clearly
    - `--agent claude --scope legacy-user` must fail clearly
    - `--scope repo` requires `--target-project` unless `--target-root` is supplied
  - Define `--all` as all discoverable repo skills under `AISkills/skills/` with `SKILL.md`; do not use `--all` for a curated bundle.
  - Update `scripts/skills/README.md` with examples for:
    - Codex repo-scope install into `<project>/.agents/skills`
    - Codex user-scope install into `$HOME/.agents/skills`
    - Codex legacy user-scope install into `$HOME/.codex/skills`
    - Claude repo-scope install into `<project>/.claude/skills`
    - Claude user-scope install into `$HOME/.claude/skills`
    - Windows 10/11 usage with explicit `--target-project` or `--target-root`
  - Document the boundary that project policy/rule initialization belongs to a separate skill such as `create-agents-md` / future `init-agent-env`, not to the sync script.
  - Add a short design note to `plan_todo/skill_design_decisions.md` or this plan explaining why repo-scope install writes into the target project, not global `.agents`.
- **Done Criteria**:
  - Dry-run output accurately shows every planned copy destination for Codex repo/user/legacy-user and Claude repo/user.
  - Dry-run/default skill sync does not write `hooks.json`, `codex_hook_bridge.py`, or `config.toml`.
  - `codex-hooks` behavior, if retained in this SOW, is explicit and documented separately from skill sync.
  - Existing overwrite safety remains opt-in.
  - Missing required arguments fail clearly, especially `--scope repo` without `--target-project` unless `--target-root` is supplied.
  - Invalid target combinations fail clearly: `claude + legacy-user` and `both + legacy-user`.
  - The implementation works with `pathlib.Path`, avoiding POSIX-only path assumptions so Windows 10/11 paths are supported.
  - Verification covers at least one temporary directory dry-run or copy scenario for each supported target class using explicit `--target-project` or `--target-root`; no real Windows machine is required for this SOW.
  - README examples are sufficient for syncing skills on a fresh macOS or Windows machine after cloning `AISkills`.
  - No project-specific `AGENTS.md`, `CLAUDE.md`, `.agents/rules`, or `.claude` policy files are created by the sync script.
- **Out-of-Scope**:
  - Creating or modifying target project `AGENTS.md`, `CLAUDE.md`, `.agents/rules`, or other policy files.
  - Building the separate `init-agent-env` skill.
  - Installing or configuring the Codex CLI / Claude Code CLI themselves.
  - Publishing to marketplaces, packaging plugins, or managing enterprise/admin skill paths.
  - Rewriting telemetry hook installation unless needed to avoid mixing hook sync with skill sync.
  - Removing existing support for `~/.codex/skills` before a migration path is proven.
- **Proposed-By**: Codex GPT-5
- **plan**: `plan_todo/agent_skill_sync_refine_plan.md`
- **Cautions / Risks**:
  - Treating `<project>/.agents/skills` as global would leak one project's rules into another project.
  - Mixing hook/config sync with skill copy can make a simple install command mutate more environment state than expected.
  - Removing `~/.codex/skills` support too early may break this user's current Codex setup.
  - Claude Code and Codex both use `SKILL.md`, but their discovery locations and optional metadata differ; the script must copy the skill tree without assuming `agents/openai.yaml` matters to Claude.
