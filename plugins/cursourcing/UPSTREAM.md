# Cursourcing distribution source

- Repository: https://github.com/cogine-ai/cursourcing
- Source commit: `42c23046bf5159d3055262495d72a2684981c221`
- Plugin version: `0.2.3`
- Bundled runtime SHA-256: `c5116b1b2bdac9a00747f5a390eaf8af4270952f9f6b863c64a7e5ca2a615fc2`.
- License: Apache-2.0 for Cursourcing's original material; bundled dependencies
  retain their respective licenses in `dist/THIRD_PARTY_NOTICES.md`.
- Export: `node scripts/export-plugin.mjs <marketplace>/plugins/cursourcing`

The 17 exported files (manifest, MCP configuration, bundled runtime, dependency
notices, assets, READMEs, documentation, skills, LICENSE, and NOTICE) match the
source commit byte for byte. This file records marketplace provenance and is
maintained here; it does not assert that a tag or GitHub Release is published.

Validation: build and all 47 offline tests passed, including host-death recovery
guards, failure recovery facts, process cleanup, compact/full results, permissions,
concurrent execution and bounded native-history replay. A separate real-time MCP
fixture check returned after 120,004 ms under the 150-second tool deadline and
verified early delivery and cancellation. Skill/plugin format, JSON/version
consistency, local documentation links and export parity passed.

The skill and tools retain the two-phase workflow: Cursor delivers the first
complete result; Codex takes over acceptance and bounded corrections. Waits now
default to 120 seconds. Failure summaries expose recovery eligibility, and an
unconfirmed previous execution blocks takeover and replacement work. Grok 4.6
xhigh fast remains the execution model.

These checks do not establish model behavior, live service reliability or token
savings for 0.2.3. The README's token comparison is the historical 0.2.2/B4
evaluation; raw evaluation artifacts stay local and outside the snapshot.
