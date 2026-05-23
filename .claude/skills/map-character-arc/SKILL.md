---
name: map-character-arc
description: Map a character's arc onto specific outline beats
agent: protagonist-specialist
mode_default: semi
mode_compatible: [full, semi, manual]
inputs:
  - node_path: optional, target node in the tree
outputs:
  - novel.characters[*].arc_beat_anchors
---

# /map-character-arc

Map a character's arc onto specific outline beats

## Workflow

1. Load character.arc + novel.outline.*.
2. Invoke `protagonist-specialist` with focus=arc_mapping.
3. Anchor each arc beat to a specific outline beat ID.
4. Write `novel.characters[?id=<id>].arc_beat_anchors`.

## Mode behavior

- **full**: agent produces deliverable, writes to tree, advances.
- **semi**: agent produces draft + alternatives, pauses for user accept/edit.
- **manual**: agent does not write; offers a brief and waits for the user's input, then validates.

## Owning agent

`protagonist-specialist` — see `agents/*/$agent.md` for the full role definition.
