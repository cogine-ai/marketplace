# Upstream source

- Repository: https://github.com/emilkowalski/skills
- Branch: `main`
- Pinned commit: `70744e3816f1d93eafb697161a8b880a7384c5ff`
- Packaged on: 2026-07-29
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
