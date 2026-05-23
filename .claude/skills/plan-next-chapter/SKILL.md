---
name: plan-next-chapter
description: (infinite_serial mode) Plan the chapter shell for the next chapter, given bible + memory_log + recent chapters + open hooks
agent: next-chapter-planner
mode_default: semi
mode_compatible: [full, semi, manual]
inputs: []
outputs:
  - novel.outline.acts.*.chapters[appended]
---

# /plan-next-chapter

Produces the next chapter's shell — id, title, POV, location, summary, opening/closing images, length target, hooks-to-advance/resolve/open — but **does not** fill beats. Beat-planner does that next.

## Workflow

1. Confirm `novel.metadata.length_mode == "infinite_serial"`.
2. Build the planner's context using `orchestrator.novel_tree.serial_planner_context(tree)`.
3. If the context estimate already exceeds `context_threshold_tokens`, prompt the user: *"Context is getting large — run `/compress-memory` first? [Y/n]"*.
4. Invoke `next-chapter-planner`.
5. Append the new chapter shell into the current act's `chapters[]`.
6. Increment `novel.metadata.serial.current_chapter_count`.

## Owning agent

`next-chapter-planner` — see `agents/structure/next-chapter-planner.md`.
