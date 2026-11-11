---
name: stack-diagram
description: "Create a standalone visual diagram of product modules and their relationships, or a branded diagram of a technical stack, deployment, or service topology. Use when the user wants a product module map with counts or a polished architecture diagram for sharing or documentation. Supports self-contained HTML, PNG, and React/TSX."
license: MIT (see LICENSE); bundled fonts are SIL OFL 1.1
---

# stack-diagram

Use a shared graph-paper style with grouped boxes, icon tiles, and orthogonal arrows. Build one self-contained HTML file and derive the other requested formats from it. Honor a request for Mermaid or another diagram format directly.

The build uses Python 3.9+. Network access is needed when fetching remote logos. Resolve scripts, assets, and references from this skill's directory. Write the draft, icon directory, and outputs to the task workspace or a temporary directory.

## 1. Define the diagram

- **Product architecture.** Read [product-architecture.md](references/product-architecture.md) to identify the modules, count them at a stated level, and show their relationships. Use bundled generic icons for an offline build.
- **Technical architecture.** Give each service or technology a node and a short role. Group nodes that share a runtime, vendor, or repository. Use accent solid arrows for the primary request or data flow, neutral solid arrows for secondary connections, and neutral dashed arrows for development and deployment. Use [technical-icons.md](references/technical-icons.md) for brand and vendor rules.

Use the user's brief or available source material to establish the nodes and links. For a flat list, infer a layout and label any proposed links or topology assumptions. Ask when an unresolved choice would materially change the diagram.

## 2. Lay out and build

Read [geometry.md](references/geometry.md) for spacing and arrow anchors. Copy `assets/template.html` and replace the sample content, including the legend and footer. Set the document language to match the labels. Keep the existing theme tokens and escape source text when inserting it into HTML or SVG labels.

Use `%%ICON_<name>%%` for icon references and leave the bundled font placeholders in place. Build with the font path to embed the bundled fonts and diagram icons. The script reports unresolved tokens before writing output.

```bash
python3 "$skill_root/scripts/build.py" draft.html "$icons_dir" diagram.html --fonts "$skill_root/assets/fonts"
```

Credit the icon sources actually used and keep the template's upstream attribution. If an official logo is unavailable, use a visibly generic icon and keep the service name on the node. Preserve the actual brand marks where available.

## 3. Inspect and deliver

Open the built HTML in an available browser. Check light and dark variants, label legibility, icon contrast, group boundaries, and arrow routing. Read the arrow direction against the stated relationships. For a product map, reconcile the visible module counts with the source list. Check the requested language in the render, especially for CJK glyphs. Revise and inspect again when the output is clipped or unclear.

- **HTML** is the default and works offline once built. Browser preview is sufficient for its visual check. Report any part of the visual check the environment could not run.
- **PNG** comes from the same HTML. Use the installed Playwright and its matching Chromium, or provision the pair in an isolated environment when available. If the browser cannot launch, deliver the HTML and explain what prevented PNG export. Inspect both exported themes before delivering them. Use `--single` for one theme or `--full-page` to include the header and footer.
- **React/TSX** uses [tsx.md](references/tsx.md). An interactive artifact can use the same HTML when the host supports it and the user wants that delivery format.

```bash
python3 "$skill_root/scripts/render_png.py" diagram.html diagram.png --selector .canvas --scale 2
```

Deliver files in the requested workspace or chat. Read [gallery.md](references/gallery.md) only when the user asks to publish to the upstream public gallery.
