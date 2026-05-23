---
name: build-world-bible
description: Build the full world bible (orchestrates 5 sub-skills)
agent: worldbuilding-lead
mode_default: full
mode_compatible: [full, semi, manual]
inputs:
  - node_path: optional, target node in the tree
outputs:
  - novel.world_bible
---

# /build-world-bible

Build the full world bible (orchestrates 5 sub-skills)

## Workflow

1. `worldbuilding-lead` triages scope.
2. Dispatches `world-builder` (geo + politics + timeline).
3. Dispatches `magic-system-designer` (if applicable).
4. Dispatches `cultural-anthropologist` (culture).
5. Compiles + prunes to load-bearing entries only.

## Mode behavior

- **full**: agent produces deliverable, writes to tree, advances.
- **semi**: agent produces draft + alternatives, pauses for user accept/edit.
- **manual**: agent does not write; offers a brief and waits for the user's input, then validates.

## Owning agent

`worldbuilding-lead` — see `agents/*/$agent.md` for the full role definition.
