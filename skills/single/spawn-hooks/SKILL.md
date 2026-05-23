---
name: spawn-hooks
description: (infinite_serial mode) Register the next chapter's new hooks; balance the open-hook count against target
agent: hook-spawner
mode_default: semi
mode_compatible: [full, semi, manual]
inputs:
  - next_chapter_shell: required (the output of /plan-next-chapter)
outputs:
  - novel.hooks
---

# /spawn-hooks

Called by the `/next-chapter` workflow between `/plan-next-chapter` and `/plan-chapter-beats`. Can also be run standalone if the user wants to plant a hook without writing a chapter yet.

## Workflow

1. Load `novel.hooks` and `novel.metadata.serial.hooks_active_target`.
2. Compute the current open-hook count (after applying any `hooks_to_resolve` from the next chapter shell).
3. Invoke `hook-spawner` with the shell + counts + target.
4. Append the returned `new_hooks` to `novel.hooks`.
5. Apply any `parked_hooks` (set `low_priority: true` on the named ids).

## Modes

- **full**: spawner decides; engine writes.
- **semi**: present spawner's suggestions; user accepts / edits / cuts.
- **manual**: spawner only suggests; user writes the hook entries by hand.

## Owning agent

`hook-spawner` — see `agents/structure/hook-spawner.md`.
