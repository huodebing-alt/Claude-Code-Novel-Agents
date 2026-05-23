---
name: calibrate-voice
description: Build or audit a character's voice card
agent: voice-coach
mode_default: semi
mode_compatible: [full, semi, manual]
inputs:
  - node_path: optional, target node in the tree
outputs:
  - novel.characters[*].voice_card
---

# /calibrate-voice

Build or audit a character's voice card

## Workflow

1. If no voice card: invoke voice-coach to build.
2. If voice card exists: invoke voice-coach to audit recent dialogue against it.
3. Write `novel.characters[?id=<id>].voice_card` or quality_reports.voice_drift.

## Mode behavior

- **full**: agent produces deliverable, writes to tree, advances.
- **semi**: agent produces draft + alternatives, pauses for user accept/edit.
- **manual**: agent does not write; offers a brief and waits for the user's input, then validates.

## Owning agent

`voice-coach` — see `agents/*/$agent.md` for the full role definition.
