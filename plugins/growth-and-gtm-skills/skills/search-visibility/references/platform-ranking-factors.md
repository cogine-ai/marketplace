# Platform-Specific Search Evidence

Access rules and citation observations serve different purposes. Search engines
and answer products can use different indexes and retrieval modes; avoid
describing a private ranking algorithm as known from a vendor correlation.

## Audit by surface

| Surface | What to verify |
|---|---|
| Google AI features | Search eligibility, actual indexing, rendered/initial content, and the observed query's sources; do not require a separate AI-only schema or file |
| ChatGPT Search | OAI-SearchBot policy and actual observed answers; GPTBot controls potential model training |
| Perplexity | Automatic discovery and user-triggered fetching separately, plus the cited sources observed for the intended query |
| Microsoft Copilot | Relevant Bing discovery and the actual product's retrieval; do not promise a LinkedIn boost or a universal sub-two-second citation threshold |
| Claude | Claude-SearchBot, Claude-User, and ClaudeBot have different purposes; verify current documentation and the tested retrieval route |

Check canonical URLs, content usefulness, attributable sources, freshness where
it matters, and page performance. None independently guarantees inclusion,
citation, recommendation, or revenue. Use [format-volatility.md](format-volatility.md)
for comparable observations and keep failed requests separate from valid answers.

## Allowing AI Bots in robots.txt

Do not copy one blanket allowlist. Choose controls by documented purpose, then check WAF and CDN rules as well as `robots.txt`.

```text
# Automatic search discovery
User-agent: Bingbot
User-agent: Googlebot
User-agent: OAI-SearchBot
User-agent: PerplexityBot
User-agent: Claude-SearchBot
Allow: /

# Potential model training (publisher choice shown as disallow)
User-agent: GPTBot
User-agent: ClaudeBot
Disallow: /

# Gemini model training and grounding (publisher choice shown as disallow)
User-agent: Google-Extended
Disallow: /
```

User-triggered fetchers such as `ChatGPT-User`, `Claude-User`, and `Perplexity-User` are separate from automatic discovery. Vendor behavior can differ: OpenAI says `robots.txt` rules may not apply to `ChatGPT-User`, and Perplexity says `Perplexity-User` generally ignores them because these fetches are user-requested. Use `OAI-SearchBot`, not `ChatGPT-User`, to manage ChatGPT Search inclusion. `Google-Extended` is a standalone product token rather than a separate HTTP crawler; Google says it controls certain Gemini training and grounding uses and does not affect Google Search inclusion or ranking.

Verify the current names and consequences in the vendors' maintained documentation: [OpenAI](https://developers.openai.com/api/docs/bots), [Perplexity](https://docs.perplexity.ai/docs/resources/perplexity-crawlers), [Anthropic](https://privacy.anthropic.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler), and [Google](https://developers.google.com/crawling/docs/crawlers-fetchers/google-common-crawlers).

For implementation, inspect `/robots.txt` manually first. Optional helpers include each vendor's own crawler documentation and robots.txt testing tools.

## Decide the next test

Choose engines from the user's audience and real decision journey. Establish
current access and a repeatable query baseline before budgeting for a format or
channel. Separate policy configuration, successful fetching, indexing, cited
answers, favorable recommendations, and qualified conversions in the report.
