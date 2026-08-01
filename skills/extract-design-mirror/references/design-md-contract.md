# DESIGN.md Contract

Write `DESIGN.md` as the portable design contract for the extracted package. Keep the file useful to many AI agents, not tied to one vendor or editor.

## Required Shape

- Use Markdown with YAML frontmatter when token data is available.
- Follow the pinned Google Labs alpha DESIGN.md shape used by this skill suite.
- Put only spec-supported token groups in YAML frontmatter.
- Use the spec's `omitted` field for intentionally absent supported groups.
- Preserve unknown extension sections in prose when needed, but do not invent unsupported normative YAML fields.

## Canonical Sections

Include concise prose sections for:

- design philosophy and intent;
- evidence summary and confidence;
- color roles;
- typography roles;
- spacing, layout, and geometry;
- radii, borders, and elevation;
- components and states;
- responsive behavior;
- motion and interaction feel;
- accessibility-relevant visual states;
- constraints for AI agents;
- known gaps and unsupported claims.

## Claim Language

- Mark claims as observed, inferred, or unsupported.
- Keep exact values tied to evidence ids from `design-mirror-evidence.json`.
- Do not rewrite weak evidence into authoritative wording.
- Avoid source product behavior, business logic, content, DOM structure, or brand assets unless the user explicitly wants those documented as non-transferable context.

## AI Guardrails

Use clear constraints that can guide future agents:

- reuse declared tokens before inventing values;
- do not use default framework colors unless mapped;
- do not create parallel design owners;
- do not clone proprietary assets or product behavior;
- defer to the target repository's local authority during application.

## Validation

Run the official Google DESIGN.md validator when available. If it is not available, state this in the extraction report and still keep the contract structurally conservative.
