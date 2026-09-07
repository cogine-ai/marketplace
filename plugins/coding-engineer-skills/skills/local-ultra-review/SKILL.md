---
name: local-ultra-review
description: Use only when explicitly asked for a high-confidence, read-only local or PR code review.
disable-model-invocation: true
---

# Local Ultra Review

Run a local Ultra Review style code review. The goal is to find real bugs introduced or worsened by the target diff, with low false positives.

This skill is read-only. Do not modify product code, commit, push, or apply fixes.

## Inputs

Invocation examples:

- `/local-ultra-review`
- `/local-ultra-review origin/main`
- `/local-ultra-review HEAD~3..HEAD`
- `/local-ultra-review pr 123`
- `/local-ultra-review https://github.com/org/repo/pull/123`
- `/local-ultra-review --base origin/main --mode deep`
- `/local-ultra-review pr 123 --post summary`
- `/local-ultra-review pr 123 --post review`
- `/local-ultra-review pr 123 --keep-worktree`

If no target is provided, review the current branch against the default base branch and include staged and unstaged tracked changes.

If the target is a GitHub PR, default to `deep` mode, collect PR metadata, review the PR head in an isolated worktree, and render a GitHub-ready summary comment locally. Every target form, including a full URL for the current repository, defaults to `--post none`. Post only when the user explicitly selected `--post summary` / `--post review` or already authorized that posting action in this session; translate such authorization into the corresponding explicit argument without asking again. A PR URL alone does not authorize posting. `--post none` always disables posting.

Modes:

- `light`: four reviewer lenses covering correctness, security/privacy, integration, and tests/verification
- `deep`: default, five reviewer lenses plus verification
- `max`: broader review for large or high-risk changes

GitHub output:

- `--post none`: default for all targets, including current-repository PR URLs; write local artifacts only
- `--post summary`: post one top-level PR summary comment after verification and report rendering
- `--post review`: create one GitHub PR review event with CodeRabbit-style inline comments for verified findings that map to diff-commentable right-side lines; list verified findings that cannot be placed inline in the review body

Worktree lifecycle:

- Default: keep review artifacts in `.local-ultra-review/<session-id>/`, then remove the temporary worktree after report generation and any selected GitHub posting succeeds.
- `--keep-worktree`: preserve the temporary worktree for debugging.
- On failed or interrupted review runs, preserve the worktree and state the path.

## Hard Rules

1. Review only. Do not edit business code.
2. Use an isolated worktree when possible.
3. Prefer `.local-ultra-review/worktrees/<session-id>/` for review workspaces.
4. Add `.local-ultra-review/` to the repository-local git exclude (`.git/info/exclude`), not to the tracked project `.gitignore`, unless the user explicitly asks for a repository file change.
5. Do not copy `.env`, credentials, private keys, tokens, gitignored secrets, or local database config unless the user explicitly allows it.
6. Do not use network access unless the user explicitly allows it, approved project checks require it, or the target is a GitHub PR that requires `gh` for metadata, checkout, or the selected post mode.
7. Do not report style, formatting, naming preference, or generic maintainability advice as findings.
8. A finding must cite exact `file:line`.
9. A finding must include a concrete failure scenario.
10. A finding must be checked by a separate verifier pass before it appears as Important or Nit.
11. If a candidate cannot be verified, put it under `Needs manual review` or omit it.
12. Generating reviewer prompt packets is preparation, not review execution. Never report a completed or verified review from packets alone.
13. The verifier must run in its own independent context, separate from every reviewer context required by the selected mode.
14. Exit code zero, an empty response, or a generated packet is not completion proof. Every reviewer and the verifier must emit its required terminal completion record.
15. `<session-dir>/verification.json` is the authoritative end-to-end execution state. GitHub output must fail closed unless it records `execution_complete: true`.

## Runtime Paths and Arguments

Resolve `<skill-root>` once as the absolute directory containing this `SKILL.md`. Use that resolved path for every supporting file and script, regardless of the current working directory.

Before creating a worktree, resolve `<repo-root>` to the original checkout's
absolute repository root, choose `<session-id>`, and set `<session-dir>` to the
absolute path `<repo-root>/.local-ultra-review/<session-id>`. Never recompute
`<session-dir>` relative to the review worktree. The prepare scripts return
absolute `session_dir` and `worktree` values; retain those returned values and
use them for every later artifact path and repository-working-directory choice.

Parse the user's invocation into explicit values first: target kind, target value, base ref, mode, repository, post mode, and keep-worktree flag. Build an argv list from those values. Never interpolate the user's raw request into a shell command or pass it as one combined shell string. Each example below shows separately quoted argv values; include only the options the user actually selected.

## Supporting Files

- `config/default.yaml`: default review behavior and safety settings.
- `config/severity.yaml`: local severity definitions.
- `config/ignore.yaml`: default low-value path and rule exclusions.
- `prompts/00-review-contract.md`: shared finding bar for all reviewers.
- `prompts/01-impact-mapper.md`: impact map prompt; does not produce findings.
- `prompts/02-*.md` through `06-*.md`: reviewer lens prompts.
- `prompts/07-verifier.md`: required verification pass.
- `prompts/08-dedupe-ranker.md`: dedupe and severity ranking rules.
- `prompts/09-final-report.md`: final report instructions.
- `schemas/*.schema.json`: review bundle and finding schemas.
- `scripts/*.sh` and `scripts/*.py`: optional local automation.
- `templates/*.j2`: report and comment templates.

Load only the supporting files needed for the current phase.

## Pipeline

### Phase 0: Preflight

Run with the parsed argv, for example:

```bash
bash "<skill-root>/scripts/preflight.sh" --base "origin/main" --mode "<mode>"
```

If the script is unavailable, manually inspect:

- git repo root and current branch
- default base branch
- staged, unstaged, and untracked status
- changed files
- package and test commands
- `REVIEW.md`, `AGENTS.md`, `CLAUDE.md`, `README.md`, or equivalent instructions

Stop only if the target cannot be determined or the directory is not a git repository.

### Phase 1: Detect Target

Run with the same parsed argv, for example:

```bash
bash "<skill-root>/scripts/detect-target.sh" --base "origin/main" --mode "<mode>"
```

If no argument is provided, use current branch versus the detected default base and include staged and unstaged tracked changes.

### Phase 2: Prepare Isolated Workspace

For branch or working-tree targets, run:

```bash
bash "<skill-root>/scripts/prepare-worktree.sh" \
  --base "<base-ref>" \
  --session-id "<session-id>" \
  --output-dir "<repo-root>/.local-ultra-review"
```

For GitHub PR targets, first collect PR metadata and then prepare the PR worktree:

```bash
python3 "<skill-root>/scripts/collect-pr-context.py" \
  --pr "<pr-number-or-url>" \
  --repo "<owner/repo-if-known>" \
  --out "<session-dir>/pr-context.json"

bash "<skill-root>/scripts/prepare-pr-worktree.sh" \
  --pr "<pr-number-or-url>" \
  --repo "<owner/repo-if-known>" \
  --base "<pr-base-ref-name>" \
  --session-id "<session-id>" \
  --output-dir "<repo-root>/.local-ultra-review"
```

Expected behavior:

1. Create the absolute `<session-dir>` under the original checkout.
2. Create a detached worktree under `<repo-root>/.local-ultra-review/worktrees/<session-id>/`.
3. Apply staged and unstaged tracked changes when reviewing local working tree changes.
4. Do not copy secrets by default.
5. Add the output directory to `.git/info/exclude` when it is inside the repository.
6. Record base, head, session id, worktree path, and patch paths.

If worktree creation fails, continue read-only from the current working tree and state that isolation was not available.

### Phase 3: Collect Context

Run with the returned absolute `worktree` as the working directory if one
exists, while keeping the output in the original checkout's absolute
`<session-dir>`:

```bash
python3 "<skill-root>/scripts/collect-context.py" \
  --base "<base-ref>" \
  --out "<session-dir>/review-bundle.json"
```

The bundle should include diff patches, changed files, relevant test files, package scripts, project instructions, ignore rules, and detected languages/frameworks. Do not load the whole repository blindly.

### Phase 4: Impact Map

Read `prompts/01-impact-mapper.md` and produce an impact map before looking for bugs. The impact map should identify changed modules, public interfaces, consumers, data models, auth/tenant/privacy boundaries, tests, and high-risk reviewer focus areas. It must not produce final findings.

### Phase 5: Reviewer Passes

Run independent reviewer passes using the shared contract in
`prompts/00-review-contract.md`. The selected mode determines the required
reviewer set:

- `light`: correctness and regression; security and privacy; integration and
  API contract; tests and verification
- `deep` and `max`: all four light lenses plus state, concurrency, migration,
  and rollback

Each reviewer must output candidate findings matching `schemas/candidate-finding.schema.json`, followed by exactly one terminal record matching `schemas/reviewer-completion.schema.json`. A valid zero-finding result contains the terminal record with `candidate_count: 0`; it is not an empty response. Prefer fewer high-confidence findings.

Generate the required reviewer packets with the user's selected mode:

```bash
python3 "<skill-root>/scripts/run-reviewers.py" \
  --bundle "<session-dir>/review-bundle.json" \
  --mode "<mode>" \
  --backend "packets" \
  --out "<session-dir>/reviewers"
```

The `packets` backend only writes prompts and an `execution_complete: false`
manifest. When the host supports subagents, dispatch every generated packet to
a distinct reviewer agent and save each response as its own JSONL file.
Validate each terminal completion record, then record the distinct agent or
task identifiers, candidate counts, per-reviewer statuses, and each validated
record under `completion_receipt` in `<session-dir>/host-dispatch.json`. Set its
`execution_complete` field to `true` only after every mode-required reviewer
returns successfully with a valid completion record.

When independent subagents are unavailable, use the `cli` backend with an explicit command argv after `--command` (which must be the final option). The CLI manifest counts as complete only when all required reviewers exit successfully and return valid completion records. Non-JSON output, an empty response, or a missing/count-mismatched record fails the reviewer.

If the required independent reviewer contexts or a working CLI backend are not
available, stop the review pipeline with status `INCOMPLETE`. Preserve the
packets, explain that reviewers were not executed, and do not claim findings
were verified.

### Phase 6: Verification

Dispatch `prompts/07-verifier.md` to a separate independent verifier context
and verify every candidate. The verifier writes
`<session-dir>/verifier-verdicts.jsonl`, with one verdict per candidate matching
`schemas/verifier-verdict.schema.json`, followed by one terminal record matching
`schemas/verifier-completion.schema.json`. Candidate ids are scoped to their
originating reviewer, so every verdict must copy both `candidate_id` and
`reviewer`. Classify each as:

- `confirmed`
- `false_positive`
- `pre_existing`
- `needs_manual_review`

Only `confirmed` findings may appear in the main Important or Nit sections.

Apply deterministic gates after the independent verifier returns:

```bash
python3 "<skill-root>/scripts/verify-findings.py" \
  --bundle "<session-dir>/review-bundle.json" \
  --candidates "<session-dir>/candidates" \
  --verdicts "<session-dir>/verifier-verdicts.jsonl" \
  --reviewers "<session-dir>/<successful-reviewer-manifest>.json" \
  --out-jsonl "<session-dir>/verification.jsonl" \
  --out-json "<session-dir>/verification.json"
```

Static gates may reject or downgrade a candidate, but they never promote one to `confirmed`. Missing, duplicate, self-authored, non-independent, or reviewer-mismatched verifier verdicts fail closed to `needs_manual_review`. Duplicate candidate ids from one reviewer make execution incomplete; the same short id from different reviewers remains distinct.

### Phase 7: Dedupe and Rank

Read `prompts/08-dedupe-ranker.md`. Deduplicate confirmed findings by root cause and rank by severity:

1. Security, privacy, permission, data loss
2. Production behavior regression
3. Migration, rollback, data compatibility
4. Integration contract break
5. Concurrency, retry, idempotency
6. Test blind spot tied to a concrete behavior risk
7. Nit

Do not pad the report. If no confirmed findings exist, say so.

### Phase 8: Report

Write:

- `<session-dir>/report.md`
- `<session-dir>/findings.json`
- `<session-dir>/candidates.jsonl`
- `<session-dir>/verification.jsonl`
- `<session-dir>/verification.json`
- `<session-dir>/verifier-verdicts.jsonl`
- `<session-dir>/review-bundle.json`
- `<session-dir>/logs/`

For GitHub PR targets, also write:

- `<session-dir>/pr-context.json`
- `<session-dir>/github-pr-comment.md`
- `<session-dir>/github-pr-review-payload.json` when `post_mode` is `review`

Render the local report with `scripts/render-report.py` and pass the
authoritative `verification.json` through `--execution`. An incomplete run may
produce this diagnostic report, but it must render `Execution status:
INCOMPLETE` and must not state a clean result.

```bash
python3 "<skill-root>/scripts/render-report.py" \
  --bundle "<session-dir>/review-bundle.json" \
  --findings "<session-dir>/findings.json" \
  --execution "<session-dir>/verification.json" \
  --out "<session-dir>/report.md"
```

Render the GitHub summary with:

```bash
python3 "<skill-root>/scripts/render-github-summary.py" \
  --pr-context "<session-dir>/pr-context.json" \
  --findings "<session-dir>/findings.json" \
  --execution "<session-dir>/verification.json" \
  --report "<session-dir>/report.md" \
  --out "<session-dir>/github-pr-comment.md" \
  --mode "<mode>" \
  --session-id "<session-id>"
```

If the authorized `post_mode` is `summary`, post exactly one top-level PR comment:

```bash
python3 "<skill-root>/scripts/post-github-summary.py" \
  --pr-context "<session-dir>/pr-context.json" \
  --execution "<session-dir>/verification.json" \
  --body-file "<session-dir>/github-pr-comment.md"
```

If the authorized `post_mode` is `review`, create exactly one GitHub PR review event:

```bash
python3 "<skill-root>/scripts/post-github-review.py" \
  --pr-context "<session-dir>/pr-context.json" \
  --findings "<session-dir>/findings.json" \
  --execution "<session-dir>/verification.json" \
  --mode "<mode>" \
  --session-id "<session-id>" \
  --out "<session-dir>/github-pr-review-payload.json"
```

The GitHub renderers and posters must refuse an incomplete execution artifact before writing or posting a clean result. A complete review event should use inline comments only for verified Important/Nit findings on GitHub diff-commentable right-side lines. Do not force inline comments onto unmappable lines; include those findings in the review body instead.

After report rendering and any selected GitHub posting succeeds, run the
finalizer with `<repo-root>` as its working directory (not from inside the
worktree being removed). Pass the same absolute `<session-dir>` to remove the
temporary worktree while keeping the session artifacts:

```bash
bash "<skill-root>/scripts/finalize-session.sh" \
  --session-dir "<session-dir>" \
  --status success
```

If the run failed, was interrupted, or the user passed `--keep-worktree`, preserve the worktree:

```bash
bash "<skill-root>/scripts/finalize-session.sh" \
  --session-dir "<session-dir>" \
  --status failure \
  --keep-worktree
```

The final response to the user should include only:

1. Execution status: `COMPLETE` or `INCOMPLETE`
2. Important count
3. Nit count
4. Pre-existing count
5. Report path
6. Top 3 findings, if any

Do not paste large logs into chat.
