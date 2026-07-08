from __future__ import annotations

from darwinSkill.src.contracts import SkillBackend, SkillFeedback, SkillSample


def demo_samples() -> list[SkillSample]:
    return [
        SkillSample(prompt="Capital of France?", expected_answer="Paris"),
        SkillSample(prompt="Largest planet?", expected_answer="Jupiter"),
        SkillSample(prompt="2 + 2 = ?", expected_answer="4"),
    ]


def _parse_skill_facts(skill_text: str) -> dict[str, str]:
    facts: dict[str, str] = {}
    for line in skill_text.splitlines():
        if not line.startswith("remember:"):
            continue
        _, payload = line.split("remember:", 1)
        if "=>" not in payload:
            continue
        prompt, answer = payload.split("=>", 1)
        facts[prompt.strip()] = answer.strip()
    return facts


class DarwinMemoryBackend(SkillBackend):
    def predict(self, skill_text: str, sample: SkillSample) -> str:
        facts = _parse_skill_facts(skill_text)
        return facts.get(sample.prompt, "unknown")

    def improve_skill(
        self,
        skill_text: str,
        feedback: list[SkillFeedback],
    ) -> str:
        learned_facts = _parse_skill_facts(skill_text)
        for item in feedback:
            if item.metric.passed:
                continue
            learned_facts[item.sample.prompt] = item.sample.expected_answer

        lines = [f"remember: {prompt} => {answer}" for prompt, answer in sorted(learned_facts.items())]
        return "\n".join(lines)
