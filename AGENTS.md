# Skill maintenance

Read `maintenance/skill-sources.md` and the matching entry in
`maintenance/skill-sources.json` before changing a skill with consumer copies.
Edit its recorded authority; update distribution aliases deliberately.

Power Gates is maintained in the separate CoginePowerGates repository. Preserve
each consumer's invocation metadata. Other role skill changes belong in this
Marketplace unless the registry identifies a different canonical source.

Installed caches are consumers. Preserve local overrides and installer origin
records; a same-name skill is not evidence of equivalent behavior. Shared
role aliases retain their namespaces and existing metadata.

For a local entry transition, verify the installed replacement version and
required transferred behavior before disabling the previous entry. Codex-only
configuration changes must not remove shared directories used by other hosts.
