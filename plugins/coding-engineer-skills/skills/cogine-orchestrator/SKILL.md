---
name: cogine-orchestrator
description: "Use for Cogine's WORK/TEST multi-repository control plane with per-repo work and shared independent verification."
disable-model-invocation: true
---

# Cogine Orchestrator

Coordinate Cogine repository work as a manual Codex App control plane. This skill defines how the root orchestrator thread maps queues to repo worker threads, monitors progress, requests owner decisions, and avoids duplicating existing scheduled automation.

## Operating Boundary

- Treat this as a manual skill, not a scheduled agent runtime.
- Do not start, rerun, or replace existing `auto-agents` launchd jobs unless the user explicitly asks.
- Use existing automation outputs as signals: labels, comments, draft readiness notes, PR review markers, CI, and GitHub state.
- Default discovery scope is non-archived `cogine-ai` repositories. Use `shared/target-repos.md` only as the auto-agents signal list; outside it, assume no scheduled-agent support unless verified.
- If Codex thread tools are unavailable, report that orchestration cannot manage worker threads in this environment. Do not pretend shell commands can replace thread lifecycle operations.

## Model To Copy

Mirror the `steipete/agent-scripts` maintainer-orchestrator model:

- One root orchestrator owns thread topology.
- One active repository maps to one all-round `WORK` thread.
- Keep one long-lived shared `TEST` thread under the Auto-agents project. It verifies one immutable candidate at a time and returns to idle after each verdict.
- Keep research and operations inside the repo `WORK` thread by default. Independent verification is the only long-lived lane split.
- Keep work for a repository in its existing orchestrator-owned worker.
- Rename a worker whenever assigning or materially changing work: `<Project>: <short current task>`.
- Do not set or request a custom model for workers; omit model selection and inherit the platform default.
- Workers cannot create subworkers, delegate work, manage other chats, or perform portfolio triage.
- The root stays lightweight: inspect, delegate, route milestone reports, ask decisions, and report.
- Substantial investigation, implementation, review, live proof, landing preparation, and release execution happen in repository worker threads.

## Start Checklist

1. Enumerate non-archived `cogine-ai` repositories; map local checkouts when useful.
2. Read `shared/target-repos.md` and `registry/local-cron-agents.yaml` for scheduled-agent signal coverage.
3. Check current Codex threads with `list_threads` when available; reuse only eligible orchestrator-owned repo workers after reading current state.
4. For each target repo, use `github-project-triage` when available to map open issues, open PRs, CI, labels, latest release, and relevant automation comments.
5. Read and update `~/cogine-orchestrator.md`.
6. Build a compact current-state ledger: `Active`, `Needs owner`, `Ready next`, `Blocked`, `Recent public mutations`, `Owner exclusions`. Omit archived, not-visible, historical, and completed-idle workers unless they still carry an unresolved owner decision or explicitly reusable lane.

## Persistent Log

- This root orchestrator owns `~/cogine-orchestrator.md`; workers do not edit it.
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
- `create_thread`: create the shared Auto-agents `TEST` thread only when no eligible test lane exists.
- `read_thread`: inspect a worker before sending instructions, renaming, archiving, or declaring it blocked.
- `send_message_to_thread`: assign the next task or unblock a worker.
- `set_thread_title`: keep titles current as `<Project>: <short current task>`.
- `set_thread_archived`: archive completed idle workers after root confirms no immediate next repo work.
- `handoff_thread`: move a worker to another Codex host only when the user asks or the current host cannot run required proof.

Never create duplicate workers for the same repo without first reading all plausible existing orchestrator-owned workers. If two threads have unique progress, leave both intact and ask the owner before merging or retiring either lane.

### Two-Lane Work/Test Protocol

Use two long-lived execution roles unless the owner explicitly requests a different topology:

- `WORK`: the all-round repo worker. It researches, plans, implements, reviews, runs focused/full checks, performs authorized real proof, and prepares a decision-ready candidate.
- `TEST`: one shared independent verifier under the Auto-agents project. It verifies one frozen candidate at a time and never becomes a second developer.

The handoff loop is:

1. `WORK` completes its own tests and proof. TEST is an additional gate, not a replacement for developer verification.
2. `WORK` commits the complete candidate, confirms an immutable SHA and clean worktree, then reports `[Lane: WORK] [Event: READY_FOR_TEST]` with the original requirement, changed behavior, proof, risks, evidence boundaries, and cleanup state.
3. Root assigns work only when TEST is `[Event: IDLE]`. The assignment names the exact SHA, original requirement, highest-risk regressions, required evidence level, environment/account boundary, and cleanup contract.
4. `TEST` uses a separate checkout or detached candidate, challenges the result independently, and reproduces the old failure on the public seam when practical.
5. `TEST_PASS` is valid only for the exact SHA. Any source change invalidates it.
6. `TEST_HOLD` returns findings to `WORK`; TEST never fixes code. WORK repairs, freezes a new SHA, and starts a new handoff cycle.
7. TEST returns to `[Event: IDLE]` after PASS or HOLD. PASS does not authorize push, PR updates, merge, deploy, release, or tag.

TEST hard boundaries:

- Do not modify the candidate, commit, push, update PRs, resolve reviews, rerun public CI, merge, deploy, migrate, release, or accept a second candidate while active.
- Do not inherit the WORK conclusion or merely rerun its preferred test list; verify the original requirement and the repair risk.
- Use real UI/runtime/staging proof when the claim depends on those boundaries. Deterministic seams are appropriate for internal parser, cancellation, state-machine, or fault paths with no independent visible UI flow; label them accurately.
- Isolate WORK and TEST stateful fixtures: separate mutable accounts, instances/resources, sessions, ports, checkouts, and disposable data. Clean per-run resources with readback.
- Keep screenshots and videos outside Git. GUI changes still require complete screenshots; video remains optional unless explicitly required.

### Report Envelope And Focus Lock

Every worker report starts with a lane and milestone event:

- WORK: `MILESTONE`, `READY_FOR_TEST`, `BLOCKED`, `COMPLETE`.
- TEST: `TEST_PASS`, `TEST_HOLD`, `IDLE`.
- Urgent cross-cutting events: `INCIDENT`, `PROOF_BLOCKED`.

Treat incoming reports as inbox events, not automatic context switches. Finish the current root action to a safe checkpoint, then process queued reports. Only an active incident, security risk, unauthorized mutation, or blocker on the current critical path should preempt immediately.

Do not monitor or poll TEST. Assign one candidate, then wait for its milestone report. Do not send unrelated follow-ups while TEST is active.

WORK titles continue to use `<Project>: <short current task>`. Use `Auto-agents: TEST <Project> <item>` while TEST is active and `Auto-agents: TEST idle` after cleanup.

### Thread Ownership Gate

Reuse only a thread that satisfies at least one condition:

- the root orchestrator created it as a repo worker for the current orchestration run;
- `~/cogine-orchestrator.md` explicitly marks it as an active or explicitly reusable `orchestrator-owned` repo worker;
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
- all-round ownership: unless the owner explicitly requests read-only work, WORK owns research, implementation, developer verification, and candidate preparation for the assigned issue/PR;
- authorization boundary: local implementation/proof, push/PR update, CI rerun/fix, merge, close, release;
- no-subdelegation rule;
- instruction to read repo `AGENTS.md`, docs, issue/PR discussion, code, tests, and current CI;
- required proof before stopping;
- explicit stop condition for owner decision.

For each TEST assignment, include:

- exact immutable candidate SHA and checkout/worktree;
- original requirement and the regression or review finding that triggered the test;
- independent verification matrix and required evidence level;
- distinct TEST account, ports, env, and disposable-resource boundary when stateful proof is involved;
- prohibition on source changes and public mutations;
- required `TEST_PASS` or `TEST_HOLD` bound to the SHA;
- cleanup/readback requirements and return to `IDLE`.

## Authorization

Treat triage, monitoring, implementation, public mutation, CI repair, and release as separate permissions.

- Queue analysis or monitoring does not authorize edits.
- Delegation or parallel-worker creation requires explicit owner authorization.
- A normal issue/PR WORK assignment authorizes end-to-end local research, implementation, and developer verification unless the owner explicitly requests read-only work. It does not authorize public mutation.
- Push permission does not imply CI repair, merge, close, release, tag, or publish permission.
- CI rerun and CI-fix permission must be explicit; a push alone does not authorize additional repair commits or workflow mutation.
- Merge and close permission must be explicit for the affected issue or PR.
- Release, version bump, tag, registry publish, deployment, and GitHub Release require a current explicit release request.
- Broad scope expansion outside `cogine-ai` and live-proof waivers require fresh explicit owner confirmation.

Record the granted permissions in every worker prompt and in `~/cogine-orchestrator.md`. Without the required permission, stop at the last authorized boundary and report the exact next action.

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
- push only when authorized;
- stop before merge/close/release unless the owner has explicitly authorized that exact action;
- end with exact status, branch, PR URL, tests, live proof, CI state, residual risk, and next decision.
- before `READY_FOR_TEST`, commit the complete candidate, report the immutable SHA, confirm the worktree is clean, and stop source work until TEST returns.
- after `TEST_HOLD`, change only the accepted repair scope, freeze a new SHA, and request a new independent test. Never apply a prior PASS to candidate drift.

## GitHub State Hygiene

- Use cached or local reads for first-pass discovery when available.
- Use live GitHub and CI reads before public writes, owner decision briefs, merge/close actions, release/tag/publish actions, and final state claims.
- After any write, perform one targeted readback of the affected issue, PR, run, release, tag, or deployment. Do not do a broad rescan unless the result is inconsistent.
- Before asking the owner for a decision, refresh the item and worker state. Do not repeat a question the owner already answered.
- Prefer full canonical GitHub URLs in reports and worker prompts. Do not rely on repo-local `#123` references across threads.

## Credential Access

- Check only exact expected environment variables; never dump env or enumerate secrets.
- Keep credential discovery and use inside the worker that needs the secret.
- Do not send credentials, tokens, cookies, auth URLs, or private secret values between threads or into `~/cogine-orchestrator.md`.
- Use the repository or service's established secret workflow when one exists.
- Ask the owner only after the targeted path is absent, inaccessible, ambiguous, or requires interactive approval.
- If access blocks live proof, finish code, tests, review, and CI first, then ask for the exact access step, item-specific waiver, or reject/close decision.

## Monitoring Protocol

Before steering a worker:

1. Read the worker's newest state.
2. Treat the worker's newest local instruction as authoritative over older plans.
3. Decide whether the worker is active, blocked, completed, idle, or off-course.
4. Send nothing when an active worker has a coherent plan and is making progress.

For TEST, confirm it is `IDLE` before assigning a candidate. Never interrupt an active test with a newer candidate; queue it until the current verdict and cleanup are complete.

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
- keep `cogine-orchestrator` concise;
- preserve trigger nouns: Cogine, orchestrator, repo worker, Codex thread, live proof, decision brief.

## Reporting

Keep reports compact and actionable:

When reporting multiple items, give each item a stable short label for follow-up dispatch.

- `Active`: repo, worker, current task URL, phase.
- `Needs owner`: exact decision/access/waiver required.
- `Ready next`: bounded, verifiable next work with no refreshed owner blocker; never infer from `status:ready` labels alone.
- `Blocked`: concrete blocker and last proof gathered; never infer from `status:blocked` labels alone.
- `Recent public mutations`: PR/issue/release URL, proof, and next state.

Mention meaningful changes only. Do not report routine polling as progress.
