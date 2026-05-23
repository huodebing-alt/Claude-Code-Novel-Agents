---
name: detect-ai-voice
description: Score the manuscript for AI tells
agent: ai-voice-detector
mode_default: full
mode_compatible: [full, semi, manual]
inputs:
  - node_path: optional, target node in the tree
outputs:
  - novel.quality_reports.ai_voice_score
---

# /detect-ai-voice

Score the manuscript for AI tells

## Workflow

1. Load all chapter text.
2. Invoke `ai-voice-detector`.
3. Compute per-chapter + overall AI-voice score.
4. Write `novel.quality_reports.ai_voice_score`.

## Mode behavior

- **full**: agent produces deliverable, writes to tree, advances.
- **semi**: agent produces draft + alternatives, pauses for user accept/edit.
- **manual**: agent does not write; offers a brief and waits for the user's input, then validates.

## Owning agent

`ai-voice-detector` — see `agents/*/$agent.md` for the full role definition.
