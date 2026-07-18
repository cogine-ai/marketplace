# Coding Engineer Skills

Coding Engineer Skills is a deliberately curated engineering toolkit for
Codex and Claude Code. It favors Cogine's own workflows and Matt Pocock's
lightweight engineering skills. It does not bundle `superpowers`.

## Included skills

### Specs and delivery — 4

- `backlog-ready-spec`
- `to-spec`
- `to-tickets`
- `implement`

### Orchestration — 3

- `cogine-orchestrator`
- `cogine-multirepo-worker`
- `cogine-power-gates`

### Architecture, debugging, and testing — 4

- `codebase-design`
- `diagnosing-bugs`
- `tdd`
- `run-smoke-tests`

### Frontend and React — 3

- `frontend-design`
- `vercel-react-best-practices`
- `shadcn`

### Review, security, and developer experience — 6

- `local-ultra-review`
- `ai-app-security-audit`
- `security-best-practices`
- `devex-review`
- `plan-devex-review`
- `planmode-engineer`

### Git, CI, and shipping — 4

- `fix-ci`
- `loop-on-ci`
- `fix-merge-conflicts`
- `review-and-ship`

## Design choices

- Cogine-authored and Cogine-adapted skills are preferred where they solve the
  same problem as a larger generic workflow pack.
- Matt Pocock's `to-spec` chain is included alongside `backlog-ready-spec` on
  purpose: one synthesizes an existing discussion, while the other checks
  readiness, duplication, boundaries, and validation.
- Platform-specialist packs such as iOS, macOS, Cloudflare, and vendor service
  integrations are not part of this core plugin.
- Some skills need local tools or services for their full workflow, such as
  GitHub CLI, Playwright, or a browser-capable host. Their instructions retain
  their own capability checks and fallbacks.
- Claude Code's plugin inspector estimates about 1,204 always-on tokens for the
  24 skill names and trigger summaries. Full skill bodies are paid only when a
  skill is invoked. This selection was reduced from a broader 44-skill draft
  after measuring its 3,571-token always-on index.

See [UPSTREAM.md](./UPSTREAM.md) and
[THIRD_PARTY_NOTICES.md](./THIRD_PARTY_NOTICES.md) for provenance.
