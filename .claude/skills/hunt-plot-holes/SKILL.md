---
name: hunt-plot-holes
description: Find plot holes with severity ranking
agent: consistency-checker
mode_default: full
mode_compatible: [full, semi, manual]
inputs:
  - node_path: optional, target node in the tree
outputs:
  - novel.quality_reports.plot_holes
---

# /hunt-plot-holes

Find plot holes with severity ranking

## Workflow

1. Load outline + chapter text.
2. Invoke `consistency-checker` with focus=plot_logic.
3. Rank by severity (story-blocker vs. nitpick).
4. Write `novel.quality_reports.plot_holes`.

## Mode behavior

- **full**: agent produces deliverable, writes to tree, advances.
- **semi**: agent produces draft + alternatives, pauses for user accept/edit.
- **manual**: agent does not write; offers a brief and waits for the user's input, then validates.

## Owning agent

`consistency-checker` — see `agents/*/$agent.md` for the full role definition.
