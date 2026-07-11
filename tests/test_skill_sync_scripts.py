from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_ROOT = REPO_ROOT / "scripts" / "skills"
SKILLS_ROOT = REPO_ROOT / "skills"


class SkillSyncScriptTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self.temp_dir.name)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def run_script(
        self,
        script_name: str,
        *args: str,
        expect_success: bool = True,
    ) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env["HOME"] = str(self.tmp_path / "home")
        command = [sys.executable, str(SCRIPT_ROOT / script_name), *args]
        result = subprocess.run(command, cwd=REPO_ROOT, env=env, text=True, capture_output=True, check=False)
        if expect_success and result.returncode != 0:
            self.fail(f"command failed: {command}\nstdout={result.stdout}\nstderr={result.stderr}")
        if not expect_success and result.returncode == 0:
            self.fail(f"command unexpectedly passed: {command}\nstdout={result.stdout}")
        return result

    def test_codex_repo_dry_run_is_skill_only(self) -> None:
        project = self.tmp_path / "project"
        result = self.run_script(
            "sync_env_codex.py",
            "--scope",
            "repo",
            "--target-project",
            str(project),
            "--skill",
            "task-router-flow",
            "--dry-run",
        )
        self.assertIn(f"{project.resolve()}/.agents/skills/task-router-flow", result.stdout)
        self.assertNotIn("hooks.json", result.stdout)
        self.assertNotIn("config.toml", result.stdout)

    def test_codex_legacy_user_dry_run(self) -> None:
        result = self.run_script(
            "sync_env_codex.py",
            "--scope",
            "legacy-user",
            "--skill",
            "task-router-flow",
            "--dry-run",
        )
        self.assertIn(f"{self.tmp_path}/home/.codex/skills/task-router-flow", result.stdout)

    def test_claude_repo_and_invalid_legacy(self) -> None:
        project = self.tmp_path / "project"
        result = self.run_script(
            "sync_env_claude.py",
            "--scope",
            "repo",
            "--target-project",
            str(project),
            "--skill",
            "task-router-flow",
            "--dry-run",
        )
        self.assertIn(f"{project.resolve()}/.claude/skills/task-router-flow", result.stdout)

        invalid = self.run_script(
            "sync_env_claude.py",
            "--scope",
            "legacy-user",
            "--skill",
            "task-router-flow",
            "--dry-run",
            expect_success=False,
        )
        self.assertIn("legacy-user is only valid for sync_env_codex.py", invalid.stderr)

    def test_opencode_repo_user_and_invalid_profile(self) -> None:
        project = self.tmp_path / "project"
        repo_result = self.run_script(
            "sync_env_opencode.py",
            "--scope",
            "repo",
            "--target-project",
            str(project),
            "--skill",
            "task-router-flow",
            "--dry-run",
        )
        self.assertIn(f"{project.resolve()}/.opencode/skills/task-router-flow", repo_result.stdout)

        user_result = self.run_script(
            "sync_env_opencode.py",
            "--scope",
            "user",
            "--skill",
            "task-router-flow",
            "--dry-run",
        )
        self.assertIn(f"{self.tmp_path}/home/.config/opencode/skills/task-router-flow", user_result.stdout)

        custom_root = self.tmp_path / "opencode-custom"
        custom_result = self.run_script(
            "sync_env_opencode.py",
            "--target-root",
            str(custom_root),
            "--skill",
            "task-router-flow",
            "--dry-run",
        )
        self.assertIn(f"{custom_root.resolve()}/task-router-flow", custom_result.stdout)

        invalid = self.run_script(
            "sync_env_opencode.py",
            "--profile",
            "codex-hooks",
            "--scope",
            "user",
            "--skill",
            "task-router-flow",
            "--dry-run",
            expect_success=False,
        )
        self.assertIn("invalid choice", invalid.stderr)

        invalid_legacy = self.run_script(
            "sync_env_opencode.py",
            "--scope",
            "legacy-user",
            "--target-root",
            str(self.tmp_path / "custom"),
            "--skill",
            "task-router-flow",
            "--dry-run",
            expect_success=False,
        )
        self.assertIn("legacy-user is only valid for sync_env_codex.py", invalid_legacy.stderr)

    def test_other_agent_requires_target_root_and_can_copy(self) -> None:
        invalid = self.run_script(
            "sync_env_others.py",
            "--skill",
            "task-router-flow",
            "--dry-run",
            expect_success=False,
        )
        self.assertIn("--target-root", invalid.stderr)

        target_root = self.tmp_path / "custom-skills"
        self.run_script("sync_env_others.py", "--target-root", str(target_root), "--skill", "task-router-flow")
        self.assertTrue((target_root / "task-router-flow" / "SKILL.md").exists())

    def test_exact_skill_overwrite_preserves_unrelated_skill(self) -> None:
        target_root = self.tmp_path / "custom-skills"
        target_skill = target_root / "task-router-flow"
        unrelated = target_root / "unrelated-skill" / "sentinel.txt"
        target_skill.mkdir(parents=True)
        unrelated.parent.mkdir(parents=True)
        (target_skill / "stale.txt").write_text("stale")
        unrelated.write_text("keep")

        self.run_script(
            "sync_env_others.py",
            "--target-root",
            str(target_root),
            "--skill",
            "task-router-flow",
            "--overwrite",
        )

        self.assertFalse((target_skill / "stale.txt").exists())
        self.assertEqual("keep", unrelated.read_text())

    def test_overwrite_dry_run_previews_replace_without_mutating(self) -> None:
        target_root = self.tmp_path / "custom-skills"
        stale = target_root / "task-router-flow" / "stale.txt"
        unrelated = target_root / "unrelated-skill" / "sentinel.txt"
        stale.parent.mkdir(parents=True)
        unrelated.parent.mkdir(parents=True)
        stale.write_text("stale")
        unrelated.write_text("keep")

        result = self.run_script(
            "sync_env_others.py",
            "--target-root",
            str(target_root),
            "--skill",
            "task-router-flow",
            "--overwrite",
            "--dry-run",
        )

        self.assertIn("replace task-router-flow ->", result.stdout)
        self.assertEqual("stale", stale.read_text())
        self.assertEqual("keep", unrelated.read_text())

    def test_verify_skill_copy_reports_mismatch_buckets(self) -> None:
        target_root = self.tmp_path / "custom-skills"
        self.run_script(
            "sync_env_others.py",
            "--target-root",
            str(target_root),
            "--skill",
            "task-router-flow",
        )

        passing = self.run_script(
            "verify_skill_copy.py",
            "--target-root",
            str(target_root),
            "--skill",
            "task-router-flow",
        )
        self.assertIn("parity: ok", passing.stdout)

        target_skill = target_root / "task-router-flow"
        (target_skill / ".DS_Store").write_text("ignored")
        ignored_dir = target_skill / "__pycache__"
        ignored_dir.mkdir()
        (ignored_dir / "cache.pyc").write_bytes(b"ignored")
        ignored = self.run_script(
            "verify_skill_copy.py",
            "--target-root",
            str(target_root),
            "--skill",
            "task-router-flow",
        )
        self.assertIn("parity: ok", ignored.stdout)

        (target_skill / "extra.txt").write_text("extra")
        (target_skill / "SKILL.md").write_text("changed")
        (target_skill / "agents" / "openai.yaml").unlink()
        failed = self.run_script(
            "verify_skill_copy.py",
            "--target-root",
            str(target_root),
            "--skill",
            "task-router-flow",
            expect_success=False,
        )
        self.assertIn("missing:\n  agents/openai.yaml", failed.stdout)
        self.assertIn("extra:\n  extra.txt", failed.stdout)
        self.assertIn("changed:\n  SKILL.md", failed.stdout)
        self.assertIn("parity: fail", failed.stdout)

    def test_missing_repo_target_project_fails(self) -> None:
        result = self.run_script(
            "sync_env_codex.py",
            "--scope",
            "repo",
            "--skill",
            "task-router-flow",
            "--dry-run",
            expect_success=False,
        )
        self.assertIn("--scope repo requires --target-project", result.stderr)

    def test_legacy_sync_environment_is_skill_copy_only(self) -> None:
        result = self.run_script("sync_environment.py", "--target", "codex", "--dry-run")
        self.assertIn("/.codex/skills/task-router-flow", result.stdout)
        self.assertNotIn("hooks.json", result.stdout)
        self.assertNotIn("config.toml", result.stdout)

    def test_skill_registry_matches_active_skill_files(self) -> None:
        registry = json.loads((SKILLS_ROOT / "registry.json").read_text())
        registered = {skill["name"]: skill for skill in registry["skills"]}
        active = {
            path.name
            for path in SKILLS_ROOT.iterdir()
            if path.is_dir() and (path / "SKILL.md").exists()
        }

        self.assertEqual(active, set(registered))

        for skill_name, skill in registered.items():
            self.assertTrue(skill["files"], skill_name)
            self.assertEqual(f"skills/{skill_name}/SKILL.md", skill["files"][0]["path"])
            listed_files = {file_entry["path"] for file_entry in skill["files"]}
            actual_files = {
                path.relative_to(REPO_ROOT).as_posix()
                for path in (SKILLS_ROOT / skill_name).rglob("*")
                if path.is_file()
                and "__pycache__" not in path.parts
                and path.name != ".DS_Store"
                and path.suffix != ".pyc"
            }
            self.assertEqual(actual_files, listed_files, skill_name)
            for file_entry in skill["files"]:
                relative_path = file_entry["path"]
                self.assertTrue((REPO_ROOT / relative_path).exists(), relative_path)
                self.assertIn(relative_path, file_entry["raw_url"])


if __name__ == "__main__":
    unittest.main()
