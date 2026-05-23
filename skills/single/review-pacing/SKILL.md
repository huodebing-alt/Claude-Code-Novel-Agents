---
name: review-pacing
description: Pacing critique at prose level
agent: style-critic
mode_default: full
mode_compatible: [full, semi, manual]
inputs:
  - node_path: optional, target node in the tree
outputs:
  - novel.quality_reports.pacing_critique
---

# /review-pacing

Pacing critique at prose level

## Workflow

1. Load chapters.
2. Invoke `style-critic` with focus=pacing.
3. Write `novel.quality_reports.pacing_critique`.

## Mode behavior

- **full**: agent produces deliverable, writes to tree, advances.
- **semi**: agent produces draft + alternatives, pauses for user accept/edit.
- **manual**: agent does not write; offers a brief and waits for the user's input, then validates.

## Owning agent

`style-critic` — see `agents/*/$agent.md` for the full role definition.
