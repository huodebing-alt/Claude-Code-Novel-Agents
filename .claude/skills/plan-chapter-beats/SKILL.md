---
name: plan-chapter-beats
description: For a chapter, generate 3-7 beats with the full detailed schema (facts/location/emotion/state/hooks)
agent: beat-planner
mode_default: semi
mode_compatible: [full, semi, manual]
inputs:
  - chapter_id: required
outputs:
  - novel.outline.acts.*.chapters.*.beats
  - novel.hooks (appended as needed)
---

# /plan-chapter-beats

Produce the detailed beat plan for one chapter. Each beat carries **all eight required fields**:

- `id`, `emotion`, `function`, `length_target`
- `opening_trigger`, `closing_image`
- `facts[]` — atomic {actor, action, object?, detail?} entries
- `location_id` — ref to `world_bible.locations[].id`
- `emotions[]` — per-character {character, emotion}
- `state_changes[]` — {character, before, after}
- `hooks_opened[]` / `hooks_resolved[]` — list of hook ids

## Workflow

1. Load the chapter (id required) and its parent act.
2. Load `world_bible.locations[]` (so beats can reference real location ids).
3. Load `characters[*].arc` (so state_changes reflect arc progression).
4. Load `novel.hooks[]` (registry — beats can reference existing hooks or declare new ones).
5. Invoke `beat-planner`.
6. **Beat-planner quality checks** (auto-run):
   - Every `location_id` exists in the bible.
   - Every `hooks_opened`/`hooks_resolved` is registered (auto-append if not).
   - At least one beat has non-empty `state_changes`.
   - Sum of `length_target` ≈ `chapter.length_target` (±10%).
   - No chapter has all beats with the same emotion.
7. Write `novel.outline.acts.*.chapters[?id=<chapter_id>].beats`.
8. Append/update `novel.hooks[]` as needed.

## Owning agent

`beat-planner` — see `agents/structure/beat-planner.md`.
