---
name: design-culture
description: Design customs, religion, kinship, calendar, taboos
agent: cultural-anthropologist
mode_default: semi
mode_compatible: [full, semi, manual]
inputs:
  - node_path: optional, target node in the tree
outputs:
  - novel.world_bible.culture
---

# /design-culture

Design customs, religion, kinship, calendar, taboos

## Workflow

1. Invoke `cultural-anthropologist`.
2. Choose 3-5 cultural axes the story will actually use.
3. Identify one defining taboo + one defining ceremony.
4. Write `novel.world_bible.culture`.

## Mode behavior

- **full**: agent produces deliverable, writes to tree, advances.
- **semi**: agent produces draft + alternatives, pauses for user accept/edit.
- **manual**: agent does not write; offers a brief and waits for the user's input, then validates.

## Owning agent

`cultural-anthropologist` — see `agents/*/$agent.md` for the full role definition.
