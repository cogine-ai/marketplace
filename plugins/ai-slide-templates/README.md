# AI Slide Templates

Turn real content into a finished HTML presentation using 87 distinct slide
systems. The skill can shape raw notes into an outline, recommend suitable
templates, show cover previews, adapt a complete deck, and check it in a browser.

## Install

Add `cogine-ai/marketplace` to your host's marketplaces, then install:

```sh
# Codex
codex plugin add ai-slide-templates@cogine-ai

# Claude Code
claude plugin install ai-slide-templates@cogine-ai
```

Start a new Codex chat or reload Claude Code plugins after installation.
In Codex, invoke `$ai-slide-templates:ai-slide-templates` and provide your notes,
audience, purpose, and desired length. In Claude Code, use
`/ai-slide-templates:ai-slide-templates` or ask to create an HTML presentation.

Example requests:

- “Turn these product research notes into an eight-slide presentation. Show a few suitable visual directions first.”
- “Use Research Readout Pastel for this customer interview summary.”
- “Use my chosen template and preserve its fonts, colors, layout and navigation.”

## Requirements and first use

Node.js 22+, Git, network access for the first library download, and an agent
with filesystem and browser access. No API key, account or MCP service is needed.
The agent runs the bundled setup helper; the user does not need to clone a repo.

The plugin contains the skill and setup helper. The roughly 217 MiB template
library is downloaded separately at the exact commit in `library.json` into
`~/.cache/cogine-ai/ai-slide-templates/<commit>/`. Later tasks verify and reuse
that local version without fetching updates. Some older templates load remote
fonts or media, and some video layouts link to online playback; cached
library availability does not guarantee every deck works entirely offline.

For manual setup or a different cache location:

```sh
node /absolute/path/to/plugin/scripts/prepare-library.mjs --cache-dir /absolute/cache/root
```

The helper prints the absolute library path, commit, and template count as JSON.
It preserves existing files and refuses a changed or mismatched cache; choose
another cache root if you need to retain local modifications. An interrupted
process can leave a `.download-*` directory, which is never reused as a library.

Previews and completed decks go in your output workspace. Complete template
folders are copied with source notices and font licenses before editing.
The plugin and library cache are source material, not working output folders.

## Deliverable

Version 0.1.1 produces browser-openable HTML, with editable text and layout.
Native PowerPoint (`.pptx`) export is outside this version. Browser verification
checks the actual finished deck; if browser access is unavailable, the agent
must state that verification was not performed.

The plugin's original code and instructions are MIT. Templates, fonts, images
and source designs retain their own notices and applicable terms. The library's
source registers document provenance; they do not assert universal clearance.

## Maintenance and validation

The template repository owns the presentation workflow and templates. Marketplace
owns the plugin packaging and setup adaptation. See [UPSTREAM.md](UPSTREAM.md)
for the pinned source and deliberate update procedure.

```sh
node --test plugins/ai-slide-templates/scripts/*.test.mjs
claude plugin validate plugins/ai-slide-templates --strict
```

See [VALIDATION.md](VALIDATION.md) for the 0.1.1 acceptance scope.
