---
name: project-concept-governance-flow
description: Use when a project needs a docs/concept authority system created, reviewed, updated, or enforced; when design-bearing work must be checked against project concepts; or when concepts, inline rules, SOW Concept Compliance, implementation status, or concept drift must be managed inside the current project.
---

# Project Concept Governance Flow

Use this skill to manage the concept authority of one current project. It defines
the reusable protocol and document shape, not the project's actual concepts.

## Core Model

`docs/concept` is the project-local authority for accepted design decisions.
Historical SOWs, plans, chat logs, and code are evidence, but they do not
override the catalog.

```text
project request
  -> read project guardrails
  -> detect docs/concept authority
  -> read relevant concept files
  -> compare request/SOW/code against concepts
  -> update concepts when approved design changes
  -> implement or review against the updated authority
  -> update implementation status only after verification
```

## When Creating Concept Authority

Create this structure when the user asks to organize or start a concept system
for a project:

```text
docs/concept/
├── README.md
├── inline_rules.md
└── mature/
    ├── foundation/
    ├── workflow/
    ├── node/
    ├── ui/
    ├── data/
    └── operations/
```

Use [concept-catalog-template.md](references/concept-catalog-template.md),
[mature-concept-template.md](references/mature-concept-template.md), and
[inline-rule-template.md](references/inline-rule-template.md). Add only domains
that fit the project; do not force the example folders.

## Mature Concept vs Inline Rule

Use a mature concept when the decision has a real model, ownership boundary,
lifecycle, extension rules, or repeated implementation impact.

Use an inline rule when the decision is short and directly actionable without a
larger model.

Do not inflate a small rule into a mature concept. Do not bury a broad ownership
model as a one-line rule.

## Concept Preflight

Before design, architecture, persistence, runtime-boundary, compatibility, or UI
lifecycle work:

1. Read the project guardrails.
2. Find whether the project declares `docs/concept` or another concept index as
   authority.
3. Read the relevant catalog entries and inline rules.
4. Extract invariants and prohibited designs.
5. Compare the request or SOW against those invariants.
6. Stop if the request conflicts and no approved concept update is included.

For a code-changing SOW under concept authority, require:

```md
## Concept Compliance

- Applicable Concepts: <stable IDs or exact paths>
- Concept Change: No | Yes
- Required Concept Updates: <None or exact concept IDs/files>
```

## Updating Concepts

When the user approves a new or changed design concept:

- update the concept file first or in the same approved scope as implementation
- preserve existing IDs unless the concept is truly retired
- keep mature concept files short and canonical
- update `docs/concept/README.md` design and implementation status
- add or move inline rules only when they stay self-contained
- record historical SOWs as provenance, not authority

Implementation status meanings:

- `documented-only`: accepted design, no active implementation
- `partial`: some behavior exists, gaps remain
- `applied`: verified implementation follows the concept

Only mark `applied` after verification evidence exists.

## Concept Closeout

Before completing concept-governed implementation:

1. Re-read changed code/docs against the concept invariants.
2. Confirm every concept change declared in the SOW was applied.
3. Confirm implementation did not create a second ownership model or hidden
   compatibility path.
4. Update implementation status only when checks prove it.
5. Leave unresolved drift as an explicit finding or follow-up.

## Anti-Patterns

- Treating a historical SOW as current authority when the concept catalog says
  otherwise.
- Adding a convenience wrapper, compatibility surface, or second owner without a
  concept update.
- Marking a concept `applied` based only on docs or assumptions.
- Copying concept content from another project instead of creating local
  project-specific concepts.
- Updating code semantics while postponing the required concept update.
