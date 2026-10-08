# SOW_20261008_VO3LKN0L_EXT_3OC6OZ3G - Creation Date Provenance

- Status: DONE
- Approval: APPROVED by user
- Proposed-By: Codex
- create_dttm: 2026-10-08T13:12:20+07:00
- approve_dttm: 2026-10-08T13:27:31+07:00
- finish_dttm: 2026-10-08T13:47:22+07:00
- Parent: [SOW_20261008_VO3LKN0L](SOW_20261008_VO3LKN0L_migrate_legacy_planning_bundles.md)
- Order: First EXT; supersedes the parent's migration-day identity basis only after approval.

## Task / Why

Correct migrated SOW/Plan date segments to their evidenced creation dates,
using labelled filesystem fallback when original creation evidence is missing.
Current migration-day IDs do not meet the user's corrected requirement.

## Location

- All 123 mapped records and their bundle paths in [migration-map.json](migration-map.json).
- Four mapped reference consumers: `plan_todo/skill_design_decisions.md`,
  `plan_todo/fix_bug.md`, `docs/mcp-skills-market-architecture.md`,
  `patches/codex-router/README.md`; identity/path/link repairs only.
- Parent bundle: correction mapping, metadata evidence and verification.
- Completed parser SOW
  `plan_todo/finished/SOW_20261008_9Q4KRK17/SOW_20261008_9Q4KRK17_darwinskill_sow_anchor_format.md`:
  one incoming migration link repair at closeout only. Approval of this EXT
  authorizes that narrow exception, not other completed new-format edits.

## Baseline / Authority

- Original fields: 20 SOWs + 1 Plan have full creation datetimes; 1 SOW has
  date-only creation evidence; 80 SOWs + 6 Plans lack usable create_dttm fields.
  This field inventory does not establish absence of creation dates in prose.
- Live source birthtimes can survive the executed rename/in-place-write path;
  live mtimes were overwritten by migration and cannot supply old timestamps.
  Pre-migration content snapshots retain old mtimes; snapshot birthtimes are
  copy metadata and MUST NOT be treated as original creation times.
- This is a proposed repo-local historical migration exception to the packaged
  rule forbidding lifecycle inference from filesystem metadata. It activates
  only on explicit EXT approval; no global skills or policy change is proposed.

## As-Is / To-Be (ASCII)

```text
as-is: original evidence -> migrated SOW_20261008_RANDOM8
to-be: evidence priority -> creation date + provenance
                        -> SOW/PLAN_YYYYMMDD_same_RANDOM8
                        -> owned names + references repaired
```

## Behavior Locks

1. Resolve creation evidence in this order: original full create_dttm;
   explicit creation date in the preserved source; original-file FS birthtime;
   verified pre-migration FS mtime. Approval/completion dates, migration time,
   Git commit dates and inferred numbering chronology are not creation evidence.
   Ambiguous/conflicting explicit creation evidence blocks that record pending
   resolution; never bypass it silently with a lower-priority fallback.
   Before FS selection, audit the preserved original content and its scoped
   existing reference/decision evidence for explicit creation claims. Record
   inspected sources and one outcome per base record: `explicit_full`,
   `explicit_date`, `fs_birthtime`, `fs_mtime`, or `blocked`. Do not infer absence
   from the create_dttm field alone or search private transcripts by default.
2. A known create_dttm remains unchanged; ID YYYYMMDD equals its date component
   in its recorded offset. Preserve RANDOM8. Each SOW and Plan uses its own date.
   EXT/decision filenames inherit the corrected parent prefix; EXT RANDOM8 and
   its independent lifecycle remain unchanged.
3. A date-only creation source sets `create_date: YYYY-MM-DD` with provenance;
   exact create_dttm remains unknown unless independently evidenced. Do not
   synthesize midnight or borrow a clock time. In this narrow historical case,
   ID date matches create_date rather than pretending a full datetime exists.
4. For missing explicit creation evidence, an approved FS fallback may populate
   create_dttm with the observed timezone-aware metadata timestamp, while
   preserving original unknown/missing values in the historical record.
   Set `create_dttm_source: filesystem_birthtime | filesystem_mtime`,
   `create_dttm_confidence: filesystem_proxy`, and the evidence reference.
   This records a physical-file proxy, not verified historical task creation.
5. FS birthtime is eligible only with documented original-file lineage through
   rename/in-place updates, not a new copy/replacement. Unix ctime is NOT creation
   time. FS mtime is eligible only from the frozen pre-migration snapshot whose
   source content hash matches the original map, with copy-preservation evidence.
   Never use post-migration live mtime or snapshot birthtime.
   Snapshot mtime evidence includes raw epoch, snapshot identity/path/hash,
   copy-operation evidence or a contemporaneous source-mtime comparison,
   observed_dttm and timezone conversion. Content hash alone does not prove
   metadata preservation. A reading captured now is labelled observed now;
   never fabricate a copy-time observation. Missing preservation evidence
   disqualifies that fallback instead of reconstructing historical metadata.
6. Before further writes, record raw FS timestamps, source/current paths,
   observed time, content hashes and selected evidence for each fallback.
   Convert FS epochs to Asia/Ho_Chi_Minh (+07:00), to seconds, then derive the
   date. Label clone/copy or clustered birthtime concerns; do not upgrade proxy
   confidence. Missing/unreliable lineage or impossible/future timestamps block
   that record; no automatic migration-day fallback.
   Preflight must locate the existing snapshot, verify it is readable and its
   source hashes match, and freeze its identity/metadata evidence before any
   correction writes. Repeat that availability check at execution. If absent,
   mark snapshot-based fallback unavailable; do not create a new snapshot and
   present its metadata as pre-migration history. Other eligible evidence may
   still resolve a record. A genuinely evidenced creation on migration day is
   valid; only selecting migration time as the fallback basis is forbidden.
7. Draft a complete correction map before renames: original source, current
   identity/path, corrected identity/path, creation evidence/source/confidence,
   and tracking state. Check collisions and all 108 base SOW/Plan date decisions.
   Collision checks cover all 123 corrected output paths/identities (108 base
   SOW/Plan plus 15 owned EXT/decision files), and existing untouched planning
   namespaces. Validate parent prefixes as well as base RANDOM8 uniqueness.
   Preserve the first migration map/evidence as superseded history, not a second
   live identity or redirect layer. Stop on content/index drift or unmapped refs.
8. Trial the correction against a temporary copy, including original datetime,
   date-only, FS birthtime, FS mtime, distinct child/Plan dates and duplicate
   legacy SOW_0056. Only after trial passes, rename the existing live bundles and
   repair headings, EXT/decision prefixes, Plan references and mapped consumers.
   No duplicate contracts, empty stubs or regeneration of RANDOM8.
9. Preserve tracking boundaries, user edits, scope/approval/finish evidence and
   all substantive historical content. Retain the parent's snapshot/recovery
   discipline; capture FS evidence before any operation that could alter it.

## Deliverables / Done Criteria

- Complete reviewed correction map for 101 SOWs + 7 Plans, with source evidence
  for every creation date and explicit proxy labels where applicable.
- All 123 mapped record paths updated consistently; each ID date equals its
  authoritative create_dttm date or explicitly permitted create_date/fallback.
- Before/after audit explains only identity/provenance/reference/placement
  changes. No approval, completion or historical clock time is fabricated.
- Negative checks reject migration-day fallback, copied birthtime, live mtime,
  ctime, missing evidence, lost RANDOM8, collision and parent-date inheritance
  by a child SOW. Duplicate legacy SOW_0056 remain separate.
- Re-run full content/link/tracking audits, package tests and both staged and
  unstaged diff checks; renew output hashes. Separate existing broken-link
  exceptions from new failures. Unresolved records block full closeout.
- Closeout repairs the one approved parser incoming link and moves the whole
  standalone migration bundle to finished after all parent/EXT gates pass.

## Out Of Scope / Risks

- No commit, push, global sync, Git-history rewrite, product code, tests or
  global policy edits. Approved correction is limited to this migration.
- FS dates can reflect clone/copy/materialization, not logical creation.
  Explicit provenance and proxy confidence are mandatory; missing lineage needs
  user resolution, not silently manufactured certainty.
- This extension does not add a persistent allocator, service or migration CLI.

## Review Resolution

- One independent static review by GLM-5.3-max, fresh `fork_turns: none`.
  Findings: two Medium and two Low; no implementation was delegated or run.
- Patched snapshot metadata provenance and availability gates; added per-record
  explicit-evidence discovery outcomes and collision coverage for all 123 outputs.
- Coordinator document checks: required lifecycle fields, links, unique EXT name,
  and staged/unstaged diff whitespace checks pass. This is draft-contract review,
  not proof that every historical creation date or FS fallback is eligible.
- No second independent review requested or performed. The user subsequently
  approved execution; this EXT now governs the correction with its parent.

## Execution / Closeout

- Corrected 108 base identities and all 123 owned record paths; RANDOM8,
  historical content and approval/completion evidence preserved.
- Sources: 21 full original datetimes, 3 date-only creation claims and 84
  filesystem birthtime proxies. Exact historical times remain unknown for
  date-only records; physical-file proxies are explicitly labelled, not proven
  logical creation. Mtime fallback passed a fixture check but was not needed live.
- Trial/live: 127 payloads, 123 preserved bodies, 108 date/RANDOM8 checks,
  53 links, zero new broken links; 13 negative checks and 47 package tests pass.
  Tracking remains 118 tracked / 5 untracked, with unrelated edits preserved.
- Independent fresh GLM-5.3-max final audit: no actionable findings. Existing
  two broken-link occurrences remain the approved baseline exception.
- Final evidence: [correction-verification-evidence.json](correction-verification-evidence.json).
  Closed with parent, repaired the authorized parser incoming link and moved
  the whole bundle to finished. No code/policy change, commit, push or sync.
