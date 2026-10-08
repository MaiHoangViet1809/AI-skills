# SOW_20260802_HG5LJ6N3 - Scope Decisions

- legacy_id: SOW_0075
- legacy_path: plan_todo/finished/SOW_0075_portable_design_mirror_skill_suite.md
- migrated_dttm: 2026-10-08T12:48:51+07:00
- Parent: [SOW_20260802_HG5LJ6N3](SOW_20260802_HG5LJ6N3_portable_design_mirror_skill_suite.md)

## Preserved Contract And Historical Evidence

## Design And Ownership Decisions

1. Implement exactly three domain skills; do not add a fourth orchestration skill. AISkills routing and execution skills own this SOW's implementation lifecycle. After installation, each skill must defer to the target repository's declared change-authority workflow and must not require AISkills-specific routing or SOW conventions.
2. Keep normative workflows capability-based. Describe required capabilities such as file inspection, browser automation, screenshots, design APIs, and shell execution without requiring Codex, Claude, Stitch, Figma, or another named vendor.
3. Keep `SKILL.md` portable. `agents/openai.yaml` may provide optional OpenAI UI metadata, but no workflow rule or required information may exist only there.
4. Treat the extracted `DESIGN.md` as the canonical agent-readable design contract for the extracted style package. Evidence and screenshots prove its claims but do not become a second design authority.
5. Treat the target repository's declared design tokens, component library, architecture, and concept authority as the runtime source of truth. `DESIGN.md` is mapped into that ownership; it must not silently replace it.
6. Treat DTCG, Tailwind, CSS-variable, or framework outputs as generated projections when requested. They must not be independently edited or become parallel owners.
7. Classify extracted claims as `observed`, `inferred`, or `unsupported`. Never convert an inferred value into an observed fact through prose.
8. Never overwrite an existing target `DESIGN.md`, token source, component library, or visual baseline without explicit user approval.
9. Keep the implementation self-contained within each skill. Cross-skill handoff occurs through documented artifacts, not shared hidden state or a new runtime framework.
10. Pin Google format validation to `@google/design.md@0.4.0` for this SOW. A later CLI or spec upgrade requires explicit review rather than silently following `latest`.
11. Use project-relative paths in normative instructions. Installed helper locations must be resolved by the invoking agent and must never be encoded as a developer-machine path.
