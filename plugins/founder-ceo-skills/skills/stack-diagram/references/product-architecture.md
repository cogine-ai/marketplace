# Product architecture

Use one view to show the product's capabilities and how they work together. Keep the template's graph paper, domain boxes, icon tiles, and labeled arrows.

## Model the product

1. Identify the product boundary, module granularity, and whether the source describes the current product or a proposed design. Use the supplied product brief, PRD, navigation, or repository evidence. Choose the scope of the view and state it on the diagram.
2. List each distinct module once, with a short name, role, and owning domain. Group by product area or workflow. A shared capability belongs to a single shared group and can connect to several domains. Navigation aliases can refer to the same module.
3. Show the total in a heading and each domain count in its group label. Count the visible modules at one stated level. Exclude grouping boxes, users, and external systems. When a view expands a module into submodules, identify which level the total describes. Use a label such as “6 mapped modules” when the source covers only part of the product.
4. Draw meaningful directed links with a verb and a defined direction. Use accent solid for the main product flow, neutral solid for secondary flows, and neutral dashed for explicit dependencies. For a dependency, the arrow points from the dependent module to the module it needs. Group membership is represented by containment. Note unconfirmed relationships separately and distinguish a proposed architecture from current behavior.

## Draw the map

- Copy `assets/generic/module.svg` into the working icon directory as `module.svg` and reference it as `%%ICON_module%%`. Use the bundled `user.svg` or `server.svg` for actors or external systems when they fit. This path works without fetching brand assets.
- Adapt the sample labels and legend to product concepts. Show the module count within `.canvas` when exporting a canvas-only PNG. Widen long node labels and recalculate spacing using [geometry.md](geometry.md). For Chinese labels, set `lang` appropriately and put the local Chinese font ahead of the template's Japanese fallback if needed.
- For a dense inventory, keep the product-level map readable and add focused detail views only where requested or needed. When delivering multiple views, state which counts belong to each view.

### Example

An invoicing product has **6 modules in 3 domains**. Workspace contains Accounts and Permissions. Billing contains Plans, Checkout, and Invoices. Shared contains Notifications. The primary flow is Plans → Checkout → Invoices. Invoices → Notifications sends an invoice notice. Checkout → Permissions checks access. A customer and an external payment provider can appear for context and are excluded from the module count.
