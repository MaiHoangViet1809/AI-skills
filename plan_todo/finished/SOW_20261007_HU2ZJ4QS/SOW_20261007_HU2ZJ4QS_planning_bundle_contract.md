# SOW_20261007_HU2ZJ4QS - Planning Bundle Contract

- Status: DONE
- Approval: APPROVED by user
- Proposed-By: Codex
- create_dttm: 2026-10-07T19:26:15+07:00
- approve_dttm: 2026-10-08T10:49:18+07:00
- finish_dttm: 2026-10-08T11:13:44+07:00
- Plan / Reference: Standalone; user-selected local bundle approach A.

## Task

Update packaged planning concepts/contracts and consuming skills to use stable date/random IDs,
standalone SOW folders, optional Plan bundles, separate extensions, and
scope-owned decision files.

## Why / Baseline

Current SOW indexing scans for the next four-digit number; concurrent checkouts
can choose the same number. Extensions may remain inline, Plan/SOW files are
scattered, and decisions are recorded separately from their owning scope.

Inspection confirmed the numbering and extension rules in
`skills/task-router-flow/references/scope-of-work.md`, file-level finished moves
in execution/delegate skills, and optional Plan semantics in `references/plan.md`.
The user selected local bundles, then specified date/random IDs and filenames.

Follow AGENTS.md: DRY/SOLID/KISS, approved scope before behavior-bearing edits,
preserve concurrent dirty work, and retain explicit approval and verification.
No project principle document or declared concept authority was found.

## Location

- `skills/task-router-flow/SKILL.md`.
- `skills/task-router-flow/references/scope-of-work.md`, `plan.md`.
- `skills/task-router-flow/references/planning-bundles.md` (new): canonical
  packaged concept for identity, relationships, placement and bundle lifecycle.
- `skills/task-execution-flow/SKILL.md`.
- `skills/sow-delegate-flow/SKILL.md`.
- `skills/task-review-investigate-compare/SKILL.md`.
- `skills/registry.json`: declare the new packaged reference for installation.
- Existing affected fixture files in `tests/skill_feedback_cases/` and
  `tests/test_plan_contract_integration.py`; required focused contract test:
  `tests/test_planning_bundle_contract.py`.
- This SOW bundle, including its decision file if a new material decision arises.

## As-Is Diagram (ASCII)

```text
plan_todo/
  PLAN_name.md
  SOW_0093_name.md
  shared_decisions.md
  finished/
    SOW_0096_name.md
    SOW_0096_EXT_01_name.md
```

## To-Be Diagram (ASCII)

```text
plan_todo/
  active/
    SOW_20261007_HU2ZJ4QS/
      SOW_20261007_HU2ZJ4QS_planning_bundle_contract.md
      SOW_20261007_HU2ZJ4QS_decision.md             # only if needed
      SOW_20261007_HU2ZJ4QS_EXT_6P8D3V9B_name.md   # only if needed
    PLAN_20261007_4T9W2N6C/
      PLAN_20261007_4T9W2N6C_name.md
      PLAN_20261007_4T9W2N6C_decision.md           # shared decisions
      SOW_20261007_8A3R5M7D/
        SOW_20261007_8A3R5M7D_name.md
  finished/
    <completed standalone SOW or whole Plan bundle>
```

## Deliverables / Behavior Locks

1. ID format: `SOW_YYYYMMDD_RANDOM8`; Plan uses
   `PLAN_YYYYMMDD_RANDOM8`. RANDOM8 contains exactly eight independently random
   uppercase ASCII letters or digits (`A-Z`, `0-9`). Use project-declared
   timezone, otherwise the user's current timezone. ID is assigned once and
   remains unchanged through rename, move, edit or reopen; it is not a content
   hash. Full lifecycle datetimes remain timezone-aware with seconds.
2. Check IDs throughout the project's planning area, including nested Plan
   bundles, namespaces and finished work, before creation; regenerate on collision.
   Random IDs remove the shared counter, not all collision or concurrent-write
   risk. A duplicate ID introduced by branch integration must be resolved before
   accepting new work. Do not add a persistent allocator or external service.
   For duplicate independent records, assign a new ID to the incoming draft and
   repair its references; never silently rename an approved identity.
3. Folder name is only the full ID. Base filename is `<SOW_ID>_<task_name>.md`.
   Standalone SOW folders are direct children of `active/`; only Plan-backed
   SOWs are children of a Plan folder. Plan filenames use the analogous format.
   Preserve repo-declared planning roots and namespaces; these examples define
   the default layout, not a reason to override another project's authority.
4. Plan remains optional under existing router rules. Creating a SOW folder
   does not require a Plan. When an existing SOW gains a parent Plan, move its
   whole folder into that bundle, retain its ID, and repair references.
   Direct adoption applies to active SOWs using the new format. A finished SOW
   needed only as prior evidence is linked, not moved or reopened. If it gains
   new owned work and already uses the new format, explicitly reopen and adopt
   it in the same authorized action. Legacy records remain linked unless a
   separate migration SOW explicitly approves their conversion and movement.
5. Every new extension is a separate `<SOW_ID>_EXT_<RANDOM8>_<name>.md` file in
   its parent SOW folder. Each has its own lifecycle/approval, parent reference,
   scope delta, deliverables and acceptance. Record extension order/dependencies
   in the parent; never use an independently allocated sequential filename.
   Check extension IDs within the parent before creation. DRAFT extensions do
   not amend approved scope; consumers read the base plus applicable approved
   extensions in recorded order, stopping on unresolved overlapping scope.
   Preserve the existing maximum of three approved extensions and replacement
   SOW routing. Do not copy the complete base contract into each extension.
6. Decisions specific to one SOW live in `<SOW_ID>_decision.md`; Plan-wide
   decisions live in `<PLAN_ID>_decision.md`. Create only when needed, use dated
   entries with context/options/chosen approach/tradeoffs, and link rather than
   duplicate a shared decision. Existing project-level authority stays canonical.
7. Standalone completion moves the whole SOW folder to `finished/`. A completed
   SOW inside an active Plan stays in place with completed status; only aggregate
   verified Plan completion moves the entire Plan bundle to `finished/`.
   Reopen moves the owning finished bundle back to `active/` when needed,
   clears only reopened completion timestamps, preserves historical evidence,
   and repairs references. Status/location alone never grants approval.
   Authorized new work in a completed child SOW reopens that SOW and its
   completed owning Plan; authorized new/reopened EXT work reopens its parent
   SOW and completed owning Plan. Clear only those ancestors' and the reopened
   scope's finish timestamps and update active statuses. If the Plan is finished,
   move the whole Plan bundle back to active; if already active, leave its
   location unchanged. Preserve all
   completed sibling SOW/EXT timestamps and approval history. A new draft EXT
   does not reopen approved lifecycle until its scope is explicitly authorized.
8. One default bundle concept owner: router's `references/planning-bundles.md`.
   Plan/SOW templates refer to it; consumers follow the resolved
   project/default contract and replace contradictory numbering/file-move
   wording. Preserve existing routing exemptions, approval gates, model
   delegation, optional tracking fields, and verification requirements.
9. Apply the layout prospectively. Existing flat/numbered records and inline
   approved extensions remain governed by their recorded contracts; follow-up
   work must not silently relocate or re-ID them. If a legacy record needs
   conversion to use a new bundle, require a separately approved migration SOW.
   No Plan/SOW/decision authority is added to the target project's concepts by
   merely installing the packaged skill reference.

## Done Criteria

- Naming examples and instructions agree across affected packaged concept,
  templates and skill files.
- Required `tests/test_planning_bundle_contract.py` checks cover valid and invalid IDs, duplicate IDs,
  standalone placement, optional Plan adoption, separate EXT approval, decision
  ownership, partial Plan completion, aggregate move, and reopen references.
  Include negative/boundary cases for draft EXT without approval, preserved
  sibling timestamps, finished evidence-only links, legacy adoption rejection,
  and target-project authority overriding default placement.
- Structural validators and affected tests pass; `git diff --check` passes.
- Inspect rendered/text examples and local temporary directory scenarios for
  create, move and reopen semantics; label static checks separately from live
  agent adherence. No global installation is required to close this SOW.
- Verify registry packaging includes the reference and consumers can resolve it
  from the installed router package without a hardcoded sibling path.
- Verify target-project placement/authority wins over the default contract;
  do not auto-edit AGENTS.md or concept indexes in consuming projects.
- Preserve unrelated dirty changes; verify
  scoped diff and record evidence before commit and bundle closeout.

## Out Of Scope

- Implementation before explicit SOW approval.
- Bulk migration, renaming or rewriting historical Plan/SOW/EXT/decision files.
- Any migration of existing planning records requires a new approved migration
  SOW with exact moves, reference repairs and verification. Only this newly
  created SOW bundle may move for its own closeout in the current scope.
- Editing `AGENTS.md`, `TEMPLATE_AGENTS.md`, existing project concept indexes,
  or adopting this default into other projects. If current project policy
  conflicts with bundle closeout, report the conflict and obtain a scoped
  policy amendment before moving; do not bypass repository authority.
- External task registration service, new CLI/generator, dependency or persistent
  runtime, global Codex/Claude sync, or Git push without a separate request.
- Changes to Redmine contracts/IDs, provider config, SOW exemptions, approval
  authority, extension limit, or mandatory delegation behavior.

## Cautions / Risks

- Several target contracts already contain concurrent uncommitted work; preserve
  those hunks and inspect ownership before staging.
- Date grouping helps navigation but cannot establish execution order; use
  explicit dependencies and lifecycle fields.
- Random IDs do not prevent overlapping approved write scopes; retain bounded
  ownership and reconcile conflicting extensions before execution.
- Historical records keep their original identities. New-record rules apply
  prospectively; old records remain references, without adding runtime aliases
  or silently granting migration scope.

## Verification / Closeout

- Implemented: canonical packaged bundle reference, router/SOW/Plan defaults,
  execution/delegate/review consumers, registry entry and focused tests.
- `uv run --no-sync --offline python -m unittest discover -s tests`: 47 tests
  PASS in the working tree and isolated task-only commit payload. Four affected
  skills passed the skill-creator structural validator; `git diff --check` PASS.
- Packaging: temporary installed copies include the canonical reference;
  local links resolve inside the router package. Consumer discovery uses the
  supplied harness catalog rather than an assumed sibling install path.
- Simulated: temporary directory create/adopt/aggregate-move/reopen scenarios,
  calendar/duplicate examples and negative legacy/draft-EXT cases. These are
  structural examples, not a runtime planning engine or live host proof.
- Independent model-based forward-check: six hypothetical requests through
  GLM-5.3-max native role, isolated with `fork_turns: none`; no nested delegation.
  It found draft-EXT parent lifecycle ambiguity, repaired in router instructions.
  Exact role/effort come from coordinator launch metadata, not child self-report.
- Gap check: contract, consumers, approval boundaries, partial completion,
  reference packaging and sibling preservation inspected. No blocking gap
  remains. Async/performance/dispose/logging runtime checks are not applicable
  to this documentation/test-only change.
- Not verified: production Codex/Claude agent adherence; global sync was not
  authorized or performed. Historical migration and policy edits were not done.
- Git handling: isolate task hunks from pre-existing Redmine changes before
  scoped commit; preserve unrelated working/index state. No push.
