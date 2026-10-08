---
name: domain-modeling
description: Build and sharpen a project's domain model. Use when discussing codebase terminology, writing or editing a GLOSSARY.md, or recording or editing an ADR.
---

# Domain Modeling

Actively build and sharpen the project's domain model as you design. This is the *active* discipline: challenging terms, inventing edge-case scenarios, and writing the glossary and decisions down the moment they crystallise. (Merely *reading* `GLOSSARY.md` for vocabulary is not this skill: that's a one-line habit any skill can do. This skill is for when you're changing the model, not just consuming it.)

## File structure

Most repos have a single context:

```
/
├── GLOSSARY.md
├── docs/
│   └── adr/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
└── src/
```

When no explicit policy selects a different layout, an active root `GLOSSARY-MAP.md` points to the project's contexts:

```
/
├── GLOSSARY-MAP.md
├── docs/
│   └── adr/                          ← system-wide decisions
├── src/
│   ├── ordering/
│   │   ├── GLOSSARY.md
│   │   └── docs/adr/                 ← context-specific decisions
│   └── billing/
│       ├── GLOSSARY.md
│       └── docs/adr/
```

Resolve the active context before writing, using the policy and path rules below. Read the active map, when present, and use the selected context's glossary and ADR locations. Use system-wide ADRs only for decisions spanning contexts. If the context is unclear during exploration, read the relevant available contexts and continue; ask only before a next write whose target remains ambiguous. Without a configured or active map, use the selected single-context glossary and ADR locations.

Read the repository's explicit domain policy in `AGENTS.md`, `CLAUDE.md`, or `docs/agents/domain.md` before applying filename defaults. Its configured glossary, map and ADR locations take precedence. An existing legacy `CONTEXT-MAP.md` / `CONTEXT.md` remains active when no replacement is configured; use the selected context's paths. A project explicitly using `GLOSSARY.md` must not gain a competing `CONTEXT.md`, and a legacy project must not gain a competing glossary merely because the default name changed. If available maps or glossaries disagree, reuse a policy or decision that already selects the active layout. Ask only if the remaining ambiguity would change the next term or ADR write; continue independent reading meanwhile. Migrate names only within the authorized task, preserving all terms, definitions and mappings.

Create files lazily: only when you have something to write. If the selected
context has no domain glossary at its resolved location, create it when the first term is resolved. If its
ADR directory does not exist, create it when the first ADR is needed.

## During the session

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in the
selected context's resolved active glossary, call it out immediately. "Your glossary
defines 'cancellation' as X, but you seem to mean Y. Which is it?"

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. "You're saying 'account': do you mean the Customer or the User? Those are different things."

### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about the boundaries between concepts.

### Cross-reference with code

When the user states how something works, check whether the code agrees. If you find a contradiction, surface it: "Your code cancels entire Orders, but you just said partial cancellation is possible. Which is right?"

### Update GLOSSARY.md inline

When a term is resolved, update the selected context's resolved glossary file (`GLOSSARY.md` by default, or its active legacy path) right
there. Preserve unrelated terms and the existing format; do not replace the whole glossary to adopt a template. Don't batch these up: capture them as they happen. Use the format in
[GLOSSARY-FORMAT.md](./GLOSSARY-FORMAT.md).

The resolved active glossary should be totally devoid of implementation details. Do not treat it as a spec, a scratch pad, or a repository for implementation decisions. It is a glossary and nothing else.

### Offer ADRs sparingly

Only offer to create an ADR when all three are true:

1. **Hard to reverse**: the cost of changing your mind later is meaningful
2. **Surprising without context**: a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off**: there were genuine alternatives and you picked one for specific reasons

If any of the three is missing, skip the ADR. Use the format in [ADR-FORMAT.md](./ADR-FORMAT.md).
