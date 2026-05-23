---
name: check-consistency
description: Run a consistency audit on the full manuscript
agent: consistency-checker
mode_default: full
mode_compatible: [full, semi, manual]
inputs:
  - node_path: optional, target node in the tree
outputs:
  - novel.quality_reports.consistency_audit
---

# /check-consistency

Run a consistency audit on the full manuscript

## Workflow

1. Load full tree.
2. Invoke `consistency-checker`.
3. Build facts ledger; detect contradictions.
4. Write `novel.quality_reports.consistency_audit`.

## Mode behavior

- **full**: agent produces deliverable, writes to tree, advances.
- **semi**: agent produces draft + alternatives, pauses for user accept/edit.
- **manual**: agent does not write; offers a brief and waits for the user's input, then validates.

## Owning agent

`consistency-checker` — see `agents/*/$agent.md` for the full role definition.
