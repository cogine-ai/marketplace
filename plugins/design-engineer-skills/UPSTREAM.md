# Upstream source

- Repository: https://github.com/emilkowalski/skills
- Branch: `main`
- Pinned commit: `70744e3816f1d93eafb697161a8b880a7384c5ff`
- Packaged on: 2026-07-29
- Skills: `animation-vocabulary`, `apple-design`, `emil-design-eng`,
  `find-animation-opportunities`, `improve-animations`, `pick-ui-library`,
  `prototype`, `review-animations`

## Compatibility adjustment

The upstream `review-animations`, `prototype`, and `pick-ui-library` skills set
explicit-invocation frontmatter that the current shared Codex skill schema does
not accept. The package removes those fields. Codex policy metadata keeps
`prototype` and `pick-ui-library` explicit-only; the skill bodies and bundled
references otherwise match the pinned upstream snapshot.
