#!/usr/bin/env python3
"""Prepare a separate CogineX package with an explicit account integration mode."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys


APP_ID_PATTERN = re.compile(r"(?:asdk_app_|connector_|templated_apps_)[A-Za-z0-9][A-Za-z0-9_-]*\Z")
MARKETPLACE_NAME_PATTERN = re.compile(r"[a-z][a-z0-9-]*\Z")
RECEIPT_NAME = "package-receipt.json"
DEFAULT_MARKETPLACE_NAME = "coginex-local"


def _contains(parent, child):
    return parent == child or parent in child.parents


def _tree_digest(source):
    digest = hashlib.sha256()
    for path in sorted(source.rglob("*")):
        relative = path.relative_to(source).as_posix().encode("utf-8")
        if path.is_symlink():
            kind, content = b"link", os.readlink(path).encode("utf-8")
        elif path.is_file():
            kind, content = b"file", path.read_bytes()
        else:
            continue
        digest.update(kind + b"\0" + relative + b"\0")
        digest.update(hashlib.sha256(content).digest())
    return digest.hexdigest()


def _write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _write_marketplaces(output, manifest, name):
    # Both native catalogs resolve ./ to this prepared plugin's root.
    for relative in (".agents", ".agents/plugins", ".claude-plugin"):
        directory = output / relative
        if directory.is_symlink():
            raise ValueError("Marketplace directories must not be symlinks: {}".format(relative))
        directory.mkdir(parents=True, exist_ok=True)
    catalogs = {
        ".agents/plugins/marketplace.json": {
            "name": name,
            "interface": {"displayName": "CogineX Local"},
            "plugins": [{
                "name": manifest["name"],
                "source": {"source": "local", "path": "./"},
                "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                "category": "Productivity",
            }],
        },
        ".claude-plugin/marketplace.json": {
            "name": name,
            "description": "Local CogineX package prepared for Codex and Claude Code.",
            "owner": manifest["author"],
            "plugins": [{
                "name": manifest["name"],
                "source": "./",
                "version": manifest["version"],
                "description": manifest.get("description", "CogineX local plugin."),
                "category": "productivity",
            }],
        },
    }
    for relative, catalog in catalogs.items():
        path = output / relative
        if path.is_symlink():
            path.unlink()
        _write_json(path, catalog)


def prepare_package(source, output, *, app_id=None, direct_mcp=False,
                    with_marketplace=False, marketplace_name=DEFAULT_MARKETPLACE_NAME):
    """Copy source into a new output folder; never alter the source or host settings."""
    if (app_id is not None) == bool(direct_mcp):
        raise ValueError("Choose exactly one of app_id or direct_mcp.")
    if app_id is not None and not APP_ID_PATTERN.fullmatch(app_id):
        raise ValueError("Use an actual asdk_app_, connector_, or templated_apps_ ID, without plugin_.")
    if with_marketplace and not MARKETPLACE_NAME_PATTERN.fullmatch(marketplace_name):
        raise ValueError("The marketplace name must use lowercase letters, digits, and hyphens, starting with a letter.")
    if not with_marketplace and marketplace_name != DEFAULT_MARKETPLACE_NAME:
        raise ValueError("marketplace_name requires with_marketplace.")

    source_path = Path(source).expanduser().absolute()
    output_path = Path(output).expanduser().absolute()
    source_root = source_path.resolve(strict=True)
    output_root = output_path.resolve()
    if not source_root.is_dir():
        raise ValueError("The package source must be a directory.")
    for candidate_source, candidate_output in ((source_path, output_path), (source_root, output_root)):
        if _contains(candidate_source, candidate_output) or _contains(candidate_output, candidate_source):
            raise ValueError("Source and output must be separate directories; nesting is not supported.")
    if os.path.lexists(output_path):
        raise FileExistsError("Output already exists: {}".format(output_path))

    manifest_dir = source_root / ".codex-plugin"
    manifest_path = manifest_dir / "plugin.json"
    if manifest_dir.is_symlink() or manifest_path.is_symlink():
        raise ValueError("The Codex manifest must be a regular package file, not a symlink.")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict):
        raise ValueError("The Codex manifest must be a JSON object.")
    source_digest = _tree_digest(source_root)
    receipt = {
        "schemaVersion": 1,
        "origin": {"kind": "package-source", "sourceTreeSha256": source_digest},
        "plugin": {"name": manifest.get("name"), "version": manifest.get("version")},
        "mode": "registered-app" if app_id is not None else "direct-mcp",
    }
    if app_id is not None:
        receipt["appId"] = app_id
        manifest["apps"] = "./.app.json"
    else:
        manifest.pop("apps", None)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.mkdir()  # Exclusive creation also rejects a competing output path.
    try:
        # Preserve links without reading anything outside the package source.
        shutil.copytree(source_root, output_path, symlinks=True, dirs_exist_ok=True)
        target_app = output_path / ".app.json"
        if os.path.lexists(target_app):
            target_app.unlink()
        if app_id is not None:
            _write_json(target_app, {"apps": {"coginex": {"id": app_id, "required": True}}})
        _write_json(output_path / ".codex-plugin" / "plugin.json", manifest)
        if with_marketplace:
            _write_marketplaces(output_path, manifest, marketplace_name)
        target_receipt = output_path / RECEIPT_NAME
        if target_receipt.is_symlink():
            target_receipt.unlink()
        _write_json(target_receipt, receipt)
    except BaseException:
        shutil.rmtree(output_path)
        raise
    return receipt


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="New output folder; it must not already exist.")
    parser.add_argument("--with-marketplace", action="store_true", help="Include native catalogs so this folder can be added as a marketplace.")
    parser.add_argument("--marketplace-name", default=DEFAULT_MARKETPLACE_NAME,
                        help="Catalog name with --with-marketplace (default: %(default)s).")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--app-id", help="Existing registered App ID, without the plugin_ prefix.")
    mode.add_argument("--direct-mcp", action="store_true", help="Prepare direct HTTP MCP for both hosts.")
    args = parser.parse_args(argv)
    try:
        receipt = prepare_package(Path(__file__).resolve().parents[1], args.output,
                                  app_id=args.app_id, direct_mcp=args.direct_mcp,
                                  with_marketplace=args.with_marketplace,
                                  marketplace_name=args.marketplace_name)
    except (OSError, ValueError) as error:
        parser.exit(1, "Package preparation failed: {}\n".format(error))
    print(json.dumps({"output": str(args.output.expanduser().resolve()), **receipt}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
