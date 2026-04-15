# Telemetry Dashboard

Boot the dashboard on `http://localhost:9999` with:

```bash
PYTHONPATH=. uv run python scripts/dashboard/run_dashboard.py
```

What the script does:

- runs `npm install` in `dashboard_ui/`
- builds the frontend into `scripts/dashboard/static/`
- serves API and frontend from the same FastAPI app on port `9999`
- reads telemetry only from `~/.logs/codex/telemetry/runs/`

Quick smoke checks:

```bash
curl http://127.0.0.1:9999/
curl http://127.0.0.1:9999/api/summary
```

Backfill existing project-local run summaries into the global ledger:

```bash
uv run python scripts/telemetry/backfill_global_ledger.py
```
