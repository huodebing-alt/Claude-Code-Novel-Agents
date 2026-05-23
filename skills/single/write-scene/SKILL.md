---
name: write-scene
description: Write a single scene (one or more contiguous beats)
agent: scene-builder
mode_default: semi
mode_compatible: [full, semi, manual]
inputs:
  - node_path: optional, target node in the tree
outputs:
  - novel.outline.acts.*.chapters.*.beats.*.text[range]
---

# /write-scene

Write a single scene (one or more contiguous beats)

## Workflow

1. Load beats (range required in input).
2. Load adjacent beats for continuity.
3. Invoke `scene-builder`.
4. Write the beat range.

## Mode behavior

- **full**: agent produces deliverable, writes to tree, advances.
- **semi**: agent produces draft + alternatives, pauses for user accept/edit.
- **manual**: agent does not write; offers a brief and waits for the user's input, then validates.

## Owning agent

`scene-builder` — see `agents/*/$agent.md` for the full role definition.
