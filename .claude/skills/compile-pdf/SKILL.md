---
name: compile-pdf
description: Render the print-ready PDF
agent: pdf-compositor
mode_default: full
mode_compatible: [full, semi, manual]
inputs:
  - node_path: optional, target node in the tree
outputs:
  - novel.manuscript.pdf_path
---

# /compile-pdf

Render the print-ready PDF

## Workflow

1. Load compiled_md + cover_brief + blurb + config.
2. Invoke `pdf-compositor` (executes output/pdf_compositor.py).
3. Verify page count within target ±10%.
4. Write PDF path to `novel.manuscript.pdf_path`.

## Mode behavior

- **full**: agent produces deliverable, writes to tree, advances.
- **semi**: agent produces draft + alternatives, pauses for user accept/edit.
- **manual**: agent does not write; offers a brief and waits for user input, then validates.

## Owning agent

`pdf-compositor` — see `agents/*/$agent.md` for the full role definition.
