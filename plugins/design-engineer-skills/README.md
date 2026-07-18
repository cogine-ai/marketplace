# Design Engineer Skills

Design Engineer Skills bundles six reusable workflows for design engineers:

- `emil-design-eng` — UI polish, component design, and animation decisions.
- `review-animations` — strict review of animation and motion code.
- `improve-animations` — codebase-wide motion audit and implementation plans.
- `find-animation-opportunities` — find useful motion without over-animating.
- `animation-vocabulary` — map vague motion descriptions to precise terms.
- `apple-design` — apply Apple-style physical interaction principles to web UI.

## Credits

The skill content is from [emilkowalski/skills](https://github.com/emilkowalski/skills)
by Emil Kowalski and is redistributed under the MIT License. Cogine AI provides
the Codex and Claude Code packaging in this repository.

## Cross-platform compatibility

The skills are shared by Codex and Claude Code. The upstream
`review-animations` skill includes `disable-model-invocation: true`, which is
not accepted by the current Codex skill schema. This package removes that one
frontmatter line; the skill body and all other upstream content remain
unchanged.
