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


## Candidate marketing-page design — 2026-09-16

- Repository: https://github.com/Leonxlnx/taste-skill
- Pinned commit: `ccbc15639c97057cbfcf32ecebc38ef716e4bb37`
- Upstream path: `skills/taste-skill/SKILL.md`
- Upstream name: `design-taste-frontend` (v2 experimental)
- Local name: `marketing-page-design-candidate`
- Local display name: 候选营销页面设计
- Version: Design Engineer Skills 0.1.4

The full upstream Markdown body is copied directly into the local `SKILL.md`,
byte for byte. Only its frontmatter `name` and `description` are changed to
identify supplementary candidate use after an existing main design; it is not
a standalone design workflow. Matching Codex UI metadata and the original MIT
license are included. There is no short wrapper or reference-only body.

The selected pin is the version used in the CogineWork comparison.

See `UPSTREAM_TASTE.json` for the source and body hashes. Future refreshes
preserve the complete upstream body and the same two discovery-field overrides.
Growth & GTM documents optional use of this Design skill without bundling a copy.
