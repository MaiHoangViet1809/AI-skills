# Concept Catalog Template

Use this for `docs/concept/README.md`.

```md
# Project Concept Catalog

This catalog is the canonical source for accepted project design. Mature
concepts explain models and boundaries. Thin invariants live in
[inline_rules.md](./inline_rules.md).

Design status and implementation status are separate:

- `canonical`: the design is accepted.
- `under-review`: the design is not yet locked.
- `applied`: the active implementation follows the concept.
- `partial`: only part of the accepted design is implemented.
- `documented-only`: the design is accepted but not implemented.

Historical SOWs explain how decisions were reached; they do not override this
catalog.

## Mature Concepts

| ID | Concept | Domain | Design | Implementation | File |
| --- | --- | --- | --- | --- | --- |
| `MC-FND-01` | Example Foundation Concept | Foundation | canonical | documented-only | [Open](./mature/foundation/example_foundation_concept.md) |

## Usage

Before changing a covered area:

1. Read its mature concept and matching inline rules.
2. Preserve the stated ownership and boundaries.
3. If the requirement conflicts, revise the concept before implementation.
4. Update implementation status only after the relevant behavior is verified.
```

Keep IDs stable and project-local. Suggested mature concept ID families:

- `MC-FND-*`: foundation and project scope
- `MC-WF-*`: workflow or process models
- `MC-NODE-*`: node/component/plugin models
- `MC-UI-*`: UI, UX, and GUI state models
- `MC-DATA-*`: data contracts
- `MC-OPS-*`: operations and local lifecycle
