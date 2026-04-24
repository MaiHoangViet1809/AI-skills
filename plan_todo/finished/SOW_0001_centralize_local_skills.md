# SOW: Centralize Local Skills Into AISkills

- **Task**: Copy the current custom Codex skills from `~/.codex/skills/` into the `AISkills` repository so they can be versioned and shared from one central project.
- **Location**: `~/Projects/AISkills/plan_todo/SOW_0001_centralize_local_skills.md`, `~/Projects/AISkills/skills/sow-delegate-flow/**`, `~/Projects/AISkills/skills/task-router-flow/**`
- **Why**: The skills currently live only under `~/.codex/skills/`, which makes versioning, reuse, and sharing harder. Centralizing them in `AISkills` creates one source-controlled place for refinement and distribution.
- **As-Is Diagram (ASCII)**:
```text
~/.codex/skills/
   |
   +--> sow-delegate-flow/
   +--> task-router-flow/
   |
   v
Local-only skill storage
```
- **To-Be Diagram (ASCII)**:
```text
~/.codex/skills/                     ~/Projects/AISkills/skills/
   |                                 |
   +--> local runtime copies         +--> sow-delegate-flow/
                                     +--> task-router-flow/
                                     |
                                     v
                             Centralized version-controlled skill repo
```
- **Deliverables**:
  - Create `skills/` in `AISkills` if missing
  - Copy the complete current contents of:
    - `~/.codex/skills/sow-delegate-flow/`
    - `~/.codex/skills/task-router-flow/`
  - Preserve each skill's internal structure (`SKILL.md`, `agents/`, `references/`, `scripts/`)
- **Done Criteria**:
  - Both custom skills exist under `AISkills/skills/`
  - Copied skill folders preserve their subdirectories and files
  - Only the approved skill content is added to the repo
  - Changes are committed in `AISkills` with a clear message
- **Out-of-Scope**:
  - Refactoring skill content during the copy
  - Installing the copied skills anywhere else
  - Publishing the repo externally
- **Proposed-By**: Codex GPT-5
- **plan**: `plan_todo/SOW_0001_centralize_local_skills.md`
- **Cautions / Risks**:
  - Some skills may contain machine-local absolute paths in docs or examples; the copy should preserve current content without rewriting semantics during this step.
  - Built-in, curated, or third-party skills such as `figma` and `playwright` are excluded from this copy step.
