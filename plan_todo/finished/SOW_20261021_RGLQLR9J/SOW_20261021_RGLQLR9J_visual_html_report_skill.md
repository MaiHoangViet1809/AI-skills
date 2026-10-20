# SOW_20261021_RGLQLR9J — Visual-first HTML reports

- Status: DONE
- Approval: approved by user
- create_dttm: 2026-10-21T03:19:42+07:00
- approve_dttm: 2026-10-21T03:32:29+07:00
- finish_dttm: 2026-10-21T03:34:15+07:00
- Proposed-By: Codex
- Plan / Reference: User-requested skill evolution for HTML, visual-first reports; skill-evolution-flow and skill-creator.

## Task

Create one concise AISkills-owned `task-report-html` skill for durable, evidence-backed reports: HTML by default, diagrams/charts/graphs first, concise explanations and decisive conclusions.

## Why / Investigation

- User feedback identifies reports dominated by tables/prose instead of explanatory visuals. The desired recurring outcome is explicit; the precise historical loading/application failure remains unknown.
- `task-diagram-explaination` owns mechanism/workflow explanations and explicitly excludes general charting. Its installed Codex SKILL.md matches canonical source; no drift was found there.
- `task-progress-report` owns lightweight progress/inventory summaries, not analytical report artifacts. Preserve its compact chat behavior.
- Analytical reporting plugins are externally owned. Do not edit or vendor them into AISkills.
- No applicable PRODUCT_PRINCIPLE_DESIGN.md, declared concept authority or .agents/rules directory was found. Preserve repository KISS/DRY and scope boundaries.

## Location

- `skills/task-report-html/SKILL.md` (new)
- `skills/task-report-html/agents/openai.yaml` (new)
- `skills/registry.json` (add this skill entry only; preserve existing unrelated dirty edits)
- `tests/skill_feedback_cases/task-report-html.json` (new)
- This SOW bundle for progress and verification evidence.

## As-Is Diagram (ASCII)

```text
Durable analytical report request
  -> no AISkills-owned report presentation contract
  -> format/visual hierarchy depends on task-specific instructions

Existing skills: mechanism diagrams | chat progress summaries
                (different responsibilities)
```

## To-Be Diagram (ASCII)

```text
Durable report request -> task-report-html
  -> decision + evidence
  -> concise conclusion
  -> chart/graph for quantitative comparisons
     diagram for mechanism/ownership/flow
  -> HTML artifact + rendered verification

Exact lookup / detail not expressed clearly visually -> compact table or prose
Quick status / explicit other output format -> honor that request
```

## Deliverables / Behavior

1. Precise automatic discovery for creating/updating durable analytical, benchmark, technical or business reports, including report-style analytical dashboards. Not quick answers, SOWs, progress updates, general frontend application development or every occurrence of the word "report". This skill owns presentation and evidence communication, not a second analysis engine or application-building workflow; preserve applicable specialist tool and project contracts.
2. Default to HTML when a durable report has no explicitly selected format. Honor an explicit PDF, slide, Markdown or other format; do not impose HTML on unrelated work.
3. Choose visuals from the question, not decoration: comparisons/distributions/trends use charts; mechanisms use diagrams. Tables and prose are supporting detail where clearer than a visual. No arbitrary chart quotas.
4. Lead with a sharp evidence-supported conclusion: answer the actual question, quantify the result where supported, explain operational meaning and recommend a next decision only when justified. Do not force a change-over-time story, recommendation or confident verdict when evidence is insufficient; state the exact unresolved question briefly. Do not claim causality, parity or capacity beyond measured evidence.
5. Make quantitative comparisons honest: units, sample size, period, resource differences and methodology matter. Show uncertainty, failed/partial runs and unavailable values truthfully. Every headline result and chart must be traceable to a supplied/current source, calculation and relevant run identity; compact source links/notes suffice, with no new provenance subsystem. Do not put unlike workloads on an apparently equivalent ranking without making the difference visible.
6. Reuse the target project's report structure and rendering tools. Prefer a simple portable HTML artifact when appropriate; do not mandate React, a chart library, a server, a template framework or new dependencies.
7. Verify rendered output and source-to-chart values when feasible. Disclose unavailable rendering; structural checks are not behavioral proof.
8. Add sanitized expected, negative and boundary feedback scenarios before editing the skill. Respect the existing fixture schema: exactly three scenarios per case, one of each kind. Use separate cases to test explicit non-HTML output and insufficient evidence independently; also cover visual-first report/dashboard, quick status, and general frontend work that must not be redirected.

## Done Criteria

- Frontmatter, registry and UI metadata agree; no overlap that redirects mechanism-only diagrams or chat progress into report generation.
- Walk through the included report/dashboard path and excluded short-status/frontend paths, plus explicit-format and insufficient-evidence boundaries; verify the instructions do not mandate artifacts or unsupported conclusions on excluded paths.
- Run skill-creator structural validation for the new skill.
- Run `uv run python -m unittest tests.test_skill_feedback_cases tests.test_skill_sync_scripts` and `git diff --check`.
- Self-review expected, negative and boundary cases. Record whether model behavior was exercised; fixture/structural checks alone do not prove future selection or output quality.
- Confirm the skill calls for source-to-chart checks, accessible labels/units, readable rendered output and disclosure of unavailable rendering. Do not claim these report-level checks passed merely because the skill text or fixtures passed validation.
- Review exact task diff and preserve concurrent registry changes; commit only approved task-owned changes after successful verification.

## Out-of-Scope

- No existing benchmark/report edits, production access, runtime runs or parent-thread work.
- No edits to plugin/system/installed skills, global AGENTS rules, existing task diagram/progress skills or unrelated dirty files.
- No new reporting framework, generator, telemetry, dependencies, push or skill synchronization. Deployment target requires separate explicit authorization.

## Cautions / Risks

- A skill is conditional guidance, not a universal always-loaded preference. Discovery metadata improves selection but cannot guarantee host behavior.
- Canonical implementation alone does not activate this behavior in an installed environment. No installation, session-wide enforcement or successful automatic invocation is claimed by this SOW.
- Over-broad triggers could make a short answer generate an unnecessary artifact. Negative scenarios must preserve that boundary.
- Visual-first must not hide exact values, missing evidence or accessibility needs.
- `skills/registry.json` is already dirty for unrelated work; update and stage only this skill's entry after approval.

## Progress

- progress_updated_dttm: 2026-10-21T03:34:15+07:00

| Item | Status | Evidence / Pending reason | Next action / Owner |
| --- | --- | --- | --- |
| T1: Ownership and target selection | DONE | Canonical diagram/progress skill and registry inspected; diagram installed copy matches | None |
| T4: SOW self-review | DONE | Report/dashboard boundary, evidence traceability and fixture schema checked and clarified | None |
| T2: New skill and sanitized cases | DONE | Concise SKILL.md, UI metadata, registry entry; 3 feedback cases / 9 scenarios added before skill | None |
| T3: Validation and canonical commit | DONE | Validator and 13 unit tests pass; scope reviewed; canonical commit includes this closeout | None |

## Review

- Mode: Review And Writeback; coordinator-only self-review, no delegation in this side conversation.
- Clarified report-style dashboard inclusion without taking over frontend/application ownership; added traceable conclusions/charts and separate schema-compliant boundary cases.
- No new framework, reporting generator, global rule or installation scope. User approved implementation; future model selection and rendered report quality remain unverified.

## Verification / Closeout

- Implemented only the new skill, UI metadata, its registry entry, feedback cases and this SOW. Existing diagram/progress skill sources remain unchanged.
- `uv run python /Users/maihoangviet/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/task-report-html`: PASS (`Skill is valid!`). The validator used the installed skill-creator script, not a new project script.
- `uv run python -m unittest tests.test_skill_feedback_cases tests.test_skill_sync_scripts`: PASS, 13 tests. Includes fixture schema/privacy and registry-to-file consistency checks.
- `git diff --check`: PASS. No dependencies, reporting framework or runtime behavior added.
- Negative review: a short progress question stays in chat, explicit non-HTML requests retain their format, frontend application work is excluded, and missing observations cannot yield invented percentiles or a confident ranking. These are instruction/case reviews, not independent model executions.
- No model forward-test or rendered report was run in this side conversation. Neither future automatic selection nor actual report quality is claimed verified by structural tests.
- No installed environment was synchronized and nothing was pushed. The skill is implemented in canonical AISkills source only.
- Before task commit, `git fetch origin` succeeded and `HEAD...origin/main` was `0 0`; unrelated dirty registry content and other files are excluded from staging.
