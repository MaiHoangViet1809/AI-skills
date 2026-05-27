from __future__ import annotations

import unittest

from darwinSkill.backends import BackendRouter, BackendRuntimeConfig, default_routing_for_family
from darwinSkill.contracts import MetricResult, SkillFeedback, SkillSample


class TargetStub:
    def predict(self, skill_text: str, sample: SkillSample) -> str:
        return f"target:{sample.prompt}"


class OptimizerStub:
    def improve_skill(self, skill_text: str, feedback: list[SkillFeedback]) -> str:
        return f"{skill_text}|optimizer:{len(feedback)}"


class BackendsTest(unittest.TestCase):
    def test_backend_router_separates_target_and_optimizer_roles(self) -> None:
        router = BackendRouter(target_backend=TargetStub(), optimizer_backend=OptimizerStub())
        sample = SkillSample(prompt="Capital of France?", expected_answer="Paris")
        feedback = [
            SkillFeedback(
                sample=sample,
                prediction="unknown",
                metric=MetricResult(score=0.0, passed=False),
            )
        ]

        self.assertEqual(router.predict("", sample), "target:Capital of France?")
        self.assertEqual(router.improve_skill("", feedback), "|optimizer:1")

    def test_backend_runtime_config_rejects_unknown_family(self) -> None:
        with self.assertRaises(ValueError):
            BackendRuntimeConfig(family="unknown")

    def test_default_routing_family_mapping(self) -> None:
        routing = default_routing_for_family("codex_exec")
        self.assertEqual(routing.target.family, "codex_exec")
        self.assertEqual(routing.optimizer.family, "openai_chat")


if __name__ == "__main__":
    unittest.main()
