"""Deterministic package tests for the canonical plan contract.

These tests verify packaged resources, links, registry parity, instructions,
and scenario fixtures. They do not prove actual model adherence to those
instructions.
"""

from __future__ import annotations

import json
import re
import tempfile
import unittest
from pathlib import Path
from typing import Iterable

from scripts.skills.skill_sync_common import copy_skill


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = REPO_ROOT / "skills"
ROUTER_SKILL = "task-router-flow"
PLAN_RELATIVE_PATH = "references/plan.md"
CONSUMER_SKILLS = (
    "task-router-flow",
    "task-review-investigate-compare",
    "task-execution-flow",
    "sow-delegate-flow",
    "task-poc-verification-flow",
    "task-progress-report",
)
CONTRACT_CASE_IDS = {
    "task-router-flow": ("plan-project-authority-001", "plan-routing-optional-001"),
    "task-review-investigate-compare": ("plan-review-contract-001",),
    "task-execution-flow": ("plan-closeout-reopen-001", "plan-execution-gates-001"),
    "sow-delegate-flow": ("plan-delegate-contract-001",),
    "task-poc-verification-flow": ("plan-poc-boundary-001",),
    "task-progress-report": ("plan-progress-acceptance-001",),
}
TEMPLATE_SECTIONS = (
    "1. Goal",
    "2. Scope",
    "3. Change Map",
    "4. SOW Sequence",
    "5. Acceptance",
    "6. Open Decisions",
)


def markdown_local_hrefs(document: Path) -> Iterable[str]:
    text = document.read_text()
    for href in re.findall(r"\]\(([^)]+)\)", text):
        if "://" in href or href.startswith("#") or href.startswith("mailto:"):
            continue
        yield href


def skill_text(skill_name: str) -> str:
    return (SKILLS_ROOT / skill_name / "SKILL.md").read_text()


def consumer_contract_section(skill_name: str) -> tuple[str, ...]:
    sections = {
        ROUTER_SKILL: ("Optional Plan Contract",),
        "task-review-investigate-compare": ("Plan-Backed Review",),
        "sow-delegate-flow": ("Delegate Prompt Contract",),
        "task-poc-verification-flow": ("POC SOW Checklist",),
        "task-progress-report": ("Completion Discipline",),
    }
    if skill_name in sections:
        return sections[skill_name]
    return ("Core Rules", "Execution Loop", "Closeout")


def extract_markdown_section(text: str, heading: str) -> str:
    section = re.search(
        rf"^## {re.escape(heading)}\s*\n(.*?)(?=^## |\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    return section.group(1) if section else ""


class PlanContractIntegrationTests(unittest.TestCase):
    def test_single_canonical_packaged_plan_template(self) -> None:
        plan_templates = sorted(path for path in SKILLS_ROOT.rglob("plan.md") if path.is_file())
        expected = SKILLS_ROOT / ROUTER_SKILL / "references" / "plan.md"
        self.assertEqual([expected], plan_templates)
        self.assertFalse((REPO_ROOT / "TEMPLATE_PLAN.md").exists())

        text = expected.read_text()
        self.assertNotIn("Plan Template (Draft)", text)
        self.assertNotIn("Draft, not yet active", text)
        template_block = re.search(r"^## Template\s+```md\n(.*?)^```$", text, flags=re.MULTILINE | re.DOTALL)
        self.assertIsNotNone(template_block)
        headings = re.findall(r"^## (.+)$", template_block.group(1), flags=re.MULTILINE)
        self.assertEqual(list(TEMPLATE_SECTIONS), headings)
        self.assertIn("[Scope of Work](scope-of-work.md)", text)
        self.assertNotIn("skills/task-router-flow/references/scope-of-work.md", text)
        self.assertIn("only when the user requests it", text)
        self.assertIn("scope is so", text)
        self.assertIn("large that", text)
        self.assertIn("Multiple files", text)

    def test_registry_parity_for_router_resources(self) -> None:
        registry = json.loads((SKILLS_ROOT / "registry.json").read_text())
        router_entry = next(
            (entry for entry in registry["skills"] if entry["name"] == ROUTER_SKILL),
            None,
        )
        self.assertIsNotNone(router_entry)
        registered_paths = {item["path"] for item in router_entry["files"]}
        actual_paths = {
            path.relative_to(REPO_ROOT).as_posix()
            for path in (SKILLS_ROOT / ROUTER_SKILL).rglob("*")
            if path.is_file()
        }
        self.assertEqual(actual_paths, registered_paths)

        plan_path = f"skills/{ROUTER_SKILL}/{PLAN_RELATIVE_PATH}"
        self.assertIn(plan_path, registered_paths)
        plan_entry = next(item for item in router_entry["files"] if item["path"] == plan_path)
        expected_url = (
            "https://raw.githubusercontent.com/MaiHoangViet1809/AI-skills/main/"
            f"skills/{ROUTER_SKILL}/{PLAN_RELATIVE_PATH}"
        )
        self.assertEqual(expected_url, plan_entry["raw_url"])

    def assert_local_links_stay_in_package(self, skill_root: Path) -> None:
        for document in skill_root.rglob("*.md"):
            for href in markdown_local_hrefs(document):
                destination = (document.parent / href.split("#", 1)[0]).resolve()
                self.assertTrue(
                    destination.is_relative_to(skill_root.resolve()),
                    f"{document}: cross-package link {href}",
                )
                self.assertTrue(destination.exists(), f"{document}: missing link {href}")

    def test_full_copy_layout_contains_owner_and_local_links(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            target_root = Path(temp) / "skills"
            for skill_name in CONSUMER_SKILLS:
                result = copy_skill(
                    skill_name,
                    SKILLS_ROOT / skill_name,
                    target_root,
                    overwrite=False,
                    dry_run=False,
                )
                self.assertTrue(result.copied, skill_name)

            installed_plan = target_root / ROUTER_SKILL / PLAN_RELATIVE_PATH
            self.assertTrue(installed_plan.is_file())
            self.assert_local_links_stay_in_package(target_root / ROUTER_SKILL)
            for skill_name in CONSUMER_SKILLS:
                self.assert_local_links_stay_in_package(target_root / skill_name)
            self.assertEqual(
                [target_root / ROUTER_SKILL / PLAN_RELATIVE_PATH],
                sorted(target_root.rglob("plan.md")),
            )

    def test_subset_copy_without_owner_keeps_consumer_package_standalone(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            for skill_name in CONSUMER_SKILLS:
                if skill_name == ROUTER_SKILL:
                    continue
                target_root = Path(temp) / skill_name
                result = copy_skill(
                    skill_name,
                    SKILLS_ROOT / skill_name,
                    target_root,
                    overwrite=False,
                    dry_run=False,
                )
                self.assertTrue(result.copied, skill_name)
                self.assertFalse((target_root / ROUTER_SKILL).exists())
                self.assertFalse(list(target_root.rglob("plan.md")))
                self.assert_local_links_stay_in_package(target_root / skill_name)

    def test_consumer_instructions_guard_plan_applicability(self) -> None:
        project_first_locks = ("declared contract", "declared plan contract")
        missing_contract_locks = ("missing", "unavailable")
        shared_locks = (
            "task-router-flow",
            "location/catalog",
            "unverified",
            "do not invent",
            "auto-install",
        )
        for skill_name in CONSUMER_SKILLS:
            with self.subTest(skill=skill_name):
                full_text = skill_text(skill_name).lower()
                self.assertTrue(
                    any(lock in full_text for lock in project_first_locks),
                    skill_name,
                )
                self.assertTrue(
                    any(lock in full_text for lock in missing_contract_locks),
                    skill_name,
                )
                for lock in shared_locks:
                    with self.subTest(skill=skill_name, shared_lock=lock):
                        self.assertIn(lock, full_text)
                section_text = "\n".join(
                    extract_markdown_section(skill_text(skill_name), section)
                    for section in consumer_contract_section(skill_name)
                ).lower()
                self.assertTrue(section_text, skill_name)
                if skill_name == ROUTER_SKILL:
                    role_locks = (
                        "target-repo guardrails",
                        "map original goal",
                        "does not require a new sow",
                        "grant implementation approval",
                    )
                elif skill_name == "task-review-investigate-compare":
                    role_locks = (
                        "goal",
                        "scope",
                        "sow scope",
                        "material unknowns",
                        "evidence",
                    )
                elif skill_name == "task-execution-flow":
                    role_locks = (
                        "standalone tasks need no plan",
                        "map the sow to its goal",
                        "dependency exit gates",
                        "update sow sequence and acceptance",
                        "outcomes, preservation/ownership locks",
                    )
                elif skill_name == "sow-delegate-flow":
                    role_locks = (
                        "applicable contract",
                        "parent goal",
                        "dependency gates",
                        "standalone sow",
                        "coordinator ownership",
                    )
                elif skill_name == "task-poc-verification-flow":
                    role_locks = (
                        "parent `g#`",
                        "declared proof boundary",
                        "prototype-only",
                        "full delivery",
                        "standalone poc",
                    )
                else:
                    role_locks = ("plan acceptance", "closed-sow counts", "separately", "overall x/y")
                for lock in role_locks:
                    with self.subTest(skill=skill_name, role_lock=lock):
                        self.assertTrue(lock in section_text or lock in full_text, lock)

    def test_fixture_scenarios_cover_plan_contract_matrix(self) -> None:
        fixture_root = REPO_ROOT / "tests" / "skill_feedback_cases"
        for skill_name in CONSUMER_SKILLS:
            fixture = fixture_root / f"{skill_name}.json"
            self.assertTrue(fixture.is_file(), skill_name)
            payload = json.loads(fixture.read_text())
            kinds = {scenario["kind"] for case in payload["cases"] for scenario in case["scenarios"]}
            self.assertEqual({"expected", "negative", "boundary"}, kinds, skill_name)

        case_ids = {
            case_id
            for fixture in fixture_root.glob("*.json")
            for case_id in (case["id"] for case in json.loads(fixture.read_text())["cases"])
        }
        required_case_ids = {
            case_id for ids in CONTRACT_CASE_IDS.values() for case_id in ids
        }
        self.assertLessEqual(required_case_ids, case_ids)

        for skill_name, required_ids in CONTRACT_CASE_IDS.items():
            with self.subTest(skill=skill_name):
                payload = json.loads((fixture_root / f"{skill_name}.json").read_text())
                actual_ids = {case["id"] for case in payload["cases"]}
                self.assertLessEqual(set(required_ids), actual_ids)


if __name__ == "__main__":
    unittest.main()
