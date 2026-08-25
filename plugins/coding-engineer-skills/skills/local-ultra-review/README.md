# Local Ultra Review

**Bring Claude Code's `/ultrareview` quality bar to your local agent workflow.**

Local Ultra Review is a portable agent skill for deep, high-precision code review. It recreates the core mechanics of Claude Code's cloud `/ultrareview` flow using local primitives: git worktrees, focused reviewer lenses, independent verification, dedupe, and severity-ranked findings.

It is built for one thing: **report real bugs before merge, not style opinions.**

> This project is not affiliated with Anthropic. It is a local, open skill inspired by the public Claude Code `/ultrareview` and Code Review documentation.

## Install

```bash
npx skills add https://github.com/cogine-ai/local-ultra-review --skill local-ultra-review
```

Then invoke it from a skill-aware agent:

```text
/local-ultra-review
```

## Why This Exists

Normal AI code review often fails in predictable ways:

- it reports style advice instead of bugs
- it guesses instead of verifying
- it reviews the diff without enough surrounding context
- it repeats the same finding in different words
- it treats "missing tests" as the main issue

Claude Code's `/ultrareview` raises the bar with isolated review environments, multiple reviewer agents, independent verification, dedupe, and severity ranking.

Local Ultra Review brings that pattern to local workflows without depending on Anthropic's remote VM or Claude Code's built-in slash command.

## Default Command

```text
/local-ultra-review
```

Default behavior:

- reviews the current branch against the detected default base branch
- includes staged and unstaged tracked changes
- excludes untracked files by default
- uses `deep` mode
- creates a local git worktree when possible
- writes artifacts under `.local-ultra-review/<session-id>/`
- removes the temporary worktree after a successful report unless `--keep-worktree` is used
- adds `.local-ultra-review/` to `.git/info/exclude`, not the tracked project `.gitignore`
- avoids copying secrets or `.env` files
- avoids network access by default
- reports only verified Important/Nit findings in the main report

## Command Examples

```text
/local-ultra-review
/local-ultra-review origin/main
/local-ultra-review HEAD~3..HEAD
/local-ultra-review pr 123
/local-ultra-review https://github.com/org/repo/pull/123
/local-ultra-review --base origin/main --mode light
/local-ultra-review --base origin/main --mode deep
/local-ultra-review --base origin/main --mode max
/local-ultra-review pr 123 --post summary
/local-ultra-review pr 123 --post review
/local-ultra-review pr 123 --keep-worktree
```

## Modes

| Mode | Use when | Reviewer coverage |
| --- | --- | --- |
| `light` | You want a faster pre-merge bug pass | correctness, security/privacy, integration, tests/verification (four reviewers) |
| `deep` | Default. You want high confidence before merge | correctness, security/privacy, integration, state/concurrency/migration, tests |
| `max` | Large or high-risk changes | same core reviewers, with room for domain-specific expansion |

## GitHub PR Review

GitHub PR targets are first-class review inputs:

```text
/local-ultra-review pr 123
/local-ultra-review https://github.com/org/repo/pull/123
/local-ultra-review pr 123 --repo org/repo
```

Default PR behavior:

- uses `deep` mode
- collects PR metadata with `gh pr view`
- checks out the PR head into an isolated local worktree
- reviews the PR diff through the normal Local Ultra Review pipeline
- writes a full local report and `findings.json`
- removes the temporary worktree after a successful run unless `--keep-worktree` is used
- renders a GitHub-ready top-level summary comment
- does **not** post to GitHub for PR numbers or non-current-repo PR URLs unless explicitly requested
- automatically posts one GitHub PR review event when the user provides a full PR URL for the current checkout's `origin` repository

To opt out of posting for a current-repo PR URL:

```text
/local-ultra-review https://github.com/org/repo/pull/123 --post none
```

To post the legacy summary comment:

```text
/local-ultra-review pr 123 --post summary
```

To post a GitHub PR review explicitly:

```text
/local-ultra-review pr 123 --post review
```

`--post review` creates one GitHub review event. It leaves CodeRabbit-style inline comments for verified Important/Nit findings that map cleanly to right-side lines in the PR diff. If a verified finding cannot be placed on a GitHub diff-commentable line, Local Ultra Review lists it in the review body instead of forcing a bad inline comment.

The generated PR comment follows this shape:

```markdown
## Automated Local Ultra Review

**Commit:** `9d6dfb537194`
**Mode:** `deep`

| Review Score | Findings | Severity Breakdown |
|---:|---:|---|
| **100/100** (Pass) | **0** | P0: 0 / P1: 0 / P2: 0 / P3: 0 |

> [!IMPORTANT]
> This is an automated Local Ultra Review. Treat findings as review candidates for human verification.

### Review Findings

I did not identify any verified, discrete, actionable bugs introduced by this PR.

<!-- pr-review-agent provider=local-ultra-review head=<sha> session=<id> -->
```

## Design Mapping

| Claude Code `/ultrareview` mechanic | Local Ultra Review equivalent |
| --- | --- |
| Remote sandbox | Local `git worktree` review workspace |
| Fleet of reviewer agents | Four independent reviewers in `light`, or five in `deep`/`max`, each with an explicit completion receipt; packets and empty responses never count as execution |
| Full codebase context | Diff bundle with changed files, nearby code, tests, project instructions, and package metadata |
| Independent finding verification | Dedicated verifier pass with reviewer-scoped candidate identities, evidence, base/head checks, and its own completion receipt |
| Dedupe and severity ranking | Local scripts merge findings and sort by impact |
| Background task | Optional local runner that writes artifacts and report files |

## Review Pipeline

1. **Preflight** checks git status, target, tools, test commands, and project instructions.
2. **Target detection** resolves branch, range, PR, base, and mode.
3. **Worktree isolation** creates a temporary review workspace and applies local tracked patches.
4. **Context collection** builds a reproducible review bundle instead of loading the whole repo.
5. **Impact mapping** identifies changed modules, public contracts, consumers, and risk areas.
6. **Reviewer lenses** run in four independent contexts for `light`, or five for `deep`/`max`; security is always included.
7. **Verification** runs in a separate independent context and filters candidates into confirmed, false positive, pre-existing, or needs manual review.
8. **Dedupe/ranking** merges duplicate root causes and ranks Important findings before Nits.
9. **Report rendering** writes Markdown and JSON artifacts.

## What Counts as a Finding

A finding must include:

- exact `file:line`
- concrete failure scenario
- evidence from code or contract paths
- why the current diff introduced or worsened it
- verification plan or verifier confirmation

The main report excludes:

- style preferences
- generic maintainability advice
- speculative risks
- unverified concerns
- missing tests with no concrete behavior risk
- generated files, lockfiles, vendored code, and CI-enforced lint noise

## Severity Model

| Severity | Meaning |
| --- | --- |
| `Important` | Should be fixed before merge: production bug, security/privacy issue, data loss, broken contract, migration risk, serious regression |
| `Nit` | Minor concrete issue worth fixing, but not a merge blocker |
| `Pre-existing` | Real issue that existed before this diff |
| `NeedsManualReview` | Plausible concern that did not meet the verification bar |

## What's Inside

```text
local-ultra-review/
├── SKILL.md
├── config/
├── prompts/
├── schemas/
├── scripts/
├── templates/
├── examples/
└── output/
```

Key files:

- `SKILL.md`: agent entrypoint and non-negotiable workflow rules
- `prompts/00-review-contract.md`: shared finding bar for every reviewer
- `prompts/02-*.md` through `06-*.md`: focused reviewer lenses
- `prompts/07-verifier.md`: independent verification contract
- `schemas/*.schema.json`: structured bundle and finding formats
- `scripts/collect-context.py`: builds the review bundle
- `scripts/collect-pr-context.py`: records GitHub PR metadata
- `scripts/prepare-pr-worktree.sh`: checks out PR heads into isolated worktrees
- `scripts/run-reviewers.py`: generates reviewer packets or runs CLI backends
- `scripts/verify-findings.py`: applies programmatic finding gates
- `scripts/dedupe-rank.py`: merges duplicate findings and ranks severity
- `scripts/render-report.py`: writes the final report
- `scripts/render-github-summary.py`: writes a GitHub-ready PR summary comment
- `scripts/post-github-summary.py`: optionally posts that summary via `gh pr comment`
- `scripts/post-github-review.py`: optionally posts a GitHub PR review with inline comments via `gh api`
- `scripts/ensure-local-ignore.sh`: adds the output directory to `.git/info/exclude`
- `scripts/finalize-session.sh`: removes or preserves the temporary worktree after report generation

## Optional Script Usage

Most users should invoke the skill from an agent. The scripts are included so agents can run deterministic steps instead of rewriting glue code. Resolve `<skill-root>` to the absolute directory containing this README or `SKILL.md`, resolve `<repo-root>` before creating the worktree, set `<session-dir>` to the absolute path `<repo-root>/.local-ultra-review/session`, and retain the user's selected `<mode>`. Retain the absolute `session_dir` and `worktree` returned by the applicable prepare script; run repository-sensitive steps in that returned worktree but keep every artifact path under `<session-dir>`. Pass each option as a separate argv value.

```bash
bash "<skill-root>/scripts/preflight.sh" --base "origin/main"
bash "<skill-root>/scripts/detect-target.sh" --base "origin/main" --mode "<mode>"
bash "<skill-root>/scripts/prepare-worktree.sh" --base "origin/main" --session-id "session" --output-dir "<repo-root>/.local-ultra-review"
python3 "<skill-root>/scripts/collect-context.py" --base "origin/main" --out "<session-dir>/review-bundle.json"
bash "<skill-root>/scripts/run-checks.sh" --dry-run --out "<session-dir>/checks"
python3 "<skill-root>/scripts/run-reviewers.py" --bundle "<session-dir>/review-bundle.json" --mode "<mode>" --backend "packets" --out "<session-dir>/reviewers"
```

The `packets` backend stops at preparation. Before verification, dispatch the
generated reviewer packets in separate contexts, validate every completion
receipt, collect their candidate JSONL under `<session-dir>/candidates/`, and write a complete
`<session-dir>/host-dispatch.json`. Then dispatch the independent verifier with
`prompts/07-verifier.md`, collect one verdict per candidate plus its completion
receipt, and write `<session-dir>/verifier-verdicts.jsonl`. Only after those host
steps succeed, continue:

```bash
python3 "<skill-root>/scripts/verify-findings.py" --bundle "<session-dir>/review-bundle.json" --candidates "<session-dir>/candidates" --verdicts "<session-dir>/verifier-verdicts.jsonl" --reviewers "<session-dir>/host-dispatch.json" --out-jsonl "<session-dir>/verification.jsonl" --out-json "<session-dir>/verification.json"
python3 "<skill-root>/scripts/dedupe-rank.py" --verification "<session-dir>/verification.jsonl" --out "<session-dir>/findings.json"
python3 "<skill-root>/scripts/render-report.py" --bundle "<session-dir>/review-bundle.json" --findings "<session-dir>/findings.json" --execution "<session-dir>/verification.json" --out "<session-dir>/report.md"
```

For GitHub PR targets only, collect `pr-context.json` and use the PR worktree
flow described in `SKILL.md`. Render GitHub output only after verification, and
run a posting script only when the user's selected post mode authorizes it:

```bash
python3 "<skill-root>/scripts/render-github-summary.py" --pr-context "<session-dir>/pr-context.json" --findings "<session-dir>/findings.json" --execution "<session-dir>/verification.json" --report "<session-dir>/report.md" --out "<session-dir>/github-pr-comment.md"
python3 "<skill-root>/scripts/post-github-review.py" --pr-context "<session-dir>/pr-context.json" --findings "<session-dir>/findings.json" --execution "<session-dir>/verification.json" --mode "<mode>" --session-id "session" --out "<session-dir>/github-pr-review-payload.json"
```

After report generation and any authorized posting succeeds, finalize from
`<repo-root>`:

```bash
bash "<skill-root>/scripts/finalize-session.sh" \
  --session-dir "<session-dir>" \
  --status "success"
```

Run the finalizer with `<repo-root>` as its working directory, not from inside
the worktree it is removing.

For `--reviewers`, pass `reviewers/manifest.json` after a successful CLI run or
`host-dispatch.json` after the host has validated every mode-required subagent
completion receipt.

`run-reviewers.py` supports two honest backend shapes:

| Backend | Status | Purpose |
| --- | --- | --- |
| `packets` | preparation only | generates the mode-required reviewer packets and records `execution_complete: false`; the host must dispatch them |
| `cli` | execution | runs all reviewer prompts through an explicit CLI argv and records complete only when every reviewer succeeds with a valid terminal receipt |

For `cli`, put `--command` last and pass the executable plus each argument as
separate argv entries. If the required independent contexts or a working CLI are not
available, the review is `INCOMPLETE`; packet generation must never be
reported as a finished review. Every reviewer returns a
`reviewer_complete` record, and the independent verifier returns a
`verifier_complete` record even when there are zero candidates. The generated
`verification.json` is the only execution state consumed by reports and
GitHub output.

## Output

Expected session artifacts:

```text
.local-ultra-review/<session-id>/
├── report.md
├── findings.json
├── candidates.jsonl
├── verifier-verdicts.jsonl
├── verification.jsonl
├── verification.json
├── review-bundle.json
├── pr-context.json
├── github-pr-comment.md
├── github-pr-review-payload.json
├── logs/
├── host-dispatch.json
└── worktree-path.txt
```

The temporary worktree is normally removed after a successful run. `worktree-path.txt` remains as provenance for the review workspace that was used. Failed or interrupted runs preserve the worktree for debugging; remove it later with `scripts/cleanup.sh` or `scripts/finalize-session.sh`.

The final agent response should stay short:

- Important count
- Nit count
- Pre-existing count
- report path
- top 3 findings, if any

## Project-Level Review Rules

Add a `REVIEW.md` file to a repository to tune the review bar:

```markdown
# Review Instructions

## Important findings

- Auth or permission bypass
- Tenant isolation bug
- PII in logs
- Backward-incompatible API change
- Data migration that cannot be rolled back
- Incorrect billing, quota, or payment behavior
- Broken async retry or idempotency behavior

## Do not report

- Formatting
- Naming preferences
- Generated files
- Lockfiles
- Issues already enforced by CI
```

`REVIEW.md` is treated as review-specific guidance and should be more important than generic project docs for severity and skip rules.

## Philosophy

Local Ultra Review is intentionally conservative:

**Fewer findings. Better findings.**

It is better to return two verified bugs than twenty plausible comments. The verifier is the product.

## References

- [Claude Code: Find bugs with ultrareview](https://code.claude.com/docs/en/ultrareview)
- [Claude Code: Code Review](https://code.claude.com/docs/en/code-review)
- [Claude Code: Skills](https://code.claude.com/docs/en/skills)
- [Claude Code: Worktrees](https://code.claude.com/docs/en/worktrees)
