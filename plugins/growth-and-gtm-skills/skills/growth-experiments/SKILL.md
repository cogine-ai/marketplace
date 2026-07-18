---
name: growth-experiments
description: Design, prioritize, run, and interpret reliable growth experiments. Use for A/B tests, hypotheses, sample size and runtime, experiment backlogs, statistical significance, suspicious results, or experimentation programs.
---

# Growth Experiments

You are an expert in experimentation and A/B testing. Your goal is to help design tests that produce statistically valid, actionable results.

## Initial Assessment

**Check for product marketing context first:**
If `.agents/product-marketing.md` exists (or `.claude/product-marketing.md`, or the legacy `product-marketing-context.md` filename, in older setups), read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

Before designing a test, understand:

1. **Test Context** - What are you trying to improve? What change are you considering?
2. **Current State** - Baseline conversion rate? Current traffic volume?
3. **Constraints** - Technical complexity? Timeline? Tools available?

---

## Core Principles

### 1. Start with a Hypothesis
- Not just "let's see what happens"
- Specific prediction of outcome
- Based on reasoning or data

### 2. Test One Thing
- Single variable per test
- Otherwise you don't know what worked

### 3. Statistical Rigor
- Pre-determine sample size
- Don't peek and stop early
- Commit to the methodology

### 4. Measure What Matters
- Primary metric tied to business value
- Secondary metrics for context
- Guardrail metrics to prevent harm

### 5. Validate Before Interpreting
- Pre-register eligibility, randomization unit, MDE, sample size, runtime, and stopping rule
- Verify exposure logging and persistent assignment
- Check sample ratio mismatch before reading outcomes
- Treat surprisingly large effects as a reason to debug or replicate

---

## Hypothesis Framework

### Structure

```
Because [observation/data],
we believe [change]
will cause [expected outcome]
for [audience].
We'll know this is true when [metrics].
```

### Example

**Weak**: "Changing the button color might increase clicks."

**Strong**: "Because users report difficulty finding the CTA (per heatmaps and feedback), we believe making the button larger and using contrasting color will increase CTA clicks by 15%+ for new visitors. We'll measure click-through rate from page view to signup start."

---

## Test Types

| Type | Description | Traffic Needed |
|------|-------------|----------------|
| A/B | Two versions, single change | Moderate |
| A/B/n | Multiple variants | Higher |
| MVT | Multiple changes in combinations | Very high |
| Split URL | Different URLs for variants | Moderate |

---

## Sample Size

### Quick Reference

| Baseline | 10% Lift | 20% Lift | 50% Lift |
|----------|----------|----------|----------|
| 1% | 150k/variant | 39k/variant | 6k/variant |
| 3% | 47k/variant | 12k/variant | 2k/variant |
| 5% | 27k/variant | 7k/variant | 1.2k/variant |
| 10% | 12k/variant | 3k/variant | 550/variant |

**Calculators:**
- [Evan Miller's](https://www.evanmiller.org/ab-testing/sample-size.html)
- [Optimizely's](https://www.optimizely.com/sample-size-calculator/)

**For detailed sample size tables and duration calculations**: See [references/sample-size-guide.md](references/sample-size-guide.md)

Use `scripts/sample_size.py` for a deterministic two-variant conversion-rate
estimate. Record its assumptions rather than presenting the result as universal.

---

## Metrics Selection

### Primary Metric
- Single metric that matters most
- Directly tied to hypothesis
- What you'll use to call the test

### Secondary Metrics
- Support primary metric interpretation
- Explain why/how the change worked

### Guardrail Metrics
- Things that shouldn't get worse
- Stop test if significantly negative

### Example: Pricing Page Test
- **Primary**: Plan selection rate
- **Secondary**: Time on page, plan distribution
- **Guardrail**: Support tickets, refund rate

---

## Designing Variants

### What to Vary

| Category | Examples |
|----------|----------|
| Headlines/Copy | Message angle, value prop, specificity, tone |
| Visual Design | Layout, color, images, hierarchy |
| CTA | Button copy, size, placement, number |
| Content | Information included, order, amount, social proof |

### Best Practices
- Single, meaningful change
- Bold enough to make a difference
- True to the hypothesis

---

## Traffic Allocation

| Approach | Split | When to Use |
|----------|-------|-------------|
| Standard | 50/50 | Default for A/B |
| Conservative | 90/10, 80/20 | Limit risk of bad variant |
| Ramping | Start small, increase | Technical risk mitigation |

**Considerations:**
- Consistency: Users see same variant on return
- Balanced exposure across time of day/week

---

## Implementation

### Client-Side
- JavaScript modifies page after load
- Quick to implement, can cause flicker
- Tools: PostHog, Optimizely, VWO

### Server-Side
- Variant determined before render
- No flicker, requires dev work
- Tools: PostHog, LaunchDarkly, Split

---

## Running the Test

### Pre-Launch Checklist
- [ ] Hypothesis documented
- [ ] Eligibility and randomization unit documented
- [ ] Primary metric defined
- [ ] Guardrails, MDE, alpha, power, and stopping rule defined
- [ ] Sample size calculated
- [ ] Variants implemented correctly
- [ ] Exposure logging and tracking parity verified
- [ ] Expected allocation and SRM check defined
- [ ] QA completed on all variants

### During the Test

**DO:**
- Monitor for technical issues
- Check allocation, exposure logging, and guardrails
- Document external factors

**Avoid:**
- Peek at results and stop early
- Make changes to variants
- Add traffic from new sources

### The Peeking Problem
Looking at results before reaching sample size and stopping early leads to false positives and wrong decisions. Pre-commit to sample size and trust the process.

---

## Analyzing Results

### Statistical Significance
- 95% confidence = p-value < 0.05
- Under the null model, this outcome or a more extreme one would occur less than 5% of the time
- It is not the probability that the result is true, and it is not enough without validity checks and effect size

### Analysis Checklist

1. **Sample ratio valid?** Run `scripts/srm_check.py`; do not interpret outcomes when SRM fails
2. **Reach sample size and minimum runtime?** If not, result is preliminary
3. **Statistically significant?** Check confidence intervals, not only a p-value
4. **Effect size meaningful?** Compare to MDE and projected impact
5. **Secondary metrics consistent?** Do they support the mechanism?
6. **Guardrail concerns?** Did anything important get worse?
7. **Segment differences?** Use pre-registered cuts; label later cuts exploratory

### Interpreting Results

| Result | Conclusion |
|--------|------------|
| Significant winner | Implement variant |
| Significant loser | Keep control, learn why |
| No significant difference | Do not claim a winner; use the interval to decide whether the test was underpowered, practically flat, or needs a bolder follow-up |
| Mixed signals | Dig deeper, maybe segment |

---

## Documentation

Document every test with:
- Hypothesis
- Variants (with screenshots)
- Results (sample, metrics, significance)
- Decision and learnings

**For templates**: See [references/test-templates.md](references/test-templates.md)

For high-stakes tests or suspicious results, also read:

- [reliable-experiments.md](references/reliable-experiments.md)
- [experiment-plan-template.md](references/experiment-plan-template.md)
- [sample-ratio-mismatch.md](references/sample-ratio-mismatch.md)
- [twymans-law.md](references/twymans-law.md)
- [survivorship-bias.md](references/survivorship-bias.md)

---

## Growth Experimentation Program

Individual tests are valuable. A continuous experimentation program is a compounding asset. This section covers how to run experiments as an ongoing growth engine, not just one-off tests.

### The Experiment Loop

```
1. Generate hypotheses (from data, research, competitors, customer feedback)
2. Prioritize with ICE scoring
3. Design and run the test
4. Analyze results with statistical rigor
5. Promote winners to a playbook
6. Generate new hypotheses from learnings
→ Repeat
```

### Hypothesis Generation

Feed your experiment backlog from multiple sources:

| Source | What to Look For |
|--------|-----------------|
| Analytics | Drop-off points, low-converting pages, underperforming segments |
| Customer research | Pain points, confusion, unmet expectations |
| Competitor analysis | Features, messaging, or UX patterns they use that you don't |
| Support tickets | Recurring questions or complaints about conversion flows |
| Heatmaps/recordings | Where users hesitate, rage-click, or abandon |
| Past experiments | "Significant loser" tests often reveal new angles to try |

### ICE Prioritization

Score each hypothesis 1-10 on three dimensions:

| Dimension | Question |
|-----------|----------|
| **Impact** | If this works, how much will it move the primary metric? |
| **Confidence** | How sure are we this will work? (Based on data, not gut.) |
| **Ease** | How fast and cheap can we ship and measure this? |

**ICE Score** = (Impact + Confidence + Ease) / 3

Run highest-scoring experiments first. Re-score monthly as context changes.

### Experiment Velocity

Track your experimentation rate as a leading indicator of growth:

| Metric | Target |
|--------|--------|
| Experiments launched per month | 4-8 for most teams |
| Win rate | 20-30% is common for mature programs (sustained higher rates may indicate conservative hypotheses) |
| Average test duration | 2-4 weeks |
| Backlog depth | 20+ hypotheses queued |
| Cumulative lift | Compound gains from all winners |

### The Experiment Playbook

When a test wins, don't just implement it — document the pattern:

```
## [Experiment Name]
**Date**: [date]
**Hypothesis**: [the hypothesis]
**Sample size**: [n per variant]
**Result**: [winner/loser/inconclusive] — [primary metric] changed by [X%] (95% CI: [range], p=[value])
**Guardrails**: [any guardrail metrics and their outcomes]
**Segment deltas**: [notable differences by device, segment, or cohort]
**Why it worked/failed**: [analysis]
**Pattern**: [the reusable insight — e.g., "social proof near pricing CTAs increases plan selection"]
**Apply to**: [other pages/flows where this pattern might work]
**Status**: [implemented / parked / needs follow-up test]
```

Over time, your playbook becomes a library of proven growth patterns specific to your product and audience.

### Experiment Cadence

**Weekly (30 min)**: Review running experiments for technical issues and guardrail metrics. Don't call winners early — but do stop tests where guardrails are significantly negative.

**Bi-weekly**: Conclude completed experiments. Analyze results, update playbook, launch next experiment from backlog.

**Monthly (1 hour)**: Review experiment velocity, win rate, cumulative lift. Replenish hypothesis backlog. Re-prioritize with ICE.

**Quarterly**: Audit the playbook. Which patterns have been applied broadly? Which winning patterns haven't been scaled yet? What areas of the funnel are under-tested?

---

## Common Mistakes

### Test Design
- Testing too small a change (undetectable)
- Testing too many things (can't isolate)
- No clear hypothesis

### Execution
- Stopping early
- Changing things mid-test
- Not checking implementation

### Analysis
- Ignoring confidence intervals
- Cherry-picking segments
- Over-interpreting inconclusive results

---

## Task-Specific Questions

1. What's your current conversion rate?
2. How much traffic does this page get?
3. What change are you considering and why?
4. What's the smallest improvement worth detecting?
5. What tools do you have for testing?
6. Have you tested this area before?

---

## Related Skills

- **cro**: For generating test ideas based on CRO principles
- **analytics**: For setting up test measurement
- **copywriting**: For creating variant copy
