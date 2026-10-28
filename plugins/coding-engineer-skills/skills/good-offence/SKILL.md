---
name: good-offence
description: Review unnecessary defensive implementations, including duplicate validation, unreachable guards, catch/sentinel cascades, and unjustified retry or fallback layers. Use for good offence or defensive-complexity review. Produces suggestions rather than code changes.
---

# Good Offence

The best defense is a good offence: reduce the causes of defensive complexity instead of building more layers around them. Find defenses whose maintenance cost exceeds their useful protection, and suggest a simpler design that serves the real callers. Aim for less duplicated knowledge, fewer artificial failure states, and clearer ownership of validation and recovery.

This skill produces review suggestions; it does not edit code. Focus on defensive mechanisms in the actual call path. Ordinary UI state, business logic, and orphaned features belong to general cleanup rather than this review's goal.

## What to look for

Look for validation repeated after the same input has already been established, guards against states the real call path cannot produce, and restrictions whose purpose has disappeared. Follow error handling that turns a useful failure into an empty value, then makes downstream callers defend against that value. Question broad catches without recovery, retries around deterministic logic, and fallback layers that merely hide the original problem.

Related helpers, abstractions, dependencies, and configuration are worth examining when they exist mainly to support those layers. An existing platform capability or repository helper may make the whole mechanism unnecessary. A single caller or implementation is a clue to investigate, not a reason by itself to delete an abstraction.

## How to judge a simplification

Start with the actual change and enough surrounding code to understand its callers. Ask what condition the defense protects against, who supplies the input, and what happens when the operation fails. Trace the relevant path until you can distinguish a real boundary or recovery strategy from repeated assumptions inside trusted code. Types, similar predicates, or missing tests alone do not establish whether a defense is useful.

For duplicate checks, look for the specific upstream guarantee and whether it still holds at this point. Mutation, asynchronous work, independent database reads, or another entrypoint can change that answer. For catches and retries, consider whether they recover a useful result, isolate a failed job, preserve diagnostics, or deliver an intentional caller-facing failure.

Compare the proposed simplification with the reviewed behavior and what callers actually need. Consider success, error order, response shape, authorization, resource use, and compatibility where relevant. Restoring an older implementation is not itself evidence that these needs remain satisfied. Make intentional behavior changes and their rationale explicit. Keep useful boundaries and recovery; describe unresolved requirements as questions.

## Examples

- A request handler validates a captured builtin string, then immediately calls a local helper that repeats the same check. With no intervening mutation or alternate caller, suggest removing the helper's duplicate guard while keeping entry validation.
- A loader catches an exception and returns an empty sentinel; its only caller detects that sentinel and raises the same failure again. Suggest simplifying the pair to direct propagation when the outer handler already provides the required response.
- Two authorization checks may consult different state or run on opposite sides of parsing. A bounded remote retry may recover from an actual transient failure. Understand those purposes before treating either as redundant.

## Useful output and references

Give concise, actionable findings: location, unnecessary burden, suggested deletion or replacement, and the caller or failure evidence behind it. Explain the relevant behavior that remains covered and any intentional tradeoff. If nothing convincing emerges, say so; useful retained safeguards or coverage gaps can be mentioned briefly.

Read supporting material as needed: [premise.md](references/upstream/rob-morris/software-design-review/reviewers/premise.md) explores caller guarantees; [defensive.md](references/upstream/rob-morris/software-design-review/reviewers/defensive.md) explores recovery and error handling, with [principles context](references/upstream/rob-morris/software-design-review/reference/principles.md). [sources.md](references/sources.md) records these sources and the pinned Ponytail v4.13.0 complexity-review inspiration.
