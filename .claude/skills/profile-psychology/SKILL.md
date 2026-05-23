---
name: profile-psychology
description: Profile a character's attachment, trauma response, defenses, loops
agent: psychology-profiler
mode_default: semi
mode_compatible: [full, semi, manual]
inputs:
  - node_path: optional, target node in the tree
outputs:
  - novel.characters[*].psychology
---

# /profile-psychology

Profile a character's attachment, trauma response, defenses, loops

## Workflow

1. Load character.backstory + arc.
2. Invoke `psychology-profiler`.
3. Write `novel.characters[?id=<id>].psychology`.

## Mode behavior

- **full**: agent produces deliverable, writes to tree, advances.
- **semi**: agent produces draft + alternatives, pauses for user accept/edit.
- **manual**: agent does not write; offers a brief and waits for the user's input, then validates.

## Owning agent

`psychology-profiler` — see `agents/*/$agent.md` for the full role definition.
