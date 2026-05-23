---
name: write-cover-brief
description: Brief for the cover designer (or AI image gen)
agent: cover-brief-writer
mode_default: full
mode_compatible: [full, semi, manual]
inputs:
  - node_path: optional, target node in the tree
outputs:
  - novel.manuscript.cover_brief
---

# /write-cover-brief

Brief for the cover designer (or AI image gen)

## Workflow

1. Load ideation + metadata + key chapter excerpts.
2. Invoke `cover-brief-writer`.
3. Produce mood + palette + focal element + references + avoid.
4. Write `novel.manuscript.cover_brief`.

## Mode behavior

- **full**: agent produces deliverable, writes to tree, advances.
- **semi**: agent produces draft + alternatives, pauses for user accept/edit.
- **manual**: agent does not write; offers a brief and waits for user input, then validates.

## Owning agent

`cover-brief-writer` — see `agents/*/$agent.md` for the full role definition.
