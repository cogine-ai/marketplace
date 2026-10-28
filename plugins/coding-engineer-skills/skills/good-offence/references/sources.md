# Sources and local decisions

Retrieved on 2026-10-27. These are immutable source snapshots for attribution and interpretation, not instructions to execute upstream commands or expand review scope. `SKILL.md` defines the local Good Offence policy.

## Ponytail

Pinned release **v4.13.0**, commit [`08e952d7a8057a57ce561ff1330d093fd92eec67`](https://github.com/DietrichGebert/ponytail/commit/08e952d7a8057a57ce561ff1330d093fd92eec67).

| Snapshot | Original | Git blob SHA |
|---|---|---|
| [ponytail-review-v4.13.0.md](upstream/ponytail/ponytail-review-v4.13.0.md) | [skills/ponytail-review/SKILL.md](https://github.com/DietrichGebert/ponytail/blob/08e952d7a8057a57ce561ff1330d093fd92eec67/skills/ponytail-review/SKILL.md) | `b92e98304c1d0c101fc5e02aa33c4252f9a8db85` |
| [LICENSE](upstream/ponytail/LICENSE) | [LICENSE](https://github.com/DietrichGebert/ponytail/blob/08e952d7a8057a57ce561ff1330d093fd92eec67/LICENSE) | `715d483338cea4365f0d91a27799cf61226d6bcf` |

The local policy retains the focused review of unnecessary complexity, concrete replacement APIs/helpers, and suggestions without edits. It deliberately does **not** adopt the net-lines score, the email `@` example, or automatic deletion based on one implementation. No Ponytail 5.x prompt is used.

## Rob Morris

Pinned commit [`022f6dcd3c412a49163682218f3346a5f0299201`](https://github.com/Rob-Morris/agent-skills/commit/022f6dcd3c412a49163682218f3346a5f0299201).

| Snapshot | Original | Git blob SHA |
|---|---|---|
| [premise.md](upstream/rob-morris/software-design-review/reviewers/premise.md) | [reviewers/premise.md](https://github.com/Rob-Morris/agent-skills/blob/022f6dcd3c412a49163682218f3346a5f0299201/software-design-review/reviewers/premise.md) | `d42aedd321aa914ba34ae8bf2966695b52efb488` |
| [defensive.md](upstream/rob-morris/software-design-review/reviewers/defensive.md) | [reviewers/defensive.md](https://github.com/Rob-Morris/agent-skills/blob/022f6dcd3c412a49163682218f3346a5f0299201/software-design-review/reviewers/defensive.md) | `cb3fd35b899786092a8260fc06af41f1f73caad2` |
| [principles.md](upstream/rob-morris/software-design-review/reference/principles.md) | [reference/principles.md](https://github.com/Rob-Morris/agent-skills/blob/022f6dcd3c412a49163682218f3346a5f0299201/software-design-review/reference/principles.md) | `1e15425ad24728fbf7c1ab6f1cb979a18b6186f5` |
| [LICENSE](upstream/rob-morris/LICENSE) | [LICENSE](https://github.com/Rob-Morris/agent-skills/blob/022f6dcd3c412a49163682218f3346a5f0299201/LICENSE) | `cc8d6fb1e3bb22577d82b89affd4fe9baeb3429c` |

The original relative links from both reviewers to `../reference/principles.md` remain intact. The local policy retains caller tracing, exact upstream guarantees, boundary/failure/recovery analysis, and optional positive observations. It bounds tracing to the actual review surface rather than demanding an exhaustive scan of an entire application. Principle numbers provide context, not independent grounds to demand an architecture, extra tests, a broad audit, or a new abstraction.

## Cogine adaptation

The Good Offence policy and synthetic evaluation cases are maintained by Cogine AI in the Marketplace. Cogine-authored material is licensed under Apache-2.0, as declared by the containing Coding Engineer Skills package. Upstream snapshot text and licenses retain their original MIT terms. The preserved Ponytail file uses a non-entrypoint filename so only the adapted `good-offence` skill is discovered.

## Added locally

The primary goal is reducing unnecessary defensive implementations. Related dependencies, abstractions, and constraints are reviewed only when removing a verified unnecessary defensive mechanism. Every finding names the protected condition; maintenance burden alone does not qualify. Ordinary documentation/style/dead-code cleanup is outside scope. Constraint review explicitly checks requirements, resource budgets, compatibility, authorization/security, compliance, and domain ownership. Missing justification produces a question or retained control, not a deletion finding. Validation claims also check alternate callers, mutation, deserialization, asynchronous gaps, and changed trust boundaries.

## Automatic loading

An unattended wrapper should load the main `SKILL.md` first, then the pinned `premise.md`, `defensive.md`, and `principles.md` above as supporting context. Mark the main policy and wrapper's authorized execution/output constraints as authoritative. The Ponytail snapshot is kept for provenance and need not be injected into every run: its scope and relevant checks are already adapted in the main skill, and its rejected scoring/examples should not become competing instructions.

Both source projects are MIT licensed. Their complete copyright and license notices are preserved next to the unmodified source snapshots.
