---
name: start
description: Entry point — figure out where the user is and route
agent: welcome-agent
mode_default: full
mode_compatible: [full, semi, manual]
inputs:
  - node_path: optional, target node in the tree
outputs:
  - next_agent_pointer
---

# /start

Entry point — figure out where the user is and route

## Workflow

1. Detect existing novel.json.
2. If exists: invoke `welcome-agent` with resume mode.
3. If new: invoke `welcome-agent` to ask the routing question.
4. Hand off to the appropriate next agent/skill.

## Mode behavior

- **full**: agent produces deliverable, writes to tree, advances.
- **semi**: agent produces draft + alternatives, pauses for user accept/edit.
- **manual**: agent does not write; offers a brief and waits for user input, then validates.

## Owning agent

`welcome-agent` — see `agents/*/$agent.md` for the full role definition.
