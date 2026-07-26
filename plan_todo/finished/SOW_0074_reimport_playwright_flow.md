- **Status**: done
- **Approval**: approved (user, 2026-07-26)
- **Task**: Re-import `playwright-flow` from local Codex skills into the AISkills repo as the canonical maintained source.
- **Location**: `skills/playwright-flow/`, `skills/registry.json`, `skills/INDEX.md`, `plan_todo/SOW_0074_reimport_playwright_flow.md`
- **Why**: `playwright-flow` is now the only retained Playwright skill in Codex, but it currently has no canonical repo source for sync, review, or parity verification.
- **As-Is Diagram (ASCII)**:
```text
~/.codex/skills/playwright-flow  -> used locally
AISkills/skills/                 -> missing playwright-flow

result:
- no repo-owned source
- no registry entry
- no parity verification path
```
- **To-Be Diagram (ASCII)**:
```text
AISkills/skills/playwright-flow  -> canonical source
              |
              +-> registry/index
              +-> sync scripts discover it
              +-> local Codex copy can be parity-checked
```
- **Deliverables**:
  - add `skills/playwright-flow/` to the repo
  - register `playwright-flow` in `skills/registry.json`
  - list `playwright-flow` in `skills/INDEX.md`
  - keep the local Codex copy parity-verifiable from repo source
- **Done Criteria**:
  - repo contains complete `skills/playwright-flow/` source
  - `registry.json` includes every tracked file for `playwright-flow`
  - `INDEX.md` lists the skill and its intended use
  - `verify_skill_copy.py` passes for `playwright-flow` against `~/.codex/skills`
- **Out-of-Scope**:
  - changing Playwright CLI behavior
  - reintroducing upstream `playwright`
  - restoring telemetry or hook bridge assets
- **Proposed-By**: Codex GPT-5
- **plan**: `SOW_0039_playwright_skill_cleanup_lifecycle.md`
- **Cautions / Risks**:
  - repo copy must match the kept local skill, not an older upstream variant
  - registry file list must stay exact or parity tests will fail
