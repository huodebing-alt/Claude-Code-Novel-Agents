---
name: format-manuscript
description: Apply smart quotes, em-dash hygiene, chapter numbering, scene breaks
agent: formatter
mode_default: full
mode_compatible: [full, semi, manual]
inputs:
  - node_path: optional, target node in the tree
outputs:
  - novel.manuscript.compiled_md
---

# /format-manuscript

Apply smart quotes, em-dash hygiene, chapter numbering, scene breaks

## Workflow

1. Load final revised manuscript.
2. Invoke `formatter`.
3. Apply 8 mechanical passes (see formatter.md).
4. Write `novel.manuscript.compiled_md`.

## Mode behavior

- **full**: agent produces deliverable, writes to tree, advances.
- **semi**: agent produces draft + alternatives, pauses for user accept/edit.
- **manual**: agent does not write; offers a brief and waits for user input, then validates.

## Owning agent

`formatter` — see `agents/*/$agent.md` for the full role definition.
