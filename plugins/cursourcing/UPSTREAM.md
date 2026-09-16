# Cursourcing release source

- Repository: https://github.com/cogine-ai/cursourcing
- Source commit: [6849794a333aedff008dfa23b4b5b1460e125484](https://github.com/cogine-ai/cursourcing/commit/6849794a333aedff008dfa23b4b5b1460e125484)
- Plugin version: `0.2.0`
- Bundled runtime SHA-256: `b0dd85751bcfbc806f0d66d94bb6a8aa58633d99e4e626f6dc3bb47da0b0b2dd`.
- License: Apache-2.0 for Cursourcing's original material; bundled dependencies
  retain their respective licenses in `dist/THIRD_PARTY_NOTICES.md`.
- Export: `node scripts/export-plugin.mjs <marketplace>/plugins/cursourcing`

The 17 exported files (manifest, MCP configuration, bundled runtime, dependency
notices, assets, READMEs, documentation, skills, LICENSE, and NOTICE) match the
source commit byte for byte. This file records marketplace provenance and is
maintained here.

Validation: all 27 offline tests passed, including bundled MCP compact/full
results, permissions, recovery, local notifications without filesystem events,
transport diagnostics, and retained output. Skill format, JSON/version
consistency, and export parity checks passed. The protocol tests use simulated
ACP peers; they do not establish live service behavior or model token savings.
Cursourcing remains the seventh Codex plugin.
