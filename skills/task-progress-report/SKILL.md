---
name: task-progress-report
description: Use for concise task progress or structured inventory summaries. Match columns to the requested subject; for plan/SOW execution show overall completion and only open items, with one default report at final closeout.
---

# Task Progress Report

Use this skill for execution progress or a structured inventory/status summary.

Keep progress reporting lightweight. The goal is to improve visibility, not to narrate every intermediate thought.

## Rules

- First identify the summary's subject. Inventory uses subject-specific columns;
  plan/SOW execution uses the progress table below. Honor requested columns or prose.
- Default to one invocation at final task closeout, not after every mini-task.
  Explicit user status requests may invoke this skill earlier or more than once.
- While still executing, only interrupt with a progress update when there is a real decision point, blocker, or substantial milestone.
- Ordinary short execution commentary is separate from this skill's reports.
- If the task is plan or SOW driven, show a compact table.
- In the table, show only SOW items that are still open or still being verified.
- Remove done SOWs only after the Completion Discipline gates below pass.
- For plan/SOW progress only, include one overall row in the form `overall x/y`.
- If a SOW is complete and no required work remains, remove it from the table and
  reflect it in the overall row. An accepted non-blocking follow-up belongs in
  the short note, not an open SOW row.
- Keep commentary below the table short and only include non-table context that matters.
- Do not repeat the same progress statement across multiple turns.
- This skill is progress-oriented, not findings-oriented; do not use a `Severity | Finding | Impact | Solution` table for a plain summary request.
- Only use a `Severity | Finding | Impact | Solution` table when the progress report includes actionable blockers or risks.

## Table Format

For plan/SOW execution, use this column order:

| plan name | SOW | %Complete | current task short desc | progress |

Rules:

- `plan name`: the active plan name, or omit the plan concept entirely when the work is ad hoc.
- `SOW`: the active SOW id or `overall x/y` for the summary row.
- `current task short desc`: a short phrase, not a paragraph.
- `progress`: one short sentence or phrase.
- If a row is only the overall summary row, the last two columns may be blank.
- If there are no open SOWs left, return only the overall row.

## Reporting Modes

### Inventory Summary

Use rows for the actual subjects and columns requested by the user. For example:

| Skill | Codex | Claude |
| --- | --- | --- |
| example-skill | Installed | Not installed |

Use verified inventory evidence; mark unavailable status unknown. Never invent
SOW IDs, percentages or an overall SOW row for inventory. A generic prose summary
need not be forced into a table when the user requests prose.

### 1. Plan or Multi-SOW Work

Use the progress table.

Default behavior:

- first row is the overall row
- remaining rows are only open SOWs
- done SOWs do not appear

### 2. Single SOW Work

Use the same table shape, but usually with:

- one overall row
- one active SOW row if it is still open

If the SOW is fully done and verified, keep only the overall row.

### 3. Ad Hoc Work

Skip the `plan name` concept if it adds no value.

You may still use a reduced table if the user asked for structured progress. Otherwise use:

- one short progress sentence
- one short note line if needed

## Detail Notes

Below the table, add a short note section only when useful:

- what was just completed
- what is being verified
- what remains, if anything

Keep it brief. Do not turn the note section into a changelog.

## Completion Discipline

A SOW counts as done for reporting only after evidence shows:

- implementation is finished
- required implementation verification passed and all done criteria are satisfied
- you performed the intended gap-finding pass
- no blocking gap or required repair loop remains open
- execution closeout handling is complete under the applicable workflow

Use `task-execution-flow` completion state when available. Accepted non-blocking
risks may remain if execution records their impact, acceptance authority and
follow-up; mention them without turning them into completed repairs.

When that skill is unavailable, use actual verification and closeout evidence;
do not require installing another skill. Missing evidence means pending, not
done. Percentages and an implementation claim alone never prove completion.
If any required gate is open or unknown, keep the SOW in the table.

## Avoid

- reporting every micro-step
- showing completed SOW rows by default
- mixing speculative next steps into the progress column
- long prose before the table
- inconsistent column names between turns

## Example

```markdown
| plan name | SOW | %Complete | current task short desc | progress |
| --- | --- | --- | --- | --- |
| `skill_framework_distillation_plan` | `overall 13/14` | `98%` |  |  |
| `skill_framework_distillation_plan` | `SOW_0054` | `99%` | `final gap-finding pass` | `checking remaining parity edges` |

Notes:
- `SOW_0054` is the only open item left after the other SOWs passed verification.
- If the final check passes, remove the `SOW_0054` row and keep only the overall row.
```
