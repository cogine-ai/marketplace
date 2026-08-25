# Coding Engineer Skills

Coding Engineer Skills is a deliberately curated engineering toolkit for
Codex and Claude Code. It favors Cogine's own workflows and lightweight
engineering skills. It does not bundle the full `superpowers` workflow pack.
The plugin contains 30 skills.

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

### Review, security, and developer experience — 7

- `code-review`
- `local-ultra-review`
- `ai-app-security-audit`
- `security-best-practices`
- `devex-review`
- `plan-devex-review`
- `planmode-engineer`

### Git, CI, worktrees, and shipping — 5

- `worktree-management`
- `fix-ci`
- `loop-on-ci`
- `fix-merge-conflicts`
- `review-and-ship`

### Repository configuration — 1

- `setup-matt-pocock-skills`

## Design choices

- Cogine-authored and Cogine-adapted skills are preferred where they solve the
  same problem as a larger generic workflow pack.
- Matt Pocock's `to-spec` chain is included alongside `backlog-ready-spec` on
  purpose: one synthesizes an existing discussion, while the other checks
  readiness, duplication, boundaries, and validation.
- `implement` uses the bundled `tdd` guidance where appropriate, runs checks,
  and reviews the result directly against the originating spec and repository
  standards before committing. `code-review` remains a separate fixed-point
  branch review, `local-ultra-review` remains the deeper read-only defect
  review, and `review-and-ship` remains the explicit push and pull-request gate.
- `improve-codebase-architecture` coordinates `grilling`, `domain-modeling`,
  and `codebase-design`. The pure `grill-with-docs` composition alias is not
  bundled because both underlying skills remain independently available.
- Platform-specialist packs such as iOS, macOS, Cloudflare, and vendor service
  integrations are not part of this core plugin.
- Some skills need local tools or services for their full workflow, such as
  GitHub CLI, Playwright, or a browser-capable host. Their instructions retain
  their own capability checks and fallbacks.
- Twelve workflow commands are explicit-only in both hosts. The remaining
  eighteen skills are model-invokable and carry concise what-and-when trigger
  descriptions. Full skill bodies are loaded only when invoked.
- Operational cross-skill calls use the full
  `coding-engineer-skills:<skill>` identity so another globally installed
  skill with the same short name cannot intercept the workflow.
- The larger `superpowers` pack remains out of the always-on index.

See [UPSTREAM.md](./UPSTREAM.md) and
[THIRD_PARTY_NOTICES.md](./THIRD_PARTY_NOTICES.md) for provenance.
