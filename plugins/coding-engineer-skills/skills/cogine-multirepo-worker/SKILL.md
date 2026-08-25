---
name: cogine-multirepo-worker
description: "Use for Cogine's classic one-worker-per-repository control plane; use cogine-orchestrator for shared WORK/TEST lanes."
disable-model-invocation: true
---

# Cogine Multirepo Worker

Coordinate Cogine repository work as a manual Codex App control plane with one guarded worker thread per active repository. Keep the root orchestrator focused on queue mapping, worker monitoring, owner decisions, and avoiding duplicate scheduled automation.

## Operating Boundary

- Treat this as a manual skill, not a scheduled agent runtime.
- Do not start, rerun, or replace existing `auto-agents` launchd jobs unless the user explicitly asks.
- Use existing automation outputs as signals: labels, comments, draft readiness notes, PR review markers, CI, and GitHub state.
- Default discovery scope is non-archived `cogine-ai` repositories. Use `shared/target-repos.md` only as the auto-agents signal list; outside it, assume no scheduled-agent support unless verified.
- If Codex thread tools are unavailable, report that orchestration cannot manage worker threads in this environment. Do not pretend shell commands can replace thread lifecycle operations.

## Model To Copy

Mirror the `steipete/agent-scripts` maintainer-orchestrator model:

- One root orchestrator owns thread topology.
- One active repository maps to one worker thread.
- Keep work for a repository in its existing orchestrator-owned worker.
- Rename a worker whenever assigning or materially changing work: `<Project>: <short current task>`.
- Keep the root/orchestrator thread title stable. The root must never retitle itself while using this skill.
- Do not set or request a custom model for workers; omit model selection and inherit the platform default.
- Workers cannot create subworkers, delegate work, manage other chats, or perform portfolio triage.
- The root stays lightweight: inspect, delegate, monitor, ask decisions, and report.
- Substantial investigation, implementation, review, live proof, landing preparation, and release execution happen in repository worker threads.

## Start Checklist

1. Enumerate non-archived `cogine-ai` repositories; map local checkouts when useful.
2. Read `shared/target-repos.md` and `registry/local-cron-agents.yaml` for scheduled-agent signal coverage.
3. Check current Codex threads with `list_threads` when available; reuse only eligible orchestrator-owned repo workers after reading current state.
4. For each target repo, use `github-project-triage` when available to map open issues, open PRs, CI, labels, latest release, and relevant automation comments.
5. Read and update `~/.codex/state/cogine-multirepo-worker/ledger.md`.
6. Build a compact current-state ledger: `Active`, `Needs owner`, `Ready next`, `Blocked`, `Recent public mutations`, `Owner exclusions`. Omit archived, not-visible, historical, and completed-idle workers unless they still carry an unresolved owner decision or explicitly reusable lane.

## Persistent Log

- This root orchestrator owns `~/.codex/state/cogine-multirepo-worker/ledger.md`; workers do not edit it.
- Treat the ledger as a current-state control surface, not an append-only transcript. Rewrite and compact it in place on every meaningful root pass.
- Record high-level current state only: active worker thread id/title, repo/PR, purpose, last known result, owner decision needed, and next root action.
- Preserve recent public mutations only when useful for readback or audit: merged PRs, closed PRs/issues, posted comments, exact commit SHAs, and canonical URLs.
- Remove archived, not-visible, user-owned, historical, and completed-idle workers once they no longer affect an owner decision or next root action.
- If an old detail matters only for audit, collapse it into one line under `Recent public mutations`; do not carry raw worker reports forward.
- Include full canonical issue/PR URLs and useful current worker thread ids or titles when relevant.
- Never record secrets, private credential values, routine polling, or raw worker transcripts.

## Ledger Compaction

- Treat ledger compaction as normal maintenance, not a separate owner-gated action.
- A compact ledger should answer: what is active, what needs the owner, what can be done next, what is blocked, what was publicly changed recently, and what the owner excluded.
- Completed work disappears from `Active` and `Ready next` as soon as its only remaining value is historical. Keep only a compact public-mutation line if the result still matters.
- `archived` and `not_visible` are transport/UI states, not orchestration states. Do not list them unless the root is actively investigating a missing current worker.

## Thread Lifecycle

Use Codex App thread tools as the lifecycle surface:

- `list_projects`: find the saved project before creating project-scoped workers.
- `create_thread`: create a new repo worker only when no suitable worker exists.
- `read_thread`: inspect a worker before sending instructions, renaming, archiving, or declaring it blocked.
- `send_message_to_thread`: assign the next task or unblock a worker.
- `set_thread_title`: keep project worker titles current only when the concrete worker thread id is known.
- `set_thread_archived`: archive completed idle workers after root confirms no immediate next repo work.
- `handoff_thread`: move a worker to another Codex host only when the user asks or the current host cannot run required proof.

Never create duplicate workers for the same repo without first reading all plausible existing orchestrator-owned workers. If two threads have unique progress, leave both intact and ask the owner before merging or retiring either lane.

### Thread Title Protocol

Thread titles are a navigation aid, not part of the task proof. They must never obscure thread ownership.

- The root/orchestrator thread keeps its existing title. When using this skill in the current thread, assume the current thread is root and do not call `set_thread_title` on it.
- Project worker titles should show lane type, item id, and phase:
  - PR lane: `<Project>: PR #<number> <phase>` such as `DearClaw: PR #709 review` or `DearClaw: PR #711 repair`.
  - Issue lane: `<Project>: Issue #<number> <phase>` for a single issue, or `<Project>: Issues #<a>+#<b> <phase>` for deliberate batching.
  - Research/live-proof lane: `<Project>: Research <topic>` or `<Project>: Live proof <topic>`.
  - Idle/completed lane: `<Project>: <lane type> idle` only after the worker has no active task.
- Do not leave project worker titles at `Phase1`, `Phase2`, `Autocode`, stale merged PR numbers, or bare `#123` names.
- Root may retitle a project worker only after it has a concrete `threadId`, and only when that `threadId` is known not to be the root thread id. Never retitle a `pendingWorktreeId`.
- The initial `create_thread` prompt must not ask the pending worker to call `set_thread_title`; the root should set the title with the thread tool after the worker thread exists, or include a plain `Suggested title` line for later root action.
- A running project worker may update its own title only if the title tool clearly targets its own project worker thread. If unavailable or ambiguous, it must end reports with `Suggested title: ...` and leave the actual title change to root.

### Thread Ownership Gate

Reuse only a thread that satisfies at least one condition:

- the root orchestrator created it as a repo worker for the current orchestration run;
- `~/.codex/state/cogine-multirepo-worker/ledger.md` explicitly marks it as an active or explicitly reusable `orchestrator-owned` repo worker;
- the owner names the exact thread id and explicitly authorizes retitling or reassignment for the current repo-worker lane.

Do not reuse, retitle, or send new worker assignments to same-repo historical, planning, review, repair, strategy, or user-owned threads merely because they mention the target repo or contain useful context. Treat those threads as context/reference only.

If preflight classifies a repo as having no current active repo-worker, later broad authorization to "create or reuse repo workers" permits reuse only of threads that pass this ownership gate. Otherwise, create a fresh project-scoped worker when delegation is authorized.

## Queue Classification

Classify every queue item:

- `Autonomous`: bounded, reproducible, technically safe, and verifiable with available tools.
- `Needs owner`: product choice, security/privacy decision, missing credentials/access, unavailable live proof, destructive choice, merge/close/release approval, or unclear priority.
- `Existing automation`: already covered by active auto-agents; observe outputs instead of rerunning.
- `Ignored by owner`: explicitly named by the owner as out of current scope.

Labels are discovery, routing, and prioritization hints, not classification proof. Do not classify an item as `Autonomous`, `Needs owner`, `Blocked`, or `Ready next` from labels alone; refresh the issue or PR body, comments, draft state, mergeability, CI, linked work, code state, and worker proof first.

Do not treat stale, difficult, draft, or platform-specific items as ignored. Only explicit owner instruction creates an ignored exception.

## Delegation Rule

For each repo worker prompt, include:

- repo full name and canonical item URLs;
- current assignment and why it was selected;
- authorization boundary: read, implement, push/PR update, CI rerun/fix, merge, close, release;
- no-subdelegation rule;
- thread-title boundary: root title is stable; project worker title changes require a concrete non-root worker `threadId`; otherwise the worker reports `Suggested title: ...`;
- CI waiting protocol: after code changes or push/PR update, report local verification and one current CI snapshot before any long CI watch/polling; wait for CI only after explicit owner instruction;
- instruction to read repo `AGENTS.md`, docs, issue/PR discussion, code, tests, and current CI;
- required proof before stopping;
- explicit stop condition for owner decision.

## Authorization

Treat triage, monitoring, implementation, public mutation, CI repair, and release as separate permissions.

- Queue analysis or monitoring does not authorize edits.
- Delegation or parallel-worker creation requires explicit owner authorization.
- Implementation permission authorizes local changes and verification only unless the owner also authorizes push or PR updates.
- Push permission does not imply CI repair, merge, close, release, tag, or publish permission.
- CI rerun and CI-fix permission must be explicit; a push alone does not authorize additional repair commits or workflow mutation.
- Merge and close permission must be explicit for the affected issue or PR.
- Release, version bump, tag, registry publish, deployment, and GitHub Release require a current explicit release request.
- Broad scope expansion outside `cogine-ai` and live-proof waivers require fresh explicit owner confirmation.

Record the granted permissions in every worker prompt and in `~/.codex/state/cogine-multirepo-worker/ledger.md`. Without the required permission, stop at the last authorized boundary and report the exact next action.

## Worker Contract

Every repo worker, within its authorization, must:

- read the full issue/PR discussion and owner comments before acting;
- use existing `auto-agents` labels/comments as context, not as proof of correctness;
- reproduce or establish root cause before accepting a bugfix;
- prefer repairing a contributor PR when writable and preserve contributor credit;
- create a PR for an issue without a PR after implementing the best bounded candidate;
- add regression coverage when appropriate;
- run focused tests and the repo's expected full/local checks when feasible;
- run live or end-to-end proof against the real affected boundary before asking to land;
- run `autoreview` or the local review equivalent when available before push/land;
- keep reports clear enough for the root to maintain the project worker title without touching the root title;
- report local verification and a current PR/check snapshot before waiting on CI; do not use long CI watch or sleep polling unless the owner explicitly asks;
- push only when authorized;
- stop before merge/close/release unless the owner has explicitly authorized that exact action;
- end with exact status, branch, PR URL, tests, live proof, CI state, residual risk, and next decision.

## GitHub State Hygiene

- Use cached or local reads for first-pass discovery when available.
- Use live GitHub and CI reads before public writes, owner decision briefs, merge/close actions, release/tag/publish actions, and final state claims.
- After any write, perform one targeted readback of the affected issue, PR, run, release, tag, or deployment. Do not do a broad rescan unless the result is inconsistent.
- Before asking the owner for a decision, refresh the item and worker state. Do not repeat a question the owner already answered.
- Prefer full canonical GitHub URLs in reports and worker prompts. Do not rely on repo-local `#123` references across threads.

## CI Waiting Protocol

Workers must not disappear into CI waiting before giving the owner local verification and the current decision state.

- After code is changed or pushed, report the local proof first: files changed, tests/builds run, browser/live proof if required, PR URL, current CI/check snapshot, and exact remaining uncertainty.
- Do not run long `gh pr checks --watch`, `sleep` polling loops, or repeated CI refresh loops before reporting that evidence to the owner.
- A single immediate `gh pr checks` / `gh run view` snapshot is allowed. If CI is still pending, stop and report `CI pending` plus the current local proof.
- Continue waiting for CI only after explicit owner instruction, or when CI completes during the immediate readback without waiting.
- If CI fails later, resume with the failure evidence and ask or proceed only within the current authorization boundary.

## Credential Access

- Check only exact expected environment variables; never dump env or enumerate secrets.
- Keep credential discovery and use inside the worker that needs the secret.
- Do not send credentials, tokens, cookies, auth URLs, or private secret values between threads or into `~/.codex/state/cogine-multirepo-worker/ledger.md`.
- Use the repository or service's established secret workflow when one exists.
- Ask the owner only after the targeted path is absent, inaccessible, ambiguous, or requires interactive approval.
- If access blocks live proof, finish code, tests, review, and CI first, then ask for the exact access step, item-specific waiver, or reject/close decision.

## Monitoring Protocol

Before steering a worker:

1. Read the worker's newest state.
2. Treat the worker's newest local instruction as authoritative over older plans.
3. Decide whether the worker is active, blocked, completed, idle, or off-course.
4. Send nothing when an active worker has a coherent plan and is making progress.

Intervene only for:

- explicit worker blocker or coordination request;
- completed worker needing next same-repo queue item;
- repeated failures with no progress and a concrete correction;
- wrong repo/item;
- unauthorized mutation or security/privacy risk;
- release gate or proof gate violation;
- direct conflict with the owner's latest instruction.

Do not raise the proof bar mid-flight. Apply the proof gate that was assigned at delegation time.

## Idle Worker Closeout

An idle repo worker must not remain as a polling lane. After reading current state, do exactly one:

1. Assign the next autonomous issue or PR for the same repo.
2. Prepare remaining non-autonomous items to a decision-ready boundary and ask the owner.
3. If the effective queue is empty and release is authorized, assign release readiness/execution.
4. If no queue or release work remains, assign dependency freshness or repo health work only when useful.
5. Archive the worker when no immediate useful repo work remains, remove it from the current ledger, and keep only a compact public-mutation line if the result still matters for readback.

## Decision Brief

Owner questions must be decision-ready. Include:

- full canonical GitHub URL and title;
- what changes and who benefits;
- why a decision is needed now;
- completed proof: reproduction, tests, live proof, review, CI, mergeability;
- material tradeoffs, residual risks, or missing evidence;
- recommendation and rationale;
- exact choices and effect of each choice.

Never ask with only `land/delete`, `approve?`, or a bare URL.

## Live Proof Gate

Treat live proof as a pre-land requirement:

- Test the exact final candidate commit through the changed user path.
- Use the real service, account, device, browser, API, CLI, database, or deployment target when applicable.
- Redact secrets and private data while keeping concrete evidence: command, behavior, response class, artifact hash, URL, or observed state transition.
- If live proof is impossible, finish code, tests, review, and CI first, then ask for exact access, explicit item-specific waiver, or reject/close decision.
- Re-run live proof after any fix that changes the runtime path.

Pure docs, test-only, CI-only, or metadata-only changes may use closest artifact/workflow proof; state why no live runtime boundary applies.

## Public Model Identifier Gate

Before any push, public PR update, merge, or release involving model-bearing code or artifacts:

- Audit the exact candidate diff, tests, fixtures, snapshots, generated metadata, workflows, CI/test logs, packaged artifacts, and public proof text.
- Public artifacts may retain only model/provider identifiers that are documented or publicly offered by the provider. Record the public source URL in the worker report when relevant.
- Never expose internal, preview-only, alias-only, inferred, synthetic provider-shaped, or otherwise undisclosed identifiers.
- Genericize questionable test and fixture values because assertion failures can print them in CI logs.
- Do not repeat a questionable identifier in worker messages, audit reports, public comments, or root reports. Describe it generically.
- Return explicit `PASS` or `BLOCKED` covering every audited surface.

No public mutation may proceed while this gate is blocked.

## Release Gate

Compute the effective queue immediately before release:

```text
effective issues = open issues - explicitly ignored issues
effective PRs    = open PRs - explicitly ignored PRs
```

Release only when all are true:

- the owner explicitly requested or authorized release execution;
- effective issue count is zero;
- effective PR count is zero;
- every ignored item is explicitly named in the current owner instructions;
- required CI is green for the exact candidate;
- user-facing runtime changes have live proof or explicit waiver;
- checkout is clean, on the expected branch, and fast-forward current;
- unreleased changes justify the selected version.

Recheck queue and CI immediately before tagging or publishing. Abort if state changed.
Never silently exclude an item. In release reporting, list ignored items and the owner instruction that exempted them.

## Existing Auto-Agents

Use these as background signal sources, not duplicate work:

- `Issue Triage`: issue label normalization and `bot:triaged`.
- `Issue Duplicate Detector`: conservative duplicate candidate marking.
- `Auto TODO Issues`: TODO/FIXME issue creation.
- `PR Intake`: PR labels and `bot:triaged`.
- `Draft PR Readiness`: draft-to-ready checks and readiness comments.
- `PR Review`: Codex review markers and review findings.

Treat `type:*`, `priority:*`, `size:*`, `workstream:*`, `dependencies`, `auto-todo`, `todo`, `fixme`, and `needs-conflict-resolve` as useful routing signals. Treat `status:*` labels and `bot:validated` as unstable auxiliary hints only; they do not prove readiness, blockage, validation, ownership, or current truth without fresh evidence from GitHub state, CI, comments, code, tests, or live proof.

If an existing scheduled agent already owns a routine, do not manually rerun that routine. Escalate only when its output conflicts, stalls, or leaves a decision-ready next step.

## Skill Hygiene

Use `skill-cleaner` periodically when available:

- check loaded skill budget and trigger clarity;
- find duplicate or stale orchestration skills;
- keep `cogine-multirepo-worker` concise;
- preserve trigger nouns: Cogine, multirepo, repo worker, Codex thread, live proof, decision brief.

## Reporting

Keep reports compact and actionable:

When reporting multiple items, give each item a stable short label for follow-up dispatch.

- `Active`: repo, worker, current task URL, phase.
- `Needs owner`: exact decision/access/waiver required.
- `Ready next`: bounded, verifiable next work with no refreshed owner blocker; never infer from `status:ready` labels alone.
- `Blocked`: concrete blocker and last proof gathered; never infer from `status:blocked` labels alone.
- `Recent public mutations`: PR/issue/release URL, proof, and next state.

Mention meaningful changes only. Do not report routine polling as progress.
