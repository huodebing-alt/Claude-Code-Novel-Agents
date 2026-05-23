---
name: write-dialogue
description: Polish a passage of dialogue to honor voice cards
agent: dialogue-specialist
mode_default: semi
mode_compatible: [full, semi, manual]
inputs:
  - node_path: optional, target node in the tree
outputs:
  - novel.outline.acts.*.chapters.*.beats.*.text[dialogue]
---

# /write-dialogue

Polish a passage of dialogue to honor voice cards

## Workflow

1. Load passage + voice cards for all speakers.
2. Invoke `dialogue-specialist`.
3. Replace generic tags with action beats; honor subtext.
4. Write revised passage.

## Mode behavior

- **full**: agent produces deliverable, writes to tree, advances.
- **semi**: agent produces draft + alternatives, pauses for user accept/edit.
- **manual**: agent does not write; offers a brief and waits for the user's input, then validates.

## Owning agent

`dialogue-specialist` — see `agents/*/$agent.md` for the full role definition.
