---
name: design-political-system
description: Design polities, succession, conflict lines
agent: world-builder
mode_default: semi
mode_compatible: [full, semi, manual]
inputs:
  - node_path: optional, target node in the tree
outputs:
  - novel.world_bible.politics
---

# /design-political-system

Design polities, succession, conflict lines

## Workflow

1. Invoke `world-builder` with focus=politics.
2. Define polities + tensions.
3. Write `novel.world_bible.politics`.

## Mode behavior

- **full**: agent produces deliverable, writes to tree, advances.
- **semi**: agent produces draft + alternatives, pauses for user accept/edit.
- **manual**: agent does not write; offers a brief and waits for the user's input, then validates.

## Owning agent

`world-builder` — see `agents/*/$agent.md` for the full role definition.
