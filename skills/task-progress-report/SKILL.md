---
name: task-progress-report
description: Use when you need to report execution progress in a stable, low-noise format for plan or SOW-driven work. Prefer a short summary after a completed block, with a progress table that shows only still-open SOW items plus one overall completion row such as `overall 4/5`.
---

# Task Progress Report

Use this skill when the work is active and the user wants disciplined progress reporting instead of ad hoc status chatter.

Keep progress reporting lightweight. The goal is to improve visibility, not to narrate every intermediate thought.

## Rules

- Report progress after a meaningful block finishes, not every small action.
- While still executing, only interrupt with a progress update when there is a real decision point, blocker, or substantial milestone.
- Default to one summary-style progress update near the end of the current block of work.
- If the task is plan or SOW driven, show a compact table.
- In the table, show only SOW items that are still open or still being verified.
- Do not keep already-done SOWs in the table after they have passed the final gap-finding pass.
- Always include one overall row in the form `overall x/y`.
- If a SOW is complete, validated, and no follow-up remains, remove it from the table and only reflect it in the overall row.
- Keep commentary below the table short and only include non-table context that matters.
- Do not repeat the same progress statement across multiple turns.
- This skill is progress-oriented, not findings-oriented; only use a `Severity | Finding | Impact | Solution` table when the progress report includes actionable blockers or risks.

## Table Format

Use this column order:

| plan name | SOW | %Complete | current task short desc | progress |

Rules:

- `plan name`: the active plan name, or omit the plan concept entirely when the work is ad hoc.
- `SOW`: the active SOW id or `overall x/y` for the summary row.
- `current task short desc`: a short phrase, not a paragraph.
- `progress`: one short sentence or phrase.
- If a row is only the overall summary row, the last two columns may be blank.
- If there are no open SOWs left, return only the overall row.

## Reporting Modes

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

A SOW counts as done for reporting only after:

- implementation is finished
- you performed the intended gap-finding pass
- no immediate repair loop remains open

If any of those are still open, keep the SOW in the table.

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
