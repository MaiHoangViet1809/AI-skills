from __future__ import annotations

from math import fsum

from darwinSkill.contracts import EvaluationReport, RunContext, SampleEvaluation, SkillFeedback


def build_report(
    *,
    skill_text: str,
    evaluations: list[SampleEvaluation],
) -> EvaluationReport:
    sample_count = len(evaluations)
    if sample_count == 0:
        return EvaluationReport(
            sample_count=0,
            mean_score=0.0,
            pass_rate=0.0,
            skill_text=skill_text,
            results=[],
        )
    total_score = fsum(item.metric.score for item in evaluations)
    passed = sum(1 for item in evaluations if item.metric.passed)
    return EvaluationReport(
        sample_count=sample_count,
        mean_score=total_score / sample_count,
        pass_rate=passed / sample_count,
        skill_text=skill_text,
        results=list(evaluations),
    )


def build_feedback(evaluations: list[SampleEvaluation]) -> list[SkillFeedback]:
    return [
        SkillFeedback(
            sample=item.sample,
            prediction=item.prediction,
            metric=item.metric,
        )
        for item in evaluations
    ]


def append_history(context: RunContext, stage_name: str, summary: dict[str, object]) -> None:
    context.history.append({"stage": stage_name, **summary})
