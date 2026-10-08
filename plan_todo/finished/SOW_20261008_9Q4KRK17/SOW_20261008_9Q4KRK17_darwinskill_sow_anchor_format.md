# SOW_20261008_9Q4KRK17 - DarwinSkill SOW Anchor Format

- Status: DONE
- Approval: User explicitly requested two reviews, patching, then implementation in this task.
- Proposed-By: Codex
- create_dttm: 2026-10-08T11:42:57+07:00
- approve_dttm: 2026-10-08T11:49:39+07:00
- finish_dttm: 2026-10-08T11:53:50+07:00
- Plan / Reference: Standalone maintenance before
  [planning migration](../../active/SOW_20261008_VO3LKN0L/SOW_20261008_VO3LKN0L_migrate_legacy_planning_bundles.md),
  per the user's selected order. No new parent Plan.

## Task

Update DarwinSkill's SOW anchor extraction for date/random IDs while preserving
legacy transcript recognition and work-unit/example semantics.

## Why / Baseline

`darwinSkill/src/extraction.py:16` recognizes only `SOW_0000`-style anchors.
A direct import probe returns `['SOW_0058']` for a legacy ID and `[]` for
`SOW_20261008_VO3LKN0L`. Its callers are work-unit segmentation, trainable-example
building, the separate extraction script and mini-project tests.

Current `skill-evolution-flow` uses sanitized fixtures, canonical edits,
validation and optional sync; it does not call DarwinSkill. This is independent
mini-project compatibility maintenance, not a demonstrated production workflow
regression or an integration of DarwinSkill into skill evolution.

Follow AGENTS.md and DRY/SOLID/KISS. No declared project principle/concept
authority was found. Preserve current APIs and unrelated dirty work.

## Location

- `darwinSkill/src/extraction.py`: existing SOW recognition path only.
- `darwinSkill/tests/test_extraction.py`: focused regression scenarios.
- This SOW bundle and linked migration SOW: sequencing/evidence only.

## As-Is Diagram (ASCII)

```text
canonical session -> legacy-only SOW matcher
                  -> work units -> examples
new ID            -> no scope anchor
```

## To-Be Diagram (ASCII)

```text
canonical session -> legacy + date/random SOW matcher
                  -> full base scope anchor -> work units -> examples
```

## Deliverables / Behavior Locks

- Recognize `SOW_YYYYMMDD_RANDOM8` with exactly eight uppercase ASCII letters
  or digits, and retain `SOW_NNNN` recognition for historical transcript inputs.
  This explicitly approved historical-input support is not a new alias layer.
- Preserve the entire new base ID, not its year/prefix; distinguish different
  random IDs on the same date. Do not recognize malformed lengths/case or partial
  numeric prefixes as valid anchors. This is text recognition, not an ID allocator
  or calendar-validation service.
- Recognize a base anchor inside its contract filename/path or EXT filename;
  an EXT stays associated with its parent SOW, not a second fabricated scope.
  Recognition reads existing user/assistant message text only; never scan
  transcript_path or artifact_refs metadata. Both legacy and new filename
  suffixes are allowed after `_`; return only the parent base ID. Thus
  `SOW_0058_EXT_01_fix.md` returns `SOW_0058`, and
  `SOW_20261008_ABCDEF12_EXT_12345678_fix.md` returns
  `SOW_20261008_ABCDEF12`. Alphanumeric characters directly after an ID are
  rejected. A four-digit legacy ID followed by `_name` remains a legacy
  filename, not a malformed new ID.
- Keep continuation merging, mixed-context abstention, result types and public
  APIs unchanged. Do not rewrite legacy fixtures into new IDs; add new cases.
- Verify both segmentation and example generation using short in-memory
  ProviderSession fixtures; do not read private historical transcripts or call LLMs.

## Done Criteria

- Positive: legacy/new IDs, new-ID continuation, filenames/EXT and full-ID
  preservation. Negative: malformed IDs, false prefix matches, no SOW present.
- Boundary: two new IDs on the same date and mixed legacy/new scopes remain
  distinct and trigger existing mixed-context behavior.
- Focused extraction tests and `uv run --no-sync --offline python -m unittest
  discover -s darwinSkill/tests` pass, plus root planning/package tests.
- `git diff --check`, code-path/gap review and exact caller inventory pass;
  record observed segmentation/example results, not syntax-only evidence.
- Scoped verified commit handling follows repo policy; record no push/sync.

## Review Resolution

Two independent reviews (GLM-5.3-max and Luna-max) completed before edits.
Resolved path-source ambiguity by retaining message-only scanning; locked
legacy/new EXT parent output and filename boundaries. Add negative cases for
date-only IDs, seven/nine-character or lowercase random suffixes, embedded
prefixes, attached alphanumeric characters, and metadata-only references.
Verify full-ID propagation through example generation and mixed-context
abstention, not only regex matching.

## Out Of Scope

- Implementation before explicit SOW approval; planning file migration.
- Integrating DarwinSkill with `skill-evolution-flow`, new APIs/helpers/CLI,
  dependencies, providers, telemetry or training runs.
- Runtime behavior outside SOW recognition; global sync and Git push.

## Cautions / Risks

- Regex boundaries can truncate IDs or miss underscore-suffixed filenames;
  test the actual consumer path, not only a matcher expression.
- No operational-use history was audited; absence of a skill call does not prove
  the mini-project has never been manually run or exercised in development.

## Verification / Closeout

- Implemented: one matcher change, six added regression tests; existing legacy
  fixtures retained. No API, provider or skill-evolution integration change.
- Scenario evidence: in-memory sessions execute segmentation and example
  generation. New ID stays intact through scope_anchor, task_family and
  skill_name; continuation merges; filename/EXT returns parent; duplicate
  parent/EXT stays one scope; different same-date IDs remain distinct;
  mixed new/new and new/legacy examples abstain with mixed_context.
- Negative evidence: malformed/embedded/attached IDs yield empty anchors;
  metadata-only paths remain ignored; punctuation and filename suffixes work.
- Checks (2026-10-08): `uv run --no-sync --offline python -m unittest
  darwinSkill.tests.test_extraction`: 13 passed; `uv run --no-sync --offline
  python -m unittest discover -s darwinSkill/tests`: 76 passed;
  `uv run --no-sync --offline python -m unittest discover -s tests`: 47 passed;
  `git diff --check`: passed.
- Caller inventory: matcher -> _distinct_scope_anchors ->
  segment_session_into_work_units -> build_trainable_examples;
  darwinSkill/scripts/extract_skill_examples.py calls the example API.
- Gap pass: reviewed boundaries, full-ID propagation, historical fixtures,
  continuation, duplicate anchors and mixed-context safety. No actionable
  findings remain in approved scope. No UI/backend boundary applies.
- Not verified/out of scope: private historical transcripts, live provider
  runs and operational adoption; this is local pipeline proof, not proof of
  DarwinSkill integration with skill-evolution-flow.
- Scoped code/SOW commit follows verification. No push or global sync.
  Migration remains a separate approved task and has not started here.
