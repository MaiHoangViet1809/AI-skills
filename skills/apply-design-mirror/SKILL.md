---
name: apply-design-mirror
description: Apply an extracted DESIGN.md design package to another UI project through the target project's existing design tokens, theme, component library, and change authority. Use when the user asks to mirror, port, transfer, apply, or restyle a project using a captured web/app/library design style without creating a parallel design owner.
---

# Apply Design Mirror

Map a source design package into a target repository's real UI ownership. Preserve the target project's behavior, accessibility, content model, and architecture while transferring visual language.

Do not treat a style request as permission to edit code. Route changes through the target repository's declared authority, and use a SOW only when that repository requires one.

## Workflow

1. Read target authority first.
   - Inspect `AGENTS.md`, nested rules, principle/design docs, concept authority when declared, existing design tokens, themes, UI primitives, component library, framework conventions, and tests.
   - Stop if the requested visual transfer conflicts with declared target authority and the user has not approved that conflict.

2. Read source artifacts.
   - Load the source `DESIGN.md`.
   - Load `design-mirror-evidence.json` when present. If absent, disclose reduced confidence and never promote inferred claims to observed facts.
   - Separate transferable visual language from source business logic, DOM structure, content, product behavior, branding assets, and interaction semantics.

3. Build the mapping.
   - Read `references/target-mapping-contract.md` before writing `design-mirror-mapping.md`.
   - Map semantic color roles, typography roles, spacing and geometry, border and elevation strategy, component variants, states, responsive behavior, and motion.
   - Record source claims as `observed`, `inferred`, or `unsupported` based on the evidence package.

4. Change through existing ownership.
   - Reuse and update existing target tokens, themes, and components.
   - Add new design-system surfaces only when the approved target scope explicitly requires them.
   - Reject wrapper components, compatibility aliases, parallel Tailwind themes, duplicated token files, and facade layers used only to avoid updating the real owner.

5. Verify locally before handoff.
   - Run the target project's relevant tests, type checks, lint, or UI smoke checks in proportion to risk.
   - For UI-visible work, inspect rendered output when feasible.
   - Produce or update `design-mirror-mapping.md` in a user-approved project location.

## Output

`design-mirror-mapping.md` records:

- target authorities read;
- source artifact versions and evidence limitations;
- source claim to target token/component mappings;
- affected files and surfaces;
- deliberate deviations and rationale;
- unresolved gaps for `verify-design-mirror`.

This mapping is a verifier handoff, not a new runtime design authority.

## Stop Conditions

- Target authority forbids the visual change and approval is missing.
- Applying the style would require copying protected assets, source code, content, trademarks, or proprietary product behavior.
- The target has an existing `DESIGN.md`, token source, component owner, or visual baseline that would be overwritten without explicit approval.
- The requested implementation requires a wrapper, shim, or parallel owner outside approved scope.

## Resource

Read `references/target-mapping-contract.md` whenever producing or reviewing `design-mirror-mapping.md`.
