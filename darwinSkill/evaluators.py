from __future__ import annotations

from darwinSkill.contracts import MetricResult, SkillEvaluator, SkillSample


def _normalize(value: str) -> str:
    return " ".join(str(value).strip().lower().split())


class ExactMatchEvaluator(SkillEvaluator):
    def evaluate(self, prediction: str, sample: SkillSample) -> MetricResult:
        normalized_prediction = _normalize(prediction)
        normalized_expected = _normalize(sample.expected_answer)
        passed = normalized_prediction == normalized_expected
        return MetricResult(
            score=1.0 if passed else 0.0,
            passed=passed,
            details={
                "prediction": prediction,
                "expected_answer": sample.expected_answer,
                "normalized_prediction": normalized_prediction,
                "normalized_expected_answer": normalized_expected,
            },
        )
