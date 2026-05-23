---
name: brainstorm-themes
description: Generate 5-10 thematic directions from a seed
agent: theme-brainstorm
mode_default: semi
mode_compatible: [full, semi, manual]
inputs:
  - node_path: optional, target node in the tree
outputs:
  - novel.ideation.theme
---

# /brainstorm-themes

Generate 5-10 thematic directions from a seed

## Workflow

1. Load `seed` from input (or prompt the user).
2. Invoke `theme-brainstorm`.
3. Present the candidate themes; user picks one.
4. Write `novel.ideation.theme`.

## Mode behavior

- **full**: agent produces deliverable, writes to tree, advances.
- **semi**: agent produces draft + alternatives, pauses for user accept/edit.
- **manual**: agent does not write; offers a brief and waits for the user's input, then validates.

## Owning agent

`theme-brainstorm` — see `agents/*/$agent.md` for the full role definition.
