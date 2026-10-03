# SOW_0098 - Canonical Plan Contract In Skills

- **Status**: COMPLETED
- **Approval**: APPROVED by user
- **create_dttm**: 2026-10-04T03:24:05+07:00
- **approve_dttm**: 2026-10-04T03:56:50+07:00
- **finish_dttm**: 2026-10-04T04:03:37+07:00
- **Proposed-By**: Codex
- **plan**: None; this bounded integration needs only a SOW

## Task

Move the compact plan template into `task-router-flow` and connect the relevant
skills to one shared plan/SOW contract, without duplicating templates.
Preserve existing SOW routing and target-repo guardrails; plan is optional.

## Why / Baseline

- The reviewed template connects the original goal, bounded SOWs, and evidence.
  Its gates address scope drift, ownership violations, false parity/completion,
  excessive phase splitting, and incorrect plan lifecycle handling.
- Current routing defines SOWs but has no packaged plan template. A temporary
  copy using the existing `copy_skill()` API confirmed that the SOW reference
  ships, while the root plan template does not. The registry also omits it.
- Follow `AGENTS.md`: SOW-first for behavior-bearing skill edits, DRY/KISS,
  explicit approval, scoped verification, and preservation of concurrent work.
  AISkills declares no concept catalog or principle-design document.

## Location

- `TEMPLATE_PLAN.md` -> `skills/task-router-flow/references/plan.md` (move)
- `skills/task-router-flow/SKILL.md`
- `skills/task-router-flow/references/scope-of-work.md`
- `skills/task-router-flow/references/routing-notes.md`
- `skills/task-review-investigate-compare/SKILL.md`
- `skills/task-execution-flow/SKILL.md`
- `skills/sow-delegate-flow/SKILL.md`
- `skills/task-poc-verification-flow/SKILL.md`
- `skills/task-progress-report/SKILL.md`
- `skills/registry.json`
- `skills/INDEX.md`
- `tests/test_plan_contract_integration.py` (new)
- `tests/skill_feedback_cases/`: only the six skills listed below
- This SOW, including its eventual move to `plan_todo/finished/`

## As-Is Diagram (ASCII)

```text
TEMPLATE_PLAN.md (root draft)       router package -> SOW definition only
            |                              |
            `-- not installed              `-- consumer-specific plan handling
```

## To-Be Diagram (ASCII)

```text
task-router-flow/references/
  plan.md <----> scope-of-work.md
       |
       +--> router: draft / route
       +--> review / POC: inspect contract
       +--> execution / delegate: enforce scope, evidence, lifecycle
       `--> progress: distinguish SOW count from plan acceptance
```

## Deliverables / Behavior Locks

1. Move, do not duplicate, the compact template into `references/plan.md`.
   Remove draft-only wording when activated, fix its SOW link to the packaged
   sibling, and retain its six sections and reviewed gates without expansion.
   Create a plan only on an explicit user request, or when scope is so large
   that completing it reliably in one SOW risks non-completion or mistakes.
   Multiple files, owners, dependencies, or coordinated delivery alone are not
   sufficient triggers. Without either trigger, do not create a plan; continue
   through the existing router branch.
2. Link the SOW definition back to the plan contract: a plan owns aggregate
   outcomes when present; each SOW owns exact implementation coverage and links
   a parent goal only when a plan exists. Plan-specific gates, discovery,
   reporting, and lifecycle handling apply only to plan-backed tasks.
   Preserve standalone SOWs, existing required fields, approval/timestamp rules,
   conditional concept authority, and the docs-only exemption.
   Do not introduce or relax SOW requirements: the existing router applies
   target-repo guardrails to choose a new SOW, exact approved coverage,
   extension/replacement, or a permitted no-SOW path. Plan creation does not
   itself require a new SOW or grant implementation approval.
3. Apply short instructions at the relevant action points:

| Skill | Integration |
| --- | --- |
| `task-router-flow` | Preserve existing SOW routing under target-repo guardrails; create a plan only for explicit request or excessive-scope risk; map goals to SOWs and acceptance when a plan exists. |
| `task-review-investigate-compare` | Check goal/scope/SOW alignment before approval; separate proposed scope, material unknowns, and evidence. |
| `task-execution-flow` | Check approved coverage/dependencies; update plan tables; verify aggregate outcomes and ownership before closing the plan. |
| `sow-delegate-flow` | Supply the applicable contract with the bounded delegate task; preserve clean-context isolation and coordinator ownership. |
| `task-poc-verification-flow` | Check the POC's declared scope and parent-goal mapping when present; do not treat prototype proof as full delivery. |
| `task-progress-report` | Report evidence-backed plan acceptance separately from closed-SOW counts; preserve existing report formats. |

4. Prefer the target repo's declared active contracts. Use the packaged AISkills
   definitions as defaults, not overrides. Consumers must resolve the canonical
   owner from the available skill context; never hardcode a user path or copy
   templates into each consumer. Read the declared project contract first;
   otherwise locate `task-router-flow` through the active harness's supplied
   skill location/catalog and read its `references/plan.md` and
   `references/scope-of-work.md`. A coordinator may supply that resolved
   contract to an isolated delegate. Do not assume sibling install roots or
   add cross-package Markdown links that break standalone package checks.
   If a subset install lacks the default resource
   and no governing contract was supplied, identify the missing contract and
   leave dependent drafting/review unverified; do not invent it or auto-install.
   This does not block unrelated work or tasks that need no plan contract.
5. Register the new resource and document the canonical owner/subset dependency.
   Add sanitized expected, negative, and boundary cases; reuse existing sync
   APIs, fixture schema, and tests. Do not add an installer dependency engine.

## Done Criteria

1. Exactly one active plan template exists, inside the router package; the root
   draft is removed. Its packaged links work without access to the source repo.
2. The six roles above use the same contract without duplicating it, forcing a
   plan for every task, or overriding target-project policy.
3. Scenario review and regression cases cover: ordinary standalone SOW;
   exact approved coverage reused; permitted docs-only/no-SOW path preserved;
   multi-file/owner/dependency work without excessive-scope risk adds no plan;
   explicit plan request; excessive scope risking non-completion or mistakes;
   project-owned template; missing default resource; unapproved/TBD SOW;
   failed dependency; changed scope; prototype-only proof; functional pass with
   ownership failure; plan/SOW closeout and explicit reopen.
4. Temporary package-copy checks exercise owner-present and owner-absent subset
   layouts. Registry/file parity, Markdown references, JSON fixtures, and
   `git diff --check` pass.
   Preserve existing standalone router/delegate link checks. Inspect the six
   consumer instructions against the scenario matrix; fixture schema validity
   alone does not verify those instructions or model behavior.
5. Run the available skill structural validator and
   `uv run python -m unittest tests.test_plan_contract_integration
   tests.test_skill_feedback_cases tests.test_skill_sync_scripts`.
6. Report deterministic contract/package verification separately from actual
   model adherence. Do not claim these checks guarantee agent behavior.

## Out Of Scope

- Global Codex/Claude sync, host configuration, push, or remote publication.
- New skills, rewritten SOW templates, automatic dependency installation, MCP
  changes, telemetry, benchmarks, or unrelated model/delegation behavior.
- Rewriting historical plans/SOWs or modifying other project policies.
- Changing existing SOW requirement, exemption, or approval-routing policy.
- Unrelated existing changes, including dirty router/fixture/install-guide work.

## Cautions / Risks

- Shared resources may be unavailable in subset installs; availability must be
  explicit, not hidden behind a dangling link or installation side effect.
- The root template was untracked; its scoped move left no duplicate or empty
  placeholder. The active resource is now packaged inside the router.
- Router and feedback files already contain unrelated edits. Preserve them,
  inspect scoped hunks, and do not stage or commit mixed ownership blindly.
- Keep wording compact. The SOW authorizes integration, not new planning layers,
  acceptance thresholds, or a promise of error-free model adherence.

## Plan / Reference

- [Plan contract](../../skills/task-router-flow/references/plan.md)
- [SOW contract](../../skills/task-router-flow/references/scope-of-work.md)
- [Sync API](../../scripts/skills/skill_sync_common.py)
- [Sync tests](../../tests/test_skill_sync_scripts.py)

## Decision

One canonical router-owned template with short consumer instructions. Existing
project contracts win; missing defaults are explicit. This avoids copy drift
and changes neither sync APIs nor unrelated workflow behavior.

## Verification / Closeout

- Implemented: one canonical packaged template, six consumer integrations,
  project-first/missing-resource handling, registry/index, and eight sanitized
  cases with 24 expected/negative/boundary scenarios. Existing SOW routing and
  standalone paths are preserved; no plan is forced by file/owner count.
- Coordinator check: `uv run --no-sync --offline python -m unittest
  tests.test_plan_contract_integration tests.test_skill_feedback_cases
  tests.test_skill_sync_scripts` passed 19 tests. Real `copy_skill()` calls into
  temporary roots proved owner-present and owner-absent layouts, resource/link
  portability, no template duplication or automatic dependency installation.
- Six skills passed the available `quick_validate.py` validator; JSON/schema,
  registry parity, Markdown links, and `git diff --check` passed.
- A temporary checkout of the staged index independently passed the same 19
  tests, excluding all unrelated dirty hunks. Initial `uv` environment setup in
  that isolated checkout panicked; rerunning with the existing project runtime
  via `uv run --project <source-repo> --no-sync --offline` passed. This was an
  environment-selection failure, not a skipped or failed contract check.
- Manual scenario review: explicit request/excessive-scope plan triggers;
  standalone, reused-coverage and docs-only paths; project override/missing
  resource; unapproved/TBD/failed-dependency stop; changed-scope approval;
  prototype/ownership/integration failures block plan closure; completed
  plan/SOW movement and explicit reopen preserve prior evidence.
- Gap check: contract and edge cases covered; old routing/report formats and
  isolation preserved. No new runtime state, cancellation, performance,
  cleanup, logging or observability paths. No actionable in-scope gaps found.
- Delegation: test file slice delegated to current native catalog role
  `router_greennode_glm_5_3` (`greennode/glm-5.3`, max), with
  `fork_turns: none`. The child changed only its owned test file, returned
  evidence, and was interrupted after completion. Coordinator reviewed the
  diff and independently reran all targeted tests. Contract/skills/fixtures
  remained coordinator-owned to preserve related invariants and dirty hunks.
- Not verified: actual LLM adherence. Deterministic assertions and manual
  contract review do not prove model behavior; that guarantee is not a done
  criterion. Production sync and push were not performed (out of scope).
- Commit boundary: exclude pre-existing router telemetry removal and its
  fixture, install-guide/README/decision-log changes, and unrelated untracked
  documents. Preserve those working-tree changes intact.
