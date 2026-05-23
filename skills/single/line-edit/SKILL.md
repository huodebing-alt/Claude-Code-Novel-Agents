---
name: line-edit
description: Sentence-level pass following an explicit plan
agent: reviser
mode_default: semi
mode_compatible: [full, semi, manual]
inputs:
  - node_path: optional, target node in the tree
outputs:
  - novel.outline.acts.*.chapters.*.beats.*.text
---

# /line-edit

Sentence-level pass following an explicit plan

## Workflow

1. Load revision_plan items of type='line'.
2. Invoke `reviser`.
3. Apply diffs surgically; track unified diff.
4. Write back to chapter text + log.

## Mode behavior

- **full**: agent produces deliverable, writes to tree, advances.
- **semi**: agent produces draft + alternatives, pauses for user accept/edit.
- **manual**: agent does not write; offers a brief and waits for user input, then validates.

## Owning agent

`reviser` — see `agents/*/$agent.md` for the full role definition.
