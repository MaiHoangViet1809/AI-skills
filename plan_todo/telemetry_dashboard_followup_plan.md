# Telemetry Dashboard Follow-Up Plan

## Scope
- `SOW_0027`: add a repeatable local install flow for repo skills into `~/.codex/skills`
- `SOW_0028`: replace the dashboard activity chart with a GitHub-style daily token heatmap

## Order
1. Implement the install script and usage docs.
2. Update backend activity aggregation to return daily token buckets.
3. Replace the frontend activity chart with a heatmap and token-source toggle.

## Notes
- Heatmap color encodes token burn, not run count.
- Initial heatmap modes: `total`, `codex`, `claude`; default is `total`.
