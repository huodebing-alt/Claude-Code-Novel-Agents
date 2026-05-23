---
name: write-chapter
description: Write a full chapter from its beat plan
agent: chapter-writer
mode_default: semi
mode_compatible: [full, semi, manual]
inputs:
  - node_path: optional, target node in the tree
outputs:
  - novel.outline.acts.*.chapters.*.beats.*.text
---

# /write-chapter

Write a full chapter from its beat plan

## Workflow

1. Load chapter + beats + world_bible + voice_cards + style_brief.
2. Choose model: Opus for opener/midpoint/climax/finale, else Sonnet.
3. Invoke `chapter-writer`.
4. Self-audit: POV stable, beats land closing images, wordcount within 15%.
5. Write `novel.outline.acts.*.chapters[?id=<id>].beats.*.text`.

## Mode behavior

- **full**: agent produces deliverable, writes to tree, advances.
- **semi**: agent produces draft + alternatives, pauses for user accept/edit.
- **manual**: agent does not write; offers a brief and waits for the user's input, then validates.

## Owning agent

`chapter-writer` — see `agents/*/$agent.md` for the full role definition.
