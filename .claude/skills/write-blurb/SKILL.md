---
name: write-blurb
description: Write the back-cover blurb (80-120 words)
agent: blurb-writer
mode_default: full
mode_compatible: [full, semi, manual]
inputs:
  - node_path: optional, target node in the tree
outputs:
  - novel.manuscript.blurb
---

# /write-blurb

Write the back-cover blurb (80-120 words)

## Workflow

1. Load ideation + protagonist + opening image + midpoint reversal.
2. Invoke `blurb-writer`.
3. Produce 3-4 sentence blurb passing all four anti-pattern checks.
4. Write `novel.manuscript.blurb`.

## Mode behavior

- **full**: agent produces deliverable, writes to tree, advances.
- **semi**: agent produces draft + alternatives, pauses for user accept/edit.
- **manual**: agent does not write; offers a brief and waits for user input, then validates.

## Owning agent

`blurb-writer` — see `agents/*/$agent.md` for the full role definition.
