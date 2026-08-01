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
SKILLS_ROOT = REPO_ROOT / "skills"
FIXTURE_ROOT = REPO_ROOT / "tests" / "fixtures" / "design_mirror"
SCRIPT_ROOT = REPO_ROOT / "scripts" / "skills"
DESIGN_MIRROR_SKILLS = [
    "extract-design-mirror",
    "apply-design-mirror",
    "verify-design-mirror",
]


class DesignMirrorSkillPortabilityTests(unittest.TestCase):
    maxDiff = None

    def skill_path(self, skill: str) -> Path:
        return SKILLS_ROOT / skill

    def read(self, path: Path) -> str:
        return path.read_text(encoding="utf-8")

    def test_skill_structure_and_frontmatter_are_portable(self) -> None:
        for skill in DESIGN_MIRROR_SKILLS:
            with self.subTest(skill=skill):
                skill_dir = self.skill_path(skill)
                skill_md = skill_dir / "SKILL.md"
                self.assertTrue(skill_md.exists())
                text = self.read(skill_md)
                self.assertTrue(text.startswith("---\n"))
                frontmatter = text.split("---", 2)[1].strip().splitlines()
                keys = [line.split(":", 1)[0] for line in frontmatter if ":" in line]
                self.assertEqual(["name", "description"], keys)
                self.assertIn(f"name: {skill}", text)
                self.assertNotIn("[TODO", text)
                self.assertLess(len(text.splitlines()), 120)

    def test_direct_references_resolve(self) -> None:
        for skill in DESIGN_MIRROR_SKILLS:
            skill_dir = self.skill_path(skill)
            text = self.read(skill_dir / "SKILL.md")
            refs = sorted(set(re.findall(r"`(references/[^`]+)`", text)))
            self.assertTrue(refs, skill)
            for ref in refs:
                with self.subTest(skill=skill, ref=ref):
                    self.assertTrue((skill_dir / ref).exists())

    def test_no_provider_specific_normative_assumptions(self) -> None:
        banned_patterns = [
            r"allowed-tools",
            r"@[A-Za-z0-9_./-]+",
            r"slash command",
            r"\bmcp__",
            r"\.claude/",
            r"\.cursor/",
            r"\.opencode/",
            r"/Users/",
            r"\$CODEX_HOME",
            r"Codex-only",
            r"Claude-only",
            r"OpenAI-only",
        ]
        for skill in DESIGN_MIRROR_SKILLS:
            skill_dir = self.skill_path(skill)
            paths = [skill_dir / "SKILL.md", *sorted((skill_dir / "references").glob("*.md"))]
            for path in paths:
                text = self.read(path)
                for pattern in banned_patterns:
                    with self.subTest(path=path, pattern=pattern):
                        self.assertIsNone(re.search(pattern, text))

    def test_openai_yaml_is_supplemental(self) -> None:
        for skill in DESIGN_MIRROR_SKILLS:
            skill_dir = self.skill_path(skill)
            yaml_path = skill_dir / "agents" / "openai.yaml"
            self.assertTrue(yaml_path.exists())
            yaml_text = self.read(yaml_path)
            self.assertIn(f"Use ${skill}", yaml_text)
            skill_text = self.read(skill_dir / "SKILL.md")
            for required in ("Workflow", "Stop Conditions"):
                self.assertIn(required, skill_text)

    def test_registry_entries_match_shipped_files(self) -> None:
        registry = json.loads(self.read(SKILLS_ROOT / "registry.json"))
        registry_by_name = {item["name"]: item for item in registry["skills"]}
        for skill in DESIGN_MIRROR_SKILLS:
            with self.subTest(skill=skill):
                actual = sorted(
                    str(path.relative_to(REPO_ROOT))
                    for path in self.skill_path(skill).rglob("*")
                    if path.is_file()
                )
                registered = sorted(file_entry["path"] for file_entry in registry_by_name[skill]["files"])
                self.assertEqual(actual, registered)

    def test_sync_scripts_copy_design_mirror_skills_to_supported_roots(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            temp_path = Path(temp)
            env = os.environ.copy()
            env["HOME"] = str(temp_path / "home")
            commands = [
                ("sync_env_codex.py", "--scope", "repo", "--target-project", str(temp_path / "codex-project")),
                ("sync_env_claude.py", "--scope", "repo", "--target-project", str(temp_path / "claude-project")),
                ("sync_env_opencode.py", "--scope", "repo", "--target-project", str(temp_path / "opencode-project")),
                ("sync_env_others.py", "--target-root", str(temp_path / "other-agent-skills")),
            ]
            for script, *base_args in commands:
                for skill in DESIGN_MIRROR_SKILLS:
                    with self.subTest(script=script, skill=skill):
                        command = [
                            sys.executable,
                            str(SCRIPT_ROOT / script),
                            *base_args,
                            "--skill",
                            skill,
                            "--dry-run",
                        ]
                        result = subprocess.run(
                            command,
                            cwd=REPO_ROOT,
                            env=env,
                            text=True,
                            capture_output=True,
                            check=False,
                        )
                        self.assertEqual(result.returncode, 0, result.stderr)
                        self.assertIn(skill, result.stdout)

    def test_fixture_contracts_are_versioned_and_relative(self) -> None:
        evidence = json.loads(self.read(FIXTURE_ROOT / "reference" / "design-mirror-evidence.json"))
        self.assertEqual("design-mirror-evidence/v1", evidence["schema_version"])
        self.assertEqual(".", evidence["package_root"])
        for source in evidence["sources"]:
            locator = source["locator"]
            self.assertFalse(Path(locator).is_absolute())
            self.assertNotRegex(locator, r"token=|password=|authorization|cookie")
        classes = {claim["classification"] for claim in evidence["claims"]}
        self.assertIn("observed", classes)
        self.assertIn("unsupported", classes)

    def test_web_collector_is_dependency_free_and_parseable(self) -> None:
        collector = self.skill_path("extract-design-mirror") / "scripts" / "collect-web-evidence.js"
        text = self.read(collector)
        self.assertNotIn("require(", text)
        self.assertNotIn("import ", text)
        result = subprocess.run(
            ["node", "--check", str(collector)],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
