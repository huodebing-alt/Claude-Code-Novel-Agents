---
name: copy-edit
description: Grammar / punctuation / style-guide pass
agent: formatter
mode_default: full
mode_compatible: [full, semi, manual]
inputs:
  - node_path: optional, target node in the tree
outputs:
  - novel.manuscript.compiled_md
---

# /copy-edit

Grammar / punctuation / style-guide pass

## Workflow

1. Load full manuscript.
2. Invoke `formatter` (for mechanical) then a copy-edit prompt to `reviser` (for grammar/style-guide).
3. Apply changes inline.
4. Write back to manuscript + log.

## Mode behavior

- **full**: agent produces deliverable, writes to tree, advances.
- **semi**: agent produces draft + alternatives, pauses for user accept/edit.
- **manual**: agent does not write; offers a brief and waits for user input, then validates.

## Owning agent

`formatter` — see `agents/*/$agent.md` for the full role definition.
