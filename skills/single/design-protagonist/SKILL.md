---
name: design-protagonist
description: Design the protagonist: want, need, lie, ghost, arc
agent: protagonist-specialist
mode_default: semi
mode_compatible: [full, semi, manual]
inputs:
  - node_path: optional, target node in the tree
outputs:
  - novel.characters[?role=protagonist]
---

# /design-protagonist

Design the protagonist: want, need, lie, ghost, arc

## Workflow

1. Load `novel.ideation.dramatic_question`.
2. Invoke `protagonist-specialist`.
3. Present arc beats; user reviews.
4. Write `novel.characters[?role=protagonist]`.

## Mode behavior

- **full**: agent produces deliverable, writes to tree, advances.
- **semi**: agent produces draft + alternatives, pauses for user accept/edit.
- **manual**: agent does not write; offers a brief and waits for the user's input, then validates.

## Owning agent

`protagonist-specialist` — see `agents/*/$agent.md` for the full role definition.
