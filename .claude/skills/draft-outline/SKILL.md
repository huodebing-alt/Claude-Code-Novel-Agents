---
name: draft-outline
description: Draft the 3-act outline with chapter list
agent: outline-architect
mode_default: semi
mode_compatible: [full, semi, manual]
inputs:
  - node_path: optional, target node in the tree
outputs:
  - novel.outline.acts
---

# /draft-outline

Draft the 3-act outline with chapter list

## Workflow

1. Load ideation + characters + world_bible.
2. Invoke `outline-architect`.
3. Verify sizing: sum(chapter.length_target) ≈ target_wordcount.
4. Write `novel.outline.acts`.

## Mode behavior

- **full**: agent produces deliverable, writes to tree, advances.
- **semi**: agent produces draft + alternatives, pauses for user accept/edit.
- **manual**: agent does not write; offers a brief and waits for the user's input, then validates.

## Owning agent

`outline-architect` — see `agents/*/$agent.md` for the full role definition.
