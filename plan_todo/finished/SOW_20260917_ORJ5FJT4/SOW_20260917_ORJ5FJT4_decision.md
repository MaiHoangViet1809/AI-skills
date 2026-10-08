# SOW_20260917_ORJ5FJT4 - Scope Decisions

- legacy_id: SOW_0088
- legacy_path: plan_todo/finished/SOW_0088_spark_connect_debug_skill.md
- migrated_dttm: 2026-10-08T12:48:51+07:00
- Parent: [SOW_20260917_ORJ5FJT4](SOW_20260917_ORJ5FJT4_spark_connect_debug_skill.md)

## Preserved Contract And Historical Evidence

## Decision Log

- **D0088-1** — Make exact SQL/source metadata the mandatory first fast path
  for every Spark Connect execution error. Missing metadata is conclusive;
  complete metadata proceeds to the normal lifecycle, transport, storage, or
  logical-plan branches. This is a priority rule, not a claim that every 502
  means missing metadata.
- **D0088-2** — Require exact runtime identity and mutation reconciliation.
  A client-side RPC failure does not prove that a write did not commit, and a
  different application identity invalidates comparison with an earlier run.
