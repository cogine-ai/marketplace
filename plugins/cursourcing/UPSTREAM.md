# Cursourcing release source

- Repository: https://github.com/cogine-ai/cursourcing
- Source commit: [bda12e68d3eb9176bcf0b9fd66b289081c9e5fad](https://github.com/cogine-ai/cursourcing/commit/bda12e68d3eb9176bcf0b9fd66b289081c9e5fad)
- Plugin version: `0.1.3`
- License: Apache-2.0 for Cursourcing's original material; bundled dependencies
  retain their respective licenses in `dist/THIRD_PARTY_NOTICES.md`.
- Export: `node scripts/export-plugin.mjs <marketplace>/plugins/cursourcing`

The manifest, MCP configuration, bundled runtime, dependency notices, visual
assets, English and Chinese READMEs, documentation, skill files, LICENSE, and
NOTICE match this commit byte for byte. This file records marketplace provenance
and is maintained here.

Validation: plugin and skill validation and all 24 automated tests passed,
including bundled MCP discovery, concurrent execution, input handling, quiet
waits, and permission persistence across recovery. Exported files were compared
byte for byte with the source commit. A real ACP review performed 23 tool calls
with zero permission requests; its five-minute run did not complete the review,
so it is evidence of coordination behavior only, not an independent approval or
a measurement of total token savings. Cursourcing remains the seventh Codex plugin.
