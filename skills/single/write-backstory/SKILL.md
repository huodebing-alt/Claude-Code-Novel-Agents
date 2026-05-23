---
name: write-backstory
description: Write a per-character backstory
agent: backstory-writer
mode_default: semi
mode_compatible: [full, semi, manual]
inputs:
  - node_path: optional, target node in the tree
outputs:
  - novel.characters[*].backstory
---

# /write-backstory

Write a per-character backstory

## Workflow

1. Load character (id required in input).
2. Invoke `backstory-writer`.
3. Produce 500-1500 words for principals, 150-300 for supporting.
4. Write `novel.characters[?id=<id>].backstory`.

## Mode behavior

- **full**: agent produces deliverable, writes to tree, advances.
- **semi**: agent produces draft + alternatives, pauses for user accept/edit.
- **manual**: agent does not write; offers a brief and waits for the user's input, then validates.

## Owning agent

`backstory-writer` — see `agents/*/$agent.md` for the full role definition.
