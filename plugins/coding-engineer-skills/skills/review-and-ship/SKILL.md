---
name: review-and-ship
description: Final self-review and shipping workflow for completed code tasks. Use when Codex is ready to review an entire task branch, resolve blockers, run verification, commit focused changes, push to the correct remote branch, and open or update a GitHub pull request.
---

# Review and ship

Use this as the final gate for a completed task, especially after long-running work with multiple commits or mixed local changes. Treat the review target as the whole branch effect relative to the correct base, not only the latest diff.

## Workflow

1. Resolve shipping context.
   - Read repository instructions first: `AGENTS.md`, `CLAUDE.md`, Cursor rules, nearest project-specific agent docs, and user instructions.
   - Resolve target/base branch from user instruction, active PR, repo instructions, or remote default branch. Do not assume `origin/main`.
   - Inspect current branch/upstream, worktree status, untracked files, recent commits, changed files, and branch diff.

2. Reconstruct task scope.
   - Review `git log <base>..HEAD`, `git diff --stat <base>...HEAD`, and the full changed-file list.
   - Compare final branch effect against user intent and recent relevant context.
   - Identify unrelated, accidental, generated, secret, or environment files before staging.

3. Self-review before shipping.
   - Check correctness, regressions, intent fit, test coverage, security/auth/permissions, data or migration impact, env/config/deployment impact, and docs/README needs.
   - Classify findings as `blocker`, `risk`, or `note`.
   - Treat blockers as required fixes before shipping; include accepted risks in the PR.

4. Fix blockers in scope.
   - Fix blockers and rerun affected checks.
   - Stop and ask before broadening scope, changing product direction, or making risky data/deployment changes.

5. Verify with evidence.
   - Choose commands from repo instructions, package scripts, CI config, or project conventions.
   - Run focused checks first; run broader checks when the diff touches shared contracts, builds, tests, or release surfaces.
   - Record exact commands and outcomes. State any check that could not run and why.

6. Commit intentionally.
   - Stage only files that belong to the task.
   - In a mixed worktree, use explicit paths; do not default to `git add -A`.
   - Review staged diff before committing.
   - Keep commit messages concise and scoped.

7. Push and open/update PR.
   - Never push directly to protected/default branches.
   - Push the current task branch with upstream tracking when needed.
   - Open or update the PR against the resolved target branch.
   - If PR checks are available, prefer `gh pr checks --json name,bucket,state,workflow,link` or equivalent PR-level status over raw workflow guesses.

## Suggested Checks

```bash
git status -sb
git branch --show-current
git log --oneline <base>..HEAD
git diff --stat <base>...HEAD
git diff --name-status <base>...HEAD
git diff <base>...HEAD
git diff --cached
```

## Guardrails

- Prioritize correctness, security, and regressions over style-only comments.
- Preserve unrelated user changes and untracked files unless the user explicitly includes them.
- Do not ship while blockers remain.
- Do not claim verification success without fresh command output.
- If pre-commit checks fail, fix the issues rather than bypassing hooks.

## Output

- Base/target branch and reviewed range
- Findings summary (`blocker`, `risk`, `note`)
- Fixes made during self-review
- Validation commands and outcomes
- Commit and PR URL
- Remaining risks or follow-ups
