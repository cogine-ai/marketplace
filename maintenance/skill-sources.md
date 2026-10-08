# Maintenance sources and consumer entries

The [registry](skill-sources.json) selects one editable authority for each
reviewed source group. It separates repository sources, role distribution
aliases, installer-managed overlays and local overrides. Paths relative to
the user home or OurSkills root describe this machine, not an installer.

## Edit and distribute

| Group | Edit authority | Consumer rule |
|---|---|---|
| Power Gates | `CoginePowerGates/cogine-power-gates`, main at `d95315b` | Copy runtime Markdown to Coding; preserve each host's agents metadata. Global copy remains disabled in Codex. |
| Other Cogine role skills | This repository's `plugins/<role>/skills` | Publish reviewed source, refresh the native catalog, install the desired version and verify hashes. Never edit an installed cache. |
| Shared grilling, backlog, spec and ticket Markdown | Coding package | Product retains distribution aliases required by existing namespace calls; synchronize shared Markdown while preserving agents metadata. |
| Shared Founder Office Hours | Product package | Founder/CEO retains its namespace alias and metadata. |
| Shared PLG sales integration and references | Growth package | Sales retains its namespace alias; synchronize all shared Markdown, including references. |
| Standalone repository matches | Registry's canonical source folder | Update consumer snapshots from that source; a dirty source folder is identified separately from its commit. |
| Differing standalone local overrides | Registry's selected `.codex/skills` folder | Maintain this override deliberately; do not replace it with a differing historical repository. `.agents` mirrors remain consumers for other hosts. |
| Installer-managed local repairs | Installer origin plus the reviewed [overlay](standalone-skills/2026-10-08.json) | Keep installer locks as origin records. Retain the before/after hashes and patch; do not present overlay hashes as raw upstream identity. |

CEO's previously validated local repair is now committed alone as `5c82799`
in cogine-dev-skillset. Its consumer entrypoints match the source. Unrelated
dirty work in that repository is retained. Power's accepted version branch
has been fast-forwarded into its canonical main; it has no configured remote.

Two Prototype variants have different support assets and behavior. Standalone
AI SEO is also not equivalent to bundled search-visibility. Keep these distinct.
Official/system plugins remain managed by their vendor.

## Local Codex entry selection — 2026-10-08

Seventeen previously enabled paths were disabled through the native
`skills/config/write` API, followed by `skills/list` with `forceReload`:

- Seven byte-equal `.agents` mirrors now use their `.codex` entry.
- Both standalone Founder Office Hours paths now use the Product plugin.
- Seven standalone Growth/Grilling overlaps now use their installed plugins.
- The deprecated `grill-me` alias is disabled.

All directories, support files and installer locks remain intact. This
selection changes Codex discovery only; it does not disable another host.
The registry's local settings are a receipt, not a rule to apply blindly to
another machine. Restore a selected path with the same native API and
`enabled: true` if its replacement is removed or a deliberate rollback is needed.

## Remaining five-entry transition

[Six bounded file transfers](source-unification-2026-10-08.json) preserve the
useful standalone changes in the packaged source:

| Standalone | Prepared replacement | Preserved behavior |
|---|---|---|
| analytics | Growth 0.1.6 | Verify connector/account/property; exports, code or manual validation when access is unavailable. |
| launch | Growth 0.1.6 | Verify partner integration/account; draft an unavailable workflow without claiming it was configured or launched. |
| domain-modeling | Coding 0.2.5 | Explicit domain policy wins over defaults; active legacy paths and existing glossary content remain. |
| setup-matt-pocock-skills | Coding 0.2.5 | Preserve settled tracker/domain policy; templates only fill agreed gaps. |
| improve-codebase-architecture | Coding 0.2.5 | Use the selected glossary/ADRs; retain namespaced calls, secure report files and HTML protections. |

These five standalone entries remain enabled until the candidate is merged,
published/available, installed and read back. Then verify the transferred
rules and disable only their exact `.agents/skills/<name>/SKILL.md` paths.
Prepared package versions do not establish installed state. Existing
agents metadata and all historical upstream sync ledgers remain unchanged.
