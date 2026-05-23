---
name: design-antagonist
description: Design the antagonist: wound, justification, collision
agent: antagonist-specialist
mode_default: semi
mode_compatible: [full, semi, manual]
inputs:
  - node_path: optional, target node in the tree
outputs:
  - novel.characters[?role=antagonist]
---

# /design-antagonist

Design the antagonist: wound, justification, collision

## Workflow

1. Load protagonist + dramatic question.
2. Invoke `antagonist-specialist`.
3. Mustache-twirl test before approval.
4. Write `novel.characters[?role=antagonist]`.

## Mode behavior

- **full**: agent produces deliverable, writes to tree, advances.
- **semi**: agent produces draft + alternatives, pauses for user accept/edit.
- **manual**: agent does not write; offers a brief and waits for the user's input, then validates.

## Owning agent

`antagonist-specialist` — see `agents/*/$agent.md` for the full role definition.
