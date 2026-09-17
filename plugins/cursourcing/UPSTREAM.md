# Cursourcing distribution source

- Repository: https://github.com/cogine-ai/cursourcing
- Source commit: `695fa239c9b209fef1e010094ba3f3ad8d93c821`
- Plugin version: `0.2.2`
- Bundled runtime SHA-256: `7b4cd4a95dd41b8a7f2c23dc6029cdf33b5d8299ecf712b220f3fd1a6d2ca16e`.
- License: Apache-2.0 for Cursourcing's original material; bundled dependencies
  retain their respective licenses in `dist/THIRD_PARTY_NOTICES.md`.
- Export: `node scripts/export-plugin.mjs <marketplace>/plugins/cursourcing`

The 17 exported files (manifest, MCP configuration, bundled runtime, dependency
notices, assets, READMEs, documentation, skills, LICENSE, and NOTICE) match the
source commit byte for byte. This file records marketplace provenance and is
maintained here; it does not assert that a tag or GitHub Release is published.

Validation: build and all 35 offline tests passed, including bundled MCP
compact/full results, permissions, recovery, local notifications, transport
failures, and bounded native-history cleanup before follow-ups. Skill format,
JSON/version consistency, local documentation links and export parity passed.
The skill, MCP guidance, invocation prompts and READMEs use the same default:
Cursor delivers the first complete result; Codex takes over acceptance and
bounded corrections. Tool schemas and execution behavior remain compatible.
These checks do not establish model behavior, live service reliability or token
savings. Historical evaluation artifacts stay local and outside the snapshot.
