# Routing Notes

## Decision Table

- New code change not covered by an active SOW: draft a new SOW
- Scope change to active work: extend the existing SOW
- Debug or bugfix request: find root cause first, then apply repo SOW policy to
  every code fix regardless of size; reuse exact approved coverage or obtain
  approval for new/extended scope before code edits
- Docs, SOW, or plan only: no new SOW

## SOW Behavior

- Use the repository's active SOW template
- Place SOW files in the repository's required planning directory
- Wait for approval before code edits when the repo requires it
- Reuse existing authorization for concrete docs edits; do not repeat approval
  unless authority is missing or scope materially expands
- If scope changes materially, update the SOW and re-approve
- Record timezone-aware `create_dttm`, `approve_dttm`, and `finish_dttm` as
  `YYYY-MM-DDTHH:mm:ss+HH:MM` for the SOW and independently for each extension;
  never use a date-only value
- Keep approval as a concise state/approver marker; do not add approval evidence
  or transcript fields

## Debug Note

For debug requests, append or update a note in `plan_todo/fix_bug.md` so the bug is tracked even if the final fix path changes later.
