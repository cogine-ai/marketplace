# CogineX icon

`icon.png` is an unchanged copy of CogineX's 512 × 512 transparent green X-knot
mark, color `#75FB81`.

Source: [`cogine-ai/CogineX-mono`, `apps/web/public/logo512.png`](https://github.com/cogine-ai/CogineX-mono/blob/0534fca901bd340c512c9f1078e4cc39c2452b3b/apps/web/public/logo512.png),
last changed in `0534fca901bd340c512c9f1078e4cc39c2452b3b`.
The current web application uses the corresponding geometry in
[`apps/web/src/components/icon/coginex-x.svg`](https://github.com/cogine-ai/CogineX-mono/blob/0534fca901bd340c512c9f1078e4cc39c2452b3b/apps/web/src/components/icon/coginex-x.svg).

The inspected upstream `apps/docs/favicon.svg`, `apps/docs/logo/{light,dark}.svg`,
and `apps/web/tauri/icon.png` retain the old Macro M-shaped mark. They are not
the source of this plugin icon.

Codex references this PNG through `interface.logo`, `logoDark`, and
`composerIcon`. Claude's `icon` field supplies directory listing metadata;
Claude Code ignores it when loading the plugin. The package does not depend
on animated icon playback.

- [Codex icon formats](https://developers.openai.com/plugins/deploy/submission#icons-and-screenshots)
- [Claude directory listing fields](https://code.claude.com/docs/en/plugins/manifest-reference#directory-listing-fields)
