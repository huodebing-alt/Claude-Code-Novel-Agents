---
name: revise-from-notes
description: Apply an explicit revision plan to text
agent: reviser
mode_default: semi
mode_compatible: [full, semi, manual]
inputs:
  - node_path: optional, target node in the tree
outputs:
  - novel.outline.acts.*.chapters.*.beats.*.text
---

# /revise-from-notes

Apply an explicit revision plan to text

## Workflow

1. Load revision_plan + manuscript.
2. Invoke `reviser`.
3. Apply each revision item in order; track diff.
4. Write revised text + log of changes.

## Mode behavior

- **full**: agent produces deliverable, writes to tree, advances.
- **semi**: agent produces draft + alternatives, pauses for user accept/edit.
- **manual**: agent does not write; offers a brief and waits for user input, then validates.

## Owning agent

`reviser` — see `agents/*/$agent.md` for the full role definition.
