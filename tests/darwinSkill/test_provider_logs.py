from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from darwinSkill.provider_logs import load_codex_session, read_provider_session, write_provider_session


def _write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")


class ProviderLogsTest(unittest.TestCase):
    def test_load_codex_session_maps_core_events(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            transcript = Path(temp_dir) / "codex-session.jsonl"
            _write_jsonl(
                transcript,
                [
                    {
                        "timestamp": "2026-05-29T10:00:00Z",
                        "type": "session_meta",
                        "payload": {
                            "id": "session-1",
                            "cwd": "/repo",
                            "timestamp": "2026-05-29T10:00:00Z",
                        },
                    },
                    {
                        "timestamp": "2026-05-29T10:00:01Z",
                        "type": "turn_context",
                        "payload": {
                            "turn_id": "turn-1",
                            "cwd": "/repo",
                            "model": "gpt-5",
                        },
                    },
                    {
                        "timestamp": "2026-05-29T10:00:02Z",
                        "type": "event_msg",
                        "payload": {
                            "type": "user_message",
                            "turn_id": "turn-1",
                            "message": "Implement SOW_0058 parser",
                        },
                    },
                    {
                        "timestamp": "2026-05-29T10:00:03Z",
                        "type": "response_item",
                        "payload": {
                            "type": "message",
                            "turn_id": "turn-1",
                            "role": "assistant",
                            "phase": "final",
                            "content": [{"type": "output_text", "text": "quality check passed"}],
                        },
                    },
                    {
                        "timestamp": "2026-05-29T10:00:04Z",
                        "type": "response_item",
                        "payload": {
                            "type": "function_call",
                            "turn_id": "turn-1",
                            "call_id": "call-1",
                            "name": "functions.exec_command",
                            "arguments": "{\"cmd\":\"git status\"}",
                        },
                    },
                    {
                        "timestamp": "2026-05-29T10:00:05Z",
                        "type": "event_msg",
                        "payload": {
                            "type": "exec_command_end",
                            "turn_id": "turn-1",
                            "call_id": "call-1",
                            "stdout": "clean",
                            "exit_code": 0,
                        },
                    },
                    {
                        "timestamp": "2026-05-29T10:00:06Z",
                        "type": "event_msg",
                        "payload": {
                            "type": "patch_apply_end",
                            "turn_id": "turn-1",
                            "call_id": "patch-1",
                            "status": "completed",
                            "success": True,
                            "changes": {
                                "darwinSkill/provider_logs.py": {
                                    "type": "modified",
                                    "unified_diff": "@@",
                                    "content": "updated",
                                }
                            },
                        },
                    },
                    {
                        "timestamp": "2026-05-29T10:00:07Z",
                        "type": "event_msg",
                        "payload": {
                            "type": "task_complete",
                            "turn_id": "turn-1",
                            "last_agent_message": "Done and committed.",
                            "duration_ms": 2500,
                            "time_to_first_token_ms": 150,
                        },
                    },
                    {
                        "timestamp": "2026-05-29T10:00:08Z",
                        "type": "event_msg",
                        "payload": {
                            "type": "unknown_event",
                            "turn_id": "turn-1",
                            "payload_note": "preserve me",
                        },
                    },
                ],
            )

            session = load_codex_session(transcript)

            self.assertEqual(session.provider, "codex")
            self.assertEqual(session.source_format_version, "codex_session_jsonl_v1")
            self.assertEqual(session.session_id, "session-1")
            self.assertEqual(session.cwd, "/repo")
            self.assertEqual(len(session.turns), 1)

            turn = session.turns[0]
            self.assertEqual(turn.turn_id, "turn-1")
            self.assertEqual(turn.metadata["model"], "gpt-5")
            self.assertEqual([message.role for message in turn.messages], ["user", "assistant"])
            self.assertEqual(turn.messages[1].content, "quality check passed")
            self.assertEqual(turn.tool_calls[0].tool_name, "functions.exec_command")
            self.assertEqual(turn.tool_calls[0].arguments, {"cmd": "git status"})
            self.assertEqual(turn.tool_results[0].tool_name, "exec_command")
            self.assertTrue(turn.tool_results[0].success)
            self.assertEqual(turn.patch_events[0].changes[0].path, "darwinSkill/provider_logs.py")
            self.assertTrue(turn.patch_events[0].success)
            self.assertEqual(turn.task_events[0].event_type, "task_complete")
            self.assertEqual(turn.task_events[0].duration_ms, 2500)
            self.assertEqual(turn.artifact_refs[0].path, str(transcript))
            self.assertEqual(turn.metadata["unclassified_events"][0]["payload_type"], "unknown_event")
            self.assertEqual(session.provider_metadata["artifact_refs"][0]["path"], str(transcript))

    def test_load_codex_session_degrades_cleanly_without_optional_fields(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            transcript = Path(temp_dir) / "minimal.jsonl"
            _write_jsonl(
                transcript,
                [
                    {
                        "timestamp": "2026-05-29T10:00:00Z",
                        "type": "event_msg",
                        "payload": {
                            "type": "user_message",
                            "message": "Continue",
                        },
                    },
                    {
                        "timestamp": "2026-05-29T10:00:01Z",
                        "type": "event_msg",
                        "payload": {
                            "type": "patch_apply_end",
                            "changes": [],
                        },
                    },
                ],
            )

            session = load_codex_session(transcript)

            self.assertEqual(session.session_id, "minimal")
            self.assertEqual(session.cwd, "")
            self.assertEqual(len(session.turns), 2)
            self.assertEqual(session.turns[0].turn_id, "unknown-turn-1")
            self.assertEqual(session.turns[0].messages[0].content, "Continue")
            self.assertEqual(session.turns[1].turn_id, "unknown-turn-2")
            self.assertEqual(session.turns[1].patch_events[0].changes, [])
            self.assertEqual(session.turns[0].artifact_refs[0].path, str(transcript))

    def test_provider_session_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            transcript = Path(temp_dir) / "roundtrip.jsonl"
            output = Path(temp_dir) / "canonical.json"
            _write_jsonl(
                transcript,
                [
                    {
                        "timestamp": "2026-05-29T10:00:00Z",
                        "type": "session_meta",
                        "payload": {"id": "roundtrip-session", "cwd": "/repo"},
                    },
                    {
                        "timestamp": "2026-05-29T10:00:01Z",
                        "type": "event_msg",
                        "payload": {"type": "user_message", "turn_id": "turn-1", "message": "Hello"},
                    },
                ],
            )

            session = load_codex_session(transcript)
            write_provider_session(output, session)
            restored = read_provider_session(output)

            self.assertEqual(restored.provider, "codex")
            self.assertEqual(restored.session_id, "roundtrip-session")
            self.assertEqual(restored.turns[0].messages[0].content, "Hello")
            self.assertEqual(restored.provider_metadata["artifact_refs"][0]["path"], str(transcript))

    def test_load_codex_session_recovers_tool_name_from_call_id_on_function_call_output(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            transcript = Path(temp_dir) / "tool-output.jsonl"
            _write_jsonl(
                transcript,
                [
                    {
                        "timestamp": "2026-05-29T10:00:00Z",
                        "type": "turn_context",
                        "payload": {"turn_id": "turn-1"},
                    },
                    {
                        "timestamp": "2026-05-29T10:00:01Z",
                        "type": "response_item",
                        "payload": {
                            "type": "function_call",
                            "turn_id": "turn-1",
                            "call_id": "call-1",
                            "name": "functions.exec_command",
                            "arguments": "{\"cmd\":\"pwd\"}",
                        },
                    },
                    {
                        "timestamp": "2026-05-29T10:00:02Z",
                        "type": "response_item",
                        "payload": {
                            "type": "function_call_output",
                            "turn_id": "turn-1",
                            "call_id": "call-1",
                            "output": "ok",
                        },
                    },
                ],
            )

            session = load_codex_session(transcript)

            self.assertEqual(session.turns[0].tool_results[0].tool_name, "functions.exec_command")


if __name__ == "__main__":
    unittest.main()
