---
name: analyze-pacing
description: Audit pacing across acts; recommend rebalancing
agent: outline-architect
mode_default: full
mode_compatible: [full, semi, manual]
inputs:
  - node_path: optional, target node in the tree
outputs:
  - novel.quality_reports.pacing_audit
---

# /analyze-pacing

Audit pacing across acts; recommend rebalancing

## Workflow

1. Load outline + chapter wordcount targets.
2. Invoke `outline-architect` with focus=pacing_audit.
3. Identify slow zones, action stacks; recommend cuts/expansions.
4. Write `novel.quality_reports.pacing_audit`.

## Mode behavior

- **full**: agent produces deliverable, writes to tree, advances.
- **semi**: agent produces draft + alternatives, pauses for user accept/edit.
- **manual**: agent does not write; offers a brief and waits for the user's input, then validates.

## Owning agent

`outline-architect` — see `agents/*/$agent.md` for the full role definition.
