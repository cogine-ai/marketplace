# AI Slide Templates 0.1.0 acceptance

The receipt records assisted workflow smoke checks with deliberately fictional
inputs. It is not an autonomous model evaluation. Source layout CSS and navigation
are preserved; all slide text is replaced. Simulated research is labeled and
uncollected operational baselines are marked TBD. The source template's
illustrative bar lengths are explicitly labeled as priorities, not measurements.

The direct case requests Airy Modern. The selection case starts from raw
architecture notes, compares Circuit Tech Dark and Midnight Executive cover
previews, and chooses Circuit for its engineering layouts. Each case contains
an eight-slide authored outline in `build-smoke.py`.

To reproduce after preparing the pinned library:

```sh
python3 maintenance/reviews/ai-slide-templates-0.1.0/build-smoke.py --library /absolute/library --out /absolute/smoke
node /absolute/library/scripts/preview.mjs --root /absolute/library --out-dir /absolute/smoke/outputs/selection/previews --title 'Relay Architecture Pilot' --subtitle 'Engineering review' circuit-tech-dark midnight-executive
node /absolute/library/scripts/validate-visual.mjs --root /absolute/smoke/outputs/direct --template airy-modern
node /absolute/library/scripts/validate-visual.mjs --root /absolute/smoke/outputs/selection --template circuit-tech-dark
node maintenance/reviews/ai-slide-templates-0.1.0/browser-smoke.mjs /absolute/smoke /absolute/path/to/package.json
```

The last command requires Playwright installed alongside the supplied
`package.json`, plus Google Chrome. It writes screenshots and a navigation/error
report outside the shipped plugin. Inspect screenshots in addition to the
validator: initial text substitutions exposed covered cover copy and lost
terminal line breaks that automated slide-bound checks did not flag. The
fixtures were corrected by shortening copy and retaining source whitespace;
no template CSS or runtime was changed.

Receipt hashes identify the tested HTML, metadata, briefs, previews and reviewed
screenshots. Bulky rendered files and template/media payloads remain outside the
Marketplace. Native installation was tested in separate temporary Codex and
Claude Code configurations; existing local skills were not migrated or disabled.
