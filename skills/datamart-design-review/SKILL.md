---
name: datamart-design-review
description: Design or review datamarts, analytical serving tables, and semantic datasets when grain, measure formulas, table or column changes, migration impact, and evidence must be explicit. Do not use for generic SQL syntax fixes or dashboard-only presentation changes.
---

# Datamart Design Review

Ground a datamart proposal in its current source, serving, and consumer
contracts, then make the entire change traceable in one merged table-and-column
impact matrix.

## Use This Skill When

- designing or reviewing Silver, Gold, datamart, warehouse serving, or semantic
  dataset contracts
- deciding whether repeated dashboard SQL belongs in a reusable data model
- assessing schema, grain, measure, materialization, backfill, or consumer impact
  of an analytical-model change

Do not use it for generic SQL syntax debugging, operational application schemas,
chart styling, or dashboard layout when no analytical data contract changes.

## Establish Authority And Evidence

Before proposing a target:

1. Read project architecture authority and the active SOW or plan when present.
2. Inspect current table SQL or exact schema, upstream sources, refresh ownership,
   and downstream datasets, measures, reports, or APIs.
3. For a deployed contract, identify the exact object, producer, environment,
   connection/provider, and relevant version. Use direct read-only evidence when
   feasible; otherwise label the affected claim `UNVERIFIED`.
4. Separate:
   - observed source grain or candidate-key evidence;
   - proposed output grain;
   - business grain approved by the domain owner.

A unique snapshot or sample is evidence about that observation, not a timeless
business-grain contract.

## Design The Target

- Choose grain from the business process and required slicing, not from an
  existing dashboard query alone.
- Preserve exact physical/source column names and semantic lineage. Identify a
  compatibility alias and its canonical formula explicitly.
- State population, grouping, null behavior, temporal/as-of meaning, and units
  for every aggregate measure.
- State partition, order, denominator, and population for ranks, windows, ratios,
  snapshots, and lifetime values.
- Identify additive, semi-additive, and non-additive behavior where it changes
  correctness.
- Keep facts separate when authority, unit, temporal meaning, or allocation
  differs. Combining them requires verified cardinality and an approved
  allocation rule.

## Report The Change

For a detailed impact report, read
[references/impact-matrix.md](references/impact-matrix.md) and produce exactly
one merged impact table unless the user explicitly requests supplemental tables.
Keep blockers, open decisions, and implementation order in short prose outside
the matrix; do not duplicate matrix rows in prose.

For a concise conceptual question that does not propose table or column changes,
answer concisely without forcing the matrix.

## Mutation Boundary

This skill supports design and review; it does not authorize schema changes,
backfills, deployment, or production writes. Follow the target repository's SOW
and approval rules before implementation.

