# Pricing Page Teardown

A structured way to score a live pricing page and return prioritized fixes. It
grades two axes: the classic **human buyer experience** and **AI-agent
readiness**—whether LLMs and agents can read, quote, and recommend the pricing.

> **Framework credit:** The two-axis structure and especially the AI-agent
> readiness lens are adapted from Kyle Poyar's Growth Unhinged pricing-page
> teardown. This rubric is independently authored; credit the framing to Poyar.

## Why the second axis matters

Buyers increasingly ask AI systems what a product costs before visiting its
site. If prices are trapped in an image, rendered only after interaction, or
absent from the page text, many text-fetching agents cannot quote them
reliably. A pricing page an agent cannot parse is less likely to be included in
a useful comparison.

**The 30-second paste test:** Give the pricing URL to a browsing-capable AI—or
paste the page's rendered text—and ask, “What are the plans and prices?” If it
cannot answer correctly and completely, similarly equipped agents are likely
to struggle. This is a heuristic, not proof that every agent fails.

## Rubric

Score each dimension **Pass / Partial / Gap**. Return two sub-scores and a
prioritized fix list, not one vanity number.

### Axis 1 — Human buyer experience

| # | Dimension | Passing looks like | Common gaps |
|---|-----------|--------------------|-------------|
| 1 | Value-prop clarity | The buyer can see what they get and why it is valuable | Feature list without outcomes |
| 2 | Plan differentiation | It is obvious who each plan is for and how plans differ | Feature-soup tables or overlapping tiers |
| 3 | Cognitive load | A buyer can decide in under 30 seconds | Too many tiers or unexplained jargon |
| 4 | Trust signals | Proof and risk reducers appear near the decision | Proof is missing or buried |
| 5 | Pricing psychology | Anchoring and the recommended tier are coherent | No recommendation or random price endings |
| 6 | Transparency | Actual prices, limits, and overages are clear | “Contact us” everywhere or hidden limits |

### Axis 2 — AI-agent readiness

| # | Dimension | Passing looks like | Common gaps |
|---|-----------|--------------------|-------------|
| 7 | Machine-readable pricing | Real numbers appear in semantic page text | Prices exist only in images, SVG, PDFs, or gated UI |
| 8 | FAQ and objections | Extractable answers cover limits, trial, cancellation, and key capabilities | Answers live only in a support portal |
| 9 | Per-tier depth | Each plan's inclusions, limits, and quotas are stated in words | Differences appear only as icons or checkmarks |
| 10 | Structured data and extractability | `Product`/`Offer` JSON-LD, semantic HTML, and appropriate crawler access | No schema, an auth wall, or search bots blocked |

Use `search-visibility` for extractability and crawler checks. Implement
`Product`/`Offer` JSON-LD directly or with the schema tooling available in the
project.

## Workflow

1. Read available product-marketing context so clarity is judged against the
   intended buyer.
2. Fetch rendered text or HTML, not only a screenshot. Record whether prices
   appear in the text.
3. Run the paste test and record errors or omissions.
4. Score all 10 dimensions with one evidence-based sentence each.
5. Prioritize fixes by impact and effort.

## Output template

```markdown
# Pricing Page Teardown — [URL] — [date]

## Scores
- Human buyer experience: [X/6 passing]
- AI-agent readiness: [X/4 passing]

## Paste test
[What the AI returned and what it missed]

## Dimension-by-dimension
| # | Dimension | Verdict | Evidence |
|---|-----------|---------|----------|
| 1 | Value-prop clarity | Pass/Partial/Gap | ... |

## Prioritized fixes
1. [impact/effort] — [fix] — [why it matters]

## The one thing
[The single highest-leverage fix]
```

## Common failure patterns

- **Image prices:** Put real prices in page text; keep imagery decorative.
- **“Contact us” everywhere:** Show a starting price or representative range
  when the sales model permits it.
- **Checkmark-only tables:** State actual limits and inclusions in words.
- **Interaction or auth walls:** Expose enough public pricing information for
  buyers and fetchers.
- **Blocked AI search bots:** Distinguish search/user agents from
  training-crawler controls before changing access rules.
