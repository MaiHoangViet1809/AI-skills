# Planning Bundles

This is the default contract for planning-record identity, relationships,
placement, decisions and lifecycle. A target project's declared contract wins;
installing this package does not create Plan/SOW/decision authority or concept
authority for that project. Apply this contract prospectively. Existing records
keep their recorded identity and lifecycle; conversion or migration requires a
separate approved migration SOW.

## Identity

- New SOW IDs use `SOW_YYYYMMDD_RANDOM8`; new Plan IDs use
  `PLAN_YYYYMMDD_RANDOM8`.
- `YYYYMMDD` is the creation date in the project-declared timezone, or the
  user's current timezone when the project does not declare one.
- `RANDOM8` is exactly eight independently random uppercase ASCII letters or
  digits (`A-Z`, `0-9`).
- Before creating an ID, check it throughout the project's planning area,
  including nested Plan bundles, namespaces and finished work. Regenerate on
  collision.
- An ID is assigned once and remains unchanged through rename, move, edit and
  reopen. It is not a content hash.
- Random IDs remove the shared counter, not every collision or concurrent-write
  risk. Resolve a duplicate introduced by branch integration before accepting
  new work. If two independent records use the same ID, assign a new ID to the
  incoming draft and repair its references; never silently rename an approved
  identity.
- Do not add a persistent allocator or external ID service.

## Placement

- A standalone SOW folder is only the full SOW ID and is a direct child of the
  resolved active planning root. Only a Plan-backed SOW folder is a child of a
  Plan folder.
- A base SOW filename is `<SOW_ID>_<task_name>.md` inside its SOW folder.
- A Plan folder is only the full Plan ID. Its base filename is
  `<PLAN_ID>_<plan_name>.md`.
- Preserve a target project's declared planning roots and namespaces. The
  default layout below does not override another project's authority:

```text
plan_todo/
  active/
    SOW_YYYYMMDD_RANDOM8/
      SOW_YYYYMMDD_RANDOM8_<task_name>.md
    PLAN_YYYYMMDD_RANDOM8/
      PLAN_YYYYMMDD_RANDOM8_<plan_name>.md
      PLAN_YYYYMMDD_RANDOM8_decision.md
      SOW_YYYYMMDD_RANDOM8/
        SOW_YYYYMMDD_RANDOM8_<task_name>.md
        SOW_YYYYMMDD_RANDOM8_decision.md
  finished/
    <completed standalone SOW or whole Plan bundle>
```

## Plan And SOW Relationships

- Plan remains optional. Creating a SOW does not require a Plan.
- A SOW gains a parent Plan only by direct adoption of an active SOW already
  using this format. Move its whole folder into the Plan bundle, retain its ID,
  and repair references.
- A finished SOW used only as prior evidence stays linked in place; do not move
  or reopen it. If it gains new owned work and already uses this format,
  explicitly reopen and adopt it in the same authorized action.
- Legacy records remain linked under their recorded contract. Do not migrate,
  rename or relocate them without a separately approved migration SOW.

## Extensions

- Every new extension is a separate
  `<SOW_ID>_EXT_<RANDOM8>_<name>.md` file in its parent SOW folder.
- Check extension IDs within that parent before creating one; regenerate on
  collision. Extension RANDOM8 follows the same identity rules.
- Each extension has its own lifecycle fields and approval, a parent reference,
  scope delta, deliverables and acceptance. Never copy the complete base
  contract into an extension.
- Record extension order and dependencies in the parent SOW. Never use an
  independently allocated sequential filename.
- Read the base SOW plus applicable approved extensions in recorded order; stop
  if approved extensions overlap without resolution.
- A DRAFT extension does not amend approved scope and does not reopen its
  parent or owning Plan.
- Keep the hard maximum of three approved extensions. If the next change would
  become extension four, create a replacement SOW that references the prior SOW.

## Decisions

- Decisions specific to one SOW live in `<SOW_ID>_decision.md` inside that SOW
  folder.
- Plan-wide decisions live in `<PLAN_ID>_decision.md` inside the Plan folder.
- Create a decision file only when it is needed. Use dated entries with context,
  options considered, chosen approach, tradeoffs and edge cases/risks.
- Link to a shared decision instead of duplicating it. Existing project-level
  authority remains canonical and is not moved into these files.

## Completion And Reopen

- Standalone completion moves the whole SOW folder to the resolved finished
  planning root and repairs references.
- A completed SOW inside an active Plan stays in place with its completed state.
  Only aggregate verified Plan completion moves the entire Plan bundle to the
  matching finished root and repairs references.
- Reopen only on authorized new or reopened owned work. Move the owning finished
  bundle back to the active root when needed and repair references; if it is
  already active, leave its location unchanged.
- Clear only the reopened scope's and affected ancestors' completion timestamps
  and return their statuses to an active state. Preserve historical evidence,
  approval history and all completed sibling SOW/EXT timestamps.
- Authorized new work in a completed child SOW reopens that SOW and its owning
  Plan. Authorized new or reopened EXT work reopens that EXT, its parent SOW and
  its owning Plan. A DRAFT EXT alone does not reopen them.
- Record new actual finish timestamps only after renewed verified completion.
- Lifecycle datetimes include seconds and numeric timezone offset; future
  events remain `null`. Follow [Scope of Work](scope-of-work.md) for lifecycle
  fields and historical unknown times, not the date-only ID segment.
- Status, location or a lifecycle field alone never grants approval.

## Target Project Authority

- Before using this default, inspect the target project's declared planning
  contract, planning roots, namespaces and concept authority.
- A project may override ID format, placement, extension form, decision
  ownership, completion movement or reopen rules. Its declared authority wins
  for that project.
- Do not auto-edit a target project's `AGENTS.md`, concept indexes or planning
  files merely because this package is installed.
