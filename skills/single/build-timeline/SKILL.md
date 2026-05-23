---
name: build-timeline
description: Build 5-10 historical events relevant to the plot's present
agent: world-builder
mode_default: semi
mode_compatible: [full, semi, manual]
inputs:
  - node_path: optional, target node in the tree
outputs:
  - novel.world_bible.timeline
---

# /build-timeline

Build 5-10 historical events relevant to the plot's present

## Workflow

1. Invoke `world-builder` with focus=timeline.
2. Each event has date + consequence_today.
3. Write `novel.world_bible.timeline`.

## Mode behavior

- **full**: agent produces deliverable, writes to tree, advances.
- **semi**: agent produces draft + alternatives, pauses for user accept/edit.
- **manual**: agent does not write; offers a brief and waits for the user's input, then validates.

## Owning agent

`world-builder` — see `agents/*/$agent.md` for the full role definition.
