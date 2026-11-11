# Public gallery

The upstream project runs a [public gallery](https://stacks.caru.moe) for technical stack diagrams. Use this procedure only when the user requests publication there.

After the user explicitly requests the public gallery, ask for a display name (don't fill it in from `gh` or git) and whether to add a GitHub login. The login is optional and never shown publicly; it only lets them delete the post later by signing in to the gallery with that account. If `gh` is signed in, offer the result of `gh api user -q .login`; include it only if they agree.

Then show exactly what will be sent before sending anything:

- the light and dark PNGs — the `.canvas` pair `render_png.py` writes (`out.png` / `out-dark.png`) — with their paths and every label in them
- a title, in plain English even when the conversation isn't. It describes the diagram, not the request. The diagram's own labels stay as they are.
- the stack: the technologies in the diagram, by their official names
- the display name
- the GitHub login, if any, marked as not public

Point out anything that looks internal — hostnames, IPs, customer or company names, internal service names — and suggest re-rendering without it first. Ask them to confirm it is their own system or one they may show publicly, and send only after a second explicit yes on that exact content.

```bash
python3 "$skill_root/scripts/share.py" submit out.png out-dark.png --title "..." --stack "..." --name "..." [--github LOGIN] [--icons DIR]
```

`--stack` lists the technologies, comma-separated, by their official names. Write `Name=key` to show a technology's logo beside it in the gallery. `key` is its entry in the icon directory's `manifest.json`, and `--icons` takes that directory. A name without `=` goes without a logo, for example `--stack "Next.js=nextjs,Hono=hono,Neon" --icons <icons-dir>`. The gallery shows logos from svgl, gilbarbara/logos and devicon.

If `share.py` rejects a PNG as too large, re-render with a lower `--scale` and show the new pair before sending.

Tell the user the URL, that a held post appears only after a manual review, and the path where `share.py` says it saved the delete key. Delete a post on request with `python3 "$skill_root/scripts/share.py" delete <id>`. The `list` subcommand shows saved posts. If the gallery confirmed the GitHub login they supplied, they can also sign in to delete the post.
