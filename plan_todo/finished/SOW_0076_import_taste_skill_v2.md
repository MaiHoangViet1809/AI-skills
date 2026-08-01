# SOW_0076 - Import Taste Skill V2

- **Status**: completed
- **Approval**: approved by user on 2026-08-02
- **Task**: Import upstream `leonxlnx/taste-skill` v2 as a repo-local AISkills skill while preserving license attribution and registry-driven install behavior.
- **Location**:
  - `skills/taste-skill/SKILL.md`
  - `skills/taste-skill/LICENSE.txt`
  - `skills/taste-skill/agents/openai.yaml`
  - `skills/registry.json`
  - `skills/INDEX.md`
  - `tests/test_taste_skill_import.py`
  - `plan_todo/finished/SOW_0076_import_taste_skill_v2.md`
- **Why**: User requested adding Taste Skill v2 to this AISkills repository so it can be discovered, synced, and installed through the repo's normal skill pipeline.
- **Proposed-By**: Codex GPT-5
- **Plan / Reference**:
  - User request: `lấy thêm phần taste-skill v2 về repo mình`
  - Upstream repo: `https://github.com/leonxlnx/taste-skill`
  - Upstream commit inspected: `e988add20dab0fa97d7a76781c48961c8184288e`
  - Upstream folder: `skills/taste-skill/SKILL.md`
  - Upstream install name/frontmatter: `design-taste-frontend`
  - Upstream license: MIT License, copyright 2026 Leonxlnx
  - `AGENTS.md`
  - `INSTALL_FOR_AGENTS.md`
  - `skills/registry.json`

## Project Guardrail Audit

- No root `PRODUCT_PRINCIPLE_DESIGN.md`, `.agents/rules/`, or declared canonical concept index exists in this checkout; concept-authority gates are inactive and `Concept Compliance` is intentionally omitted.
- Applicable repository invariants:
  - keep repo skills installable through `skills/registry.json`;
  - preserve external license/copyright notices;
  - avoid empty files and `__init__.py`;
  - do not create provider-specific workflow copies;
  - do not change install scripts unless a verified blocker appears.

## As-Is Diagram (ASCII)

```text
AISkills repo
  |
  +-> local workflow skills
  +-> design mirror skills
  +-> no taste-skill v2 entry

Codex/Claude/OpenCode sync
  |
  +-> can only copy registry-listed repo skills
```

## To-Be Diagram (ASCII)

```text
leonxlnx/taste-skill @ e988add
  |
  +-> skills/taste-skill/SKILL.md
  +-> MIT license notice
  |
  v
AISkills repo
  |
  +-> skills/taste-skill/
  +-> registry + index entry
  +-> targeted import test
  |
  v
existing sync scripts can install taste-skill
```

## Deliverables

1. Add `skills/taste-skill/SKILL.md` from upstream v2 with minimal AISkills-local changes only if required for validation, attribution, or install consistency.
2. Add `skills/taste-skill/LICENSE.txt` containing the upstream MIT license notice.
3. Add `skills/taste-skill/agents/openai.yaml` as supplemental metadata; workflow rules must remain in `SKILL.md`.
4. Add registry and index entries. The repo-facing registry/folder name should be `taste-skill`; the skill frontmatter/invocation name should remain upstream-compatible as `design-taste-frontend` unless implementation finds a hard validator conflict.
5. Add targeted tests that verify:
   - imported skill files exist and are non-empty;
   - frontmatter name/description are valid and intentionally preserve `design-taste-frontend`;
   - upstream MIT notice is preserved;
   - registry shipped files exactly match the skill folder;
   - sync scripts can dry-run install `taste-skill` by folder name.

## Done Criteria

1. `skills/taste-skill/` exists with only approved files.
2. License attribution is present in the skill folder.
3. Registry and index entries include `taste-skill`, and the index clearly shows that the invocation/frontmatter name is `design-taste-frontend`.
4. Targeted import test passes.
5. Existing skill sync tests pass.
6. `quick_validate.py skills/taste-skill` passes, or any upstream frontmatter incompatibility is documented and fixed without changing the skill's intent.
7. `git diff --check` passes.
8. Work is committed after verification unless user explicitly defers commit.

## Out-of-Scope

- Importing the entire upstream repository, examples, research folder, assets, image-generation skills, v1 skill, or other variant skills.
- Installing `taste-skill` into local Codex/Claude/OpenCode skill roots unless the user asks after repo import.
- Rewriting Taste Skill v2's design rules into AISkills house style.
- Adding new package managers, runtime dependencies, MCP servers, plugins, or sync-script behavior.
- Claiming endorsement or official ownership of upstream Taste Skill.

## Cautions / Risks

- Upstream `SKILL.md` is large, about 1206 lines, which exceeds the preferred concise-skill guidance. This SOW intentionally preserves v2 behavior rather than compressing it, unless validation reveals a hard blocker.
- Upstream contains package-install command examples. They are design guidance for future frontend implementation, not commands to run during import.
- Folder name and frontmatter name differ upstream: folder `taste-skill`, install/frontmatter name `design-taste-frontend`. The repo sync scripts select by folder name, while agent invocation should expose the frontmatter name.
- Upstream defines a future `skills/taste-skill/blocks/` schema inside `SKILL.md`, but the inspected upstream v2 folder contains no block files. Do not fabricate block files during this import.
- Future upstream updates should be treated as a separate review/import task, not silently pulled from `latest`.
