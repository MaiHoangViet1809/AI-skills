- **Status**: completed
- **Approval**: approved 2026-07-07
- **Completed**: 2026-07-07
- **Task**: Refine the shared AISkills skill copy base and add a Codex-specific sync entrypoint for repo/user/legacy-user skill destinations.
- **Location**: `scripts/skills/install_skills.py`, `scripts/skills/sync_environment.py`, `scripts/skills/sync_env_codex.py`, shared helper files under `scripts/skills/` if needed, `scripts/skills/README.md`, `plan_todo/finished/agent_skill_sync_refine_plan.md`, `plan_todo/finished/SOW_0062_core_codex_skill_sync.md`, and focused tests or verification scripts if needed under `tests/` or `scripts/skills/`
- **Why**: Current sync tooling is designed around local Codex setup and `~/.codex/skills`. Before adding other agents, the repo needs a safe shared copy base plus an explicit Codex command that supports the current preferred Codex paths and legacy compatibility without mixing hook/config mutation into normal skill sync.
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
sync_env_codex.py
  -> --scope repo         <target-project>/.agents/skills/<skill>
  -> --scope user         $HOME/.agents/skills/<skill>
  -> --scope legacy-user  $HOME/.codex/skills/<skill>

sync_env_codex.py --profile skills
  -> skill directories only

sync_env_codex.py --profile codex-hooks
  -> explicit Codex hook/config sync only, if retained
```
- **Deliverables**:
  - Extract shared skill discovery/copy helpers only where they remove real duplication.
  - Add `scripts/skills/sync_env_codex.py` as a first-class Codex entrypoint.
  - Support `--scope repo|user|legacy-user`.
  - Support `--profile skills|codex-hooks`, with `skills` as the default and no hook/config mutation unless `codex-hooks` is explicit.
  - Support `--target-project <path>` for repo-scoped installs.
  - Support `--skill <name>`, `--all`, `--target-root <path>`, `--dry-run`, and `--overwrite`.
  - Resolve repo scope to `<target-project>/.agents/skills/<skill-name>/`.
  - Resolve user scope to `$HOME/.agents/skills/<skill-name>/`.
  - Resolve legacy-user scope to `$HOME/.codex/skills/<skill-name>/`.
  - Preserve or adapt `scripts/skills/install_skills.py` as the low-level skill copier, or fold its behavior into shared helpers only if that reduces duplication without creating a facade/wrapper split.
  - Define `--all` as all discoverable repo skills under `AISkills/skills/` with `SKILL.md`; do not use `--all` for a curated bundle.
  - Add focused README examples for Codex repo/user/legacy-user sync.
- **Done Criteria**:
  - Codex repo-scope dry-run shows `<target-project>/.agents/skills/<skill-name>/`.
  - Codex user-scope dry-run shows `$HOME/.agents/skills/<skill-name>/`.
  - Codex legacy-user dry-run shows `$HOME/.codex/skills/<skill-name>/`.
  - Dry-run/default skill sync does not write `hooks.json`, `codex_hook_bridge.py`, or `config.toml`.
  - `codex-hooks` behavior, if retained, is explicit and documented separately from skill sync.
  - Existing overwrite safety remains opt-in.
  - Missing `--target-project` for repo scope fails unless `--target-root` is supplied.
  - Implementation uses `pathlib.Path` and supports explicit Windows-style paths without hardcoded POSIX assumptions.
  - No project-specific `AGENTS.md`, `CLAUDE.md`, `.agents/rules`, or `.claude` policy files are created by the sync script.
- **Out-of-Scope**:
  - Claude Code sync; handled by `plan_todo/finished/SOW_0063_claude_skill_sync.md`.
  - OpenCode and other-agent sync; handled by `plan_todo/finished/SOW_0064_opencode_other_skill_sync.md`.
  - Final full-matrix docs and verification; handled by `plan_todo/finished/SOW_0065_skill_sync_docs_verification.md`.
  - Creating or modifying target project `AGENTS.md`, `CLAUDE.md`, `.agents/rules`, or other policy files.
  - Building the separate `init-agent-env` skill.
  - Installing or configuring the Codex CLI.
  - Publishing to marketplaces, packaging plugins, or managing enterprise/admin skill paths.
  - Removing existing support for `~/.codex/skills` before a migration path is proven.
  - Hybrid multi-agent sync in a single command.
- **Proposed-By**: Codex GPT-5
- **plan**: `plan_todo/finished/agent_skill_sync_refine_plan.md`
- **Cautions / Risks**:
  - Treating `<project>/.agents/skills` as global would leak one project's rules into another project.
  - Mixing hook/config sync with skill copy can make a simple install command mutate more environment state than expected.
  - Removing `~/.codex/skills` support too early may break this user's current Codex setup.
  - A hybrid multi-agent mode would hide intent and may install skills for agents that do not need them; keep one explicit command per agent.
