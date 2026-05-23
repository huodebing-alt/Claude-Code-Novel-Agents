---
name: audit-character-voice
description: Audit dialogue + close-third interior for voice drift
agent: voice-coach
mode_default: full
mode_compatible: [full, semi, manual]
inputs:
  - node_path: optional, target node in the tree
outputs:
  - novel.quality_reports.voice_drift
---

# /audit-character-voice

Audit dialogue + close-third interior for voice drift

## Workflow

1. Load voice cards + chapter dialogue.
2. Invoke `voice-coach` per character.
3. Score drift; flag passages.
4. Write `novel.quality_reports.voice_drift`.

## Mode behavior

- **full**: agent produces deliverable, writes to tree, advances.
- **semi**: agent produces draft + alternatives, pauses for user accept/edit.
- **manual**: agent does not write; offers a brief and waits for the user's input, then validates.

## Owning agent

`voice-coach` — see `agents/*/$agent.md` for the full role definition.
