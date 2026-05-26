from __future__ import annotations

from darwinSkill.contracts import RunContext, SampleEvaluation, SkillStage
from darwinSkill.runtime import append_history, build_feedback, build_report


class PredictionStage(SkillStage):
    name = "predict"

    def run(self, context: RunContext) -> RunContext:
        context.predictions = [
            context.backend.predict(context.skill_text, sample)
            for sample in context.samples
        ]
        append_history(
            context,
            self.name,
            {"sample_count": len(context.samples), "skill_length": len(context.skill_text)},
        )
        return context


class EvaluationStage(SkillStage):
    name = "evaluate"

    def run(self, context: RunContext) -> RunContext:
        if len(context.predictions) != len(context.samples):
            raise ValueError("Predictions must align with samples before evaluation.")
        evaluations: list[SampleEvaluation] = []
        for sample, prediction in zip(context.samples, context.predictions):
            metric = context.evaluator.evaluate(prediction, sample)
            evaluations.append(
                SampleEvaluation(sample=sample, prediction=prediction, metric=metric)
            )
        context.evaluations = evaluations
        context.evaluation_report = build_report(
            skill_text=context.skill_text,
            evaluations=evaluations,
        )
        append_history(
            context,
            self.name,
            {
                "sample_count": context.evaluation_report.sample_count,
                "mean_score": context.evaluation_report.mean_score,
                "pass_rate": context.evaluation_report.pass_rate,
            },
        )
        return context


class ImprovementStage(SkillStage):
    name = "improve"

    def run(self, context: RunContext) -> RunContext:
        if not context.evaluations:
            raise ValueError("Evaluations must exist before skill improvement.")
        previous_skill = context.skill_text
        context.skill_text = context.backend.improve_skill(
            context.skill_text,
            build_feedback(context.evaluations),
        )
        append_history(
            context,
            self.name,
            {
                "previous_skill_length": len(previous_skill),
                "new_skill_length": len(context.skill_text),
            },
        )
        return context


def run_stages(context: RunContext, stages: list[SkillStage]) -> RunContext:
    for stage in stages:
        context = stage.run(context)
    return context
