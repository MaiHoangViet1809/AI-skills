from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from darwinSkill.contracts import ArtifactStore, RunArtifacts, RunContext, RunState, RunStateEntry


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


def build_run_state(context: RunContext, *, finished_at: str) -> RunState:
    history = [
        RunStateEntry(
            stage=str(entry.get("stage", "unknown")),
            details={key: value for key, value in entry.items() if key != "stage"},
        )
        for entry in context.history
    ]
    return RunState(
        run_id=context.run_id,
        run_name=context.run_name,
        run_kind=context.run_kind,
        started_at=context.started_at,
        finished_at=finished_at,
        last_stage=history[-1].stage if history else "start",
        sample_count=context.evaluation_report.sample_count if context.evaluation_report else len(context.samples),
        prediction_count=len(context.predictions),
        evaluation_count=len(context.evaluations),
        skill_text=context.skill_text,
        history=history,
    )


def load_run_state(path: Path | str) -> RunState:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    history = [
        RunStateEntry(
            stage=str(entry["stage"]),
            details=dict(entry.get("details", {})),
        )
        for entry in payload.get("history", [])
    ]
    return RunState(
        run_id=str(payload["run_id"]),
        run_name=str(payload["run_name"]),
        run_kind=str(payload["run_kind"]),
        started_at=str(payload["started_at"]),
        finished_at=str(payload["finished_at"]),
        last_stage=str(payload["last_stage"]),
        sample_count=int(payload["sample_count"]),
        prediction_count=int(payload["prediction_count"]),
        evaluation_count=int(payload["evaluation_count"]),
        skill_text=str(payload["skill_text"]),
        history=history,
    )


class LocalArtifactStore(ArtifactStore):
    def persist(self, context: RunContext) -> RunArtifacts:
        if context.evaluation_report is None:
            raise ValueError("Cannot persist a run without an evaluation report.")

        finished_at = isoformat(utc_now())
        run_state = build_run_state(context, finished_at=finished_at)

        output_dir = context.output_root / f"{context.run_name}-{context.run_id}"
        output_dir.mkdir(parents=True, exist_ok=True)

        summary_path = output_dir / "summary.json"
        history_path = output_dir / "history.json"
        run_state_path = output_dir / "run_state.json"
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
                    "started_at": context.started_at,
                    "finished_at": finished_at,
                },
                handle,
                ensure_ascii=False,
                indent=2,
            )

        with history_path.open("w", encoding="utf-8") as handle:
            json.dump(_to_jsonable(context.history), handle, ensure_ascii=False, indent=2)

        with run_state_path.open("w", encoding="utf-8") as handle:
            json.dump(_to_jsonable(run_state), handle, ensure_ascii=False, indent=2)

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
            started_at=context.started_at,
            finished_at=finished_at,
            sample_count=context.evaluation_report.sample_count,
            mean_score=context.evaluation_report.mean_score,
            pass_rate=context.evaluation_report.pass_rate,
            final_skill=context.skill_text,
            summary_path=summary_path,
            history_path=history_path,
            run_state_path=run_state_path,
            evaluations_path=evaluations_path,
            final_skill_path=final_skill_path,
        )
