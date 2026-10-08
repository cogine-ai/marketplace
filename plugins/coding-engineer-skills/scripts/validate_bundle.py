#!/usr/bin/env python3
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

import yaml


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PLUGIN_ROOT.parents[1]
SKILLS_ROOT = PLUGIN_ROOT / "skills"

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

OPERATIONAL_MODEL_CALLS = {
    "implement": {"tdd"},
    "tdd": {"codebase-design"},
    "improve-codebase-architecture": {
        "codebase-design",
        "grilling",
        "domain-modeling",
    },
}

EXPLICIT_USER_HANDOFFS = {
    "code-review": {"setup-matt-pocock-skills"},
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_frontmatter(path: Path):
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not match:
        raise ValueError("missing YAML frontmatter")
    data = yaml.safe_load(match.group(1))
    if not isinstance(data, dict):
        raise ValueError("frontmatter must be a mapping")
    return data, text


def contains_bare_skill_call(text: str, target: str) -> bool:
    return bool(
        re.search(
            rf"(?:^|[\s`])/{re.escape(target)}(?![A-Za-z0-9_/-])",
            text,
            flags=re.MULTILINE,
        )
    )


def validate_inventory(errors):
    expected = USER_ONLY | MODEL_INVOKED
    actual = {path.name for path in SKILLS_ROOT.iterdir() if path.is_dir()}
    if actual != expected:
        errors.append(
            f"skill inventory differs: missing={sorted(expected - actual)} "
            f"extra={sorted(actual - expected)}"
        )
    if len(actual) != 30:
        errors.append(f"expected 30 skills, found {len(actual)}")

    for name in sorted(actual):
        skill_dir = SKILLS_ROOT / name
        try:
            frontmatter, text = load_frontmatter(skill_dir / "SKILL.md")
        except (OSError, ValueError, yaml.YAMLError) as exc:
            errors.append(f"{name}: invalid SKILL.md: {exc}")
            continue

        if frontmatter.get("name") != name:
            errors.append(f"{name}: frontmatter name does not match directory")
        for placeholder in ("${CLAUDE_SKILL_DIR}", "$ARGUMENTS"):
            if placeholder in text:
                errors.append(f"{name}: contains unsupported runtime placeholder {placeholder}")

        openai_path = skill_dir / "agents" / "openai.yaml"
        if not openai_path.is_file():
            errors.append(f"{name}: missing agents/openai.yaml")
            continue
        try:
            agent = yaml.safe_load(openai_path.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError as exc:
            errors.append(f"{name}: invalid agents/openai.yaml: {exc}")
            continue

        policy = agent.get("policy", {})
        if name in USER_ONLY:
            if frontmatter.get("disable-model-invocation") is not True:
                errors.append(f"{name}: explicit-only frontmatter policy is missing")
            if policy.get("allow_implicit_invocation") is not False:
                errors.append(f"{name}: Codex explicit-only policy is missing")
        else:
            if "disable-model-invocation" in frontmatter:
                errors.append(f"{name}: model skill has Claude explicit-only policy")
            if "allow_implicit_invocation" in policy:
                errors.append(f"{name}: model skill overrides Codex invocation default")

        interface = agent.get("interface", {})
        short_description = interface.get("short_description", "")
        if not 25 <= len(short_description) <= 64:
            errors.append(
                f"{name}: short_description must be 25-64 characters "
                f"(found {len(short_description)})"
            )
        default_prompt = interface.get("default_prompt")
        if default_prompt and f"${name}" not in default_prompt:
            errors.append(f"{name}: default_prompt must mention ${name}")


def validate_cross_skill_calls(errors):
    expected = USER_ONLY | MODEL_INVOKED
    for source, targets in OPERATIONAL_MODEL_CALLS.items():
        text = (SKILLS_ROOT / source / "SKILL.md").read_text(encoding="utf-8")
        for target in targets:
            if target not in MODEL_INVOKED:
                errors.append(f"{source}: operational target {target} is not model-invokable")
            if f"coding-engineer-skills:{target}" not in text:
                errors.append(f"{source}: missing namespaced call to {target}")

    for source, targets in EXPLICIT_USER_HANDOFFS.items():
        text = (SKILLS_ROOT / source / "SKILL.md").read_text(encoding="utf-8")
        for target in targets:
            if target not in USER_ONLY:
                errors.append(f"{source}: explicit handoff target {target} is not user-only")
            if f"coding-engineer-skills:{target}" not in text:
                errors.append(f"{source}: missing namespaced handoff to {target}")

    for source, targets in {**OPERATIONAL_MODEL_CALLS, **EXPLICIT_USER_HANDOFFS}.items():
        text = (SKILLS_ROOT / source / "SKILL.md").read_text(encoding="utf-8")
        for target in targets:
            if target not in expected:
                errors.append(f"{source}: references missing skill {target}")
            if contains_bare_skill_call(text, target):
                errors.append(f"{source}: contains bare operational /{target} reference")


def validate_metadata(errors):
    readme = (PLUGIN_ROOT / "README.md").read_text(encoding="utf-8")
    listed = set(re.findall(r"^- `([a-z0-9-]+)`$", readme, re.MULTILINE))
    expected = USER_ONLY | MODEL_INVOKED
    if listed != expected:
        errors.append("plugin README skill list differs from the directory inventory")
    if "30 skill" not in readme:
        errors.append("plugin README does not state the 30-skill inventory")

    versions = []
    for manifest_path in (
        PLUGIN_ROOT / ".claude-plugin" / "plugin.json",
        PLUGIN_ROOT / ".codex-plugin" / "plugin.json",
    ):
        manifest = load_json(manifest_path)
        versions.append(manifest.get("version"))
        if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", manifest.get("version", "")):
            errors.append(f"{manifest_path}: invalid semantic version")
        if "Thirty focused" not in manifest.get("description", ""):
            errors.append(f"{manifest_path}: description does not state Thirty focused skills")

    marketplace = load_json(REPO_ROOT / ".claude-plugin" / "marketplace.json")
    entries = {entry["name"]: entry for entry in marketplace.get("plugins", [])}
    coding = entries.get("coding-engineer-skills", {})
    versions.append(coding.get("version"))
    if len(set(versions)) != 1:
        errors.append("coding versions differ between manifests and marketplace")
    if "Thirty focused" not in coding.get("description", ""):
        errors.append("marketplace description does not state Thirty focused skills")


def validate_lock(errors, matt_root=None):
    lock = load_json(PLUGIN_ROOT / "UPSTREAM_LOCK.json")
    if lock.get("format_version") != 2:
        errors.append("UPSTREAM_LOCK.json must use per-file source mapping format 2")
    default_commit = lock.get("source", {}).get("commit", "")
    if not re.fullmatch(r"[0-9a-f]{40}", default_commit):
        errors.append("UPSTREAM_LOCK.json has an invalid default source commit")
    if set(lock.get("skills", {})) != CURRENT_MATT_IMPORTS:
        errors.append("UPSTREAM_LOCK.json does not cover the 12 retained Matt imports")

    for skill_name, entry in lock.get("skills", {}).items():
        if not isinstance(entry.get("adaptations"), list):
            errors.append(f"{skill_name}: adaptations must be a list")
        if entry.get("status") == "retired-upstream-retained-local":
            if entry.get("latest_source_path_exists") is not False:
                errors.append(f"{skill_name}: retired source must not claim a current path")
            if not re.fullmatch(r"[0-9a-f]{40}", entry.get("retired_at_commit", "")):
                errors.append(f"{skill_name}: retirement commit is missing")
        for relative_path, hashes in entry.get("files", {}).items():
            local_relative = Path(relative_path)
            if local_relative.is_absolute() or ".." in local_relative.parts:
                errors.append(f"{skill_name}: invalid local file mapping: {relative_path}")
                continue
            local_path = SKILLS_ROOT / skill_name / local_relative
            if not local_path.is_file():
                errors.append(f"{skill_name}: locked file is missing: {relative_path}")
                continue
            local_bytes = local_path.read_bytes()
            if hashlib.sha256(local_bytes).hexdigest() != hashes.get("local_sha256"):
                errors.append(f"{skill_name}: local hash drift: {relative_path}")
            if not re.fullmatch(r"[0-9a-f]{64}", hashes.get("upstream_sha256", "")):
                errors.append(f"{skill_name}: invalid upstream hash: {relative_path}")
            source_commit = hashes.get("source_commit", entry.get("source_commit", default_commit))
            source_path = hashes.get("source_path", "")
            source_relative = Path(source_path)
            if not re.fullmatch(r"[0-9a-f]{40}", source_commit):
                errors.append(f"{skill_name}: invalid source commit: {relative_path}")
                continue
            if (not source_path or source_relative.is_absolute()
                    or ".." in source_relative.parts):
                errors.append(f"{skill_name}: invalid source path: {relative_path}")
                continue
            if hashes.get("mapping") not in {"byte-identical", "adapted"}:
                errors.append(f"{skill_name}: invalid mapping mode: {relative_path}")
            if hashes.get("mapping") == "byte-identical" and hashes.get("local_sha256") != hashes.get("upstream_sha256"):
                errors.append(f"{skill_name}: byte-identical mapping has unequal hashes: {relative_path}")

            source_bytes = None
            if matt_root is not None:
                proc = subprocess.run(
                    ["git", "-C", str(matt_root), "show", f"{source_commit}:{source_path}"],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                )
                if proc.returncode != 0:
                    errors.append(f"{skill_name}: cannot read pinned source {source_commit}:{source_path}")
                else:
                    source_bytes = proc.stdout
                    if hashlib.sha256(source_bytes).hexdigest() != hashes.get("upstream_sha256"):
                        errors.append(f"{skill_name}: upstream hash drift: {relative_path}")
            for region in hashes.get("raw_source_regions", []):
                try:
                    start, end = region["landing_byte_range_half_open"]
                    if not (0 <= start <= end <= len(local_bytes)):
                        raise ValueError("invalid landing range")
                    if hashlib.sha256(local_bytes[start:end]).hexdigest() != region["sha256"]:
                        raise ValueError("landing bytes differ")
                    if source_bytes is not None:
                        start, end = region["byte_range_half_open"]
                        if not (0 <= start <= end <= len(source_bytes)):
                            raise ValueError("invalid source range")
                        if hashlib.sha256(source_bytes[start:end]).hexdigest() != region["sha256"]:
                            raise ValueError("source bytes differ")
                except (KeyError, TypeError, ValueError) as exc:
                    errors.append(f"{skill_name}: raw source region drift: {relative_path}: {exc}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--matt-root",
        type=Path,
        help="Optional mattpocock/skills Git checkout containing all per-file pinned commits.",
    )
    args = parser.parse_args()

    errors = []
    validate_inventory(errors)
    validate_cross_skill_calls(errors)
    validate_metadata(errors)
    validate_lock(errors, args.matt_root)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Bundle validation failed with {len(errors)} error(s).", file=sys.stderr)
        sys.exit(1)

    lock = load_json(PLUGIN_ROOT / "UPSTREAM_LOCK.json")
    file_count = sum(len(entry["files"]) for entry in lock["skills"].values())
    print(
        "Validated 30 skills, 12 explicit-only policies, "
        f"18 model-invokable policies, and {file_count} locked upstream files."
    )


if __name__ == "__main__":
    main()
