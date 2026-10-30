# CogineX icon

`mark.svg` preserves CogineX's theme-neutral X-knot geometry with
`fill="currentColor"`. `icon.png` renders that mark at 512 × 512 with a
transparent background and the current static brand orange, `#FF8F05`.

Shape source: [`apps/web/src/components/icon/coginex-x.svg`](https://github.com/cogine-ai/CogineX-mono/blob/0534fca901bd340c512c9f1078e4cc39c2452b3b/apps/web/src/components/icon/coginex-x.svg),
copied unchanged from `0534fca901bd340c512c9f1078e4cc39c2452b3b`.
Palette source: [`apps/docs/docs.json`, `colors`](https://github.com/cogine-ai/CogineX-mono/blob/75cf35c4c95112b22f5e30b2ae129c6f465a5a67/apps/docs/docs.json),
which declares `#ff8f05` for primary, light and dark branding. The web app's
light/dark accent tokens can vary; the packaged icon uses this fixed orange.

To reproduce the PNG with `sharp`, read `mark.svg`, replace its
`fill="currentColor"` with `fill="#FF8F05"`, resize to 512 × 512 and write PNG.

The inspected upstream `apps/docs/favicon.svg`, `apps/docs/logo/{light,dark}.svg`,
and `apps/web/tauri/icon.png` retain the old Macro M-shaped mark. They are not
the source of this plugin icon. This finding concerns the M-shaped geometry,
not the orange theme color.

Codex references this PNG through `interface.logo`, `logoDark`, and
`composerIcon`. Claude's `icon` field supplies directory listing metadata;
Claude Code ignores it when loading the plugin. The package does not depend
on animated icon playback.

- [Codex icon formats](https://developers.openai.com/plugins/deploy/submission#icons-and-screenshots)
- [Claude directory listing fields](https://code.claude.com/docs/en/plugins/manifest-reference#directory-listing-fields)
