---
name: select-genre
description: Pick or confirm genre + apply genre defaults
agent: genre-selection-agent
mode_default: semi
mode_compatible: [full, semi, manual]
inputs:
  - node_path: optional, target node in the tree
outputs:
  - novel.metadata.genre
---

# /select-genre

Pick or confirm genre + apply genre defaults

## Workflow

1. Invoke `genre-selection-agent`.
2. Update `novel.metadata.{genre, subgenre, target_audience}` and apply defaults.

## Mode behavior

- **full**: agent produces deliverable, writes to tree, advances.
- **semi**: agent produces draft + alternatives, pauses for user accept/edit.
- **manual**: agent does not write; offers a brief and waits for user input, then validates.

## Owning agent

`genre-selection-agent` — see `agents/*/$agent.md` for the full role definition.
