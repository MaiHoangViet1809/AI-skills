---
name: spark-connect-debug
description: Diagnose Spark Connect execution failures by checking exact SQL/source metadata first, then separating metadata, lifecycle, transport, storage, and query-plan causes from runtime evidence.
---

# Spark Connect Debug

Use this skill for Spark Connect gRPC/HTTP errors (`502`, invalid session,
analysis failures, write/read failures, or unexplained long-running plans).

## Non-negotiable triage order

An HTTP/gRPC status is a symptom, not a root-cause label. For every execution
error, inspect the exact SQL/source metadata first. Do not start with retries,
timeouts, persistence, a full data scan, or a mutation replay.

```text
Spark Connect execution error
  -> exact SQL/source metadata fast path (bounded, read-only)
       missing table/view/schema/column/type/object
         -> conclude metadata/analysis root cause
       metadata complete
         -> investigate the normal runtime branches
       probe unavailable / SQL-source unavailable
         -> report metadata preflight as unverified
```

## 1. Metadata fast path

Use the exact environment, connection, catalog, schema, source, and sink from
the failed task. From the SQL or source definition, enumerate referenced
tables/views and columns, then perform the cheapest read-only checks available:

- catalog/schema/table or view existence;
- referenced column and nested-field existence;
- source/sink schema and relevant type compatibility;
- mapping/reference tables used by the query;
- parser/analyzer or `EXPLAIN` only when it is safe and does not require a
  full data scan.

If a probe explicitly reports a missing object, record the exact identifier and
stop: that is the metadata/analysis conclusion. If the probe itself returns
`502`, `UNAVAILABLE`, or another service failure, it is not evidence that
metadata is missing. If the exact SQL/source cannot be obtained, mark the
preflight `unverified`; do not invent references or skip directly to a broad
investigation.

## 2. Runtime branches after metadata passes

Capture these values before comparing environments or attributing a remaining
failure: application ID, application start time, driver host, client session
ID, endpoint/provider, environment, Spark/client version, and relevant config.

Classify the remaining evidence:

- **Lifecycle/memory**: `OOMKilled`, exit `137`, restart count, or changed
  application identity. Treat this as a driver/service lifecycle issue, not a
  metadata conclusion.
- **Session/transport/service**: `INVALID_HANDLE`, connection reset, `502`, or
  timeout after metadata is complete. Check service availability and session
  continuity; do not blindly replay a write.
- **Storage/catalog**: REST, filesystem, commit, permission, or Iceberg/catalog
  errors after the query is accepted.
- **Logical plan/data**: skew, large scan, join/aggregation explosion, or
  executor-stage failure after metadata and service health are established.
- **Unknown**: evidence is insufficient; state exactly what is missing.

## Mutation safety

For `MERGE`, `OVERWRITE`, `REPLACE`, append, DDL, or other mutations, a lost
RPC response does not prove that the operation failed. Reconcile target state
and commit evidence in a fresh/read-only path before any retry. Never replay a
mutation solely because the client saw `502` or `UNAVAILABLE`.

## Response format

Keep the result compact and evidence-backed:

1. **Confirmed facts** — exact error, SQL/source identity, metadata result,
   runtime identity, and lifecycle/service evidence.
2. **Conclusion** — metadata root cause, runtime branch, or `unverified`.
3. **Rejected hypotheses** — only when evidence rules them out.
4. **Next safe probe** — one bounded read-only action; no speculative config
   changes.

Do not claim that every `502` is a missing-table/column error. Do not treat a
similar table, another environment, synthetic fixture, or producer code as
proof of the failed runtime contract.
