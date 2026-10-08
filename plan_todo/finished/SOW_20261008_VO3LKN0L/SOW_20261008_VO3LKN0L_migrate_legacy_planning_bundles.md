# SOW_20261008_VO3LKN0L - Migrate Legacy Planning Bundles

- Status: DONE
- Approval: User approved migration explicitly in this task on 2026-10-08.
- Proposed-By: Codex
- create_dttm: 2026-10-08T11:20:20+07:00
- approve_dttm: 2026-10-08T12:28:49+07:00
- finish_dttm: 2026-10-08T13:47:22+07:00
- Plan / Reference: Standalone migration; follows
  [bundle contract SOW](../SOW_20261007_HU2ZJ4QS/SOW_20261007_HU2ZJ4QS_planning_bundle_contract.md).

## Task

Trial-migrate all legacy SOWs in this project to the new bundle format,
including their existing owning Plans, extensions and scoped decisions.

## Why / Baseline

- Read-only inventory: 101 base SOWs, 7 existing Plans, 2 separate EXT files
  and 2 detected inline extensions. Sources and exact proposed destinations
  are locked in [migration-map.json](migration-map.json), with SHA-256 snapshots,
  tracked/untracked state, 11 scoped decision extractions and 4 reference consumers.
- 15 base SOWs are at `plan_todo/` root; 86 are in `finished/`. Root placement
  does not establish active status: several records explicitly say completed.
- Two independent records share `SOW_0056`; source path, not numeric ID alone,
  is the migration identity key. Forty base records lack an explicit Status.
- Several sources and reference consumers are untracked or dirty. Re-check
  snapshots and ownership before edits; stop on changed inputs, never overwrite.
- Follow AGENTS.md and DRY/SOLID/KISS. No project principle document or declared
  concept authority was found. The packaged planning contract governs this
  explicitly requested conversion, not unrelated target repositories.

## Location

- Source and destination files enumerated in `migration-map.json`: 101 base
  SOWs, 7 Plans and 4 extracted/separate extensions, including their bundle folders.
- The 11 scope-owned decision files and section boundaries in the map. EXT-owned
  decisions stay inside their EXT; binding design/scope clauses not listed for
  extraction remain in the base contract. Additional extraction needs reviewed
  mapping and explicit scope approval before edits.
- `plan_todo/skill_design_decisions.md`, `plan_todo/fix_bug.md`: reference repairs
  only; retain the shared canonical decision log and unrelated text.
- `docs/mcp-skills-market-architecture.md`, `patches/codex-router/README.md`:
  mapped identity/path/link repairs only, preserving architecture and patch behavior.
- This migration bundle: mapping, evidence and necessary migration decisions.
- No code, tests, skills, dependencies, policy or runtime changes.

## As-Is Diagram (ASCII)

```text
plan_todo/
  SOW_0047_*.md ... SOW_0097_*.md   # mixed active/completed
  *_plan.md
  skill_design_decisions.md
  finished/
    SOW_0001_*.md ... SOW_0101_*.md
    SOW_0096_EXT_01_*.md
    *_plan.md
```

## To-Be Diagram (ASCII)

```text
plan_todo/
  active/
    SOW_YYYYMMDD_RANDOM8/
      SOW_YYYYMMDD_RANDOM8_<task>.md
    PLAN_YYYYMMDD_RANDOM8/
      PLAN_YYYYMMDD_RANDOM8_<plan>.md
      SOW_YYYYMMDD_RANDOM8/
        SOW_YYYYMMDD_RANDOM8_<task>.md
  finished/
    <completed/archived standalone SOW bundles>
    <completed/archived Plan bundles with owned SOWs>
  skill_design_decisions.md          # shared authority stays
```

## Deliverables / Behavior Locks

1. Treat the map as the approved file-level move allowlist. Keep assigned IDs
   stable; scan all planning records for collisions before execution. Approval
   of this SOW explicitly permits re-identification of these legacy records,
   not silent renaming of any other approved identity.
2. Per the user's correction, the date segment of each SOW/Plan ID MUST equal
   the calendar date of that record's original `create_dttm`, not the migration
   date. Preserve RANDOM8 while correcting the date, and propagate the resulting
   identity/path changes to owned EXT/decision files and affected references.
   Each child SOW uses its own creation date, not its parent Plan's date.
   Retain original approval/completion evidence and actual `migrated_dttm`
   separately. Never invent a creation date or clock time when history is unknown;
   unresolved dates require explicit user direction before re-identification.
   Distinguish the two SOW_0056 records by path.
3. Preserve task, scope, decisions, acceptance, evidence, approval and lifecycle
   meaning. Do not reauthor historical implementation contracts or claim new
   verification. Retain known full datetimes; use `unknown` for unavailable
   historical times and preserve original date-only evidence separately.
   Missing historical Status/Approval becomes `UNKNOWN`, never inferred approval
   or successful completion from a folder. Future events remain `null`.
   Preserve the original authority text separately when normalizing lifecycle
   fields; do not replace a known event date with fabricated clock time.
4. Existing explicit Plan ownership defines nesting. The proposed map assigns
   dashboard 0021-0026, follow-up 0027-0028, distillation 0042-0055, data 0058-0059,
   sync 0062-0065, cleanup 0066-0069 and MCP 0093 to their recorded Plans.
   Confirm ownership against source text before writes; stop on contradiction.
   Other SOWs remain standalone. Do not invent a new umbrella Plan.
5. Preserve active versus completed/obsolete states. The distillation Plan has
   recorded completed acceptance and moves as a whole to finished. An unfinished
   Plan retains completed children. Existing archived records lacking status stay
   archived with explicit unknown history, not newly certified DONE. No migration
   action reopens implementation, closes draft work or grants scope approval.
6. Extract inline extensions of SOW_0071 and SOW_0092, preserving their exact
   lifecycle, approval, evidence and nested decisions. Record approved order and
   dependencies in the base. Move separate EXT files of SOW_0096 and SOW_0099
   into their owners. The map locks unique start/end headings, line ranges and
   section hashes, including nested evidence/decisions, for both inline extractions.
   Use heading/hash identity, not line numbers alone. Inventory additional
   variants before conversion; newly found records require map review and explicit
   scope approval before their moves.
   Do not invent missing approval, retroactively enforce the extension limit by
   discarding history, or duplicate full base content in an EXT.
7. Extract clearly owned inline decisions only when content and authority remain
   intact; preserve chronology and original wording. Shared project decisions
   remain canonical. Unclear ownership stays linked/in place and needs a decision
   before any extraction; never copy it into several bundles.
   Keep an authoritative link at each extraction site; require the base/EXT
   consumer to read those decisions when they govern scope. Do not weaken binding
   constraints by turning them into optional background material.
8. Repair live relative/absolute repo references, mapped filename strings and
   affected heading anchors in allowed docs. Resolve duplicate numeric references
   from context, never global replace by number alone. Preserve intentional
   historical IDs in quotes, fixtures and baseline diagrams with traceability;
   distinguish them from obsolete live links. No redirect stubs or duplicate files.
9. First exercise a representative subset in a temporary copy: standalone,
   Plan-backed, inline EXT, separate EXT, duplicate ID and unknown history.
   Verify content/link preservation before applying the full approved mapping.
   Use `git mv` for tracked files and scoped moves for untracked files; never
   add unrelated local artifacts to a migration commit.
   Preserve original Git tracking boundaries: mapped untracked sources and their
   transformed destinations remain untracked unless the user separately approves
   adding them. Tracked dirty hunks remain local unless explicitly owned by this
   migration. Stop on source/consumer hash or tracking-state drift; refresh and
   review the map rather than silently rebasing onto user changes.
   Before live moves, keep a task-owned temporary content/index snapshot for
   reversible recovery, including untracked inputs. On failure, stop and repair
   or roll back only this migration's moves/hunks after checking for new user
   changes; never broad-reset, stash or overwrite shared work. Record partial
   progress explicitly and verify restored contents against the baseline hashes.

## Done Criteria

- Every baseline source has exactly one accounted destination; inline EXT
  sections have explicit preserved extraction boundaries. No lost/duplicate
  records; new IDs and filenames are valid and unique.
- Before/after content audit explains every delta: identity/metadata, physical
  placement, extension/decision extraction and repaired references only.
  Historical approval, timestamps, task/scope/acceptance and evidence survive.
- All previously resolving links, including links to unmoved code/docs, still
  resolve after relocation/extraction. Required mapped references resolve.
  Inventory pre-existing broken links separately; preserve them as explicit
  baseline exceptions, not new migration failures or silently fixed unrelated gaps.
- All recorded source/consumer and extraction hashes match preflight. Every
  mapped decision section is preserved once with a working authority link.
- Negative checks: duplicate SOW_0056 are not merged; unknown lifecycle does not
  become approved/done; incomplete Plan does not move; unchanged source hashes
  are required before edits; deliberate missing mapping/link is detected.
- Existing new-format bundles and unrelated dirty hunks remain untouched except
  this migration SOW's own lifecycle/closeout. Inventory changes require review.
- Run existing planning/package tests and `git diff --check`; inspect scoped
  diff and record exact outcomes, mapping counts and remaining gaps here.
- Complete all 101 base SOW conversions, associated Plan/EXT conversion and
  required reference repairs before claiming full migration. Unresolved required
  records block closeout, not a silent reduced denominator.

## Selected Sequence / Parser Maintenance

- Confirmed direct check: `darwinSkill/src/extraction.py:16` uses
  `SOW_PATTERN = re.compile(r"\bSOW_\d{4}\b")`. `SOW_0058` matches;
  `SOW_20261008_VO3LKN0L` does not. New-ID logs can lose their scope anchor.
  Existing legacy fixture tests do not prove new-format compatibility.
- Current `skill-evolution-flow` does not call DarwinSkill. The matcher belongs
  to an independent mini-project; no direct production skill-workflow regression
  was established. It is not inherently required to move planning documents.
- User selected parser maintenance first. Track it in
  [SOW_20261008_9Q4KRK17](../../finished/SOW_20261008_9Q4KRK17/SOW_20261008_9Q4KRK17_darwinskill_sow_anchor_format.md).
  Follow that selected order before bulk migration; this migration SOW does not
  edit the parser, invent aliases or silently expand into runtime work.

## Review Evidence

- Two coordinator review passes: original scope/mapping and revised-contract
  audit. Coverage, hashes, 123 unique destinations, 13 non-overlapping extraction
  ranges, tracking states, parent destinations and draft links checked; PASS.
  `git diff --check` PASS. Parser compatibility probe confirms the gap above.
- Two independent native GLM-5.3-max reviews were launched with
  `fork_turns: none`, but returned no final result within the bounded wait and
  were interrupted. They are incomplete, not counted as completed reviews.
- Review/writeback only: no legacy file moves, implementation, commit or push.

## First Structural Trial Evidence

- Approval recorded from the user's explicit approval on 2026-10-08.
- Initial preflight: all source/consumer SHA-256 and recorded tracking states
  match the frozen map. 110 whole-file moves: 106 tracked and 4 untracked;
  13 section extractions produce 123 mapped destination documents.
- Snapshot: 114 unique input documents and the Git index retained in a
  task-owned temporary directory before any live moves.
- Baseline: `uv run --no-sync --offline python -m unittest discover -s tests`:
  47 passed. No live migration moves performed at this stage.
- delegation_decision: delegated; exact registered GLM-5.3 role at max,
  isolated `fork_turns: none`. Four bounded responsibilities: preflight,
  temporary transformation, link rewriting, independent output audit.
  Delegates do not edit live source documents; coordinator owns final writes.
- Temporary import-only tooling is validation/migration support, not a new
  repository CLI or product capability. Historical lifecycle evidence remains
  authoritative; metadata normalization does not approve or complete old work.

## Implementation Verification

- State: SUPERSEDED_STRUCTURAL_TRIAL; the completed structural verification below
  predates the user's corrected identity-date requirement and does not establish
  acceptance under that requirement. The creation-date correction below is the
  final accepted result; retain this first trial as historical evidence only.
  Exact results and output hashes: [verification-evidence.json](verification-evidence.json).
- Applied all 101 base SOWs, 7 existing Plans, 4 EXT records and 11 decision
  files: 110 whole-file moves and 13 preserved extractions, 123 destination
  records plus 4 reference consumers. All 33 owning-Plan relationships retained.
- Preflight independently passed source/tracking hashes, 13 exact extraction
  hashes, 123 unique nonexisting targets and 33 explicit Plan ownerships.
- Trial generated and audited all outputs before live moves, including
  standalone, Plan-backed, both EXT forms, duplicate SOW_0056 and unknown history.
  Coordinator verified full substantive preservation in all 127 outputs,
  canonical lifecycle fields in 112 records and unchanged historical evidence.
- Live payload matched trial exactly; all 110 old whole-file paths are absent
  and all destinations exist. Tracking boundaries verified: 118 destination
  records tracked, 5 untracked (4 originally untracked inputs plus their owned
  decision extraction). Unrelated edits and untracked drafts remain local.
- Root planning/package suite: 47 tests passed after live migration;
  `git diff --check` and scoped index check passed. Trailing EOF blank lines
  in three base files and ten extracted files were removed as formatting-only
  repairs; final content preservation and exact payload checks passed again.
- Negative probes detect missing mapping/output, removed substantive evidence
  and missing links. Duplicate SOW_0056 maps to two distinct identities;
  unknown history is not converted to approval or certified completion.
- Gap pass repaired current identity/path references in architecture authority,
  patch README and bug log; a fresh isolated GLM-5.3-max review confirmed those
  consumers. Historical review mentions remain unchanged.
- Remaining baseline exception: two links in the former SOW_0084 refer to
  missing `2026-09-15_skill_complexity_audit.md`. They were already broken,
  remain recorded, and are not new migration failures or waived done criteria.
- Delegation: four isolated GLM-5.3-max responsibilities were launched in
  parallel. Preflight and link rewriting completed. Temporary transformation
  had observed zip-length, missing-key and range failures; coordinator took
  ownership after bounded repairs (`fallback-failure`). Independent auditor
  verified actual outputs with coordinator checks; its own experimental audit
  normalization had false positives and is not presented as passing evidence.
  No temporary Python tooling was added to repository/product surfaces.
- Git: scoped tracked destination changes are staged; mixed consumer edits
  remain unstaged. This docs-only request did not request commit, push or sync.

## Creation-Date Correction / Closeout

- Extension order: first
  [EXT_3OC6OZ3G](SOW_20261008_VO3LKN0L_EXT_3OC6OZ3G_creation_date_provenance.md),
  explicitly approved by user on 2026-10-08. Read it with this base; its
  creation-date/provenance locks supersede conflicting parent date-basis notes.
  The repo-local FS fallback and one parser incoming-link repair are authorized.

- The user rejected using migration-day IDs: SOW/Plan date segments must match
  the corresponding original create_dttm. This supersedes the prior date basis.
- Completed all 108 creation-date decisions and 123 record renames. Discovery
  found 21 full original datetimes, 3 original dates (one SOW and two Plans),
  and 84 eligible original-file birthtimes (80 SOWs and four Plans).
  Date-only records retain unknown clock time. FS records explicitly carry
  filesystem_proxy confidence; they do not prove historical logical creation.
- Canonical correction: [correction-map.json](correction-map.json).
  Source/provenance: [creation-date-evidence.json](creation-date-evidence.json).
  Frozen metadata: [filesystem-date-evidence.json](filesystem-date-evidence.json).
  Final checks/hashes: [correction-verification-evidence.json](correction-verification-evidence.json).
- Trial and live checks passed: 127 exact payloads, 123 historical bodies,
  108 dates and unchanged RANDOM8 values, 33 Plan ownerships, 53 links and
  zero new broken links. Thirteen targeted negative checks passed, including
  verified pre-migration mtime fallback; no live record needed that fallback.
- Package tests: 47 passed. Both staged and unstaged whitespace checks passed.
  Tracking remains 118 tracked / 5 untracked outputs; unrelated index entries
  and nine protected dirty/untracked files are unchanged. Mixed consumers
  remain unstaged, with their original user hunks preserved.
- A transient Git lock interrupted after 104 renames. The lock disappeared
  naturally; exact source hashes and index entries were checked before resuming
  the remaining 19 moves. No foreign lock was removed or broad rollback used.
- Delegation: one fresh GLM-5.3-max discovery completed 54 records; the second
  discovery stayed unresolved after the bounded wait and was interrupted.
  Coordinator completed that slice; it is not counted as an independent review.
  A separate fresh GLM-5.3-max final audit exercised live/trial and negative
  checks, parent prefixes, own dates and stale-ID coverage: no actionable findings.
- Gap check: substantive contracts, lifecycle history, duplicate SOW_0056,
  decision/EXT ownership and separate child/Plan dates remain intact. The two
  pre-existing broken-link occurrences remain baseline exceptions explicitly
  allowed by this migration; FS proxy limitations are accepted by approved EXT.
- Closeout: parent and EXT completed together; whole bundle moved to finished.
  The EXT-authorized single incoming link in the completed parser SOW now
  targets this finished bundle; no parser implementation contract changed.
  No commit, push or installed-skill sync was requested or performed.

## Out Of Scope

- Migration before explicit approval; another project or Git-history rewrite.
- Skill evolution, sync, AGENTS/TEMPLATE changes, runtime/code/test-fixture edits,
  new migration CLI/service, dependency or persistent allocator.
- Recreating old implementations, revalidating old product acceptance, changing
  approval authority, hiding evidence or scrubbing private history under this task.
- Rewriting completed new-format SOW bundles; unrelated docs and decisions.
- Push or global Codex/Claude synchronization without a separate request.

## Cautions / Risks

- Mapping is proposed, not execution approval. Exact IDs are reserved by this
  draft; collision or source drift must be resolved before implementation.
- Existing ownership can differ from loose references; frozen map review is the
  gate, not numerical proximity. Historical lifecycle gaps remain explicit.
- Dirty/untracked MCP/privacy/Claude-router drafts must retain user-authored
  content. Migration does not authorize publishing their private material.
- Git cannot track locally while excluding those commits from push. Preserve
  existing tracking boundaries and do not introduce a local-only push illusion.
