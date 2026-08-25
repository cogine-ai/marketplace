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
            if re.search(rf"(?<!coding-engineer-skills:)/{re.escape(target)}\b", text):
                errors.append(f"{source}: contains bare operational /{target} reference")


def validate_metadata(errors):
    readme = (PLUGIN_ROOT / "README.md").read_text(encoding="utf-8")
    listed = set(re.findall(r"^- `([a-z0-9-]+)`$", readme, re.MULTILINE))
    expected = USER_ONLY | MODEL_INVOKED
    if listed != expected:
        errors.append("plugin README skill list differs from the directory inventory")
    if "30 skill" not in readme:
        errors.append("plugin README does not state the 30-skill inventory")

    for manifest_path in (
        PLUGIN_ROOT / ".claude-plugin" / "plugin.json",
        PLUGIN_ROOT / ".codex-plugin" / "plugin.json",
    ):
        manifest = load_json(manifest_path)
        if manifest.get("version") != "0.2.0":
            errors.append(f"{manifest_path}: expected version 0.2.0")
        if "Thirty focused" not in manifest.get("description", ""):
            errors.append(f"{manifest_path}: description does not state Thirty focused skills")

    marketplace = load_json(REPO_ROOT / ".claude-plugin" / "marketplace.json")
    entries = {entry["name"]: entry for entry in marketplace.get("plugins", [])}
    coding = entries.get("coding-engineer-skills", {})
    if coding.get("version") != "0.2.0":
        errors.append("marketplace coding-engineer-skills version is not 0.2.0")
    if "Thirty focused" not in coding.get("description", ""):
        errors.append("marketplace description does not state Thirty focused skills")


def validate_lock(errors, matt_root=None):
    lock = load_json(PLUGIN_ROOT / "UPSTREAM_LOCK.json")
    if lock.get("source", {}).get("commit") != "6654f6b60cd9d5be8b54c6fafe44346dabeb3b76":
        errors.append("UPSTREAM_LOCK.json has the wrong Matt commit")
    if set(lock.get("skills", {})) != CURRENT_MATT_IMPORTS:
        errors.append("UPSTREAM_LOCK.json does not cover the 10 current Matt imports")

    for skill_name, entry in lock.get("skills", {}).items():
        if not isinstance(entry.get("adaptations"), list):
            errors.append(f"{skill_name}: adaptations must be a list")
        for relative_path, hashes in entry.get("files", {}).items():
            local_path = SKILLS_ROOT / skill_name / relative_path
            if not local_path.is_file():
                errors.append(f"{skill_name}: locked file is missing: {relative_path}")
                continue
            if digest(local_path) != hashes.get("local_sha256"):
                errors.append(f"{skill_name}: local hash drift: {relative_path}")
            if not re.fullmatch(r"[0-9a-f]{64}", hashes.get("upstream_sha256", "")):
                errors.append(f"{skill_name}: invalid upstream hash: {relative_path}")

    if matt_root is None:
        return
    proc = subprocess.run(
        ["git", "-C", str(matt_root), "rev-parse", "HEAD"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if proc.returncode != 0:
        errors.append(f"cannot read Matt checkout: {proc.stderr.strip()}")
        return
    if proc.stdout.strip() != lock["source"]["commit"]:
        errors.append(
            f"Matt checkout is {proc.stdout.strip()}, expected {lock['source']['commit']}"
        )
        return
    for skill_name, entry in lock["skills"].items():
        for relative_path, hashes in entry["files"].items():
            upstream_path = matt_root / entry["upstream_path"] / relative_path
            if not upstream_path.is_file():
                errors.append(f"{skill_name}: upstream file is missing: {relative_path}")
            elif digest(upstream_path) != hashes["upstream_sha256"]:
                errors.append(f"{skill_name}: upstream hash drift: {relative_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--matt-root",
        type=Path,
        help="Optional checkout of mattpocock/skills at the locked commit.",
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
