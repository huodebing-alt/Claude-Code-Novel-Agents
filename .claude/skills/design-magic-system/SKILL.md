---
name: design-magic-system
description: Design hard/soft magic or speculative tech: rules, costs, limits
agent: magic-system-designer
mode_default: semi
mode_compatible: [full, semi, manual]
inputs:
  - node_path: optional, target node in the tree
outputs:
  - novel.world_bible.magic_or_tech
---

# /design-magic-system

Design hard/soft magic or speculative tech: rules, costs, limits

## Workflow

1. Invoke `magic-system-designer`.
2. Apply Sanderson's 3 laws; define rules + costs + limits + cultural impact.
3. Write `novel.world_bible.magic_or_tech`.

## Mode behavior

- **full**: agent produces deliverable, writes to tree, advances.
- **semi**: agent produces draft + alternatives, pauses for user accept/edit.
- **manual**: agent does not write; offers a brief and waits for the user's input, then validates.

## Owning agent

`magic-system-designer` — see `agents/*/$agent.md` for the full role definition.
