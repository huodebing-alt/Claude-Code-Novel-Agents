---
name: apply-save-the-cat
description: Map existing outline to Save the Cat beats
agent: outline-architect
mode_default: full
mode_compatible: [full, semi, manual]
inputs:
  - node_path: optional, target node in the tree
outputs:
  - novel.outline.stc_mapping
---

# /apply-save-the-cat

Map existing outline to Save the Cat beats

## Workflow

1. Load outline.
2. Invoke `outline-architect` with focus=stc_mapping.
3. Place 15 STC beats onto existing chapters; flag missing beats.
4. Write outline.stc_mapping.

## Mode behavior

- **full**: agent produces deliverable, writes to tree, advances.
- **semi**: agent produces draft + alternatives, pauses for user accept/edit.
- **manual**: agent does not write; offers a brief and waits for the user's input, then validates.

## Owning agent

`outline-architect` — see `agents/*/$agent.md` for the full role definition.
