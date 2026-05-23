---
name: audit-continuity
description: Senior pass: timeline + geography + character-knowledge audit
agent: continuity-director
mode_default: full
mode_compatible: [full, semi, manual]
inputs:
  - node_path: optional, target node in the tree
outputs:
  - novel.quality_reports.continuity_audit
---

# /audit-continuity

Senior pass: timeline + geography + character-knowledge audit

## Workflow

1. Load consistency-checker raw report.
2. Invoke `continuity-director` to synthesize.
3. Write `novel.quality_reports.continuity_audit` with block/warn/clean verdict.

## Mode behavior

- **full**: agent produces deliverable, writes to tree, advances.
- **semi**: agent produces draft + alternatives, pauses for user accept/edit.
- **manual**: agent does not write; offers a brief and waits for the user's input, then validates.

## Owning agent

`continuity-director` — see `agents/*/$agent.md` for the full role definition.
