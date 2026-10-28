---
name: good-offence
description: Review unnecessary guards, duplicate validation, catch/sentinel cascades, and unjustified retry or fallback layers using verified callers and failure contracts. Use for good offence or defensive-complexity review. Suggestions only; excludes general dead-code or UI-state cleanup, style, and security audits.
---

# Good Offence

The best defense is a good offence: remove a defensive layer only when call-path and recovery-contract evidence shows it adds no useful protection. Reduce the cause of defensive complexity instead of adding more layers around it. Preserve necessary boundaries and failure contracts. This is a review of **unnecessary defensive complexity**, not network offense or a security audit.

The skill adapts Ponytail's **v4.13.0** complexity-only review and Rob Morris's premise/defensive reviewers. Fixed upstream snapshots and context are listed in [sources.md](references/sources.md). These local instructions take precedence over conflicting examples, scoring rules, and broader principles in those references.

Review and recommend only. Do not edit, refactor, approve, request changes, publish, merge, or change runtime/configuration. An explicitly authorized automation wrapper may publish the returned suggestions; the skill itself does not grant that permission.

## Two decisions, in order

First establish **scope**, then establish **necessity**. Both must pass for every finding.

1. **Is this a defensive mechanism?** Identify code that rejects or normalizes invalid/disallowed input, guards an operation against an invalid state, handles or cleans up a failure, retries for recovery, or supplies a fallback after a failed/missing operation. Name the concrete condition/failure, the protected operation or caller, and the boundary/recovery contract. A `defensive` label or a field called `error` is not evidence.
2. **Is that defense unnecessary?** Verify the real callers, upstream guarantee or recovery premise, then show that removing the identified mechanism preserves the required success and failure contracts. A safe deletion can still fail the scope decision.

Ordinary business-state transitions, selectors, UI progress/status mapping, and their state storage are functional behavior. They do not become defensive because they use `if`, include a failed-state label, are duplicated, or have lost their callers. An orphaned progress state machine is general dead-code cleanup even when all its branches are unreachable and deletion changes no current output.

Keep the proposed deletion bounded to the proven defensive mechanism and plumbing needed solely for it. An incidental `Array.isArray`/null guard inside an unused feature does not put the entire feature, its handlers, or its tests in scope. If that local guard is the candidate, prove that guard redundant on its own; do not use it to justify deleting the surrounding feature. Zero callers for an entire functional feature is not an upstream guarantee about invalid inputs to a live operation.

Reject an out-of-scope candidate before spending time proving its deletion equivalent. For a retained candidate, keep the scope evidence distinct from the equivalence evidence. An unattended verifier must evaluate both, rather than merely agreeing that deletion is harmless.

## Establish the surface

For a PR, pin its full head/base SHAs, check the actual PR diff, and read relevant code at those versions. The current checkout and a moving branch are not proof of the PR's contents. Use immutable Git objects or source APIs at full SHAs when needed. Respect the host's read/write limits; do not fetch, check out, build, or run tests that write files under a read-only review.

Focus on changed code and the real callers, callees, tests, and contracts needed to judge it. Follow adjacent paths far enough to verify a claim; do not turn a small diff into an unbounded audit of every downstream guard. State unavailable code or missing caller coverage instead of inventing certainty. Prior comments and the PR description are leads to verify, not proof.

Compare a proposed simplification against the **reviewed head's observable behavior**, including newly added behavior. The base version explains the change; restoring it is not proof of equivalence. Treat an observable difference as a counterexample unless a verified, explicit caller contract permits that exact difference. Missing documentation, tests, or a stated reason for the new behavior does not grant permission to discard it. Do not substitute your preferred API behavior for the behavior being reviewed.

## Main review: defense that does not earn its place

Read [premise.md](references/upstream/rob-morris/software-design-review/reviewers/premise.md) and [defensive.md](references/upstream/rob-morris/software-design-review/reviewers/defensive.md) with their [principles context](references/upstream/rob-morris/software-design-review/reference/principles.md) for these lenses:

- **Duplicate validation and unreachable guards:** name the real system/trust boundary, every reachable entry relevant to the candidate, the exact predicate, and the specific upstream function that guarantees it. Check mutation, deserialization, authorization changes, alternate/direct callers, and async gaps between checks. An annotation is not runtime validation. Rechecking at a different boundary, version, or trust level may be necessary.
- **Catch, wrapper, and sentinel cascades:** name the actual failure, recovery, and caller contract. Trace whether swallowing an error or returning an empty value forces each downstream caller to add more defense. Show what happens if the operation fails directly; preserve useful diagnostic context and any real recovery or isolation of one failed job. A broad catch is a lead, not proof that deletion is safe.
- **Retry, sleep, and fallback layers:** establish whether the failure is transient or deterministic, and whether a recovery changes the outcome. Do not use waiting or retry as a substitute for fixing a deterministic premise. Preserve bounded I/O retries, lock-contention handling, cancellation, cleanup, and graceful user-facing failure where their contracts require them. Local filesystem/process operations can fail; local does not mean infallible.

## Related complexity: the same defensive mechanism

Every finding must identify an executable defensive mechanism and the failure or condition it protects. Consider the following only when removing that verified unnecessary defense. Maintenance benefit alone does not bring an issue into scope. Exclude stale comments/docs, unused helpers or configuration, generic abstraction cleanup, style, and test/coverage suggestions unless they remove a proven unnecessary defensive mechanism.

- **Dependencies and reimplementation:** check the standard library, platform, and existing repository helpers. Name the exact replacement API/path and compare semantics, compatibility, supported environments, and failure behavior. Similar names or fewer dependencies alone do not prove equivalence.
- **Abstractions and flexibility:** enumerate actual callers, implementations, and configuration consumers. A single implementation/caller, a long function, or an unset option is a lead, not a verdict. Check ownership, lifecycle, test seams, and documented requirements before proposing an inline/delete. Do not invent a new abstraction to simplify one caller.
- **Constraints and restrictions:** for allowlists, caps, limits, format restrictions, feature gates, and configuration locks, trace the requirement and current consumers. Check resource budgets, compatibility, security/authorization, compliance, and the responsible product/domain owner. A missing explanation does not prove a restriction is unnecessary. Recommend removal only with positive evidence that its purpose is obsolete or covered by an equivalent control. Otherwise preserve it and name an unresolved requirement as a question.

## Attack the proposed simplification

Before keeping a finding, seek a concrete counterexample in the real call path. Identical predicates and arguments do not prove equivalent state: two independent database reads separated by async work are not one validated snapshot. A guard before request extraction/JSON parsing and a domain check after parsing may enforce different failure contracts within the same HTTP request. Trace intervening work and compare error order, status, response shape, side effects, and recovery. For example, removing an outer 403 guard can expose a parser's 400/415 before the remaining domain guard runs. Preserve the guard when equivalent behavior is unproved; cite an explicit caller contract if a proposed failure change is intended and permitted.

An unchanged final write authorization does not establish equivalence of the full request. If deletion changes which failure happens first, its status/body/content type, or which authorization snapshot is consulted, withhold the finding even if both versions prevent unauthorized writes. Calling the added layer divergent or undocumented does not resolve those counterexamples.

## Evidence bar

Report a finding only when you can show all of:

1. Scope evidence: the specific defensive mechanism in the reviewed change, the operation/caller it protects, its invalid condition or failure, and why it is protection/recovery rather than ordinary functional state or presentation.
2. The code/call-path evidence that makes it unnecessary; for duplicate validation, cite the upstream guarantee and why it covers the same inputs at the same relevant boundary.
3. A specific deletion or simpler replacement, including the existing helper/native API when applicable.
4. The behavior that remains preserved, including meaningful failure, authorization, compatibility, and resource contracts.
5. A maintenance benefit such as fewer independent rules, fewer failure states, less duplicate knowledge, or less dependency surface.

Count lines only as a rough description of a change. Do not score by net deleted lines, weaken validation to a superficial check, remove a useful smoke test/invariant, or replace clear code with terse cleverness. A retained seam or safeguard can be the simplest design that works.

If a premise or preservation claim cannot be established, withhold the finding. An important unresolved product question may be stated separately; it is not a proven simplification. General correctness bugs, security findings, test-coverage campaigns, and performance optimisation are outside this review. Their contracts still constrain which simplifications are safe; preserve a control when its necessity is unresolved.

## Return useful suggestions

Number findings so a person can refer to them. Keep each concise, with:

- **Location:** file and line/symbol at the reviewed head.
- **Scope and protected condition:** the concrete defensive operation, the caller it protects, and the invalid condition or failure it handles. Keep this separate from proof that deletion is equivalent.
- **Burden and evidence:** the unnecessary mechanism and verified caller/boundary or replacement evidence.
- **Simplify:** what to delete/change and the exact replacement, or nothing when deletion is enough.
- **Preserves:** the relevant behavior/failure contract and why it remains covered.
- **Benefit:** the maintenance burden removed, not a line-count target.

Use concern labels when helpful: `validation`, `defensive`, `retry`, `fallback`, or `constraint`. Do not promote suggestions to correctness blockers or fabricate findings to fill a quota.

If none meet the evidence bar, say **No proven simplification findings.** Include coverage gaps when they materially limit that conclusion. Optionally name up to three correctly placed safeguards that were considered and retained; do not pad every result with positive observations.

For unattended review, follow the wrapper's output schema and publication boundary. Preserve this skill's evidence bar and primary focus even when the transport format differs from the manual list above.
