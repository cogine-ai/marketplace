import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "prepare_package.py"
SPEC = importlib.util.spec_from_file_location("prepare_package", SCRIPT)
PACKAGE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PACKAGE)
SKILL_NAMES = ("coginex", "setup", "tasks", "knowledge", "collaboration")


def snapshot(root):
    return {str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in root.rglob("*") if path.is_file()}


class PreparePackageTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.source = self.root / "source"
        self.source.mkdir()
        self.manifest = {
            "name": "coginex", "version": "0.2.0", "skills": "./skills/",
            "author": {"name": "Cogine AI", "url": "https://github.com/cogine-ai"},
            "apps": "./.app.json", "mcpServers": "./.mcp.json",
            "extensions": {"com.openai": {"onboardingSkill": "./skills/setup/SKILL.md"}},
        }
        self.write_json(".codex-plugin/plugin.json", self.manifest)
        self.write_json(".claude-plugin/plugin.json", {"name": "coginex", "version": "0.2.0",
                                                     "mcpServers": "./.mcp.json"})
        self.write_json(".app.json", {"apps": {"coginex": {"id": "asdk_app_old"}}})
        self.write_json(".mcp.json", {"mcpServers": {"coginex": {"type": "http",
                                                                "url": "https://mcp.x.cogine.ai/mcp"}}})
        for name in SKILL_NAMES:
            self.write("skills/{}/SKILL.md".format(name), "---\nname: {}\n---\nSkill {}\n".format(name, name))
            self.write("skills/{}/agents/openai.yaml".format(name), "interface:\n  display_name: {}\n".format(name))

    def write(self, relative, content):
        path = self.source / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def write_json(self, relative, value):
        self.write(relative, json.dumps(value))

    def test_registered_package_preserves_source_and_all_five_skills(self):
        before = snapshot(self.source)
        output = self.root / "registered"
        receipt = PACKAGE.prepare_package(self.source, output, app_id="asdk_app_actual123")
        self.assertEqual(snapshot(self.source), before)
        self.assertEqual(json.loads((output / ".app.json").read_text()),
                         {"apps": {"coginex": {"id": "asdk_app_actual123", "required": True}}})
        self.assertEqual(json.loads((output / ".codex-plugin/plugin.json").read_text()), self.manifest)
        for path, digest in before.items():
            if path.startswith("skills/") or path in (".mcp.json", ".claude-plugin/plugin.json"):
                self.assertEqual(snapshot(output)[path], digest)
        self.assertEqual(len(list((output / "skills").glob("*/SKILL.md"))), 5)
        self.assertEqual(receipt["mode"], "registered-app")
        self.assertEqual(receipt["plugin"]["version"], "0.2.0")
        self.assertEqual(len(receipt["origin"]["sourceTreeSha256"]), 64)

    def test_direct_package_removes_only_app_binding(self):
        before = snapshot(self.source)
        output = self.root / "direct"
        receipt = PACKAGE.prepare_package(self.source, output, direct_mcp=True)
        self.assertEqual(snapshot(self.source), before)
        self.assertFalse((output / ".app.json").exists())
        expected = dict(self.manifest)
        expected.pop("apps")
        self.assertEqual(json.loads((output / ".codex-plugin/plugin.json").read_text()), expected)
        self.assertEqual(expected["extensions"]["com.openai"]["onboardingSkill"], "./skills/setup/SKILL.md")
        self.assertNotIn("appId", receipt)
        self.assertEqual(receipt["mode"], "direct-mcp")
        for path, digest in before.items():
            if path not in (".app.json", ".codex-plugin/plugin.json"):
                self.assertEqual(snapshot(output)[path], digest)

    def test_accepts_each_supported_app_id_prefix(self):
        for index, app_id in enumerate(("asdk_app_123abc", "connector_team-tools", "templated_apps_abc-123")):
            with self.subTest(app_id=app_id):
                output = self.root / "variant-{}".format(index)
                PACKAGE.prepare_package(self.source, output, app_id=app_id)
                self.assertEqual(json.loads((output / ".app.json").read_text())["apps"]["coginex"]["id"], app_id)

    def test_rejects_invalid_app_ids_without_creating_output(self):
        for app_id in ("plugin_asdk_app_123", "asdk_app_", "connector_", "templated_apps_", "unknown_123",
                       "asdk_app_../secret", "asdk_app_space here", "asdk_app_new\n", " connector_123"):
            with self.subTest(app_id=app_id):
                output = self.root / "invalid"
                with self.assertRaises(ValueError):
                    PACKAGE.prepare_package(self.source, output, app_id=app_id)
                self.assertFalse(output.exists())

    def test_requires_exactly_one_mode(self):
        for options in ({}, {"app_id": "asdk_app_123", "direct_mcp": True}):
            with self.subTest(options=options), self.assertRaises(ValueError):
                PACKAGE.prepare_package(self.source, self.root / "invalid", **options)

    def test_existing_output_is_not_overwritten(self):
        output = self.root / "existing"
        output.mkdir()
        marker = output / "keep.txt"
        marker.write_text("keep")
        with self.assertRaises(FileExistsError):
            PACKAGE.prepare_package(self.source, output, direct_mcp=True)
        self.assertEqual(marker.read_text(), "keep")

    def test_rejects_source_output_nesting(self):
        for output in (self.source, self.source / "nested", self.root):
            with self.subTest(output=output), self.assertRaises(ValueError):
                PACKAGE.prepare_package(self.source, output, direct_mcp=True)
        self.assertFalse((self.source / "nested").exists())

    def test_rejects_output_symlink_to_source(self):
        output = self.root / "alias"
        output.symlink_to(self.source, target_is_directory=True)
        with self.assertRaises(ValueError):
            PACKAGE.prepare_package(self.source, output, direct_mcp=True)

    def test_broken_output_symlink_is_not_overwritten(self):
        output = self.root / "broken"
        output.symlink_to(self.root / "missing")
        with self.assertRaises(FileExistsError):
            PACKAGE.prepare_package(self.source, output, direct_mcp=True)
        self.assertTrue(output.is_symlink())

    def test_handles_empty_canonical_app_map(self):
        self.write_json(".app.json", {"apps": {}})
        output = self.root / "from-empty"
        PACKAGE.prepare_package(self.source, output, app_id="connector_registered")
        self.assertEqual(json.loads((output / ".app.json").read_text())["apps"]["coginex"]["id"],
                         "connector_registered")

    def test_receipt_has_no_personal_source_path(self):
        output = self.root / "receipt"
        receipt = PACKAGE.prepare_package(self.source, output, direct_mcp=True)
        self.assertEqual(json.loads((output / PACKAGE.RECEIPT_NAME).read_text()), receipt)
        self.assertNotIn(str(self.root), json.dumps(receipt))

    def test_optional_catalogs_point_to_prepared_root_and_preserve_receipt(self):
        before = snapshot(self.source)
        for mode in ({"direct_mcp": True}, {"app_id": "connector_registered"}):
            with self.subTest(mode=mode):
                suffix = "direct" if "direct_mcp" in mode else "registered"
                plain = PACKAGE.prepare_package(self.source, self.root / (suffix + "-plain"), **mode)
                output = self.root / (suffix + "-catalog")
                cataloged = PACKAGE.prepare_package(self.source, output, with_marketplace=True, **mode)
                codex = json.loads((output / ".agents/plugins/marketplace.json").read_text())
                claude = json.loads((output / ".claude-plugin/marketplace.json").read_text())
                self.assertEqual(codex["name"], "coginex-local")
                self.assertEqual(claude["name"], codex["name"])
                self.assertEqual(codex["plugins"][0]["source"], {"source": "local", "path": "./"})
                self.assertEqual(claude["plugins"][0]["source"], "./")
                self.assertEqual(claude["plugins"][0]["version"], self.manifest["version"])
                self.assertEqual(codex["plugins"][0]["name"], self.manifest["name"])
                self.assertEqual(claude["plugins"][0]["name"], self.manifest["name"])
                self.assertEqual(cataloged, plain)
                self.assertEqual(snapshot(self.source), before)

    def test_custom_marketplace_name_is_shared_by_both_catalogs(self):
        output = self.root / "custom-marketplace"
        PACKAGE.prepare_package(self.source, output, direct_mcp=True, with_marketplace=True,
                                marketplace_name="coginex-test-42")
        for relative in (".agents/plugins/marketplace.json", ".claude-plugin/marketplace.json"):
            self.assertEqual(json.loads((output / relative).read_text())["name"], "coginex-test-42")

    def test_invalid_marketplace_configuration_does_not_create_output(self):
        for options in ({"marketplace_name": "custom"},
                        {"with_marketplace": True, "marketplace_name": "../bad"},
                        {"with_marketplace": True, "marketplace_name": "Uppercase"}):
            with self.subTest(options=options), self.assertRaises(ValueError):
                PACKAGE.prepare_package(self.source, self.root / "invalid-catalog", direct_mcp=True, **options)
        self.assertFalse((self.root / "invalid-catalog").exists())

    def test_cli_requires_output_and_exclusive_mode(self):
        for arguments in ([], ["--output", str(self.root / "cli")],
                          ["--output", str(self.root / "cli"), "--direct-mcp", "--app-id", "asdk_app_123"]):
            result = subprocess.run([sys.executable, "-B", str(SCRIPT), *arguments], capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
        self.assertFalse((self.root / "cli").exists())


if __name__ == "__main__":
    unittest.main()
