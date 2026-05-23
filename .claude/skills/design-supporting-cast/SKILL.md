---
name: design-supporting-cast
description: Design the supporting cast with function-overlap audit
agent: character-designer
mode_default: semi
mode_compatible: [full, semi, manual]
inputs:
  - node_path: optional, target node in the tree
outputs:
  - novel.characters[?role!=protagonist,antagonist]
---

# /design-supporting-cast

Design the supporting cast with function-overlap audit

## Workflow

1. Load existing protagonist + antagonist.
2. Invoke `character-designer` to add allies / mentors / complicators.
3. Run function-overlap audit; merge or cut redundancies.
4. Write `novel.characters` (supporting roles).

## Mode behavior

- **full**: agent produces deliverable, writes to tree, advances.
- **semi**: agent produces draft + alternatives, pauses for user accept/edit.
- **manual**: agent does not write; offers a brief and waits for the user's input, then validates.

## Owning agent

`character-designer` — see `agents/*/$agent.md` for the full role definition.
