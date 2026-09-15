---
name: startup-finance
description: Analyze startup burn, runway, scenarios, unit economics, hiring, and fundraising tradeoffs. Use when a founder or CEO needs a cash plan, financial model, budget decision, runway extension plan, or financing scenario.
---

# Startup Finance

Turn available financial data into a decision-ready view of cash, runway, and
the assumptions that matter most.

## Working Rules

- Use supplied actuals first; label estimates and assumptions.
- Keep cash timing separate from accounting revenue and expense recognition.
- Use monthly granularity unless the decision requires more detail.
- Compare a small number of meaningful scenarios, usually bear, base, and bull.
- Never invent benchmarks or hide uncertainty behind false precision.

## Decision-Critical Inputs

Collect only what the decision needs:

- unrestricted cash and the as-of date
- monthly cash inflows and operating cash outflows
- revenue, gross margin, and growth assumptions when relevant
- headcount, hiring dates, compensation, and major planned commitments
- receivable, payable, debt, or financing timing if material
- the decision, target date, and minimum cash buffer

If inputs are missing, state the gap and ask only for values that could change
the recommendation.

## Core Calculations

- Gross burn = recurring monthly operating cash outflows.
- Net burn = monthly cash outflows minus monthly cash inflows.
- Runway = unrestricted cash divided by positive net burn.
- Approximate cash-out date from the monthly cash schedule, not a rounded
  headline alone.
- Gross margin = revenue minus cost of revenue, divided by revenue.
- CAC payback months = CAC divided by monthly gross profit per new customer.
- Simple LTV may use monthly gross profit per customer divided by monthly churn
  only when churn is stable enough for that approximation; state the caveat.

If net burn is zero or negative, report that the company is cash-generating and
do not calculate runway by division. Model downside scenarios when the decision requires them.

## Workflow (Cash Plans and Scenario Decisions)

1. Normalize actuals, one-time items, commitments, and assumptions.
2. Build a monthly cash bridge from opening to ending cash.
3. Model bear, base, and bull cases around the few variables that drive the
   decision.
4. Test hiring, spending, pricing, growth, and financing timing separately so
   their effects stay visible.
5. Identify the earliest constraint and the two or three highest-sensitivity
   assumptions.
6. Recommend a decision, trigger, or next checkpoint with explicit evidence.

## Output

Use the sections relevant to the question; single-metric requests can be answered directly:

1. **Current state** — cash, gross burn, net burn, runway, and data date.
2. **Scenario table** — key assumptions, cash-out date, and minimum cash.
3. **Sensitivities** — variables that materially change the outcome.
4. **Decision implications** — what to do now, what to defer, and what trigger
   would change the decision.
5. **Risks and gaps** — missing inputs, timing risk, and assumptions to verify.

When creating a spreadsheet or model, keep an assumptions section, formulas
that can be audited, and a visible reconciliation from opening to ending cash.

## Guardrails

- Distinguish bookings, recognized revenue, collections, and cash.
- Do not treat an unsigned financing round or uncollected receivable as cash.
- Show one-time costs and debt obligations explicitly.
- Flag tax, legal, accounting, and financing questions that need a qualified
  professional; do not present the analysis as professional financial advice.
