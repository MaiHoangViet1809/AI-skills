# Fidelity Matrix

Use this matrix to score `design-mirror-verification.md`. A full claim requires the source package and `design-mirror-mapping.md`.

## Status Values

- `pass`: evidence matches the mapped source claim and target behavior is preserved.
- `approximate`: the result is intentionally close but not exact, with rationale.
- `fail`: evidence contradicts the mapping or target behavior regressed.
- `not_verified`: required input, route, state, environment, or evidence is missing.

## Matrix

| Area | Required Evidence | Failure Examples |
| --- | --- | --- |
| Token coverage | Source claims mapped to target token/theme/component owners | unmapped observed token, parallel token owner |
| Color roles | Semantic roles, not only raw hex values | default framework color substituted, contrast regression |
| Typography | family, size, weight, line height, letter spacing | generic font fallback without disclosure |
| Spacing and geometry | padding, gap, layout anchors, density, responsive constraints | card density inconsistent with source |
| Radius, border, elevation | radius scale, border color/width, shadow depth | heavy shadow added where source is flat |
| Components | variants and reusable states | only page-level styling changed |
| Interaction states | focus, hover, active, selected, disabled, loading, empty, error | focus state lost, disabled state unreadable |
| Responsive behavior | representative mobile/tablet/desktop viewports | mobile wraps badly or target layout shifts |
| Themes | light/dark or other declared modes | dark mode unmapped or contrast mismatch |
| Motion | duration, easing, reduced-motion behavior when known | animation copied without reduced-motion guard |
| Accessibility | contrast, focus visibility, semantic behavior preservation | visual match breaks keyboard path |
| Target behavior | domain flows and tests still pass | style change breaks interaction or data display |

## Scoring Rules

- Do not let pixel difference alone decide the result.
- Pair visual evidence with structural or behavioral evidence when feasible.
- Keep screenshot-only source claims lower confidence.
- Never update a target baseline before documenting why a mismatch is acceptable.
- Mark inaccessible states as `not_verified`, not `pass`.

## Report Minimum

Include environment, commands run, routes or components inspected, matrix rows, screenshots or artifact references, limitations, and repair recommendations. Keep repair ownership outside the verifier unless the user explicitly authorizes a separate target implementation pass.
