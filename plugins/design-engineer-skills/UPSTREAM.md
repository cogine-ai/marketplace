# Upstream source

- Repository: https://github.com/emilkowalski/skills
- Branch: `main`
- Pinned commit: `0b85d4b36ad772ed2c46a66522ede1c8a26f9929`
- Refreshed on: 2026-09-15
- Skills: `animation-vocabulary`, `apple-design`, `emil-design-eng`,
  `find-animation-opportunities`, `improve-animations`, `pick-ui-library`,
  `prototype`, `review-animations`

## Compatibility adjustment

On 2026-09-08, `prototype` and `pick-ui-library` gained Claude Code's
`disable-model-invocation: true`, matching their existing explicit-only
descriptions and Codex `policy.allow_implicit_invocation: false` metadata.
`review-animations` retains its current invocation policy. The skill bodies
and bundled references otherwise match the pinned upstream snapshot; this is
a local host-policy correction, not an upstream body refresh.

## Complete upstream refresh with retained local adaptations — 2026-09-15

Seven existing entries receive the upstream Initial Response addition. All upstream bodies and support files match this pin. Existing Codex metadata and Claude invocation controls remain intact; emil-design-eng has no upstream file change.

See `UPSTREAM_SYNC_2026-09-15.json` for the per-entry overlay ledger. The refresh ships as version 0.1.3 in both Codex and Claude Code manifests and the Claude marketplace catalog.
