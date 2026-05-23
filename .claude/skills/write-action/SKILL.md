---
name: write-action
description: Render an action sequence (beat range)
agent: scene-builder
mode_default: semi
mode_compatible: [full, semi, manual]
inputs:
  - node_path: optional, target node in the tree
outputs:
  - novel.outline.acts.*.chapters.*.beats.*.text[range]
---

# /write-action

Render an action sequence (beat range)

## Workflow

1. Load beats + POV character.
2. Invoke `scene-builder` with focus=action.
3. Apply choreography: who, where, what hits what, in what order.
4. Write the beat range.

## Mode behavior

- **full**: agent produces deliverable, writes to tree, advances.
- **semi**: agent produces draft + alternatives, pauses for user accept/edit.
- **manual**: agent does not write; offers a brief and waits for the user's input, then validates.

## Owning agent

`scene-builder` — see `agents/*/$agent.md` for the full role definition.
