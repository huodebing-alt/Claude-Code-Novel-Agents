# Example: chapter-only revision

When you already have a chapter draft and want the atelier to perform one
revision cycle, use `/chapter-revision`.

## Setup

You have a chapter draft. You drop it into the tree at the chapter's beat
texts (or as a single `compiled_text` block on the chapter node).

```bash
python orchestrator/runner.py skill --skill write-chapter \
    --novel my_novel.json --chapter ch04 --mode manual
```

In manual mode the chapter-writer does NOT write — it loads the chapter as
given and proceeds to quality.

## What runs

```
write-chapter (manual; loads existing draft)
   ↓
critique-style + detect-ai-voice + audit-character-voice + check-consistency (parallel)
   ↓
developmental-edit (scoped to single chapter)
   ↓
revise-from-notes
   ↓
(if ai_voice_score still > threshold or high_severity > 0)
   loop back to critique, max 3 iterations
```

## Example output diff

For *Trial of Memory* chapter 4, the revision agent applied two changes:

```diff
@@ ch04.b02 @@
-She felt the cold of the marble bench pressing through her coat.
+The cold of the marble pressed through her coat.

@@ ch04.b03 @@
-Of course, the truth was not just complicated — it was a tapestry of lies she could now delve into.
+The truth was complicated. She had spent a year not looking at it. She could begin to look.
```

The first change drops the filtering verb ("she felt"). The second kills three AI tells at once: "of course" opener, "not just X — it's Y" construction, "delve" + "tapestry."

The AI-voice score drops from 18 (warn) to 6 (clean). The chapter exits the loop.

## When this workflow shines

- You have a draft chapter you're not happy with but can't name why
- The chapter "reads as AI" without you being able to point to specific lines
- The chapter contradicts an earlier chapter and you don't know which one
- You want to keep your prose voice but improve mechanics

It does not shine when:

- The chapter has a structural problem (wrong scene order, missing beat). Run `/plan-chapter-beats --rerun ch04` first.
- The chapter is in the wrong voice for the novel. Run `/calibrate-voice` first.
