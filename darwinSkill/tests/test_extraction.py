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
