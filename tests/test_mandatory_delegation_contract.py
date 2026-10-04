"""Deterministic contract tests for mandatory available GLM-5.3-max delegation.

These tests verify packaged skill text, discovery metadata, and feedback
fixtures. They do not prove runtime model adherence.
"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = REPO_ROOT / "skills"
FIXTURES_ROOT = REPO_ROOT / "tests" / "skill_feedback_cases"
EXECUTION_SKILL = "task-execution-flow"
DELEGATE_SKILL = "sow-delegate-flow"
REVIEW_SKILL = "task-review-investigate-compare"
TARGET_SKILLS = (EXECUTION_SKILL, DELEGATE_SKILL, REVIEW_SKILL)
EXACT_MODEL = "greennode/glm-5.3"
EXACT_EFFORT = "reasoning_effort=max"


def skill_path(skill_name: str) -> Path:
    return SKILLS_ROOT / skill_name / "SKILL.md"


def metadata_path(skill_name: str) -> Path:
    return SKILLS_ROOT / skill_name / "agents" / "openai.yaml"


def fixture_path(skill_name: str) -> Path:
    return FIXTURES_ROOT / f"{skill_name}.json"


def skill_text(skill_name: str) -> str:
    return skill_path(skill_name).read_text()


def metadata(skill_name: str) -> dict[str, Any]:
    payload = yaml.safe_load(metadata_path(skill_name).read_text())
    assert isinstance(payload, dict)
    return payload


def fixture_cases(skill_name: str) -> list[dict[str, Any]]:
    payload = json.loads(fixture_path(skill_name).read_text())
    cases = payload["cases"]
    assert isinstance(cases, list)
    return cases


def mandatory_cases(skill_name: str) -> list[dict[str, Any]]:
    cases = fixture_cases(skill_name)
    selected = [
        case
        for case in cases
        if EXACT_MODEL in json.dumps(case) or "GLM-5.3" in json.dumps(case)
    ]
    assert selected, f"{skill_name}: no GLM-5.3 contract fixture case"
    return selected


def assert_locks(test: unittest.TestCase, text: str, locks: tuple[str, ...]) -> None:
    lowered = text.lower()
    missing = [lock for lock in locks if lock.lower() not in lowered]
    test.assertFalse(missing, f"missing contract locks: {missing}")


def assert_not_locks(test: unittest.TestCase, text: str, locks: tuple[str, ...]) -> None:
    lowered = text.lower()
    present = [lock for lock in locks if lock.lower() in lowered]
    test.assertFalse(present, f"stale contradictory contract wording: {present}")


class MandatoryDelegationContractTests(unittest.TestCase):
    def test_execution_requires_delegation_when_exact_target_is_available(self) -> None:
        text = skill_text(EXECUTION_SKILL)
        assert_locks(
            self,
            text,
            (
                "mandatory GLM-5.3-max delegation gate",
                EXACT_MODEL,
                EXACT_EFFORT,
                "safe bounded slice",
                "do not skip because the work is simple, mechanical, routine, costly, or judged unsuitable",
                "confirmed unavailability",
                "observed delegation failure",
                "record capability evidence",
                "record concrete evidence",
                "user override",
                "stop for scope/authority clarification",
            ),
        )
        assert_not_locks(
            self,
            text,
            (
                "preference, not a hard gate",
                "prefer one bounded delegated slice",
                "otherwise execute locally",
                "explicit local-only, unsafe, unbounded, or unverifiable -> execute locally",
            ),
        )

    def test_delegate_owns_transport_failure_and_cleanup_contract(self) -> None:
        text = skill_text(DELEGATE_SKILL)
        assert_locks(
            self,
            text,
            (
                EXACT_MODEL,
                EXACT_EFFORT,
                "current native catalog",
                "documented provider transport",
                "flash-thirdparty",
                "aliases, stale role names",
                "confirmed launch",
                "transport",
                "session",
                "isolation error",
                "terminal child failure",
                "delegate output",
                "failed stage",
                "concrete error or capability evidence",
                "task impact",
                "fallback decision",
                "clean up failed task-owned sessions",
                "discard invalid output",
                "fork_turns: \"none\"",
                "brand-new provider-owned session",
                "coordinator verification",
                "read-only",
                "before approval",
                "not required to spawn nested",
            ),
        )
        assert_not_locks(
            self,
            text,
            (
                "do not spawn an independent delegate for a simple status",
                "routine local check",
                "optional independent review",
                "for an optional independent pass",
            ),
        )

    def test_review_requires_exact_reviewer_and_keeps_coordinator_owner(self) -> None:
        text = skill_text(REVIEW_SKILL)
        assert_locks(
            self,
            text,
            (
                "mandatory GLM-5.3-max",
                EXACT_MODEL,
                EXACT_EFFORT,
                "current native catalog",
                "documented provider transport",
                "flash-thirdparty",
                "aliases, stale role names",
                "confirmed unavailability",
                "observed delegation failure",
                "record capability evidence",
                "record concrete evidence",
                "user override",
                "fork_turns: \"none\"",
                "brand-new provider-owned session",
                "coordinator owns the review conclusion",
                "read-only and advisory",
            ),
        )
        assert_not_locks(
            self,
            text,
            (
                "use an independent pass only",
                "keep simple status",
                "routine local checks coordinator-only",
                "for an optional independent pass",
                "skipped by the bounded trigger",
            ),
        )

    def test_discovery_metadata_has_no_optional_delegation_wording(self) -> None:
        stale_words = ("optional", "preference", "suitability", "unsuitable")
        for skill_name in TARGET_SKILLS:
            with self.subTest(skill=skill_name):
                payload = metadata(skill_name)
                rendered = json.dumps(payload, sort_keys=True).lower()
                present = [word for word in stale_words if word in rendered]
                self.assertFalse(present, f"{skill_name}: stale metadata wording {present}")

        execution_metadata = json.dumps(metadata(EXECUTION_SKILL)).lower()
        self.assertIn("mandatory", execution_metadata)
        self.assertIn("glm-5.3-max", execution_metadata)

    def test_fixtures_cover_mandatory_branch_and_boundary_matrix(self) -> None:
        for skill_name in TARGET_SKILLS:
            with self.subTest(skill=skill_name):
                cases = mandatory_cases(skill_name)
                rendered = json.dumps(cases)
                self.assertIn(EXACT_MODEL, rendered)
                self.assertIn(EXACT_EFFORT, rendered)
                kinds = {
                    scenario["kind"]
                    for case in cases
                    for scenario in case["scenarios"]
                }
                self.assertEqual({"expected", "negative", "boundary"}, kinds)

        execution_cases = json.dumps(mandatory_cases(EXECUTION_SKILL)).lower()
        delegate_cases = json.dumps(mandatory_cases(DELEGATE_SKILL)).lower()
        review_cases = json.dumps(mandatory_cases(REVIEW_SKILL)).lower()

        self.assertIn("simple", execution_cases)
        self.assertIn("flash-only", execution_cases)
        self.assertIn("unavailable", execution_cases)
        self.assertIn("user override", execution_cases)
        self.assertIn("unapproved implementation", execution_cases)
        self.assertIn("unsafe context", execution_cases)
        self.assertIn("failed coordinator verification", execution_cases)

        self.assertIn("launch failure", delegate_cases)
        self.assertIn("runtime failure", delegate_cases)
        self.assertIn("isolation failure", delegate_cases)
        self.assertIn("invalid delegate output", delegate_cases)
        self.assertIn("nested", delegate_cases)
        self.assertIn("cleanup", delegate_cases)

        self.assertIn("read-only", review_cases)
        self.assertIn("before approval", review_cases)
        self.assertIn("coordinator verification", review_cases)

        stale_fixture_wording = (
            "optional",
            "suitability",
            "optional skip",
            "suitability skip",
            "skip delegation",
            "skipping delegation",
            "suitability reason",
            "when suitable",
            "otherwise keep the coordinator local",
            "routine status",
            "optional independent review",
            "does not need an independent pass",
            "suitability decision",
        )
        for skill_name in TARGET_SKILLS:
            with self.subTest(stale_fixture=skill_name):
                rendered = json.dumps(mandatory_cases(skill_name)).lower()
                present = [phrase for phrase in stale_fixture_wording if phrase in rendered]
                self.assertFalse(present, f"{skill_name}: stale fixture wording {present}")

    def test_contract_has_no_stale_section_heading(self) -> None:
        execution_text = skill_text(EXECUTION_SKILL)
        self.assertNotRegex(execution_text, re.compile(r"^## Delegation Suitability Gate$", re.MULTILINE))


if __name__ == "__main__":
    unittest.main()
