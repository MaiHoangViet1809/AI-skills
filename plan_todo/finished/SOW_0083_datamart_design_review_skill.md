# SOW_0083 - Datamart Design Review Skill

## Lifecycle

- Status: done
- Approval: approved by user
- create_dttm: `2026-09-15T01:00:37+07:00`
- approve_dttm: `2026-09-15T01:07:59+07:00`
- finish_dttm: `2026-09-15T01:12:03+07:00`

## Task

Create an AISkills-owned `datamart-design-review` skill that grounds datamart
changes in source/runtime evidence and reports every affected table and column
through one merged impact matrix.

## Location

- `skills/datamart-design-review/SKILL.md` (new)
- `skills/datamart-design-review/agents/openai.yaml` (new)
- `skills/datamart-design-review/references/impact-matrix.md` (new)
- `skills/registry.json`
- `skills/INDEX.md`
- `tests/skill_feedback_cases/datamart-design-review.json` (new)
- `plan_todo/skill_design_decisions.md`
- this SOW, later
  `plan_todo/finished/SOW_0083_datamart_design_review_skill.md`
- exact post-commit deployment targets explicitly approved by the user:
  `~/.codex/skills/datamart-design-review/`
  and `~/.claude/skills/datamart-design-review/`

## Why

Datamart discussions currently produce useful design conclusions but do not
consistently expose the full migration impact. Reviewers need one traceable view
that answers, for every table and changed column: whether it is new, updated or
dropped; how its grain and formula change; why the change exists; which
consumers are affected; and whether the claim is proven or proposed.

No existing AISkills-owned skill specializes in semantic-model or datamart
design. Adding this contract to the generic task-review skill would broaden its
trigger and burden unrelated reviews. Plugin-owned Data Analytics skills are not
AISkills source and are not editable through this evolution flow.

The skill-evolution ownership gate therefore does not authorize an update to an
existing skill: there is no registered canonical target to patch. This SOW uses
the feedback normalization and regression discipline from skill evolution, then
routes the approved implementation to `skill-creator` as a new canonical skill.

## Feedback Contract

- Target skill: new `datamart-design-review`
- Trigger: design, review or impact analysis for a datamart, warehouse serving
  table, semantic dataset or materialized analytical model
- Observed behavior: table-level design and column-level formulas are reported
  separately or incompletely, making migration impact hard to trace
- Expected behavior: inspect the present contract, distinguish observed source
  grain from proposed output grain, and return one merged table/column impact
  matrix with exact formulas, reasons, consumers and evidence status
- Reusable invariant: every material datamart change is traceable from table
  lifecycle through column semantics to downstream impact and verification
- Cause class: missing specialized procedure
- Evidence reference:
  `sanitized:user-feedback-datamart-impact-matrix-2026-09-15`

## Authority And Principles

Read `AGENTS.md`, `skills/registry.json`, `skills/INDEX.md`,
`skills/task-review-investigate-compare/SKILL.md` and the skill-creator
instructions before implementation. No root principle-design file or declared
concept authority exists in AISkills.

Apply DRY, SOLID and KISS: add one specialized skill and one conditional
reference rather than duplicating this domain contract across generic review,
execution and Data Analytics skills.

## As-Is Diagram (ASCII)

```text
source SQL/profile -> design prose
                         |-> table changes
                         `-> column formulas elsewhere

reviewer manually reconstructs grain, migration and consumer impact
```

## To-Be Diagram (ASCII)

```text
runtime/source evidence + current SQL + consumer inventory
                         |
                         v
              datamart-design-review
                         |
                         v
 one impact matrix: table -> grain -> column -> formula -> reason -> impact
                         |
                         v
              proposal / SOW / implementation review
```

## Deliverables And Behavior Locks

1. Create a narrowly triggered skill for datamart and analytical serving-model
   work. It must not trigger for generic SQL syntax debugging, chart styling,
   operational database schemas or dashboard-only layout changes.
2. Require the reviewer to inspect current table SQL/schema, upstream sources,
   downstream consumers and applicable project authority before proposing a
   target contract.
3. When a claim depends on a deployed source, require exact runtime evidence or
   mark it `UNVERIFIED`. Repository SQL and similarly named environments are not
   production grain proof.
4. Distinguish three concepts explicitly:
   - observed source grain or candidate-key evidence;
   - proposed datamart output grain;
   - business grain approved by the owning domain.
   A unique sample or snapshot must not be promoted into a timeless business
   contract.
5. Use exactly one table for a datamart impact report unless the user explicitly
   requests supplemental tables. That table is the merged impact matrix. Repeat
   table context on its affected column rows rather than splitting table and
   column changes into separate tables; keep blockers and recommendations in
   short prose outside it.
6. The compact default matrix columns are:

   | Field | Contract |
   | --- | --- |
   | `Layer / Table` | Exact target relation; no friendly alias replacing its name |
   | `Table action` | `NEW`, `UPDATE`, `DROP`, or `KEEP` when required for context |
   | `Grain / refresh before -> after` | Exact grain plus materialization, partition or refresh transition when affected; `N/A` where genuinely unavailable |
   | `Column` | Exact physical column; `*` only for a whole-table drop or table-only action |
   | `Column action / type before -> after` | `NEW`, `UPDATE`, `DROP`, or material `KEEP`, plus physical type transition when known |
   | `Formula / semantics before -> after` | SQL-like expression or precise business rule; preserve original source names |
   | `Reason` | Business or technical reason tied to the row |
   | `Downstream / migration impact` | Affected datasets, measures or reports plus backfill and cutover consequences |
   | `Evidence status` | `VERIFIED`, `PROPOSED`, or `UNVERIFIED`, with the compact evidence identity or reference |

7. List every physical column of a new table and every new, changed or dropped
   column of an updated table. Do not enumerate untouched columns unless they
   are keys, grain columns or compatibility contracts whose unchanged semantics
   are material to the review.
8. Represent a newly created table with one row per physical column. Represent
   a whole-table drop with `Column = *`. Express a rename as the old physical
   name `DROP` plus the new physical name `NEW`, linked in formula/semantics;
   do not hide it inside a generic update. State explicitly when there are no
   table or column drops; do not make the reader infer that omission means none.
9. For aggregate columns, state the population, grouping and null behavior in
   addition to the aggregate function. For ranks, windows, ratios, snapshots
   and lifetime values, state partition/order/denominator/as-of semantics.
10. Preserve source names and semantic lineage. A compatibility alias must be
    labelled as such and must name its canonical source formula.
11. Identify additive, semi-additive and non-additive risks when they affect
    correctness. Do not propose summing daily snapshots, ranks, ratios or
    different measure definitions without an explicit contract.
12. Keep facts separate when authorities, units, temporal meaning or allocation
    rules differ. Joining them into one wide mart requires verified cardinality
    and an approved allocation rule.
13. End with a short conclusion containing only blockers, open decisions and
    the recommended implementation order. Do not duplicate the impact matrix in
    prose.
14. Apply repository SOW and approval gates before mutation. The skill reports
    and reviews; it does not grant permission to change schemas, data or
    production runtimes.
15. Keep automatic discovery enabled. The UI metadata must use display name
    `Datamart Design Review`, describe grain/formula/migration impact, and use a
    concise default prompt that explicitly invokes `$datamart-design-review`.

## Regression Scenarios

| Kind | Scenario | Required behavior |
| --- | --- | --- |
| Expected | User asks how a profiled source should change existing and new serving models; the proposal changes a type/formula, creates a table, retires another and preserves one compatibility key | Inspect exact evidence and current consumers; distinguish observed, proposed and business-approved grains; return exactly one table containing the merged impact matrix for every affected table and required physical column, including type, formula, migration and evidence status |
| Negative | User asks why one Superset chart has the wrong colour and title | Do not invoke datamart design procedure or demand a schema impact matrix |
| Boundary | User asks to optimize a long virtual-dataset SQL and it is unclear whether logic belongs in Gold | First determine whether the issue is query-local or a reusable semantic-model change; use the matrix only if a datamart contract is actually proposed |

## Execution Order

1. Preserve the existing unrelated worktree changes and confirm SOW_0083 is
   approved before behavior-bearing edits.
2. Add regression fixture `datamart-impact-matrix-001` before creating the
   canonical skill.
3. Create the skill with `skill-creator`, keeping the entrypoint concise and the
   detailed matrix contract in its conditional reference.
4. Add UI metadata with explicit implicit-invocation policy, then register the
   exact canonical files in `registry.json` and `INDEX.md`.
5. Record the new-skill boundary and reporting contract in
   `plan_todo/skill_design_decisions.md`.
6. Run structural and deterministic regression checks, inspect the scoped diff,
   and run isolated forward-tests when available.
7. Commit only SOW_0083-owned files. Dry-run and execute one-skill sync commands
   separately for Codex legacy-user and Claude user targets, then verify exact-copy
   parity for each target. The explicit two-target user request supersedes the
   evolution flow's normal one-environment default for this task only.

## Done Criteria

- Canonical `datamart-design-review` source, focused reference and UI metadata
  are present and registered.
- Regression case `datamart-impact-matrix-001` includes one sanitized expected,
  negative and boundary scenario.
- The impact-matrix reference includes a compact template and one sanitized
  example demonstrating table and column `NEW`, `UPDATE`, `DROP`, a physical
  type change, formula change, compatibility key, migration impact and evidence
  status without embedding company-specific identifiers or values.
- `SKILL.md` routes to the reference only when a detailed change matrix is
  needed; ordinary concise datamart questions remain concise.
- The skill frontmatter discriminates datamart/semantic serving-model work from
  generic SQL and dashboard presentation. `agents/openai.yaml` explicitly keeps
  implicit invocation enabled and its default prompt names
  `$datamart-design-review`.
- The skill passes the available skill-creator structural validator.
- `uv run python -m unittest tests.test_skill_feedback_cases tests.test_skill_sync_scripts`
  passes.
- A clean isolated forward-test checks the three regression scenarios when
  available; otherwise behavioral validation is reported as incomplete.
- `git diff --check` passes and the task-owned diff excludes the existing
  unrelated `task-router-flow`, fixture and SOW_0082 changes.
- Commit includes only approved SOW_0083 files and hunks; no push occurs.
- Preview and execute exact one-skill sync for Codex legacy-user and Claude user
  targets separately; verify canonical-to-installed parity for both.

## Out-of-Scope

- Changing any plugin-owned Data Analytics skill.
- Modifying `task-review-investigate-compare` or broad task routing behavior.
- Treating the new skill as a canonical update authorized by the evolution
  ownership gate before it is created and registered.
- Creating a SQL parser, lineage engine, profiler or schema migration tool.
- Prescribing one universal medallion architecture, number of layers, naming
  convention or physical grain for every project.
- Mutating a warehouse, running backfills or deploying datamarts.
- Syncing any skill other than `datamart-design-review`, or any environment other
  than the explicitly approved Codex and Claude user targets.
- Pushing commits or publishing the skill.

## Proposed-By

Codex, from explicit user feedback on 2026-09-15.

## Plan / Reference

- `$skill-evolution-flow`
- `$skill-creator`
- The finalized-revenue table/column impact matrix supplied in the originating
  conversation as the reporting baseline.

## Cautions / Risks

- An over-wide matrix can become unreadable. Keep the core nine columns and put
  detailed evidence in existing findings or SOW references rather than adding
  more default columns.
- A matrix can look precise while being assumption-driven. Evidence status and
  the source/business/proposed grain distinction are mandatory.
- Listing only changed columns can hide a broken key. Material grain, identity,
  partition and compatibility columns must remain visible even when retained.
- Automatic triggering must remain narrow so generic SQL and visualization work
  is not routed into an architecture review.
- The AISkills worktree already contains unrelated edits. Preserve them and use
  scoped staging after approval.

## Review Summary

Two review passes completed. The effective contract now covers physical type
and refresh changes, separates downstream impact from evidence, requires every
new-table column, records rename/drop behavior, strengthens the regression case,
and routes new-skill creation correctly through `skill-creator`. No remaining
actionable SOW finding; implementation is explicitly approved.

## Verification

- Skill-creator structural validator: passed.
- Feedback and sync regression tests: 12 passed.
- Registry and feedback JSON parsing: passed; `git diff --check`: passed.
- Regression fixture: `datamart-impact-matrix-001` contains expected, negative
  and boundary scenarios.
- Manual gap review covered contract completeness, edge cases, trigger safety,
  packaging, overwrite scope and installed cleanup boundaries; no actionable
  gap remained.
- Canonical implementation commit: `2d07cbf`.
- Codex legacy-user dry-run, one-skill sync and exact-copy parity: passed at
  `~/.codex/skills/datamart-design-review/`.
- Claude user dry-run, one-skill sync and exact-copy parity: passed at
  `~/.claude/skills/datamart-design-review/`.
- Independent model forward-test: not run because sub-agents are unavailable in
  this side conversation. Structural and parity checks do not prove future model
  selection or response quality; the sanitized regression fixture is retained
  for a later isolated evaluation.
