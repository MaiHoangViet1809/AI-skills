"""Focused tests for the default planning bundle contract.

The file-layout scenarios below are simulated in temporary directories. They
verify the packaged contract text and deterministic structural outcomes, not
actual agent adherence to those instructions.
"""

from __future__ import annotations

import re
import tempfile
import unittest
from datetime import datetime
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
BUNDLE_CONTRACT = REPO_ROOT / "skills/task-router-flow/references/planning-bundles.md"
ID_PATTERN = r"[A-Z0-9]{8}"
SOW_ID = "SOW_20261007_8A3R5M7D"
EXT_ID = "SOW_20261007_8A3R5M7D_EXT_6P8D3V9B"
PLAN_ID = "PLAN_20261007_4T9W2N6C"


def write_record(path: Path, *, finish: str = "2026-10-07T11:20:30+07:00") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(
            (
                f"# {path.stem}",
                f"- Status: {'IN_PROGRESS' if finish == 'null' else 'DONE'}",
                "- Approval: APPROVED",
                "- create_dttm: 2026-10-07T10:00:00+07:00",
                "- approve_dttm: 2026-10-07T10:01:00+07:00",
                f"- finish_dttm: {finish}",
            )
        )
        + "\n"
    )


def ensure_lifecycle_roots(root: Path) -> None:
    (root / "active").mkdir(parents=True, exist_ok=True)
    (root / "finished").mkdir(parents=True, exist_ok=True)


def set_finish(path: Path, value: str) -> None:
    text = path.read_text()
    text = re.sub(r"(?m)^- finish_dttm: .*$", f"- finish_dttm: {value}", text)
    status = "IN_PROGRESS" if value == "null" else "DONE"
    path.write_text(re.sub(r"(?m)^- Status: .*$", f"- Status: {status}", text))


def assert_still_done(*paths: Path) -> None:
    for path in paths:
        assert path.is_file(), path
        assert "- finish_dttm: 2026-10-07T11:20:30+07:00" in path.read_text(), path


class PlanningBundleContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.contract = re.sub(r"\s+", " ", BUNDLE_CONTRACT.read_text())

    def test_identity_lock_covers_valid_invalid_and_stable_ids(self) -> None:
        valid = re.compile(rf"^SOW_20261007_{ID_PATTERN}$")
        invalid = (
            "SOW_2026-10-07_8A3R5M7D",
            "SOW_20261007_8a3r5m7d",
            "SOW_20261007_8A3R5M7",
            "SOW_20261007_8A3R5M7DX",
            "SOW_20261007_8A3R5M_",
            "SOW_20261007_A3-R5M7D",
        )
        self.assertTrue(valid.fullmatch(SOW_ID))
        for value in invalid:
            self.assertIsNone(valid.fullmatch(value), value)
        for lock in (
            "SOW_YYYYMMDD_RANDOM8",
            "PLAN_YYYYMMDD_RANDOM8",
            "exactly eight independently random uppercase ASCII letters or digits",
            "including nested Plan bundles, namespaces and finished work",
            "regenerate on collision",
            "assigned once and remains unchanged",
            "never silently rename an approved identity",
            "Do not add a persistent allocator",
        ):
            with self.subTest(lock=lock):
                self.assertIn(lock, self.contract)
        self.assertNotIn("next available sequential index", self.contract)

    def test_placement_and_project_authority_locks(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "plan_todo"
            ensure_lifecycle_roots(root)
            standalone = root / "active" / SOW_ID
            write_record(standalone / f"{SOW_ID}_contract.md", finish="null")
            nested = root / "active" / PLAN_ID / SOW_ID
            write_record(nested / f"{SOW_ID}_child.md", finish="null")

            self.assertEqual(SOW_ID, standalone.name)
            self.assertEqual(root / "active" / SOW_ID, standalone)
            self.assertEqual(root / "active" / PLAN_ID / SOW_ID, nested)
            self.assertTrue(standalone.parent != nested.parent)

        for lock in (
            "A standalone SOW folder is only the full SOW ID",
            "Only a Plan-backed SOW folder is a child of a Plan folder",
            "<SOW_ID>_<task_name>.md",
            "<PLAN_ID>_<plan_name>.md",
            "declared planning roots and namespaces",
            "A project may override",
            "declared authority wins",
            "Do not auto-edit a target project's `AGENTS.md`",
        ):
            with self.subTest(lock=lock):
                self.assertIn(lock, self.contract)

    def test_calendar_and_duplicate_inventory_examples(self) -> None:
        # Calendar validity supplements the shape check; no product allocator exists.
        self.assertEqual(2026, datetime.strptime("20261007", "%Y%m%d").year)
        for invalid in ("20260230", "20261301"):
            with self.assertRaises(ValueError):
                datetime.strptime(invalid, "%Y%m%d")
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            first = root / "codex/active" / SOW_ID
            second = root / "other/finished" / PLAN_ID / SOW_ID
            write_record(first / f"{SOW_ID}_first.md")
            write_record(second / f"{SOW_ID}_second.md")
            matches = [p for p in root.rglob(SOW_ID) if p.is_dir()]
            self.assertEqual({first, second}, set(matches))
            self.assertIn("incoming draft and repair its references", self.contract)
            self.assertIn("never silently rename an approved identity", self.contract)

    def test_optional_plan_adoption_and_legacy_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "plan_todo"
            ensure_lifecycle_roots(root)
            sow = root / "active" / SOW_ID
            write_record(sow / f"{SOW_ID}_contract.md", finish="null")
            plan = root / "active" / PLAN_ID
            write_record(plan / f"{PLAN_ID}_plan.md", finish="null")

            adopted = plan / sow.name
            sow.rename(adopted)
            self.assertFalse(sow.exists())
            self.assertEqual(plan / SOW_ID, adopted)
            self.assertTrue((adopted / f"{SOW_ID}_contract.md").is_file())

        for lock in (
            "Plan remains optional",
            "Creating a SOW does not require a Plan",
            "Move its whole folder into the Plan bundle, retain its ID",
            "already using this format",
            "Legacy records remain linked",
            "separately approved migration SOW",
        ):
            with self.subTest(lock=lock):
                self.assertIn(lock, self.contract)

    def test_extension_approval_and_decision_ownership_locks(self) -> None:
        self.assertRegex(EXT_ID, rf"^SOW_\d{{8}}_{ID_PATTERN}_EXT_{ID_PATTERN}$")
        with tempfile.TemporaryDirectory() as temp:
            sow = Path(temp) / "plan_todo/active" / SOW_ID
            write_record(sow / f"{SOW_ID}_contract.md", finish="null")
            write_record(sow / f"{EXT_ID}_scope.md", finish="null")
            (sow / f"{SOW_ID}_decision.md").write_text(
                "# Decision\n2026-10-07: context, options, choice, tradeoffs, risks\n"
            )
            plan = Path(temp) / "plan_todo/active" / PLAN_ID
            write_record(plan / f"{PLAN_ID}_plan.md", finish="null")
            (plan / f"{PLAN_ID}_decision.md").write_text("# Plan decision\n")

            self.assertTrue((sow / f"{SOW_ID}_decision.md").is_file())
            self.assertTrue((plan / f"{PLAN_ID}_decision.md").is_file())

        for lock in (
            "<SOW_ID>_EXT_<RANDOM8>_<name>.md",
            "parent SOW folder",
            "own lifecycle fields and approval",
            "scope delta",
            "Record extension order and dependencies in the parent SOW",
            "DRAFT extension does not amend approved scope",
            "maximum of three approved extensions",
            "<SOW_ID>_decision.md",
            "<PLAN_ID>_decision.md",
            "Link to a shared decision instead of duplicating it",
        ):
            with self.subTest(lock=lock):
                self.assertIn(lock, self.contract)

    def test_partial_and_aggregate_plan_completion(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "plan_todo"
            ensure_lifecycle_roots(root)
            plan = root / "active" / PLAN_ID
            write_record(plan / f"{PLAN_ID}_plan.md", finish="null")
            first = plan / SOW_ID
            write_record(first / f"{SOW_ID}_first.md")
            second = plan / "SOW_20261007_9B4T6N8E"
            write_record(second / "SOW_20261007_9B4T6N8E_second.md", finish="null")

            self.assertTrue(first.is_dir())
            self.assertTrue(second.is_dir())
            self.assertIn("active", first.relative_to(root).parts)
            self.assertFalse((root / "finished" / PLAN_ID).exists())
            set_finish(second / "SOW_20261007_9B4T6N8E_second.md", "2026-10-07T11:59:00+07:00")
            set_finish(plan / f"{PLAN_ID}_plan.md", "2026-10-07T12:00:00+07:00")

            finished_plan = root / "finished" / plan.name
            plan.rename(finished_plan)
            self.assertFalse(plan.exists())
            self.assertTrue((finished_plan / SOW_ID / f"{SOW_ID}_first.md").is_file())
            self.assertTrue((finished_plan / "SOW_20261007_9B4T6N8E").is_dir())

        for lock in (
            "A completed SOW inside an active Plan stays in place",
            "Only aggregate verified Plan completion moves the entire Plan bundle",
            "repair references",
        ):
            with self.subTest(lock=lock):
                self.assertIn(lock, self.contract)

    def test_reopen_preserves_completed_siblings_and_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "plan_todo"
            ensure_lifecycle_roots(root)
            plan = root / "finished" / PLAN_ID
            write_record(plan / f"{PLAN_ID}_plan.md")
            sibling = plan / "SOW_20261007_9B4T6N8E"
            write_record(sibling / "SOW_20261007_9B4T6N8E_sibling.md")
            reopened = plan / SOW_ID
            write_record(reopened / f"{SOW_ID}_parent.md")
            ext = reopened / f"{EXT_ID}_scope.md"
            write_record(ext)
            sibling_ext = reopened / f"{SOW_ID}_EXT_ABC12345_previous.md"
            write_record(sibling_ext)

            active_plan = root / "active" / plan.name
            plan.rename(active_plan)
            active_parent = active_plan / reopened.name
            set_finish(active_parent / f"{SOW_ID}_parent.md", "null")
            set_finish(active_parent / f"{EXT_ID}_scope.md", "null")
            set_finish(active_plan / f"{PLAN_ID}_plan.md", "null")
            assert_still_done(
                active_plan / sibling.name / "SOW_20261007_9B4T6N8E_sibling.md",
                active_parent / sibling_ext.name,
            )

            self.assertTrue(active_plan.is_dir())
            self.assertIn("null", (active_parent / f"{SOW_ID}_parent.md").read_text())
            self.assertIn("null", (active_parent / f"{EXT_ID}_scope.md").read_text())
            self.assertIn("null", (active_plan / f"{PLAN_ID}_plan.md").read_text())
            for path in (active_parent / f"{SOW_ID}_parent.md", active_parent / f"{EXT_ID}_scope.md", active_plan / f"{PLAN_ID}_plan.md"):
                self.assertIn("- Status: IN_PROGRESS", path.read_text())

        for lock in (
            "Move the owning finished bundle back to the active root",
            "Clear only the reopened scope's and affected ancestors' completion timestamps",
            "completed sibling SOW/EXT timestamps",
            "A DRAFT EXT alone does not reopen them",
            "Status, location or a lifecycle field alone never grants approval",
        ):
            with self.subTest(lock=lock):
                self.assertIn(lock, self.contract)

    def test_simulated_negative_cases_leave_history_in_place(self) -> None:
        # No runtime planner is being tested: these are explicit contract examples.
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            legacy = root / "finished/SOW_0093_old.md"
            finished_plan = root / "finished" / PLAN_ID
            write_record(legacy)
            write_record(finished_plan / f"{PLAN_ID}_plan.md")
            before = {p: p.read_bytes() for p in root.rglob("*.md")}
            draft_ext = finished_plan / SOW_ID / f"{EXT_ID}_draft.md"
            draft_ext.parent.mkdir()
            draft_ext.write_text("- Status: DRAFT\n- Approval: PENDING\n- finish_dttm: null\n")
            evidence_plan = root / "active/PLAN_20261008_ABCD1234"
            evidence_plan.mkdir(parents=True)
            reference = evidence_plan / "PLAN_20261008_ABCD1234_evidence.md"
            reference.write_text("[Prior evidence](../../finished/SOW_0093_old.md)\n")
            for path, content in before.items():
                self.assertEqual(content, path.read_bytes())
            self.assertFalse((root / "active" / PLAN_ID).exists())
            self.assertTrue(legacy.is_file())
            self.assertTrue((reference.parent / "../../finished/SOW_0093_old.md").resolve().is_file())
        for lock in (
            "A finished SOW used only as prior evidence stays linked in place",
            "A DRAFT extension does not amend approved scope",
            "Legacy records remain linked under their recorded contract",
            "A project may override ID format, placement",
        ):
            self.assertIn(lock, self.contract)
