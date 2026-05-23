---
name: weave-subplot
description: Design a B or C plot interlocked with main
agent: subplot-weaver
mode_default: semi
mode_compatible: [full, semi, manual]
inputs:
  - node_path: optional, target node in the tree
outputs:
  - novel.outline.subplots
---

# /weave-subplot

Design a B or C plot interlocked with main

## Workflow

1. Load main outline.
2. Invoke `subplot-weaver`.
3. Define dramatic question + intersection points.
4. Write `novel.outline.subplots[]`.

## Mode behavior

- **full**: agent produces deliverable, writes to tree, advances.
- **semi**: agent produces draft + alternatives, pauses for user accept/edit.
- **manual**: agent does not write; offers a brief and waits for the user's input, then validates.

## Owning agent

`subplot-weaver` — see `agents/*/$agent.md` for the full role definition.
