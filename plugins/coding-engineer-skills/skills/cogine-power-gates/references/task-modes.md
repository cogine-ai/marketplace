# Task Modes

Use this reference when the mode boundary is unclear.

## Routing Algorithm

1. If the requested scope is discovery, critique, prompt improvement, or an explicit preimplementation-only unknown pass, use `blind-spot-only` and stop after Discovery.
2. Determine the minimum safe risk mode from the consequences of the action.
3. A user-named mode may increase caution. Use a lower mode only when its predicates are actually satisfied.
4. Without a named mode, use `fast` only when every fast predicate holds; otherwise use `standard`.

Never create an extra mode for a task category such as review, research, design, or deploy.

## Fast Predicate

Use `fast` only when all are true:

- Scope and success criteria are explicit.
- The action is local and reversible.
- It cannot change user-facing meaning, architecture/contracts, data, permissions, security, cost, release/public state, or remote/live state.
- Direct validation is obvious and available.

If any predicate fails, use `standard` or `high-risk`.

## High-Risk Floor

Use `high-risk` when the action can:

- Change architecture, cross-module contracts, or cross-repo consistency.
- Release, deploy, roll back, publish, or mutate material remote/live state.
- Affect production/customer data, authentication, authorization, permissions, privacy, secrets, or security posture.
- Affect billing, payments, quotas, vendors, or material cost.
- Be destructive, irreversible, expensive, or hard to verify.

Classify the intended next action, not incidental vocabulary. Reading architecture is not changing it; drafting is not publishing; inspecting production state is not mutating it. Apply existing authorization even in `high-risk`.

## Calibrated Routes

- **Reference-rich implementation:** Treat a precise source reference as Discovery evidence. Proceed when semantics, scope, and verification are clear.
- **Design/prototype:** Use `standard` and expose unknown knowns with options or prototypes. Default visual/interaction prototypes to HTML when no format is named.
- **Release/deploy:** Use `high-risk`. Check target, revision, preflight, rollback, authorization, and read-back from available evidence. Ask only for uncovered material decisions or unavailable input.
- **Review follow-up:** Verify findings against current evidence before changing anything. Escalate only when the validated fix crosses a material boundary.
- **Research/docs:** Use `standard` unless the output changes policy, public state, legal/security/financial decisions, or another high-risk boundary.
- **Cross-repo:** Reading multiple repos is not automatically high-risk; coordinated contract or state changes are.

## Implicit Invocation

After implicit activation, exit without ceremony when inspection finds no material uncertainty, risk, deviation, or evidence gap.

Otherwise:

- Do not announce the mode unless it changes behavior.
- Keep `fast` gates inline.
- Use `gate-reports.md` only for interruption, incomplete required validation, or a requested blind-spot artifact. High-risk mode and authorized adaptation alone do not require reports.
- Ask an artifact-format question only when the answer materially changes usefulness.
