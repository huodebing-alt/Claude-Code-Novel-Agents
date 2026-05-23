---
name: set-stylistic-direction
description: Decide POV, tense, register, density, banned/encouraged moves
agent: style-director
mode_default: semi
mode_compatible: [full, semi, manual]
inputs:
  - node_path: optional, target node in the tree
outputs:
  - novel.ideation.stylistic_direction
---

# /set-stylistic-direction

Decide POV, tense, register, density, banned/encouraged moves

## Workflow

1. Load `novel.ideation.*` and `novel.metadata.style.*`.
2. Invoke `style-director`.
3. Present 3 sample paragraphs of the same scene in different registers.
4. User picks; write to `novel.ideation.stylistic_direction`.

## Mode behavior

- **full**: agent produces deliverable, writes to tree, advances.
- **semi**: agent produces draft + alternatives, pauses for user accept/edit.
- **manual**: agent does not write; offers a brief and waits for the user's input, then validates.

## Owning agent

`style-director` — see `agents/*/$agent.md` for the full role definition.
