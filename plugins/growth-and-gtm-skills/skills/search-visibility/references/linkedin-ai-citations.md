# LinkedIn Surfaces in AI Search

Use this to decide whether posts, articles, profiles, or company pages support
the intended professional audience. Upstream vendor studies report changing,
engine-specific citation mixes. Their samples and counts do not establish the
best surface or a causal lift for this user.

## Establish the evidence

- Record the target engine, prompt set, date, locale, search mode, and observed
  cited URLs, including their path type. Separate raw citation count from the
  share of answers that cite a domain; different metrics can reverse rankings.
- Inspect the actual public URL, response status, redirects, login/challenge,
  robots meta tag, and `X-Robots-Tag` header when available. Crawler behavior
  depends on documented purpose; a spoofed user agent alone does not reproduce
  the real crawler or its authenticated/network context.
- Missing `noindex` is not proof of indexing. A positive search observation can
  support discovery for that query; a negative `site:` search is not proof the
  whole engine excludes the URL. Note inaccessible evidence rather than guessing.
- Check current canonical behavior before republishing. Publish original work
  where the user owns it and choose an adapted LinkedIn version or a summary
  with a source link when appropriate; do not promise the platforms treat copies
  identically.

## Select and test

Choose surfaces from audience fit and observed retrieval, not a fixed article
length, follower count, posting cadence, or engagement threshold. Provide useful
original evidence, clear headings where the format supports them, accurate
entities, and truthful profile positioning. Keep company/profile descriptions
consistent with the About page; see [positioning-and-consensus.md](positioning-and-consensus.md).

Run a comparable sample before and after the chosen change using
[format-volatility.md](format-volatility.md). Measure qualified visits and
conversions alongside citations. Keep third-party channels diversified and owned
pages useful. Profile edits, posting, and paid campaigns require authorization;
research and drafts do not imply permission to publish.
