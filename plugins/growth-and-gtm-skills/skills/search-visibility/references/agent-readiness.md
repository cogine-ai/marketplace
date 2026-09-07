# Agent Readiness: Access, Discovery, Parseability

Use these checks for the specific agent or crawler and user journey under review. Available rendering and retrieval capabilities differ; verify them rather than assuming every agent behaves the same way.

## Access

Fetch the public entry page and an important destination. Record status codes, redirects, authentication requirements, and whether the useful content is present. Compare raw HTML and rendered output when relevant. Identify cookie walls, JavaScript-only content, or bot restrictions that actually block the tested route.

## Discovery

Inspect navigation, canonical URLs, sitemaps, and crawler rules. Distinguish training controls from search/discovery policies using current official crawler documentation before recommending access changes. If the site exposes Markdown, content negotiation, `Link` headers, or an agent index, verify the linked content exists and stays consistent with the canonical page. Do not require `llms.txt`, `llms-full.txt`, or a vendor score for every site.

## Parseability

Check whether the agent can identify the product, entity, offer, price, limits, date, and relevant source from the text it actually received. Use headings and structured data appropriate to the page. Validate critical facts against the rendered human-facing page and the underlying source of truth.

## Report the tested journey

Record entry URL, target task, steps, observed content, and the first demonstrated failure. Mark unavailable or inapplicable surfaces separately. Optional diagnostic tools can help, but a score is not proof of discovery, citation, or successful task completion.

If evaluating an action interface such as an API, MCP, or WebMCP, distinguish “readable” from “can perform the requested action”. Do not perform live writes merely to improve a readiness score; use existing authorization and a suitable test surface.

Method adapted from [Corey Haines AI SEO](https://github.com/coreyhaines31/marketingskills/blob/5b2c0007766c6a1cf1d53fd8fc73e979e0821022/skills/ai-seo/references/agent-readiness.md) at `5b2c000`. Platform-specific market shares, vendor scores, and uplift claims are not adopted as universal benchmarks.
