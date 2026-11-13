# Coding Engineer Skills

Coding Engineer Skills is a deliberately curated engineering toolkit for
Codex and Claude Code. It favors Cogine's own workflows and lightweight
engineering skills. It does not bundle the full `superpowers` workflow pack.
The plugin contains 36 skills.

## Included skills

### Specs and delivery — 3

- `backlog-ready-spec`
- `to-spec`
- `to-tickets`

### Orchestration — 3

- `cogine-orchestrator`
- `cogine-multirepo-worker`
- `cogine-power-gates`

### Architecture, domain, debugging, and testing — 7

- `codebase-design`
- `domain-modeling`
- `grilling`
- `improve-codebase-architecture`
- `diagnosing-bugs`
- `tdd`
- `run-smoke-tests`

### Frontend and React — 3

- `frontend-design`
- `vercel-react-best-practices`
- `shadcn`

### Review, security, and developer experience — 10

- `code-review`
- `sol-loop`
- `council`
- `local-ultra-review`
- `good-offence`
- `ai-app-security-audit`
- `security-best-practices`
- `devex-review`
- `plan-devex-review`
- `planmode-engineer`

### Git, CI, worktrees, and shipping — 10

- `worktree-management`
- `fix-ci`
- `review-and-ship`
- `modernize`
- `takeover`
- `leaving-pr-comments`
- `file-pr`
- `babysit-pr`
- `full-send`
- `full-stop`

## Design choices

- Cogine-authored and Cogine-adapted skills are preferred where they solve the
  same problem as a larger generic workflow pack.
- Matt Pocock's `to-spec` chain is included alongside `backlog-ready-spec` on
  purpose: one synthesizes an existing discussion, while the other checks
  readiness, duplication, boundaries, and validation.
- To implement a spec or ticket, ask your coding agent directly. Use `tdd`
  when the work calls for test-first development. Request a commit explicitly
  if you want one. `code-review` reviews committed changes from a fixed point,
  `local-ultra-review` provides deeper read-only review, and `review-and-ship`
  handles an explicitly requested push and pull request.
- `good-offence` guides agents reviewing unnecessary defensive implementations:
  duplicate checks, guards, catches and recovery layers. It offers suggestions,
  with practical examples and deeper references available as needed.
- `improve-codebase-architecture` coordinates `grilling`, `domain-modeling`,
  and `codebase-design`. The pure `grill-with-docs` composition alias is not
  bundled because both underlying skills remain independently available.
- Platform-specialist packs such as iOS, macOS, Cloudflare, and vendor service
  integrations are not part of this core plugin.
- Some skills need local tools or services for their full workflow, such as
  GitHub CLI, Playwright, or a browser-capable host. Their instructions retain
  their own capability checks and fallbacks.
- Ten workflow commands are explicit-only in both hosts. The remaining
  twenty-six skills are model-invokable. Full skill bodies are loaded only
  when invoked.
- Local cross-skill calls use the full `coding-engineer-skills:<skill>`
  identity. The unmodified tstack skills keep their upstream references.
- The larger `superpowers` pack remains out of the always-on index.

See [UPSTREAM.md](./UPSTREAM.md) and
[THIRD_PARTY_NOTICES.md](./THIRD_PARTY_NOTICES.md) for provenance.
