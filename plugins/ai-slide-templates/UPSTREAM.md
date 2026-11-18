# Distribution source

- Canonical workflow/templates: https://github.com/cogine-ai/ai-slide-templates
- Reviewed commit: `7d0f48d6a37af48856e6143c70cdbc1b88d4e91a`
- Upstream skill: `skills/ai-slide-templates/SKILL.md`
- Plugin version: `0.1.1`
- Library selection: `library.json` (87 templates, 1,334 demo slides)

This is a lightweight consumer package. Templates and their notices are fetched
from the pinned source rather than copied into the Marketplace. The MIT LICENSE
is copied from that source. No upstream release or tag is implied.

The packaged skill retains upstream selection, outline, layout-slot,
content-limit, design-system, preview and verification behavior. Marketplace
adaptations replace manual cloning with the pinned setup helper, keep output and
browser dependencies out of the plugin/cache, describe HTML/PPTX scope, direct
visual validation to the output deck, and namespace the Codex default prompt.
The upstream AGENTS.md governs deck construction at this pinned revision; the
plugin governs library preparation. No runtime tracking of main is performed.

For updates, change canonical presentation behavior upstream first. Review the
new source commit, deliberately refresh the packaged skill and library.json,
retain documented packaging adaptations and host invocation metadata, bump both
host manifest versions and the Claude catalog entry, then repeat installation
and output-deck validation. Do not edit installed caches. The legacy
cogine-dev-skillset skill and any local overrides remain separate consumers;
this release neither overwrites nor disables them.
