# Plan Contract

Plan defines the big goal; SOWs define bounded changes. Use the target repo's
declared contract first; this is the default when none is declared.

Identity, relationships, placement, decisions and moves follow
[Planning Bundles](planning-bundles.md) unless the target project declares
another contract. This reference does not authorize historical migration.

## Authoring Contract

- Preserve existing SOW routing: `task-router-flow` applies target-repo
  guardrails to choose new SOW, existing coverage/extension, or no SOW.
  Plan is optional: create one only when the user requests it, or scope is so
  large that completing it reliably in one SOW risks failure or mistakes.
  Multiple files, owners, or dependencies alone do not require a plan.
- Map original goal -> `G#` -> SOW -> evidence. No invented scope or prototype-as-target.
- Read baseline, governing rules, and prior decisions. Preserve strengths;
  justify additions; fix root causes. Style references do not change behavior.
- Use the fewest SOWs by deliverable, owner, and dependency, not edit/test steps.
  Honor the requested breakdown.
- Follow repo paths and its SOW template (default: [Scope of Work](scope-of-work.md)).
  Each SOW defines exact files, deliverables, and done criteria; link `G#` only
  when a parent plan exists.
- When SOW approval is required, execute only approved coverage after dependency
  gates pass. Plan approval,
  `TBD`, status, and timestamps are not implementation authority.
- Material changes need explicit approval. Separate proposed/approved work;
  resolve material unknowns before approving affected work.
- Update sequence/acceptance after each SOW. Keep requirements current; preserve
  history/details in existing docs, not duplicate trackers.

## Template

```md
# PLAN_<YYYYMMDD>_<RANDOM8> - <Title>

- Status: DRAFT
- Approval: PENDING
- Proposed-By: <author>
- create_dttm: <YYYY-MM-DDTHH:mm:ss+HH:MM>
- approve_dttm: null
- finish_dttm: null
- References: <policy, concepts, architecture, decisions>

## 1. Goal
Original request: <problem + consumer + why>
- G1: <observable end result>
- Path (if applicable): <caller/input -> capability -> output>

## 2. Scope
- In scope: <capabilities, environments>
- Out of scope: <exclusions, separate follow-ups>
- Preserve: <working behavior/UX and baseline reference>
- Ownership: <responsible layers; forbidden alternate paths>
- Constraints: <principles/concepts, limits>

## 3. Change Map
| Area / Owner | Current / Evidence | Action | Target / Reason |
| --- | --- | --- | --- |
| <area / owner> | <confirmed state, limits, evidence; or unverified> | <keep/change/add/remove> | <target / reason for G1> |

<Optional As-Is -> To-Be ASCII; link detailed architecture.>

## 4. SOW Sequence
| Order | SOW | Outcome / Owner | Depends On | Exit Gate | Status |
| --- | --- | --- | --- | --- | --- |
| 1 | <reference/TBD> | <G1 deliverable / owner> | None | <completion proof; prerequisite if any> | DRAFT |

## 5. Acceptance
| Outcome / Lock | Required Evidence | Result / Gap |
| --- | --- | --- |
| G1 | <consumer scenario; exact target; expected result; evidence> | NOT VERIFIED: <next check> |

<Verify applicable behavior, preservation, ownership, parity, and one negative
case. Parity must match the referenced baseline, not just smoke/build.>

## 6. Open Decisions
| Question / Risk | Decision / Next Check | Owner |
| --- | --- | --- |
| <unresolved item> | <required decision or check> | <person / role> |

<Unresolved only; None if empty. Every unknown needs an owner and next check.>
```

## Lifecycle

- Approval: record approver/`approve_dttm` only when explicit. Completion: actual
  `finish_dttm`. Use full datetimes; future events stay `null`.
- Results: `PASS`, `FAIL`, `PARTIAL`, `BLOCKED`, `NOT VERIFIED` plus gaps.
  Static/simulated checks and SOW counts are not runtime proof.
- `DONE`: evidence for all outcomes/locks and required integration/deployment.
  Functional success does not waive ownership violations.
- Follow the resolved bundle lifecycle: completed children stay in an active
  Plan; only verified aggregate completion moves the whole Plan to matching
  `finished/`. Repair links; exclude unrelated follow-ups.
- Authorized reopen restores the owning bundle and affected parent states;
  clear only reopened scope/ancestor finish times and preserve completed siblings.
