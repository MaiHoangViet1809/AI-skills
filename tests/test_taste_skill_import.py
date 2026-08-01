from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "skills" / "taste-skill"
SCRIPT_ROOT = REPO_ROOT / "scripts" / "skills"


class TasteSkillImportTests(unittest.TestCase):
    def read(self, path: Path) -> str:
        return path.read_text(encoding="utf-8")

    def test_imported_files_exist_and_are_non_empty(self) -> None:
        expected_files = [
            SKILL_ROOT / "SKILL.md",
            SKILL_ROOT / "LICENSE.txt",
            SKILL_ROOT / "agents" / "openai.yaml",
        ]
        for path in expected_files:
            with self.subTest(path=path):
                self.assertTrue(path.exists())
                self.assertGreater(path.stat().st_size, 0)

    def test_frontmatter_preserves_upstream_invocation_name(self) -> None:
        text = self.read(SKILL_ROOT / "SKILL.md")
        match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
        self.assertIsNotNone(match)
        frontmatter = match.group(1)
        self.assertIn("name: design-taste-frontend", frontmatter)
        self.assertIn("description: Anti-slop frontend skill", frontmatter)

    def test_license_notice_is_preserved(self) -> None:
        license_text = self.read(SKILL_ROOT / "LICENSE.txt")
        self.assertIn("MIT License", license_text)
        self.assertIn("Copyright (c) 2026 Leonxlnx", license_text)
        self.assertIn("THE SOFTWARE IS PROVIDED \"AS IS\"", license_text)

    def test_registry_files_match_taste_skill_folder(self) -> None:
        registry = json.loads(self.read(REPO_ROOT / "skills" / "registry.json"))
        entry = next(skill for skill in registry["skills"] if skill["name"] == "taste-skill")
        listed_files = {file_entry["path"] for file_entry in entry["files"]}
        actual_files = {
            path.relative_to(REPO_ROOT).as_posix()
            for path in SKILL_ROOT.rglob("*")
            if path.is_file()
        }
        self.assertEqual(actual_files, listed_files)
        self.assertEqual("skills/taste-skill/SKILL.md", entry["files"][0]["path"])

    def test_index_documents_registry_and_invocation_names(self) -> None:
        index = self.read(REPO_ROOT / "skills" / "INDEX.md")
        self.assertIn("`taste-skill`", index)
        self.assertIn("`$design-taste-frontend`", index)

    def test_sync_script_can_dry_run_install_by_folder_name(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            env = os.environ.copy()
            env["HOME"] = str(Path(temp) / "home")
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_ROOT / "sync_env_codex.py"),
                    "--scope",
                    "legacy-user",
                    "--skill",
                    "taste-skill",
                    "--dry-run",
                ],
                cwd=REPO_ROOT,
                env=env,
                text=True,
                capture_output=True,
                check=False,
            )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("install taste-skill ->", result.stdout)
        self.assertIn(".codex/skills/taste-skill", result.stdout)


if __name__ == "__main__":
    unittest.main()
