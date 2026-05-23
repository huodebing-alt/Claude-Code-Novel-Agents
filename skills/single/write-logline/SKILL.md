---
name: write-logline
description: Write a 25-word logline from theme + genre
agent: logline-specialist
mode_default: semi
mode_compatible: [full, semi, manual]
inputs:
  - node_path: optional, target node in the tree
outputs:
  - novel.ideation.logline
---

# /write-logline

Write a 25-word logline from theme + genre

## Workflow

1. Load `novel.ideation.theme` and `novel.metadata.genre`.
2. Invoke `logline-specialist`.
3. Present recommended + alternatives; user picks.
4. Write `novel.ideation.logline`.

## Mode behavior

- **full**: agent produces deliverable, writes to tree, advances.
- **semi**: agent produces draft + alternatives, pauses for user accept/edit.
- **manual**: agent does not write; offers a brief and waits for the user's input, then validates.

## Owning agent

`logline-specialist` — see `agents/*/$agent.md` for the full role definition.
