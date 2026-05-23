---
name: profile-author
description: Capture the user's taste (4-question conversation)
agent: author-profile-agent
mode_default: semi
mode_compatible: [full, semi, manual]
inputs:
  - node_path: optional, target node in the tree
outputs:
  - novel.metadata.author_profile
---

# /profile-author

Capture the user's taste (4-question conversation)

## Workflow

1. Invoke `author-profile-agent`.
2. Write `novel.metadata.author_profile`.

## Mode behavior

- **full**: agent produces deliverable, writes to tree, advances.
- **semi**: agent produces draft + alternatives, pauses for user accept/edit.
- **manual**: agent does not write; offers a brief and waits for user input, then validates.

## Owning agent

`author-profile-agent` — see `agents/*/$agent.md` for the full role definition.
