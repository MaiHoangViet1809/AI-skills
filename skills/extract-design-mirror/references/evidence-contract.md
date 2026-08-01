# Evidence Contract

Write `design-mirror-evidence.json` as the provenance file for `DESIGN.md`. It is evidence, not a second design authority.

## Required Top-Level Fields

```json
{
  "schema_version": "design-mirror-evidence/v1",
  "package_root": ".",
  "generated_at": "ISO-8601 timestamp or unknown",
  "sources": [],
  "capture_conditions": {},
  "sampled_surfaces": [],
  "claims": [],
  "known_gaps": []
}
```

## Sources

Each source should include:

- `id`: stable local id such as `source-1`;
- `type`: `website`, `local_app`, `repository`, `component_library`, `design_api`, or `screenshot`;
- `locator`: sanitized URL, path, frame id, or artifact-relative file reference;
- `authorization`: `public`, `user_authorized`, `supplied`, or `unknown`;
- `notes`: short limitations.

Sanitize locators. Remove credentials, cookies, authorization headers, storage values, secret-bearing query strings, form values, and unrelated user content.

## Claims

Each claim should include:

- `id`: stable local id such as `color-primary`;
- `dimension`: `color`, `typography`, `spacing`, `radius`, `border`, `elevation`, `layout`, `motion`, `component`, `state`, `responsive`, or `accessibility`;
- `classification`: `observed`, `inferred`, or `unsupported`;
- `value`: exact captured value, summarized inference, or `null`;
- `evidence`: artifact-relative references, selectors, source ids, screenshot ids, or code locations;
- `confidence`: `high`, `medium`, `low`, or `none`;
- `notes`: short rationale.

## Capture Conditions

Record browser, OS, viewport, DPR, theme, font availability, animation handling, data state, and timestamp when known. Use `unknown` instead of guessing.

## Known Gaps

Record blocked routes, inaccessible states, cross-origin frames, closed shadow roots, canvas/WebGL, native surfaces, screenshot-only ambiguity, sensitive UI constraints, and unavailable design APIs.
