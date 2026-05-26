from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from darwinSkill.contracts import ArtifactStore, RunArtifacts, RunContext


def _to_jsonable(value: Any) -> Any:
    if isinstance(value, Path):
        return str(value)
    if is_dataclass(value):
        return _to_jsonable(asdict(value))
    if isinstance(value, dict):
        return {str(key): _to_jsonable(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_to_jsonable(item) for item in value]
    return value


def utc_now() -> datetime:
    return datetime.now(tz=timezone.utc)


def isoformat(value: datetime) -> str:
    return value.isoformat()


def make_run_id() -> str:
    return uuid4().hex[:10]


class LocalArtifactStore(ArtifactStore):
    def persist(self, context: RunContext) -> RunArtifacts:
        if context.evaluation_report is None:
            raise ValueError("Cannot persist a run without an evaluation report.")

        started_at = context.history[0].get("started_at") if context.history else None
        finished_at = isoformat(utc_now())
        if not isinstance(started_at, str):
            started_at = finished_at

        output_dir = context.output_root / f"{context.run_name}-{context.run_id}"
        output_dir.mkdir(parents=True, exist_ok=True)

        summary_path = output_dir / "summary.json"
        history_path = output_dir / "history.json"
        evaluations_path = output_dir / "evaluations.json"
        final_skill_path = output_dir / "final_skill.txt"

        with summary_path.open("w", encoding="utf-8") as handle:
            json.dump(
                {
                    "run_id": context.run_id,
                    "run_name": context.run_name,
                    "run_kind": context.run_kind,
                    "sample_count": context.evaluation_report.sample_count,
                    "mean_score": context.evaluation_report.mean_score,
                    "pass_rate": context.evaluation_report.pass_rate,
                    "started_at": started_at,
                    "finished_at": finished_at,
                },
                handle,
                ensure_ascii=False,
                indent=2,
            )

        with history_path.open("w", encoding="utf-8") as handle:
            json.dump(_to_jsonable(context.history), handle, ensure_ascii=False, indent=2)

        with evaluations_path.open("w", encoding="utf-8") as handle:
            json.dump(
                _to_jsonable(context.evaluation_report.results),
                handle,
                ensure_ascii=False,
                indent=2,
            )

        final_skill_path.write_text(context.skill_text, encoding="utf-8")

        return RunArtifacts(
            run_id=context.run_id,
            run_name=context.run_name,
            run_kind=context.run_kind,
            output_dir=output_dir,
            started_at=started_at,
            finished_at=finished_at,
            sample_count=context.evaluation_report.sample_count,
            mean_score=context.evaluation_report.mean_score,
            pass_rate=context.evaluation_report.pass_rate,
            final_skill=context.skill_text,
            summary_path=summary_path,
            history_path=history_path,
            evaluations_path=evaluations_path,
            final_skill_path=final_skill_path,
        )
