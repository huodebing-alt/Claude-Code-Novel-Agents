---
name: setup-novel
description: Initialize config and empty tree
agent: project-setup-agent
mode_default: full
mode_compatible: [full, semi, manual]
inputs:
  - node_path: optional, target node in the tree
outputs:
  - config/novel_meta.yaml
---

# /setup-novel

Initialize config and empty tree

## Workflow

1. Invoke `project-setup-agent`.
2. Write config/novel_meta.yaml + novel.json (empty tree).

## Mode behavior

- **full**: agent produces deliverable, writes to tree, advances.
- **semi**: agent produces draft + alternatives, pauses for user accept/edit.
- **manual**: agent does not write; offers a brief and waits for user input, then validates.

## Owning agent

`project-setup-agent` — see `agents/*/$agent.md` for the full role definition.
