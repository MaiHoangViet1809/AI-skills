# Datamart Impact Matrix

Use this reference when a proposed or reviewed change affects a datamart,
analytical serving table, or semantic dataset contract.

## Output Contract

Produce exactly one table for the impact report unless the user explicitly asks
for supplemental tables. Repeat table context for every affected column so each
row remains understandable independently.

| Field | Required content |
| --- | --- |
| `Layer / Table` | Exact physical relation. For a rename, show the applicable old or new physical name. |
| `Table action` | `NEW`, `UPDATE`, `DROP`, or material `KEEP`. |
| `Grain / refresh before -> after` | Grain and any affected materialization, partition, or refresh contract. Use `N/A` only when genuinely unavailable. |
| `Column` | Exact physical name. Use `*` only for a whole-table drop or table-only action. |
| `Column action / type before -> after` | `NEW`, `UPDATE`, `DROP`, or material `KEEP`, plus the physical type transition when known. |
| `Formula / semantics before -> after` | SQL-like expression or precise business rule, including source lineage. |
| `Reason` | Business or technical reason specific to the row. |
| `Downstream / migration impact` | Affected datasets, measures, reports, compatibility, backfill, and cutover consequences. |
| `Evidence status` | `VERIFIED`, `PROPOSED`, or `UNVERIFIED`, plus a compact exact-runtime identity or authoritative reference. |

Rules:

- List every physical column for a `NEW` table.
- For an `UPDATE` table, list every `NEW`, `UPDATE`, and `DROP` column. Include a
  `KEEP` column only when it is a grain key, identity, partition, or compatibility
  contract material to the change.
- Represent a whole-table drop with `Column = *`.
- Represent a rename as old physical column `DROP` and new physical column `NEW`;
  link the two in their formula/semantics cells.
- State explicitly after the matrix when there are no table or column drops.
- For aggregates, include population, grouping, and null behavior—not only
  `SUM`, `COUNT`, or `AVG`.
- For ranks, windows, ratios, snapshots, and lifetime values, include partition,
  order, denominator, and as-of semantics as applicable.
- Preserve original source names. Friendly labels belong in presentation
  metadata and must not replace physical lineage in this matrix.

## Sanitized Example

| Layer / Table | Table action | Grain / refresh before -> after | Column | Column action / type before -> after | Formula / semantics before -> after | Reason | Downstream / migration impact | Evidence status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `SILVER.FCT_ORDER_REVENUE` | `UPDATE` | `ORDER_LINE`, append -> `ORDER_LINE`, merge by `ORDER_LINE_ID` | `ORDER_LINE_ID` | `KEEP`; `STRING -> STRING` | Stable source identifier unchanged | Preserve candidate key and merge ownership | Existing consumers retain their join key; no backfill for this column | `VERIFIED`: deployed source schema and duplicate profile |
| `SILVER.FCT_ORDER_REVENUE` | `UPDATE` | `ORDER_LINE`, append -> `ORDER_LINE`, merge by `ORDER_LINE_ID` | `REVENUE_AMT` | `UPDATE`; `DECIMAL(12,2) -> DECIMAL(18,2)` | `GROSS_AMT -> BASE_AMT + COALESCE(ADJUSTMENT_AMT, 0)`; grouped by `ORDER_LINE_ID`; null base remains null | Publish the approved adjusted-revenue definition without overflow | Revenue measures change; full rebuild and reconciliation required | `PROPOSED`: formula approved; target runtime not built |
| `SILVER.FCT_ORDER_REVENUE` | `UPDATE` | `ORDER_LINE`, append -> `ORDER_LINE`, merge by `ORDER_LINE_ID` | `LEGACY_ACCOUNT_ID` | `DROP`; `STRING -> N/A` | Replaced by `ACCOUNT_ID`; no coalescing across namespaces | Remove ambiguous identity name | Consumers must migrate before column removal | `PROPOSED`: consumer inventory complete |
| `SILVER.FCT_ORDER_REVENUE` | `UPDATE` | `ORDER_LINE`, append -> `ORDER_LINE`, merge by `ORDER_LINE_ID` | `ACCOUNT_ID` | `NEW`; `N/A -> STRING` | Exact source `ACCOUNT_ID`; replacement for `LEGACY_ACCOUNT_ID` | Preserve source identity naming | Requires consumer rename and rebuild | `PROPOSED`: source column verified; target pending |
| `GOLD.MART_ACCOUNT_REVENUE` | `NEW` | `N/A -> ACCOUNT_ID x PERIOD_MONTH`; monthly full replacement | `ACCOUNT_ID` | `NEW`; `N/A -> STRING` | From `SILVER.FCT_ORDER_REVENUE.ACCOUNT_ID` | Expose account slicing without a user join | New semantic dataset key | `PROPOSED`: target design |
| `GOLD.MART_ACCOUNT_REVENUE` | `NEW` | `N/A -> ACCOUNT_ID x PERIOD_MONTH`; monthly full replacement | `PERIOD_MONTH` | `NEW`; `N/A -> STRING` | Month derived from the governed event date in `yyyy-MM` | Standardize monthly filtering | Dashboard filters must target this physical column | `PROPOSED`: target design |
| `GOLD.MART_ACCOUNT_REVENUE` | `NEW` | `N/A -> ACCOUNT_ID x PERIOD_MONTH`; monthly full replacement | `REVENUE_AMT` | `NEW`; `N/A -> DECIMAL(18,2)` | `SUM(SILVER.FCT_ORDER_REVENUE.REVENUE_AMT)` by `ACCOUNT_ID, PERIOD_MONTH`; null-only groups remain null | Serve one reusable monthly revenue measure | Replaces repeated dashboard aggregation; reconcile before cutover | `PROPOSED`: target design |
| `GOLD.OLD_ACCOUNT_REVENUE` | `DROP` | `ACCOUNT_ID x PERIOD_MONTH`, full replacement -> N/A | `*` | `DROP`; all columns | Superseded by `GOLD.MART_ACCOUNT_REVENUE` after consumer cutover | Remove duplicate semantic ownership | Drop only after consumer inventory reaches zero and replacement reconciles | `UNVERIFIED`: cutover and zero-consumer checks pending |

After the matrix, state only the remaining blockers, open decisions, recommended
implementation order, and whether any table or column drops exist. Do not restate
the rows.

