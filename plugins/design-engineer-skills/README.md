# Design Engineer Skills

Design Engineer Skills bundles eight reusable workflows for design engineers:

- `emil-design-eng` — UI polish, component design, and animation decisions.
- `prototype` — build three to five genuinely different UI directions behind a live picker.
- `pick-ui-library` — choose one suitable frontend library from Emil's curated list.
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
`review-animations`, `prototype`, and `pick-ui-library` use explicit-invocation
metadata upstream that is not accepted by the shared Codex skill schema. This
package removes those frontmatter fields and preserves explicit invocation for
the two new skills through Codex `agents/openai.yaml` policy files.
