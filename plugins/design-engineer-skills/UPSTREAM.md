# Upstream source

- Repository: https://github.com/emilkowalski/skills
- Branch: `main`
- Pinned commit: `6bf24434f7730ad169077756cf9c7cd7bd675fc6`
- Packaged on: 2026-07-18

## Compatibility adjustment

The upstream `review-animations` skill sets `disable-model-invocation: true`.
The current Codex skill schema does not accept that frontmatter key, so the
shared cross-platform copy removes that single line. The skill body and all
other upstream files are unchanged.
