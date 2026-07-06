- **Status**: draft
- **Approval**: pending
- **Task**: Refine AISkills skill installer/synchronizer so repo-owned skills can be installed through separate agent-specific commands for Codex, Claude Code, OpenCode, and custom/other agents on macOS and Windows 10/11.
- **Location**: `scripts/skills/install_skills.py`, `scripts/skills/sync_environment.py`, `scripts/skills/sync_env_codex.py`, `scripts/skills/sync_env_claude.py`, `scripts/skills/sync_env_opencode.py`, `scripts/skills/sync_env_others.py`, shared helper files under `scripts/skills/` if needed, `scripts/skills/README.md`, `plan_todo/agent_skill_sync_refine_plan.md`, `plan_todo/SOW_0062_cross_agent_skill_sync.md`, and focused tests or verification scripts if needed under `tests/` or `scripts/skills/`
- **Why**: Current sync tooling is designed around Codex local setup and `~/.codex/skills`. The user needs repeatable, explicit per-agent sync commands for Codex, Claude Code, OpenCode, and custom/other agents across macOS and Windows machines, without one command silently installing skills for multiple agents or globalizing project-specific rules.
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
  +--> sync_env_codex.py
  |      -> --scope repo         <repo>/.agents/skills/<skill>
  |      -> --scope user         $HOME/.agents/skills/<skill>
  |      -> --scope legacy-user  $HOME/.codex/skills/<skill>
  |
  +--> sync_env_claude.py
  |      -> --scope repo         <repo>/.claude/skills/<skill>
  |      -> --scope user         $HOME/.claude/skills/<skill>
  |
  +--> sync_env_opencode.py
  |      -> destinations only after target semantics are confirmed
  |
  +--> sync_env_others.py
         -> explicit --target-root only

sync_env_<agent>.py --profile skills
  -> skill directories only

sync_env_codex.py --profile codex-hooks
  -> explicit Codex hook/config sync only

init-agent-env skill
  -> owns AGENTS.md / CLAUDE.md / .agents/rules creation
  -> not owned by sync_environment.py
```
- **Deliverables**:
  - Refine the sync surface into separate public entrypoints:
    - `scripts/skills/sync_env_codex.py`
    - `scripts/skills/sync_env_claude.py`
    - `scripts/skills/sync_env_opencode.py`
    - `scripts/skills/sync_env_others.py`
  - Each entrypoint should support only its own agent's target semantics:
    - `--scope repo|user|legacy-user`
    - `--profile skills|codex-hooks`, with `skills` as the default and no hook/config mutation unless `codex-hooks` is explicit
    - `--target-project <path>` for repo-scoped installs
    - `--skill <name>` and `--all`
    - `--target-root <path>` override
    - `--dry-run`
    - `--overwrite`
  - Preserve or adapt `scripts/skills/install_skills.py` as the low-level skill copier, or fold its behavior into shared helpers only if that reduces duplication without creating a facade/wrapper split.
  - Define target validation rules:
    - `legacy-user` is valid only in `sync_env_codex.py`
    - `sync_env_claude.py --scope legacy-user` must fail clearly
    - `sync_env_opencode.py` must not invent default destinations until OpenCode skill target semantics are verified
    - `sync_env_others.py` requires explicit `--target-root`
    - `--scope repo` requires `--target-project` unless `--target-root` is supplied
  - Define `--all` as all discoverable repo skills under `AISkills/skills/` with `SKILL.md`; do not use `--all` for a curated bundle.
  - Update `scripts/skills/README.md` with examples for:
    - Codex repo-scope install into `<project>/.agents/skills`
    - Codex user-scope install into `$HOME/.agents/skills`
    - Codex legacy user-scope install into `$HOME/.codex/skills`
    - Claude repo-scope install into `<project>/.claude/skills`
    - Claude user-scope install into `$HOME/.claude/skills`
    - OpenCode guarded behavior pending verified destination semantics
    - custom/other-agent sync with explicit `--target-root`
    - Windows 10/11 usage with explicit `--target-project` or `--target-root`
  - Document the boundary that project policy/rule initialization belongs to a separate skill such as `create-agents-md` / future `init-agent-env`, not to the sync script.
  - Add a short design note to `plan_todo/skill_design_decisions.md` or this plan explaining why repo-scope install writes into the target project, not global `.agents`.
- **Done Criteria**:
  - Dry-run output accurately shows every planned copy destination for Codex repo/user/legacy-user and Claude repo/user.
  - Dry-run/default skill sync does not write `hooks.json`, `codex_hook_bridge.py`, or `config.toml`.
  - `codex-hooks` behavior, if retained in this SOW, is explicit and documented separately from skill sync.
  - Existing overwrite safety remains opt-in.
  - Missing required arguments fail clearly, especially `--scope repo` without `--target-project` unless `--target-root` is supplied.
  - Invalid or unsafe target combinations fail clearly: Claude legacy-user, OpenCode without verified destination or explicit `--target-root`, and other-agent sync without explicit `--target-root`.
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
  - Hybrid multi-agent sync in a single command.
  - Guessing OpenCode skill destinations before they are verified from docs or user-provided target roots.
- **Proposed-By**: Codex GPT-5
- **plan**: `plan_todo/agent_skill_sync_refine_plan.md`
- **Cautions / Risks**:
  - Treating `<project>/.agents/skills` as global would leak one project's rules into another project.
  - Mixing hook/config sync with skill copy can make a simple install command mutate more environment state than expected.
  - Removing `~/.codex/skills` support too early may break this user's current Codex setup.
  - Claude Code and Codex both use `SKILL.md`, but their discovery locations and optional metadata differ; the script must copy the skill tree without assuming `agents/openai.yaml` matters to Claude.
  - A hybrid `both` mode would hide intent and may install skills for agents that do not need them; keep one explicit command per agent.
