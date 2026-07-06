from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_ROOT = REPO_ROOT / "scripts" / "skills"


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

    def test_opencode_repo_user_and_invalid_codex_hooks(self) -> None:
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
        self.assertIn("codex-hooks is only valid for sync_env_codex.py", invalid.stderr)

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

    def test_legacy_sync_environment_still_includes_old_skill_bundle(self) -> None:
        result = self.run_script("sync_environment.py", "--target", "codex", "--dry-run")
        self.assertIn("hooks.json", result.stdout)
        self.assertIn("/.codex/skills/task-router-flow", result.stdout)


if __name__ == "__main__":
    unittest.main()
