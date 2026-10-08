import hashlib
import importlib.util
import json
import re
import unittest
import subprocess
import tempfile
from unittest.mock import patch
from pathlib import Path

import yaml


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = PLUGIN_ROOT / "skills"
VALIDATOR_PATH = PLUGIN_ROOT / "scripts" / "validate_bundle.py"
VALIDATOR_SPEC = importlib.util.spec_from_file_location("bundle_validator", VALIDATOR_PATH)
VALIDATOR = importlib.util.module_from_spec(VALIDATOR_SPEC)
VALIDATOR_SPEC.loader.exec_module(VALIDATOR)

USER_ONLY = {
    "cogine-multirepo-worker",
    "cogine-orchestrator",
    "implement",
    "improve-codebase-architecture",
    "local-ultra-review",
    "loop-on-ci",
    "planmode-engineer",
    "review-and-ship",
    "security-best-practices",
    "setup-matt-pocock-skills",
    "to-spec",
    "to-tickets",
}

MODEL_INVOKED = {
    "ai-app-security-audit",
    "backlog-ready-spec",
    "code-review",
    "codebase-design",
    "cogine-power-gates",
    "devex-review",
    "diagnosing-bugs",
    "domain-modeling",
    "fix-ci",
    "fix-merge-conflicts",
    "frontend-design",
    "grilling",
    "plan-devex-review",
    "run-smoke-tests",
    "shadcn",
    "tdd",
    "vercel-react-best-practices",
    "worktree-management",
}

CURRENT_MATT_IMPORTS = {
    "code-review",
    "codebase-design",
    "diagnosing-bugs",
    "domain-modeling",
    "fix-merge-conflicts",
    "grilling",
    "implement",
    "improve-codebase-architecture",
    "setup-matt-pocock-skills",
    "tdd",
    "to-spec",
    "to-tickets",
}

REQUIRED_SKILL_REFERENCES = {
    "implement": {"tdd"},
    "tdd": {"codebase-design"},
    "code-review": {"setup-matt-pocock-skills"},
    "improve-codebase-architecture": {
        "codebase-design",
        "grilling",
        "domain-modeling",
    },
}


def load_frontmatter(path: Path):
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not match:
        raise AssertionError(f"missing frontmatter: {path}")
    return yaml.safe_load(match.group(1)), text


class BundleContractTests(unittest.TestCase):
    def test_inventory_is_exactly_the_approved_30_skills(self):
        actual = {path.name for path in SKILLS_ROOT.iterdir() if path.is_dir()}
        self.assertEqual(USER_ONLY | MODEL_INVOKED, actual)
        self.assertEqual(30, len(actual))

    def test_every_skill_has_matching_frontmatter_and_openai_metadata(self):
        for skill_dir in sorted(SKILLS_ROOT.iterdir()):
            if not skill_dir.is_dir():
                continue
            metadata, _ = load_frontmatter(skill_dir / "SKILL.md")
            self.assertEqual(skill_dir.name, metadata.get("name"), skill_dir.name)
            self.assertTrue((skill_dir / "agents" / "openai.yaml").is_file(), skill_dir.name)

    def test_invocation_policy_has_one_source_of_truth_per_host(self):
        for name in sorted(USER_ONLY | MODEL_INVOKED):
            metadata, _ = load_frontmatter(SKILLS_ROOT / name / "SKILL.md")
            agent = yaml.safe_load(
                (SKILLS_ROOT / name / "agents" / "openai.yaml").read_text(encoding="utf-8")
            )
            policy = (agent or {}).get("policy", {})
            if name in USER_ONLY:
                self.assertIs(metadata.get("disable-model-invocation"), True, name)
                self.assertIs(policy.get("allow_implicit_invocation"), False, name)
            else:
                self.assertNotIn("disable-model-invocation", metadata, name)
                self.assertNotIn("allow_implicit_invocation", policy, name)

    def test_operational_cross_skill_calls_are_namespaced(self):
        for source, targets in REQUIRED_SKILL_REFERENCES.items():
            text = (SKILLS_ROOT / source / "SKILL.md").read_text(encoding="utf-8")
            for target in targets:
                self.assertIn(f"coding-engineer-skills:{target}", text, f"{source} -> {target}")

    def test_bare_skill_call_detection_ignores_paths_and_urls(self):
        self.assertTrue(VALIDATOR.contains_bare_skill_call("/tdd", "tdd"))
        self.assertTrue(VALIDATOR.contains_bare_skill_call("Use `/tdd` now", "tdd"))
        self.assertFalse(
            VALIDATOR.contains_bare_skill_call("Read skills/tdd/SKILL.md", "tdd")
        )
        self.assertFalse(
            VALIDATOR.contains_bare_skill_call("See https://example.test/tdd", "tdd")
        )
        self.assertFalse(
            VALIDATOR.contains_bare_skill_call("Open /tdd/SKILL.md", "tdd")
        )

    def test_implement_uses_the_local_pre_commit_review_instead_of_code_review(self):
        text = (SKILLS_ROOT / "implement" / "SKILL.md").read_text(encoding="utf-8")
        review = "review the work against the originating spec or tickets"
        commit = "Commit your work to the current branch."
        self.assertIn(review, text)
        self.assertIn(commit, text)
        self.assertLess(text.index(review), text.index(commit))
        self.assertNotIn("coding-engineer-skills:code-review", text)

        code_review = (SKILLS_ROOT / "code-review" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("work-in-progress changes", code_review)
        self.assertIn("fixed point", code_review)

    def test_skill_bodies_do_not_depend_on_claude_only_runtime_placeholders(self):
        for skill_md in sorted(SKILLS_ROOT.glob("*/SKILL.md")):
            text = skill_md.read_text(encoding="utf-8")
            self.assertNotIn("${CLAUDE_SKILL_DIR}", text, str(skill_md))
            self.assertNotIn("$ARGUMENTS", text, str(skill_md))
            self.assertNotRegex(text, r"!`[^`]+`", str(skill_md))

    def test_readme_and_manifests_publish_the_same_inventory_and_version(self):
        readme = (PLUGIN_ROOT / "README.md").read_text(encoding="utf-8")
        listed = set(re.findall(r"^- `([a-z0-9-]+)`$", readme, re.MULTILINE))
        self.assertEqual(USER_ONLY | MODEL_INVOKED, listed)
        self.assertIn("30 skill", readme)
        for manifest_path in [
            PLUGIN_ROOT / ".claude-plugin" / "plugin.json",
            PLUGIN_ROOT / ".codex-plugin" / "plugin.json",
        ]:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertRegex(manifest["version"], r"^[0-9]+\.[0-9]+\.[0-9]+$")
            self.assertEqual(
                json.loads((PLUGIN_ROOT / ".codex-plugin" / "plugin.json").read_text())["version"],
                manifest["version"],
            )
            self.assertIn("Thirty focused", manifest["description"])

    def test_host_specific_update_instructions_verify_the_installed_version(self):
        readme = (PLUGIN_ROOT.parents[1] / "README.md").read_text(encoding="utf-8")
        self.assertIn("codex plugin marketplace upgrade cogine-ai", readme)
        self.assertIn("codex plugin list --json", readme)
        self.assertIn("claude plugin marketplace update cogine-ai", readme)
        self.assertIn("claude plugin update coding-engineer-skills@cogine-ai", readme)
        self.assertIn("claude plugin list --json", readme)

    def test_upstream_lock_covers_current_matt_imports_and_local_hashes(self):
        lock = json.loads((PLUGIN_ROOT / "UPSTREAM_LOCK.json").read_text(encoding="utf-8"))
        self.assertEqual(2, lock["format_version"])
        self.assertRegex(lock["source"]["commit"], r"^[0-9a-f]{40}$")
        self.assertEqual(CURRENT_MATT_IMPORTS, set(lock["skills"]))
        for skill_name, entry in lock["skills"].items():
            self.assertTrue(entry["upstream_path"].startswith("skills/"), skill_name)
            self.assertIsInstance(entry["adaptations"], list, skill_name)
            self.assertRegex(entry["source_commit"], r"^[0-9a-f]{40}$")
            for relative_path, expected in entry["files"].items():
                local_path = PLUGIN_ROOT / "skills" / skill_name / relative_path
                actual = hashlib.sha256(local_path.read_bytes()).hexdigest()
                self.assertEqual(expected["local_sha256"], actual, str(local_path))
                self.assertRegex(expected["upstream_sha256"], r"^[0-9a-f]{64}$")
                self.assertRegex(expected["source_commit"], r"^[0-9a-f]{40}$")
                self.assertTrue(expected["source_path"].startswith("skills/"))
                self.assertIn(expected["mapping"], {"byte-identical", "adapted"})

    def test_reviewed_upstream_adaptations_preserve_local_safety_contracts(self):
        lock = json.loads((PLUGIN_ROOT / "UPSTREAM_LOCK.json").read_text(encoding="utf-8"))
        self.assertEqual([], lock["skills"]["codebase-design"]["adaptations"])
        self.assertTrue(
            any(
                "GLOSSARY-MAP.md" in adaptation
                for adaptation in lock["skills"]["domain-modeling"]["adaptations"]
            )
        )

        merge_skill = (SKILLS_ROOT / "fix-merge-conflicts" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("Stage everything", merge_skill)
        self.assertIn("Stage only", merge_skill)
        self.assertIn("abort", merge_skill.lower())
        self.assertIn("confirmation", merge_skill.lower())

        domain_skill = (SKILLS_ROOT / "domain-modeling" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        adr_format = (SKILLS_ROOT / "domain-modeling" / "ADR-FORMAT.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("selected context", domain_skill)
        self.assertIn("zero-padded", adr_format)

        architecture_skill = (
            SKILLS_ROOT / "improve-codebase-architecture" / "SKILL.md"
        ).read_text(encoding="utf-8")
        html_report = (
            SKILLS_ROOT / "improve-codebase-architecture" / "HTML-REPORT.md"
        ).read_text(encoding="utf-8")
        self.assertIn("secure unique temporary-file", architecture_skill)
        self.assertNotIn("self-contained HTML", architecture_skill)
        self.assertIn('securityLevel: "strict"', html_report)
        self.assertIn("HTML-escape", html_report)

        setup_skill = (
            SKILLS_ROOT / "setup-matt-pocock-skills" / "SKILL.md"
        ).read_text(encoding="utf-8")
        github_tracker = (
            SKILLS_ROOT / "setup-matt-pocock-skills" / "issue-tracker-github.md"
        ).read_text(encoding="utf-8")
        local_tracker = (
            SKILLS_ROOT / "setup-matt-pocock-skills" / "issue-tracker-local.md"
        ).read_text(encoding="utf-8")
        self.assertIn("author_association", github_tracker)
        self.assertNotIn("authorAssociation", github_tracker)
        self.assertIn(".issue_dependencies_summary.blocked_by", github_tracker)
        self.assertNotIn("blockedBy.totalCount", github_tracker)
        self.assertIn(
            ".scratch/<feature-slug>/issues/<NN>-<slug>.md", local_tracker
        )
        self.assertIn("GLOSSARY-MAP.md` already exists", setup_skill)


    def test_lock_verifies_renamed_and_retired_sources_at_their_own_commits(self):
        # Current HEAD lacks the retired path; the renamed source has a different
        # relative filename. Validation must read the declared Git blobs.
        with tempfile.TemporaryDirectory() as tmp:
            temp = Path(tmp)
            upstream = temp / "upstream"
            upstream.mkdir()
            def git(*args):
                return subprocess.run(
                    ["git", "-C", str(upstream), *args], check=True,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                ).stdout.decode().strip()
            git("init", "-q")
            git("config", "user.email", "fixture@example.test")
            git("config", "user.name", "Fixture")
            (upstream / "skills/live").mkdir(parents=True)
            (upstream / "skills/retired").mkdir(parents=True)
            (upstream / "skills/live/OLD.md").write_bytes(b"old live\n")
            (upstream / "skills/retired/SKILL.md").write_bytes(b"retained snapshot\n")
            git("add", "skills")
            git("commit", "-qm", "original")
            original = git("rev-parse", "HEAD")
            (upstream / "skills/live/OLD.md").unlink()
            (upstream / "skills/live/RENAMED.md").write_bytes(b"latest source\n")
            (upstream / "skills/retired/SKILL.md").unlink()
            git("add", "-A")
            git("commit", "-qm", "rename and retire")
            current = git("rev-parse", "HEAD")
            plugin = temp / "plugin"
            skills = plugin / "skills"
            lock = {"format_version": 2, "source": {"commit": current}, "skills": {}}
            for name, commit, source_path, body in (
                ("live", current, "skills/live/RENAMED.md", b"latest source\n"),
                ("retired", original, "skills/retired/SKILL.md", b"retained snapshot\n"),
            ):
                (skills / name).mkdir(parents=True)
                (skills / name / "SKILL.md").write_bytes(body)
                sha = hashlib.sha256(body).hexdigest()
                entry = {"source_commit": commit, "adaptations": [], "files": {
                    "SKILL.md": {"source_commit": commit, "source_path": source_path,
                                 "mapping": "byte-identical", "local_sha256": sha,
                                 "upstream_sha256": sha}}}
                if name == "retired":
                    entry.update(status="retired-upstream-retained-local",
                                 latest_source_path_exists=False, retired_at_commit=current)
                lock["skills"][name] = entry
            (plugin / "UPSTREAM_LOCK.json").write_text(json.dumps(lock))
            with patch.object(VALIDATOR, "PLUGIN_ROOT", plugin), \
                    patch.object(VALIDATOR, "SKILLS_ROOT", skills), \
                    patch.object(VALIDATOR, "CURRENT_MATT_IMPORTS", {"live", "retired"}):
                errors = []
                VALIDATOR.validate_lock(errors, upstream)
                self.assertEqual([], errors)
                (skills / "live/SKILL.md").write_bytes(b"unexpected local drift\n")
                errors = []
                VALIDATOR.validate_lock(errors, upstream)
                self.assertTrue(any("local hash drift" in error for error in errors), errors)
                (skills / "live/SKILL.md").write_bytes(b"latest source\n")
                lock["skills"]["retired"]["files"]["SKILL.md"]["source_commit"] = current
                (plugin / "UPSTREAM_LOCK.json").write_text(json.dumps(lock))
                errors = []
                VALIDATOR.validate_lock(errors, upstream)
                self.assertTrue(any("cannot read pinned source" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
