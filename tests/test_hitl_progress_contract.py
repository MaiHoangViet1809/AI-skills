"""Deterministic HITL progress contract tests for packaged skills."""

from __future__ import annotations

import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = REPO_ROOT / "skills"
ROUTER_SKILL = "task-router-flow"
CONSUMERS = (
    ROUTER_SKILL,
    "task-execution-flow",
    "task-review-investigate-compare",
    "task-progress-report",
    "sow-delegate-flow",
)
CANONICAL_CONTRACT = (
    SKILLS_ROOT / ROUTER_SKILL / "references" / "scope-of-work.md"
)
PLAN_CONTRACT = SKILLS_ROOT / ROUTER_SKILL / "references" / "plan.md"
ITEM_STATUSES = (
    "PENDING",
    "IN_PROGRESS",
    "AWAITING_VERIFICATION",
    "DONE",
    "BLOCKED",
    "WAITING_HITL",
)


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def require_phrases(test: unittest.TestCase, text: str, phrases: tuple[str, ...]) -> None:
    normalized = normalize(text)
    missing = [phrase for phrase in phrases if normalize(phrase) not in normalized]
    test.assertFalse(missing, f"missing HITL progress contract phrases: {missing}")


def forbid_phrases(test: unittest.TestCase, text: str, phrases: tuple[str, ...]) -> None:
    normalized = normalize(text)
    present = [phrase for phrase in phrases if normalize(phrase) in normalized]
    test.assertFalse(present, f"stale HITL progress contract wording: {present}")


def skill_text(skill_name: str) -> str:
    return (SKILLS_ROOT / skill_name / "SKILL.md").read_text()


class HITLProgressContractTests(unittest.TestCase):
    def test_canonical_contract_owns_hitl_progress_gate(self) -> None:
        text = CANONICAL_CONTRACT.read_text()
        self.assertRegex(text, re.compile(r"^## HITL Progress Gate$", re.MULTILINE))
        require_phrases(
            self,
            text,
            (
                "| Item | Status | Evidence / Pending reason | Next action / Owner |",
                "progress_updated_dttm",
                "stable row key",
                "never renumber on reorder or reuse keys",
                "required human input",
                "user-paused",
                "UNSAVED is a persistence outcome",
                "keep truthful work states",
                "read back saved rows before claiming persistence",
                "dependent tracking unverified",
                "before the existing completion move",
                "base SOW owns base rows",
                "each EXT owns delta rows",
                "draft EXT progress does not amend base scope",
                "on resume, reread the owning record and approval",
                "expected prior content",
                "no-op passes the gate",
                "only when persisted progress changes",
                "an item state",
                "not atomic writes",
                "a DONE item does not complete its SOW/Plan",
                "otherwise N/A",
            ),
        )
        require_phrases(self, text, ITEM_STATUSES)
        forbid_phrases(
            self,
            text,
            (
                "PAUSED lifecycle state",
                "derive task completion from row counts",
                "chat-only summary is sufficient",
                "percentage estimates",
            ),
        )

    def test_optional_plan_reuses_existing_sequence_table(self) -> None:
        text = PLAN_CONTRACT.read_text()
        require_phrases(
            self,
            text,
            (
                "Pending reason / Next action / Owner",
                "reuse SOW Sequence",
                "link child progress",
                "do not copy its item list",
                "child completion alone does not prove Plan completion",
                "progress_updated_dttm",
                "update progress_updated_dttm only on change",
            ),
        )

    def test_all_five_consumers_locate_the_project_or_packaged_contract(self) -> None:
        for skill_name in CONSUMERS:
            with self.subTest(skill=skill_name):
                text = skill_text(skill_name)
                require_phrases(self, text, ("HITL Progress Gate",))

                if skill_name == ROUTER_SKILL:
                    require_phrases(
                        self,
                        text,
                        ("target project's declared contract", "scope-of-work.md"),
                    )
                else:
                    require_phrases(
                        self,
                        text,
                        (
                            "project's declared contract",
                            "task-router-flow",
                            "harness's supplied skill location/catalog",
                            "references/scope-of-work.md",
                            "missing contract",
                            "on resume",
                            "file writeback",
                        ),
                    )

    def test_file_gate_and_final_report_are_separate(self) -> None:
        canonical = CANONICAL_CONTRACT.read_text()
        reporting = skill_text("task-progress-report")
        require_phrases(
            self,
            canonical,
            (
                "before every turn-ending HITL handoff",
                "persist changed progress and read back the result",
                "report UNSAVED plus reason and next action",
            ),
        )
        require_phrases(
            self,
            reporting,
            (
                "one invocation at final task closeout",
                "explicit user status requests",
            ),
        )
        forbid_phrases(
            self,
            reporting,
            ("report once per tool call", "report after each meaningful block"),
        )

    def test_consumer_text_does_not_duplicate_canonical_implementation(self) -> None:
        heading = re.compile(r"^## HITL Progress Gate$", re.MULTILINE)
        for skill_name in CONSUMERS:
            with self.subTest(skill=skill_name):
                self.assertIsNone(
                    heading.search(skill_text(skill_name)),
                    f"{skill_name}: duplicate canonical HITL Progress Gate section",
                )


if __name__ == "__main__":
    unittest.main()
