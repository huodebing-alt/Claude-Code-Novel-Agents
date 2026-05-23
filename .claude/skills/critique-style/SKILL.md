---
name: critique-style
description: Prose-level critique with examples and rewrites
agent: style-critic
mode_default: full
mode_compatible: [full, semi, manual]
inputs:
  - node_path: optional, target node in the tree
outputs:
  - novel.quality_reports.style_critique
---

# /critique-style

Prose-level critique with examples and rewrites

## Workflow

1. Load chapter(s) + style brief.
2. Invoke `style-critic`.
3. Provide cliché / adverb / filtering metrics + two worst-passage rewrites.
4. Write `novel.quality_reports.style_critique`.

## Mode behavior

- **full**: agent produces deliverable, writes to tree, advances.
- **semi**: agent produces draft + alternatives, pauses for user accept/edit.
- **manual**: agent does not write; offers a brief and waits for the user's input, then validates.

## Owning agent

`style-critic` — see `agents/*/$agent.md` for the full role definition.
