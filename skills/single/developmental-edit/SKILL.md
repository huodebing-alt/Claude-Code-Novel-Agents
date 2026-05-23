---
name: developmental-edit
description: Macro-level edit letter from chief-editor
agent: chief-editor
mode_default: full
mode_compatible: [full, semi, manual]
inputs:
  - node_path: optional, target node in the tree
outputs:
  - novel.quality_reports.chief_editor_letter
---

# /developmental-edit

Macro-level edit letter from chief-editor

## Workflow

1. Load full manuscript + quality reports.
2. Invoke `chief-editor`.
3. Produce the 6-section letter + revision_plan.json.
4. Write `novel.quality_reports.chief_editor_letter` and `.revision_plan`.

## Mode behavior

- **full**: agent produces deliverable, writes to tree, advances.
- **semi**: agent produces draft + alternatives, pauses for user accept/edit.
- **manual**: agent does not write; offers a brief and waits for user input, then validates.

## Owning agent

`chief-editor` — see `agents/*/$agent.md` for the full role definition.
