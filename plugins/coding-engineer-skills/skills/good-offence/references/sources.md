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

## Using the references

The adapted skill gives the review's goal and approach. Read the pinned premise,
defensive or Ponytail reference when it helps with the code under review; they
are supporting material rather than a mandatory checklist. The Rob Morris
principles file supplies context for its two reviewers. The adapted skill does
not use Ponytail's deleted-line scoring.

Synthetic development cases live outside the installed skill, under
`maintenance/evals/good-offence` in the Marketplace repository.

Both source projects are MIT licensed. Their complete copyright and license
notices are preserved beside the unmodified snapshots.
