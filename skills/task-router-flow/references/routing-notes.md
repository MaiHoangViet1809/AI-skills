# Routing Notes

## Decision Table

- New code change not covered by an active SOW: draft a new SOW
- Scope change to active work: extend the existing SOW
- Debug or bugfix request: find root cause first, then decide whether the fix needs a SOW change
- Docs, SOW, or plan only: no new SOW

## SOW Behavior

- Use the repository's active SOW template
- Place SOW files in the repository's required planning directory
- Wait for approval before code edits when the repo requires it
- If scope changes materially, update the SOW and re-approve

## Debug Note

For debug requests, append or update a note in `plan_todo/fix_bug.md` so the bug is tracked even if the final fix path changes later.
