# Target Mapping Contract

Write `design-mirror-mapping.md` before or during application. The file is a handoff for verification, not a new runtime design authority.

## Required Sections

```md
# Design Mirror Mapping

## Target Authority
## Source Package
## Evidence Limitations
## Mapping Summary
## Token And Component Mapping
## Affected Surfaces
## Deliberate Deviations
## Unresolved Gaps
## Verification Handoff
```

## Target Authority

List the target files and rules read:

- repo guardrails;
- principle/design docs;
- concept authority when declared;
- token/theme/component owners;
- relevant tests or visual baselines.

State the target change-authority workflow used. Do not claim a SOW is required unless the target repo requires it.

## Mapping Rows

Use compact tables for mappings:

```md
| Source claim | Classification | Target owner | Target value or component | Action | Notes |
| --- | --- | --- | --- | --- | --- |
| color-primary | observed | theme.css --color-primary | #3b82f6 | update existing token | matched role, not brand asset |
```

Actions should be one of:

- `reuse`;
- `update existing token`;
- `update existing component`;
- `add approved token`;
- `add approved component`;
- `defer`;
- `reject as non-transferable`.

## Ownership Rules

- Reuse existing tokens, themes, components, primitives, and tests.
- Do not create wrapper components, compatibility aliases, parallel themes, duplicated token owners, or facade layers to avoid updating the real owner.
- Preserve target content, business logic, user flows, accessibility, and behavior.
- Require explicit approval before overwriting an existing target `DESIGN.md`, token source, component owner, or baseline.

## Verification Handoff

List routes, components, states, themes, viewports, and commands that `verify-design-mirror` should inspect. Include unresolved gaps and deliberate deviations so the verifier can distinguish accepted tradeoffs from defects.
