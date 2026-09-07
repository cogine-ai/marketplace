"""Portable adaptation of upstream's documented script-path regression check."""

import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[2]


class PortableScriptPathTests(unittest.TestCase):
    def test_documented_search_commands_resolve_inside_the_installed_skill(self):
        text = (SKILL_ROOT / "SKILL.md").read_text()
        commands = re.findall(r'^python3 "([^"]+)"', text, re.MULTILINE)
        self.assertTrue(commands)
        for command in commands:
            with self.subTest(command=command):
                self.assertTrue(command.startswith("$UI_UX_SKILL_DIR/"))
                path = SKILL_ROOT / command.removeprefix("$UI_UX_SKILL_DIR/")
                self.assertTrue(path.is_file(), path)
                self.assertEqual(path.parent, SKILL_ROOT / "scripts")

    def test_domain_search_from_an_unrelated_working_directory(self):
        with tempfile.TemporaryDirectory(prefix="ui ux cwd ") as cwd:
            # Resolve the same script path documented by the skill, without a
            # Claude-specific environment variable or a project-local script.
            result = subprocess.run(
                [sys.executable, str(SKILL_ROOT / "scripts/search.py"),
                 "error summary validation", "--domain", "ux", "--json"],
                cwd=cwd, capture_output=True, text=True, check=True,
            )
            output = json.loads(result.stdout)
            self.assertEqual(output["domain"], "ux")
            self.assertEqual(output["results"][0]["Issue"], "Focusable Error Summary")
            self.assertFalse((Path(cwd) / "design-system").exists())


if __name__ == "__main__":
    unittest.main()
