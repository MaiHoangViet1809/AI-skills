# PLAN_20260708_GOBS4HRF - Telemetry Dashboard Follow-Up Plan

- Status: UNKNOWN
- Approval: UNKNOWN
- create_dttm: 2026-07-08T01:38:56+07:00
- create_date: 2026-07-08
- create_dttm_source: filesystem_birthtime
- create_dttm_confidence: filesystem_proxy
- create_dttm_evidence: `plan_todo/finished/SOW_20261008_VO3LKN0L/creation-date-evidence.json` (record: PLAN_20260708_GOBS4HRF)
- approve_dttm: unknown
- finish_dttm: unknown
- legacy_id: null
- legacy_path: plan_todo/finished/telemetry_dashboard_followup_plan.md
- migrated_dttm: 2026-10-08T12:48:51+07:00
- legacy_title: Telemetry Dashboard Follow-Up Plan

## Preserved Contract And Historical Evidence

Status: obsolete as of 2026-07-08. AISkills no longer maintains a repo-owned
telemetry skill, Codex hooks, telemetry runtime, or dashboard. This file is kept
only as historical planning context.

## Scope
- `SOW_20260425_984F0YF8`: add a repeatable local install flow for repo skills into `~/.codex/skills`
- `SOW_20260425_6X92J74B`: replace the dashboard activity chart with a GitHub-style daily token heatmap

## Order
1. Implement the install script and usage docs.
2. Update backend activity aggregation to return daily token buckets.
3. Replace the frontend activity chart with a heatmap and token-source toggle.

## Notes
- Heatmap color encodes token burn, not run count.
- Initial heatmap modes: `total`, `codex`, `claude`; default is `total`.
