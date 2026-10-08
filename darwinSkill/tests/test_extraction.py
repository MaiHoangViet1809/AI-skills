from __future__ import annotations

import unittest

from darwinSkill.src.extraction import (
    CallbackEvidenceInterpreter,
    EvidenceBundle,
    build_evidence_bundle,
    build_trainable_examples,
    segment_session_into_work_units,
)
from darwinSkill.src.provider_logs import (
    ArtifactReference,
    ProviderMessage,
    ProviderPatchEvent,
    ProviderSession,
    ProviderTaskEvent,
    ProviderToolResult,
    ProviderTurn,
    PatchChange,
)


def _session_with_turns(*turns: ProviderTurn) -> ProviderSession:
    return ProviderSession(
        provider="codex",
        source_format_version="codex_session_jsonl_v1",
        session_id="session-1",
        transcript_path="/tmp/codex-session.jsonl",
        cwd="/repo",
        started_at="2026-05-29T10:00:00Z",
        turns=list(turns),
    )


def _anchor_turn(turn_id: str, user_text: str, assistant_text: str) -> ProviderTurn:
    timestamp = "2026-05-29T10:00:01Z"
    return ProviderTurn(
        turn_id=turn_id,
        timestamp=timestamp,
        cwd="/repo",
        messages=[
            ProviderMessage(f"user-{turn_id}", turn_id, timestamp, "user", user_text),
            ProviderMessage(f"assistant-{turn_id}", turn_id, timestamp, "assistant", assistant_text),
        ],
        task_events=[ProviderTaskEvent(f"task-{turn_id}", turn_id, timestamp, "task_complete", "done")],
    )


class ExtractionTest(unittest.TestCase):
    def test_segment_session_links_short_continuation_turns(self) -> None:
        turn1 = ProviderTurn(
            turn_id="turn-1",
            timestamp="2026-05-29T10:00:01Z",
            cwd="/repo",
            messages=[
                ProviderMessage("m1", "turn-1", "2026-05-29T10:00:01Z", "user", "Implement SOW_0058 parser"),
                ProviderMessage("m2", "turn-1", "2026-05-29T10:00:02Z", "assistant", "I will start with the parser."),
            ],
            task_events=[ProviderTaskEvent("t1", "turn-1", "2026-05-29T10:00:03Z", "task_complete", "parser drafted")],
            artifact_refs=[ArtifactReference(ref_id="a1", ref_type="transcript", path="/tmp/codex-session.jsonl")],
        )
        turn2 = ProviderTurn(
            turn_id="turn-2",
            timestamp="2026-05-29T10:05:01Z",
            cwd="/repo",
            messages=[
                ProviderMessage("m3", "turn-2", "2026-05-29T10:05:01Z", "user", "tiếp tục"),
                ProviderMessage("m4", "turn-2", "2026-05-29T10:05:02Z", "assistant", "quality check passed"),
            ],
            task_events=[ProviderTaskEvent("t2", "turn-2", "2026-05-29T10:05:03Z", "task_complete", "done")],
            artifact_refs=[ArtifactReference(ref_id="a2", ref_type="transcript", path="/tmp/codex-session.jsonl")],
        )

        work_units = segment_session_into_work_units(_session_with_turns(turn1, turn2))

        self.assertEqual(len(work_units), 1)
        self.assertEqual(work_units[0].scope_anchor, "SOW_0058")
        self.assertEqual(work_units[0].turn_ids, ["turn-1", "turn-2"])
        self.assertEqual(work_units[0].task_family, "SOW_0058")
        self.assertEqual(work_units[0].metadata["followup_prompts"], ["tiếp tục"])
        self.assertEqual(work_units[0].metadata["merged_turn_ids"], ["turn-1", "turn-2"])

    def test_new_id_segmentation_and_example_generation_preserve_full_anchor(self) -> None:
        anchor = "SOW_20261008_ABCDEF12"
        turn1 = _anchor_turn("turn-1", f"Implement {anchor} parser", "Starting the parser.")
        turn2 = _anchor_turn("turn-2", "continue", "quality check passed")

        work_units = segment_session_into_work_units(_session_with_turns(turn1, turn2))
        example = build_trainable_examples(_session_with_turns(turn1, turn2))[0]

        self.assertEqual(len(work_units), 1)
        self.assertEqual(work_units[0].scope_anchor, anchor)
        self.assertEqual(work_units[0].task_family, anchor)
        self.assertEqual(work_units[0].turn_ids, ["turn-1", "turn-2"])
        self.assertEqual(example.skill_name, anchor)
        self.assertEqual(example.task_family, anchor)
        self.assertEqual(example.metadata["merged_turn_ids"], ["turn-1", "turn-2"])

    def test_filename_and_ext_suffixes_return_parent_anchor(self) -> None:
        cases = {
            "Review (SOW_20261008_ABCDEF12).": "SOW_20261008_ABCDEF12",
            "Update plan_todo/SOW_0058_EXT_01_fix.md": "SOW_0058",
            "Update SOW_0058_name.md": "SOW_0058",
            "Update plan_todo/SOW_20261008_ABCDEF12_EXT_12345678_fix.md": "SOW_20261008_ABCDEF12",
            "Update SOW_20261008_ABCDEF12_fix.md": "SOW_20261008_ABCDEF12",
        }
        for user_text, expected_anchor in cases.items():
            with self.subTest(user_text=user_text):
                session = _session_with_turns(_anchor_turn("turn-1", user_text, "Updated the file."))
                work_unit = segment_session_into_work_units(session)[0]
                example = build_trainable_examples(session)[0]

                self.assertEqual(work_unit.scope_anchor, expected_anchor)
                self.assertEqual(example.skill_name, expected_anchor)
                self.assertEqual(example.task_family, expected_anchor)

    def test_rejects_malformed_and_attached_anchors(self) -> None:
        cases = (
            "Review the parser without a scope reference.",
            "Review SOW_20261008.",
            "Review SOW_20261008_ABCDEF1.",
            "Review SOW_20261008_ABCDEF123.",
            "Review SOW_20261008_abcdef12.",
            "Review PREFIXSOW_20261008_ABCDEF12.",
            "Review SOW_20261008_ABCDEF12X.",
            "Review SOW_0058X.",
        )
        for user_text in cases:
            with self.subTest(user_text=user_text):
                work_unit = segment_session_into_work_units(
                    _session_with_turns(_anchor_turn("turn-1", user_text, "No valid anchor."))
                )[0]

                self.assertEqual(work_unit.scope_anchor, "")
                self.assertFalse(work_unit.mixed_context)

    def test_parent_and_ext_references_share_one_scope(self) -> None:
        anchor = "SOW_20261008_ABCDEF12"
        session = _session_with_turns(_anchor_turn(
            "turn-1", f"Review {anchor}", f"Read {anchor}_EXT_12345678_fix.md."
        ))
        unit = segment_session_into_work_units(session)[0]
        self.assertEqual(unit.scope_anchor, anchor)
        self.assertFalse(unit.mixed_context)
        self.assertFalse(build_trainable_examples(session)[0].metadata["mixed_context"])

    def test_metadata_only_anchor_paths_are_not_scanned(self) -> None:
        timestamp = "2026-05-29T10:00:01Z"
        turn = ProviderTurn(
            turn_id="turn-1",
            timestamp=timestamp,
            cwd="/repo",
            messages=[
                ProviderMessage("m1", "turn-1", timestamp, "user", "Continue the update."),
                ProviderMessage("m2", "turn-1", timestamp, "assistant", "No anchor appears in messages."),
            ],
            task_events=[ProviderTaskEvent("t1", "turn-1", timestamp, "task_complete", "done")],
            artifact_refs=[
                ArtifactReference(
                    ref_id="a1",
                    ref_type="transcript",
                    path="/tmp/SOW_20261008_ABCDEF12.jsonl",
                )
            ],
        )
        session = ProviderSession(
            provider="codex",
            source_format_version="codex_session_jsonl_v1",
            session_id="session-1",
            transcript_path="/tmp/SOW_20261008_ABCDEF12.jsonl",
            cwd="/repo",
            started_at="2026-05-29T10:00:00Z",
            turns=[turn],
        )

        work_unit = segment_session_into_work_units(session)[0]

        self.assertEqual(work_unit.scope_anchor, "")
        self.assertFalse(work_unit.mixed_context)

    def test_same_date_ids_remain_distinct_and_mixed_context_abstains(self) -> None:
        anchor_a = "SOW_20261008_ABCDEF12"
        anchor_b = "SOW_20261008_ABCDEF34"
        separate_units = segment_session_into_work_units(
            _session_with_turns(
                _anchor_turn("turn-1", f"Implement {anchor_a}", "Done."),
                _anchor_turn("turn-2", f"Implement {anchor_b}", "Done."),
            )
        )
        self.assertEqual([unit.scope_anchor for unit in separate_units], [anchor_a, anchor_b])

        mixed_prompts = (
            f"Compare {anchor_a} and {anchor_b}.",
            f"Compare {anchor_a} and SOW_0058.",
        )
        for prompt in mixed_prompts:
            with self.subTest(prompt=prompt):
                session = _session_with_turns(_anchor_turn("turn-1", prompt, "Inspect both scopes."))
                work_unit = segment_session_into_work_units(session)[0]
                example = build_trainable_examples(session)[0]

                self.assertTrue(work_unit.mixed_context)
                self.assertEqual(example.outcome_label, "abstain")
                self.assertEqual(example.outcome_class, "insufficient_evidence")
                self.assertEqual(example.gap_type, "mixed_context")

    def test_build_trainable_examples_abstains_on_mixed_context(self) -> None:
        turn = ProviderTurn(
            turn_id="turn-1",
            timestamp="2026-05-29T10:00:01Z",
            messages=[
                ProviderMessage(
                    "m1",
                    "turn-1",
                    "2026-05-29T10:00:01Z",
                    "user",
                    "Compare SOW_0058 and SOW_0059 before deciding the implementation.",
                ),
                ProviderMessage("m2", "turn-1", "2026-05-29T10:00:02Z", "assistant", "I need to inspect both scopes."),
            ],
            task_events=[ProviderTaskEvent("t1", "turn-1", "2026-05-29T10:00:03Z", "task_complete", "analysis only")],
        )

        examples = build_trainable_examples(_session_with_turns(turn))

        self.assertEqual(len(examples), 1)
        self.assertEqual(examples[0].outcome_label, "abstain")
        self.assertEqual(examples[0].outcome_class, "insufficient_evidence")
        self.assertEqual(examples[0].gap_type, "mixed_context")
        self.assertTrue(examples[0].metadata["mixed_context"])

    def test_build_trainable_examples_marks_positive_repair_history(self) -> None:
        turn = ProviderTurn(
            turn_id="turn-1",
            timestamp="2026-05-29T10:00:01Z",
            messages=[
                ProviderMessage("m1", "turn-1", "2026-05-29T10:00:01Z", "user", "Finish SOW_0058"),
                ProviderMessage(
                    "m2",
                    "turn-1",
                    "2026-05-29T10:00:02Z",
                    "assistant",
                    "Double-check complete. Fixed the parser gap and quality check passed.",
                ),
            ],
            tool_results=[
                ProviderToolResult(
                    "r1",
                    "call-1",
                    "turn-1",
                    "2026-05-29T10:00:03Z",
                    "exec_command",
                    output="59 tests passed",
                    success=True,
                )
            ],
            patch_events=[
                ProviderPatchEvent(
                    "p1",
                    "patch-1",
                    "turn-1",
                    "2026-05-29T10:00:04Z",
                    status="completed",
                    success=True,
                    changes=[PatchChange(path="darwinSkill/provider_logs.py", change_type="modified")],
                )
            ],
            task_events=[
                ProviderTaskEvent("t1", "turn-1", "2026-05-29T10:00:05Z", "task_complete", "Done and commit created.")
            ],
        )

        examples = build_trainable_examples(_session_with_turns(turn))
        example = examples[0]

        self.assertEqual(example.outcome_label, "positive")
        self.assertEqual(example.outcome_class, "accepted_with_repair_history")
        self.assertEqual(example.gap_type, "resolved")
        self.assertIn("p1", example.raw_evidence_refs)
        self.assertEqual(example.metadata["files_touched"], ["darwinSkill/provider_logs.py"])
        self.assertEqual(example.metadata["turn_ids"], ["turn-1"])
        self.assertEqual(example.metadata["merged_turn_ids"], ["turn-1"])
        self.assertIn("patch success=True", example.repair_actions)

    def test_build_trainable_examples_marks_shallow_or_incomplete_solution(self) -> None:
        turn = ProviderTurn(
            turn_id="turn-1",
            timestamp="2026-05-29T10:00:01Z",
            messages=[
                ProviderMessage("m1", "turn-1", "2026-05-29T10:00:01Z", "user", "Review SOW_0059 output."),
                ProviderMessage(
                    "m2",
                    "turn-1",
                    "2026-05-29T10:00:02Z",
                    "assistant",
                    "The implementation is shallow and still needs a fill gap pass.",
                ),
            ],
            task_events=[ProviderTaskEvent("t1", "turn-1", "2026-05-29T10:00:03Z", "task_complete", "review done")],
        )

        example = build_trainable_examples(_session_with_turns(turn))[0]

        self.assertEqual(example.outcome_label, "negative")
        self.assertEqual(example.outcome_class, "shallow_or_incomplete_solution")
        self.assertEqual(example.gap_type, "incomplete_coverage")

    def test_build_trainable_examples_marks_scope_miss_or_wrong_approach(self) -> None:
        turn = ProviderTurn(
            turn_id="turn-1",
            timestamp="2026-05-29T10:00:01Z",
            messages=[
                ProviderMessage("m1", "turn-1", "2026-05-29T10:00:01Z", "user", "Review SOW_0059 output."),
                ProviderMessage(
                    "m2",
                    "turn-1",
                    "2026-05-29T10:00:02Z",
                    "assistant",
                    "This is a wrong approach and does not really solve the agreed task.",
                ),
            ],
            task_events=[ProviderTaskEvent("t1", "turn-1", "2026-05-29T10:00:03Z", "task_complete", "review done")],
        )

        example = build_trainable_examples(_session_with_turns(turn))[0]

        self.assertEqual(example.outcome_label, "negative")
        self.assertEqual(example.outcome_class, "scope_miss_or_wrong_approach")
        self.assertEqual(example.gap_type, "wrong_approach")

    def test_callback_interpreter_can_override_default_judgment(self) -> None:
        turn = ProviderTurn(
            turn_id="turn-1",
            timestamp="2026-05-29T10:00:01Z",
            messages=[
                ProviderMessage("m1", "turn-1", "2026-05-29T10:00:01Z", "user", "Review the integration plan."),
                ProviderMessage("m2", "turn-1", "2026-05-29T10:00:02Z", "assistant", "The approach misses the scope boundary."),
            ],
        )

        interpreter = CallbackEvidenceInterpreter(
            lambda bundle: {
                "polarity": "negative",
                "outcome_class": "scope_miss_or_wrong_approach",
                "gap_type": "wrong_approach",
                "severity": 0.8,
                "confidence": 0.9,
                "needs_review": False,
                "task_summary": bundle["prompt"],
                "accepted_resolution": "Re-scope before implementation.",
                "derived_reasoning_summary": "The task drifted outside the approved boundary.",
                "metadata": {"judge": "callback"},
            }
        )

        example = build_trainable_examples(_session_with_turns(turn), interpreter=interpreter)[0]

        self.assertEqual(example.outcome_class, "scope_miss_or_wrong_approach")
        self.assertEqual(example.gap_type, "wrong_approach")
        self.assertEqual(example.accepted_resolution, "Re-scope before implementation.")
        self.assertEqual(example.metadata["judge"], "callback")

    def test_build_evidence_bundle_preserves_summary_surfaces(self) -> None:
        turn = ProviderTurn(
            turn_id="turn-1",
            timestamp="2026-05-29T10:00:01Z",
            messages=[
                ProviderMessage("m1", "turn-1", "2026-05-29T10:00:01Z", "user", "Implement SOW_0058 parser"),
                ProviderMessage("m2", "turn-1", "2026-05-29T10:00:02Z", "assistant", "I used the transcript artifact."),
            ],
            tool_results=[
                ProviderToolResult(
                    "r1",
                    "call-1",
                    "turn-1",
                    "2026-05-29T10:00:03Z",
                    "exec_command",
                    output="ok",
                    success=True,
                )
            ],
            patch_events=[
                ProviderPatchEvent(
                    "p1",
                    "patch-1",
                    "turn-1",
                    "2026-05-29T10:00:04Z",
                    status="completed",
                    success=True,
                    changes=[PatchChange(path="darwinSkill/extraction.py", change_type="modified")],
                )
            ],
            task_events=[ProviderTaskEvent("t1", "turn-1", "2026-05-29T10:00:05Z", "task_complete", "done")],
            artifact_refs=[ArtifactReference(ref_id="a1", ref_type="transcript", path="/tmp/codex-session.jsonl")],
        )
        session = _session_with_turns(turn)
        work_unit = segment_session_into_work_units(session)[0]

        bundle = build_evidence_bundle(session, work_unit)

        self.assertIsInstance(bundle, EvidenceBundle)
        self.assertEqual(bundle.files_touched, ["darwinSkill/extraction.py"])
        self.assertEqual(bundle.tool_summaries, ["exec_command: ok"])
        self.assertEqual(bundle.patch_summaries, ["patch success=True files=darwinSkill/extraction.py"])
        self.assertEqual(bundle.task_summaries, ["task_complete: done"])


if __name__ == "__main__":
    unittest.main()
