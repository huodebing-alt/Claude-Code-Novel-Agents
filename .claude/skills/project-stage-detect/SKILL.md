---
name: project-stage-detect
description: Detect which phase an existing project is at
agent: welcome-agent
mode_default: full
mode_compatible: [full, semi, manual]
inputs:
  - node_path: optional, target node in the tree
outputs:
  - phase_pointer
---

# /project-stage-detect

Detect which phase an existing project is at

## Workflow

1. Inspect novel.json: which fields are populated?
2. Map populated fields to a phase (1-6).
3. Recommend the next workflow to run.

## Mode behavior

- **full**: agent produces deliverable, writes to tree, advances.
- **semi**: agent produces draft + alternatives, pauses for user accept/edit.
- **manual**: agent does not write; offers a brief and waits for user input, then validates.

## Owning agent

`welcome-agent` — see `agents/*/$agent.md` for the full role definition.
