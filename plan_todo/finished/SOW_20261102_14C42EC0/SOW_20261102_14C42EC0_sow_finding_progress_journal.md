# SOW_20261102_14C42EC0 — SOW-scoped finding/progress journal

- **Status**: DONE
- **Approval**: approved by user
- **create_dttm**: 2026-11-02T15:11:41+07:00
- **approve_dttm**: 2026-11-02T15:20:12+07:00
- **finish_dttm**: 2026-11-02T15:22:55+07:00
- **Task**: Define one append-only finding/progress journal per iterative SOW and update the canonical routing/review skills to distinguish ordinary findings from research-only probe records.
- **Location**:
  - `skills/task-router-flow/SKILL.md`
  - `skills/task-router-flow/references/scope-of-work.md`
  - `skills/task-router-flow/references/planning-bundles.md`
  - `skills/task-review-investigate-compare/SKILL.md`
  - `tests/skill_feedback_cases/task-router-flow.json`
  - `tests/skill_feedback_cases/task-review-investigate-compare.json`
- **Why**: The current SOW Progress table is a current-state/HITL summary, while iterative findings are written back into SOW/EXT narrative. This makes the running history harder to scan and encourages repeated planning-artifact edits for routine progress.
- **Proposed-By**: Codex
- **Plan**: None; standalone SOW.

## As-Is Diagram (ASCII)

```text
probe / finding -> edit SOW or add EXT repeatedly -> history and current contract mix
```

## To-Be Diagram (ASCII)

```text
meaningful event -> append per-SOW JSONL -> concise SOW Progress snapshot at milestone/HITL
scope or acceptance change ----------------> EXT/new SOW + explicit approval
```

## Proposed Contract

1. **One journal per SOW bundle.** Use
   `plan_todo/{active,finished}/<SOW_ID>/<SOW_ID>_finding_progress.jsonl`.
   Use it for iterative investigation or meaningful repeated findings/progress,
   not for a simple one-step task. Create it on the first meaningful event; do
   not create empty files or a project-global journal. A log moves with its
   owning bundle. Events owned by an EXT use that EXT ID in `scope_ref`; a Plan
   links to child-SOW journals rather than copying their entries.
2. **Append meaningful events, not tool-call telemetry.** Do not log every
   tool call, repeated review pass, or no-finding review; append only a new
   material finding, progress transition, blocker, or research probe. Each
   JSONL line is
   one valid JSON object with `schema_version`, a `record_id` unique within the
   SOW journal, `timestamp` (ISO-8601 with offset in the project's declared
   timezone, or user's timezone if none is declared), `scope_ref`, `kind`,
   `summary`, `evidence_refs`, and `next_step`. `evidence_refs` may be an empty
   array when no artifact exists yet; `next_step` may be `null` when the item
   has no remaining action. Allowed kinds are `progress`, `finding`,
   `blocker`, and `research_probe`. `supersedes` is optional and points to the
   prior `record_id` when correcting or replacing a conclusion. Append order is
   the event order; do not reorder prior lines. Keep evidence as safe
   repository-relative paths or artifact identifiers; never include
   credentials, secrets, raw environment values, or unredacted logs. The
   append-only rule does not override mandatory secret-removal policy.
3. **Research is task-specific.** `research_probe` is allowed only when the
   SOW's primary Task is explicitly research; it additionally records the
   question, hypothesis, method, result (`confirmed`, `no_go`, or
   `inconclusive`), and measured values when available. In v1 this is a
   research-specific record kind in the same journal, not a second
   `research_log.jsonl` file. Ordinary implementation tasks must not be
   described as research just to use that record kind.

   Example ordinary finding (one JSON object / JSONL line):

   ```json
   {"schema_version":1,"record_id":"<unique-id>","timestamp":"2026-11-02T15:00:00+07:00","scope_ref":"SOW_YYYYMMDD_RANDOM8","kind":"finding","summary":"A request path repeats the same metadata lookup.","evidence_refs":["path/to/sanitized-evidence.md"],"next_step":"Measure the duplicate count."}
   ```

   A `research_probe` record adds `question`, `hypothesis`, `method`, `result`,
   and `measurements`; it is used only for an explicitly research-scoped SOW.
4. **Keep authority boundaries.** The SOW Progress table remains the concise
   current snapshot for handoffs and progress reports. SOW/EXT/decision files
   remain authoritative for scope, approval, formal decisions, and acceptance;
   a JSONL entry never grants or changes approval. Append corrections as new
   records with `supersedes: <record_id>`; do not rewrite old entries during
   normal progress updates.
5. **Do not create an EXT for ordinary findings.** Append in-scope findings and
   progress to the journal, then refresh the SOW snapshot at meaningful
   milestones and HITL handoffs. Material changes to scope, deliverables, or
   acceptance continue through the existing EXT/SOW approval path.
6. **Use one writer.** The SOW coordinator verifies and appends records;
   delegates may return proposed entries but do not write the shared journal.
   Historical SOWs remain untouched; there is no migration in this scope.

## Deliverables

- Update the listed canonical skills/references with the journal trigger,
  ownership, record schema, research-only boundary, summary relationship, and
  scope-change rule.
- Add one sanitized skill-feedback case to each owning skill's existing
  fixture, covering expected, negative, and boundary behavior. The fixture
  filename must continue to match its `target_skill` as required by the test
  harness.
- Preserve the existing Progress/HITL contract and the current user's unrelated
  working-tree changes.

## Done Criteria

- The skill definitions agree on when to create a journal, its bundle path,
  append-only record shape, who writes, and how the SOW snapshot is maintained.
- The two feedback cases verify: ordinary findings do not create an EXT; simple
  one-step tasks do not get empty journals; only research SOWs can emit
  `research_probe`; JSONL cannot alter approval; material scope changes still
  route through EXT/SOW; corrections supersede rather than rewrite records; a
  repeated review with no new finding creates no journal event.
- Every example JSONL record is valid JSON, contains no secrets/raw output, and
  uses only repository-relative or safe artifact references.
- Run the skill-creator structural validator and
  `uv run python -m unittest tests.test_skill_feedback_cases tests.test_skill_sync_scripts`.
- When the host supports isolated skill forward-checks, exercise one ordinary
  iterative task and one research task plus the simple-task/scope-change
  boundaries. Structural checks and scenario review alone must not be reported
  as proof of runtime skill behavior; mark that evidence unverified if no
  forward-check is available.
- Review the final diff and confirm no historical SOW, `skills/registry.json`,
  `agents/openai.yaml`, or non-target skill was changed without a demonstrated
  discovery/contract need.

## Out of Scope

- Editing or migrating SOWs in other projects, including DE-project/Spark SDK.
- Backfilling journals for historical or finished SOWs.
- A separate physical `research_log.jsonl`, global log service, parser,
  dashboard, or automated progress-report generator.
- Changing `skill-evolution-flow` or `task-progress-report`; their current
  ownership remains unchanged unless implementation evidence proves a direct
  dependency and the SOW is explicitly extended.
- Implementing application code or changing SOW/EXT approval semantics.

## Cautions / Risks

- The JSONL history and current SOW snapshot can drift; refresh the snapshot at
  the existing HITL/milestone points and treat the log as history, not authority.
- A malformed line or overly detailed record harms readability; keep entries
  compact and validate examples without adding a logging framework.
- `skills/task-router-flow/SKILL.md` and
  `skills/task-router-flow/references/scope-of-work.md` already have unrelated
  uncommitted changes in the AISkills worktree. Preserve and reconcile those
  changes before implementation; this draft does not authorize rewriting them.

## Progress

- **progress_updated_dttm**: 2026-11-02T15:22:55+07:00

| Item | Status | Evidence / Pending reason | Next action / Owner |
| --- | --- | --- | --- |
| D1: Draft SOW and complete three self-review passes | DONE | Three reviews completed; fixture naming, record lifecycle, and no-finding behavior clarified | None |
| I1: Update canonical skill definitions and feedback cases | DONE | Router/review guidance, journal contract, and both three-scenario feedback cases updated; both skill validators pass, 13 targeted tests pass, and two fenced JSON examples parse. Isolated host forward-check unavailable in this environment; runtime behavior remains unverified. | None |
