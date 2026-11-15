# Version 0.1.0 validation

2026-11-16; macOS, Node.js 24.22.1, Google Chrome at 1280×720.

- Native Codex and Claude Code local-marketplace installation succeeded in
  separate temporary host configurations. Both reported enabled version 0.1.0;
  the installed setup helpers returned the pinned library path and 81 templates.
- A real first-use GitHub fetch checked out the pinned commit. Repeat setup
  reused the same cache. Seven regression tests cover fetching, offline reuse,
  dirty-cache preservation, download failure cleanup, incomplete libraries,
  occupied paths, and symlinked installed/cache paths.
- Strict Claude plugin and marketplace manifest validation passed. Native
  Codex installation accepted its manifest and catalog. Existing Coding bundle
  validation also passed.
- The pinned source passed 81-template structural validation and 46 tool tests.
  Six asset manifests passed; 75 templates were outside that manifest review.
- Assisted direct-template and raw-notes/selection smoke cases each produced an
  eight-slide HTML deck. Both passed the pinned visual validator across all
  slides, and explicit ArrowRight/End/Home navigation checks. Two candidate
  previews rendered as one-slide decks. No page exceptions were recorded.
- Cover, agenda and candidate-preview screenshots were inspected. Overlong cover
  text and terminal whitespace in initial fixture substitutions were corrected
  before final verification. Template CSS and runtime were preserved.

Inputs, reproduction steps and artifact hashes are recorded in
[the acceptance receipt](https://github.com/cogine-ai/marketplace/tree/main/maintenance/reviews/ai-slide-templates-0.1.0).
They stay outside the installable plugin package. These checks do not establish
an autonomous model success rate, all-template browser acceptance, Windows/Linux
or real touchscreen coverage, native PPTX support, or universal asset clearance.
The PR prepares 0.1.0; marketplace publication requires its merge.
