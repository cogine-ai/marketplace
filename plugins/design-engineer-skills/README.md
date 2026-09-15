# Design Engineer Skills

Design Engineer Skills bundles nine reusable workflows for design engineers:

- `marketing-page-design-candidate` — 候选营销页面设计: supplement an established main design with an extra marketing-page candidate; not a standalone design workflow.
- `emil-design-eng` — UI polish, component design, and animation decisions.
- `prototype` — build three to five genuinely different UI directions behind a live picker.
- `pick-ui-library` — choose one suitable frontend library from Emil's curated list.
- `review-animations` — strict review of animation and motion code.
- `improve-animations` — codebase-wide motion audit and implementation plans.
- `find-animation-opportunities` — find useful motion without over-animating.
- `animation-vocabulary` — map vague motion descriptions to precise terms.
- `apple-design` — apply Apple-style physical interaction principles to web UI.

## Credits

The eight existing skills are from [emilkowalski/skills](https://github.com/emilkowalski/skills)
by Emil Kowalski. The supplementary marketing-page skill is from
[Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill), with its complete
body preserved and only the skill name and description adapted. Both sources
are MIT licensed; Taste Skill's license is retained in its skill directory.
Cogine AI provides the Codex and Claude Code packaging. See [UPSTREAM.md](UPSTREAM.md)
for source pins and local metadata adjustments.

## Cross-platform compatibility

The skills are shared by Codex and Claude Code. The upstream
`review-animations`, `prototype`, and `pick-ui-library` use explicit-invocation
metadata upstream that is not accepted by the shared Codex skill schema. This
package removes those frontmatter fields and preserves explicit invocation for
the two new skills through Codex `agents/openai.yaml` policy files.
