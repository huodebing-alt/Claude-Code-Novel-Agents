---
name: draft-dramatic-question
description: Frame the dramatic question the novel answers
agent: dramatic-question-coach
mode_default: semi
mode_compatible: [full, semi, manual]
inputs:
  - node_path: optional, target node in the tree
outputs:
  - novel.ideation.dramatic_question
---

# /draft-dramatic-question

Frame the dramatic question the novel answers

## Workflow

1. Load `novel.ideation.{theme, logline}`.
2. Invoke `dramatic-question-coach`.
3. Present; user picks phrasing.
4. Write `novel.ideation.dramatic_question`.

## Mode behavior

- **full**: agent produces deliverable, writes to tree, advances.
- **semi**: agent produces draft + alternatives, pauses for user accept/edit.
- **manual**: agent does not write; offers a brief and waits for the user's input, then validates.

## Owning agent

`dramatic-question-coach` — see `agents/*/$agent.md` for the full role definition.
