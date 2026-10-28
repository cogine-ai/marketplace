# Good Offence behavior evaluation

Give a fresh reviewer the current skill and one `cases/<id>/input.md` at a time, or a labeled batch from `suite.json`. Supply the same review request to every case. Do not give the reviewer `expected.json`, prior conclusions, score labels, or the evaluator's reasoning. Do not run fixture code or query live repositories.

Record the model/host, exact skill and input hashes, date, findings, source evidence and relevant retained safeguards. A structured result can use one item per case with `id`, `findings` and `scope_reason`; each finding should identify its location, defensive mechanism, protected condition, evidence, simplification and preserved behavior.

Only after the raw response is saved, read `expected.json`. Judge each case on both scope and equivalence. Inspect the mechanism and call path: a nonempty finding, a concern label, a self-assessed confidence value, or a `keep=true` verdict is not a pass by itself. Location requirements identify a file and symbol, not an exact string to reproduce. A positive case needs a supported in-scope suggestion, while every other suggestion must also meet the evidence bar. Negative cases pass only when the reviewer withholds the unsupported simplification; an out-of-scope case must not be praised as defensive cleanup.

Report behavior results separately from packaging/link/schema checks. Timeout, missing output, unavailable evidence, or structural validation alone does not establish semantic success. Keep real run artifacts outside the distributed skill; these inputs are synthetic and contain no production code or credentials.
