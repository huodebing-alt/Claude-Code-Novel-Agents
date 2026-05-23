---
name: apply-three-act
description: Identify or repair 3-act structure on an existing outline
agent: outline-architect
mode_default: full
mode_compatible: [full, semi, manual]
inputs:
  - node_path: optional, target node in the tree
outputs:
  - novel.outline.acts
---

# /apply-three-act

Identify or repair 3-act structure on an existing outline

## Workflow

1. Load existing outline.
2. Invoke `outline-architect` with focus=three_act_audit.
3. Identify act breaks; recommend restructure if needed.
4. Write outline.grammar=three_act + adjusted act boundaries.

## Mode behavior

- **full**: agent produces deliverable, writes to tree, advances.
- **semi**: agent produces draft + alternatives, pauses for user accept/edit.
- **manual**: agent does not write; offers a brief and waits for the user's input, then validates.

## Owning agent

`outline-architect` — see `agents/*/$agent.md` for the full role definition.
