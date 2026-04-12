# SOW: Copy Telemetry Tooling Into AISkills

- **Task**: Copy the current telemetry measurement tooling and related design references into `AISkills` so telemetry-aware skills can be designed from one central repository.
- **Location**: `/Users/maihoangviet/Projects/AISkills/plan_todo/SOW_0002_copy_telemetry_tooling.md`, `/Users/maihoangviet/Projects/AISkills/scripts/telemetry/**`, `/Users/maihoangviet/Projects/AISkills/references/telemetry/**`
- **Why**: Telemetry measurement is now part of the workflow design surface. Keeping the relevant parser code and measurement notes inside `AISkills` makes it easier to evolve skills that depend on telemetry without jumping back to the project repo or local runtime folders.
- **As-Is Diagram (ASCII)**:
```text
libraries repo
   |
   +--> scripts/telemetry/parse_codex_rollout.py
   +--> scripts/telemetry/README_codex_rollout.md
   |
~/.codex/skills/sow-delegate-flow/
   |
   +--> references/log-parsing.md
   +--> references/claude-delegate-contract.md
   +--> scripts/parse_delegate_log.py
   |
   v
Telemetry design split across runtime repo + local skill folders
```
- **To-Be Diagram (ASCII)**:
```text
AISkills repo
   |
   +--> scripts/telemetry/
   +--> references/telemetry/
   |
   v
Centralized telemetry-aware skill design inputs
```
- **Deliverables**:
  - Copy Codex rollout telemetry tooling from `libraries/scripts/telemetry/`
  - Copy the Claude raw-log parser design references needed for skill design
  - Preserve source structure where practical
  - Keep the copied material scoped to telemetry/measurement design, not unrelated project logic
- **Done Criteria**:
  - `AISkills` contains the current telemetry parser/code needed to inspect Codex rollout history
  - `AISkills` contains the current Claude raw-log parsing references or parser code needed to design telemetry-aware delegation skills
  - Changes are committed in `AISkills` with a clear message
- **Out-of-Scope**:
  - Rewriting telemetry logic during the copy
  - Installing copied tooling into any runtime path
  - Publishing or packaging the telemetry tooling
- **Proposed-By**: Codex GPT-5
- **plan**: `plan_todo/SOW_0002_copy_telemetry_tooling.md`
- **Cautions / Risks**:
  - Some copied references may still contain absolute machine-local paths; this step should preserve current content first, then normalize later if needed.
  - The repo should centralize only the telemetry-related parts, not pull in unrelated project files from `libraries`.
