---
name: write-description
description: Render or rewrite a description passage with sensory specificity
agent: description-painter
mode_default: semi
mode_compatible: [full, semi, manual]
inputs:
  - node_path: optional, target node in the tree
outputs:
  - novel.outline.acts.*.chapters.*.beats.*.text[description]
---

# /write-description

Render or rewrite a description passage with sensory specificity

## Workflow

1. Load passage + POV character (voice + psychology).
2. Invoke `description-painter`.
3. One sense per sentence, filtered through POV.
4. Write revised passage.

## Mode behavior

- **full**: agent produces deliverable, writes to tree, advances.
- **semi**: agent produces draft + alternatives, pauses for user accept/edit.
- **manual**: agent does not write; offers a brief and waits for the user's input, then validates.

## Owning agent

`description-painter` — see `agents/*/$agent.md` for the full role definition.
