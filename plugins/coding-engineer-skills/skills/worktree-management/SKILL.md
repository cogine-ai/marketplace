---
name: worktree-management
description: Create, use, and safely retire an isolated Git worktree for coding changes. Use when the user requests a worktree or isolation, the current checkout is dirty, parallel branches or agents need separation, or a large or risky change should not disturb the current workspace. Do not use for read-only work, small low-risk edits, or when already in an adequate isolated worktree.
---

# Worktree Management

Ensure coding work is isolated when the isolation is worth its cost, then leave a clear cleanup path.

**Core principle:** Detect existing isolation first. Prefer native worktree tools. Fall back to Git only when needed. Never discard work to clean up.

Announce when using this skill.

## 1. Detect Existing Isolation

```bash
git_dir=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
git_common=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
branch_name=$(git branch --show-current)
git rev-parse --show-superproject-working-tree 2>/dev/null
```

If the last command returns a path, this is a submodule, not a linked worktree.

If `git_dir != git_common` and this is not a submodule, reuse the existing worktree. Report its path and branch; do not create a nested worktree. Treat detached HEAD as externally managed unless the user asks to create a branch.

## 2. Decide Whether To Isolate

Create or recommend a worktree when the user requests one, the checkout has unrelated changes, work must run beside another branch or release lane, multiple agents need separate filesystems, or the change is broad or risky.

If isolation is only a recommendation and no standing preference exists, ask before creating it. Otherwise work in place.

## 3. Create The Worktree

Prefer a native worktree or isolation tool supplied by the host. It owns placement and cleanup; do not create parallel Git metadata behind it.

When no native tool exists:

1. Verify the requested base branch or commit.
2. Follow an explicit path preference or an existing repository convention.
3. For a project-local `.worktrees/` or `worktrees/` directory, require `git check-ignore` to confirm it is ignored. Do not modify or commit `.gitignore` solely to create a worktree without approval; use an external sibling/task directory or ask instead.
4. Create the worktree and branch:

```bash
git worktree add "$worktree_path" -b "$new_branch" "$base_ref"
```

If creation is blocked by the sandbox, report it and continue in place only when doing so will not disturb unrelated work.

## 4. Set Up And Verify

Read the repository's `AGENTS.md` and setup instructions first. Install or build dependencies only when the task or validation requires them; use the repository's lockfile-aware command instead of a generic install recipe.

Run a proportional clean-baseline check. Prefer focused checks for small changes and broader checks for risky changes. If the baseline fails, separate environmental or pre-existing failures from product failures and report them before implementation.

Report the worktree path, branch, base ref, and baseline result.

## 5. Finish And Clean Up

At task completion, always state whether the worktree is retained or ready to remove. For a manually created worktree, inspect before proposing cleanup:

```bash
git -C "$worktree_path" status --short
git worktree list
du -sh "$worktree_path"
```

Remove it only after the user confirms, a standing cleanup instruction applies, or the host's native lifecycle owns cleanup. Require a clean worktree and verify that no needed branch or untracked work will be lost.

```bash
git worktree remove "$worktree_path"
git worktree prune
```

Never use `--force` or delete the local branch without separate authorization. `git worktree prune` removes stale metadata; it does not remove an existing worktree directory. If cleanup is deferred, report the path, branch, disk usage, and reason.

## Safety Rules

- Never create a nested worktree.
- Never overwrite or remove a worktree containing uncommitted work.
- Never manually remove a host-managed worktree.
- Never assume dependency directories are shared safely across worktrees.
- Keep branch deletion separate from worktree removal.
