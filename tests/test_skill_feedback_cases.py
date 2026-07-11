from __future__ import annotations

import json
import re
import unittest
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
CASES_ROOT = REPO_ROOT / "tests" / "skill_feedback_cases"
SKILLS_ROOT = REPO_ROOT / "skills"
REQUIRED_FEEDBACK_FIELDS = {
    "trigger",
    "actual_behavior",
    "expected_behavior",
    "invariant",
    "evidence_ref",
}
REQUIRED_SCENARIO_FIELDS = {
    "kind",
    "request",
    "context",
    "expected_behavior",
    "must_not",
}
SCENARIO_KINDS = {"expected", "negative", "boundary"}
CAUSE_CLASSES = {
    "trigger",
    "decision_procedure",
    "deterministic_resource",
    "deployment_drift",
    "metadata",
    "policy_conflict",
}
PRIVATE_PATH_PATTERNS = (
    re.compile(r"/Users/[^/\s]+/"),
    re.compile(r"/home/[^/\s]+/"),
    re.compile(r"[A-Za-z]:\\Users\\[^\\\s]+\\"),
)
SENSITIVE_KEYS = {"api_key", "password", "secret", "token", "credential"}


def strings_in(value: Any):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for key, item in value.items():
            yield str(key)
            yield from strings_in(item)
    elif isinstance(value, list):
        for item in value:
            yield from strings_in(item)


class SkillFeedbackCaseTests(unittest.TestCase):
    def test_feedback_case_contracts(self) -> None:
        fixture_paths = sorted(CASES_ROOT.glob("*.json"))
        self.assertTrue(fixture_paths, "at least one feedback fixture is required")
        known_skills = {
            path.name
            for path in SKILLS_ROOT.iterdir()
            if path.is_dir() and (path / "SKILL.md").exists()
        }
        seen_ids: set[str] = set()

        for fixture_path in fixture_paths:
            payload = json.loads(fixture_path.read_text())
            self.assertEqual(1, payload.get("schema_version"), fixture_path.name)
            cases = payload.get("cases")
            self.assertIsInstance(cases, list, fixture_path.name)
            self.assertTrue(cases, fixture_path.name)

            for case in cases:
                case_id = case.get("id")
                self.assertIsInstance(case_id, str, fixture_path.name)
                self.assertTrue(case_id.strip(), fixture_path.name)
                self.assertNotIn(case_id, seen_ids, case_id)
                seen_ids.add(case_id)

                target_skill = case.get("target_skill")
                self.assertIn(target_skill, known_skills, case_id)
                self.assertEqual(fixture_path.stem, target_skill, case_id)
                self.assertIn(case.get("cause_class"), CAUSE_CLASSES, case_id)

                feedback = case.get("feedback")
                self.assertIsInstance(feedback, dict, case_id)
                self.assertEqual(REQUIRED_FEEDBACK_FIELDS, set(feedback), case_id)
                self.assertTrue(all(isinstance(value, str) and value.strip() for value in feedback.values()), case_id)

                scenarios = case.get("scenarios")
                self.assertIsInstance(scenarios, list, case_id)
                self.assertEqual(3, len(scenarios), case_id)
                self.assertEqual(SCENARIO_KINDS, {scenario.get("kind") for scenario in scenarios}, case_id)
                for scenario in scenarios:
                    self.assertEqual(REQUIRED_SCENARIO_FIELDS, set(scenario), case_id)
                    self.assertTrue(
                        all(isinstance(value, str) and value.strip() for value in scenario.values()),
                        case_id,
                    )

                lowered_keys = {key.lower() for key in strings_in(case) if key.lower() in SENSITIVE_KEYS}
                self.assertFalse(lowered_keys, f"{case_id}: sensitive keys {sorted(lowered_keys)}")
                for value in strings_in(case):
                    self.assertFalse(
                        any(pattern.search(value) for pattern in PRIVATE_PATH_PATTERNS),
                        f"{case_id}: private path in fixture",
                    )


if __name__ == "__main__":
    unittest.main()
