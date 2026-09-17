# SOW_0088 — Spark Connect Debug Evidence Skill

## Lifecycle

- Status: completed
- Approval: approved by user in current conversation
- create_dttm: `2026-09-17T00:00:00+07:00`
- approve_dttm: `2026-09-17T00:00:00+07:00`
- finish_dttm: `2026-09-17T00:00:00+07:00`
- Proposed-By: Codex GPT-6
- plan: Standalone

## Task

Create a canonical `spark-connect-debug` skill that diagnoses Spark Connect
failures from exact runtime evidence. When a Spark Connect error appears, the
skill must immediately check SQL/source metadata; only when those checks pass
does it continue through the normal runtime branches.

## Why

Recent Spark Connect incidents presented as gRPC/HTTP 502 while the useful
root-cause evidence was split across SQL analysis, catalog/schema state, query
plan, driver lifecycle, and storage/runtime logs. The shortest useful path is
an immediate metadata check against the exact SQL/source: missing table,
column, schema, or catalog object is the conclusion. Only a clean metadata
check should open the slower lifecycle, transport, storage, or plan branches.
This prevents token-wasting detours, blind timeout increases, retries, or
mutation replay.

## Evidence boundary

- Confirmed source lesson: a missing table/column or incompatible query plan
  can surface through Spark Connect as a generic upstream error when the error
  response is lost or the service is unhealthy.
- Confirmed adjacent failure class: OOMKilled/exit 137/restart count and a
  changed Spark application identity indicate a lifecycle failure, not proof of
  a metadata failure.
- Unresolved by this SOW: a universal mapping from HTTP status to root cause;
  the skill must require direct evidence and report uncertainty.
- No secrets, `.env` contents, private endpoints, or machine-specific paths
  enter the skill or regression fixture.

## Location

- `skills/spark-connect-debug/SKILL.md`
- `skills/spark-connect-debug/agents/openai.yaml`
- `skills/registry.json`: registry entry for this skill only
- `tests/skill_feedback_cases/spark-connect-debug.json`
- This SOW

Unrelated dirty files remain untouched. No DE-project runtime code, Spark
Connect server, Airflow DAG, proxy, catalog, or installed skill copy changes.

## As-Is Diagram

```text
Spark Connect error (often 502)
  -> ambiguous symptom
  -> ad-hoc retry / timeout / replay risk
  -> root cause may remain unverified
```

## To-Be Diagram

```text
Spark Connect failure
  -> immediately inspect exact SQL/source metadata
       catalog/schema/table/view/column/type/query-plan references
  -> missing object/column/schema
       -> conclude metadata/analysis root cause
  -> metadata complete
       -> capture runtime identity
            app/start | driver | client session | endpoint/provider | version/config
       -> classify remaining evidence
            plan/data | lifecycle/memory | transport/service
            storage/catalog | unknown
  -> run cheapest safe probes
       only the probes for the selected branch
  -> reconcile mutation state before replay
  -> report confirmed facts, rejected hypotheses, unknowns, next safe probe
```

## Deliverables

1. Add the canonical `spark-connect-debug` skill with:
   - a discriminating trigger for Spark Connect 502, invalid session, analysis,
     OOM/restart, storage, and query-plan failures;
   - an immediate, bounded, read-only metadata fast path for every Spark
     Connect execution error; it must not begin with a full data scan;
   - a conclusive missing-metadata branch before any broader investigation;
   - an explicit distinction between “the metadata probe reports a missing
     object” and “the metadata probe itself is unavailable or returns 502”;
   - required runtime identity fields after metadata passes and before further
     attribution;
   - metadata/query-plan checks before changing retry or timeout settings;
   - explicit classification of metadata, lifecycle/memory, transport/service,
     storage/catalog, logical-plan/data, and unknown failures;
   - a no-blind-replay rule for writes/merges/overwrites after ambiguous RPC
     loss;
   - concise evidence-first output separating fact, interpretation, and next
     read-only action.
2. Register the skill and its shipped interface metadata in `skills/registry.json`.
3. Add one sanitized feedback fixture with expected, negative, and boundary
   scenarios for the new triage procedure.
4. Validate the canonical skill structure and the existing feedback/sync test
   contracts. Do not claim live Spark Connect behavior from structural tests.

## Done Criteria

1. Every Spark Connect execution error starts with an immediate exact
   SQL/source metadata check; no broader branch may run first.
2. Missing table, column, schema, or catalog object is reported as the
   metadata/analysis conclusion with the exact missing reference.
3. If the metadata probe itself fails because Spark Connect is unavailable, it
   is not treated as proof of missing metadata; the normal transport/service
   branch remains available.
4. A clean metadata check opens the normal lifecycle, transport, storage, or
   logical-plan branches; the skill does not state that 502 always means
   missing metadata.
5. If exact SQL/source metadata is unavailable, the skill reports the
   metadata preflight as `unverified` and requests the missing artifact rather
   than inferring a root cause or skipping directly to broad runtime checks.
6. The skill captures application/session/driver identity and environment
   before comparing non-metadata incidents across deployments.
7. The skill forbids blind replay of a mutation whose commit status is unknown.
8. Fixture contains exactly one `expected`, one `negative`, and one `boundary`
   scenario with sanitized evidence references.
9. `quick_validate.py`, `uv run python -m unittest
   tests.test_skill_feedback_cases tests.test_skill_sync_scripts`, and
   `git diff --check` pass for the scoped change.
10. Forward model behavior is not claimed; only structural validation and
   scenario review are reported unless a later isolated run provides evidence.
11. No installed environment is synchronized and no push is performed unless
   separately requested.

## Out-of-Scope

- Modifying Spark Connect, Spark Operator, proxy, Gravitino, Iceberg, Airflow,
  or DE-project runtime code.
- Adding automatic probes, telemetry, retry policy, session persistence, or a
  production remediation layer.
- Treating a similar table/schema, another environment, or synthetic fixture
  as proof of the exact failing runtime contract.
- Reading or storing credentials, `.env` files, raw PII, private endpoints, or
  full production logs in AISkills.
- Syncing the skill to an installed agent or pushing the repository.

## Decision Log

- **D0088-1** — Make exact SQL/source metadata the mandatory first fast path
  for every Spark Connect execution error. Missing metadata is conclusive;
  complete metadata proceeds to the normal lifecycle, transport, storage, or
  logical-plan branches. This is a priority rule, not a claim that every 502
  means missing metadata.
- **D0088-2** — Require exact runtime identity and mutation reconciliation.
  A client-side RPC failure does not prove that a write did not commit, and a
  different application identity invalidates comparison with an earlier run.

## Cautions / Risks

- Metadata checks can themselves fail while the service is unhealthy; record
  that limitation instead of converting a failed probe into a root-cause claim.
- A 502 may hide an analysis exception, but it may also be caused by driver
  restart, OOM, proxy, or catalog/storage failure.
- The skill is a diagnostic procedure, not a guarantee that the host exposes
  every server-side metric.
