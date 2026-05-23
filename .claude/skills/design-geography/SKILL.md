---
name: design-geography
description: Design 3-5 regions: climate, economy, key locations
agent: world-builder
mode_default: semi
mode_compatible: [full, semi, manual]
inputs:
  - node_path: optional, target node in the tree
outputs:
  - novel.world_bible.geography
---

# /design-geography

Design 3-5 regions: climate, economy, key locations

## Workflow

1. Invoke `world-builder` with focus=geography.
2. Generate 3-5 regions; cross-link to politics if exists.
3. Write `novel.world_bible.geography`.

## Mode behavior

- **full**: agent produces deliverable, writes to tree, advances.
- **semi**: agent produces draft + alternatives, pauses for user accept/edit.
- **manual**: agent does not write; offers a brief and waits for the user's input, then validates.

## Owning agent

`world-builder` — see `agents/*/$agent.md` for the full role definition.
