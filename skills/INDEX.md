# AISkills Index

Use `registry.json` for exact files and raw download URLs.

## Skills

| Skill | Use when |
| --- | --- |
| `apply-design-mirror` | Applying an extracted design package through a target project's real design-system ownership. |
| `claude-code-glm-setup` | Connecting GreenNode GLM-5.3 via codex-router to Claude Code desktop as a one-level `glm-worker` sub-agent, with a check per phase. |
| `datamart-design-review` | Designing or reviewing datamart grain, formulas, table and column changes, migration impact, and evidence. |
| `extract-design-mirror` | Extracting a UI design language into `DESIGN.md` plus evidence for later reuse. |
| `task-escalation-flow` | Escalating a genuinely stuck Luna, GLM-high, Sonnet, or Haiku executor through isolated Sol and Astra advisor tiers. |
| `playwright-flow` | Automating Playwright CLI browser work with explicit session lifecycle and cleanup. |
| `project-concept-governance-flow` | Creating, reviewing, updating, or enforcing a project's local `docs/concept` authority. |
| `skill-evolution-flow` | Diagnosing task mismatches and unapplied instructions; evidence-backed, authorized skill evolution. |
| `sow-delegate-flow` | Delegating SOW or plan work to native or custom external agents with fresh non-native sessions and local verification. |
| `spark-connect-debug` | Checking exact SQL/source metadata first, then diagnosing remaining Spark Connect failures from runtime evidence. |
| `task-execution-flow` | Executing an already-approved or otherwise clear task with verification discipline. |
| `task-diagram-explaination` | Explaining mechanisms through evidence-grounded diagrams with clear ownership, handoffs, decisions and state changes. |
| `task-poc-verification-flow` | Reviewing POC SOWs and POC plans against runtime evidence and safety gates. |
| `task-progress-report` | Reporting evidence-backed execution progress or an inventory with subject-specific columns. |
| `task-review-investigate-compare` | Reviewing plans, SOWs, ideas, root causes, or implementation approaches before execution. |
| `task-router-flow` | Routing work into SOW, debug, code-change, or docs-only branches. |
| `taste-skill` (`$design-taste-frontend`) | Anti-slop frontend guidance for landing pages, portfolios, and redesigns. |
| `verify-design-mirror` | Independently verifying mirrored UI fidelity against the source package and mapping. |

## Install

Agents should follow the root `INSTALL_FOR_AGENTS.md` guide. A normal install
installs every skill listed in `registry.json`; use this table only for
reference or explicit subset installs.

Users with a local clone can use scripts under `scripts/skills/`.

## Shared Planning Contracts

`task-router-flow` owns the packaged defaults `references/plan.md` and
`references/scope-of-work.md`; target-project declared contracts take precedence.
Plan is optional: explicit user request or excessive-scope risk only. Existing
SOW routing is unchanged. The review, execution, delegate, POC, and progress
skills use these defaults only for applicable plan-backed work.

Subset installs may omit the owner. Resolve it via harness-supplied skill
location/catalog or use a supplied authoritative contract, never assumed sibling
roots. If unavailable, dependent drafting/review/acceptance remains unverified;
unrelated work is not blocked. No template duplication or auto-installation.
