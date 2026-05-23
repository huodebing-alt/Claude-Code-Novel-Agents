---
name: next-chapter
type: workflow
description: (infinite_serial mode) Plan + write the next chapter; automatically compresses memory when needed
workflow_yaml: orchestrator/workflows/infinite-serial-next-chapter.yaml
mode_default: semi
---

# /next-chapter

The default loop for an infinite-serial novel. Run once per chapter you want to publish.

## Workflow (per chapter)

```
1. Auto-check: is planner context > context_threshold_tokens?
   → if yes, invoke /compress-memory first
   → also runs every chapters_per_compression_check chapters as a safety net

2. /plan-next-chapter (next-chapter-planner)
   → emits the chapter shell (id, POV, location, summary, hooks_to_*)

3. /spawn-hooks (hook-spawner)
   → registers new hooks; balances open-hook count vs. target
   → may park low-priority hooks if surplus

4. /plan-chapter-beats (beat-planner)
   → fills 3-7 detailed beats with the canonical schema
   → references location_id from bible, registers hooks_opened/resolved

5. (semi mode) === USER REVIEW ===
   → /review-outline launches the HTML reviewer on JUST this new chapter
   → user edits / accepts; clicks Done

6. /write-chapter (chapter-writer, parallel-ready but only one chapter here)
   → renders prose using strict context isolation
   → sees bible + own beats + memory_log of older chapters + last 3 chapters' prose

7. /critique-style + /audit-hooks (post-write quality pass on the new chapter)

8. /revise-from-notes (apply chief-editor's notes to this chapter)

9. Format updates: increment current_chapter_count; append chapter to outline.
```

## Output

- A new compiled chapter ready for publication / posting.
- Updated `novel.hooks` (new ones opened, some resolved, some advanced).
- Possibly updated `novel.memory_log` if compaction triggered.
- The chapter is committed to `novel.outline.acts[*].chapters[]`. If you publish chapter-by-chapter, also: `python3 output/pdf_compositor.py --novel novel.json --chapters-from N --chapters-to N` to render just this chapter.

## Modes

- **full**: agents run end-to-end; user reviews the published chapter at the end.
- **semi** (default): user reviews the outline of the new chapter before prose is written.
- **manual**: user writes the chapter; agents only critique / check hooks afterward.

## Compaction-on-the-fly

If during `/plan-next-chapter` the engine sees that the planner's loaded context exceeds `context_threshold_tokens`, it pauses and runs `/compress-memory` first. This is what lets the serial run for thousands of chapters without context bloat.
