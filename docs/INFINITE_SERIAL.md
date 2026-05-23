# Infinite Serial Mode

> *For web-serials, light novels, multi-year ongoing fiction. The mode where the story is never "finished" — only the next chapter.*

This mode is for novels that grow chapter-by-chapter rather than being pre-planned end-to-end. Think Royal Road, Wattpad, Substack fiction, qidian-style long-form: works that can run for hundreds or thousands of chapters and millions of words.

## When to pick this mode

Pick `infinite_serial` if **any** of these is true:

- You don't know where the story ends and you're okay with that.
- You publish chapter-by-chapter and want each chapter to plant a fresh hook.
- The work might run for years.
- The cumulative wordcount could exceed 200,000 — long enough that loading "everything you've written so far" into one LLM context becomes a problem.

Pick a finite mode (short story / novella / novel) if:

- You want the story to end at a planned wordcount.
- You want a 3-act outline before any chapter is written.
- You're optimizing for editorial coherence over reader retention chapter-by-chapter.

## How it differs from the finite pipeline

| | Finite pipeline (`/full-novel-pipeline`) | Infinite serial (`/start-serial` + `/next-chapter`) |
| --- | --- | --- |
| Outline scope | All N chapters before any prose | Only the next chapter |
| World bible | Built once, up front | Grown organically chapter-by-chapter |
| Character roster | Full cast designed in Phase 2 | Protagonist + 1-2 supports at bootstrap; new chars introduced as needed |
| Hooks | Planted across the full outline; audit verifies all are resolved by Phase 5 | Steady-state pool of N open hooks; spawner plants new ones each chapter to maintain count |
| Quality phase | Manuscript-wide critique + chief editor letter | Per-chapter quality pass after each `/next-chapter` |
| PDF output | One book | Per-arc / per-volume; user decides when to compile a slice |
| Memory mgmt | Not needed | `serial-memory-keeper` compresses old chapters into `novel.memory_log` as the chapter count grows |

## The two workflows

### `/start-serial` — bootstrap (run once)

```
ideation (theme, logline, dramatic_question, style)
   ↓
minimal world bible + locations + protagonist + voice card
   ↓
spawn 3-5 SEED HOOKS  (the bait — what makes a stranger read chapter 2?)
   ↓
plan chapter 1 + detailed beats
   ↓
USER REVIEW (HTML reviewer on chapter 1 only)
   ↓
write chapter 1
   ↓
critique-style + detect-ai-voice + check-consistency on chapter 1
```

After this, the serial is "live." From here on, every chapter is one `/next-chapter` call.

### `/next-chapter` — the publish loop (run per chapter)

```
0. Auto-check: planner context > threshold?  →  /compress-memory first
1. /plan-next-chapter  →  chapter shell (no beats yet)
2. /spawn-hooks         →  plant new hooks; park surplus
3. /plan-chapter-beats  →  detailed beats (facts / loc / emotion / state / hooks)
4. /audit-hooks         →  verify the new hook bookkeeping is sound
5. USER REVIEW          →  HTML reviewer scoped to THIS chapter
6. /write-chapter       →  prose (chapter-writer with strict context isolation)
7. /critique-style + /detect-ai-voice + /check-consistency + /audit-hooks
8. /revise-from-notes   →  apply any chief-editor notes
9. Report               →  word count, hooks delta, next steps
```

## The three new agents

| Agent | Tier | What it does |
| --- | --- | --- |
| `next-chapter-planner` | 3 (structure) | Plans one chapter at a time given the bible + memory_log + recent chapters + open hooks. Decides what hook to advance, what to open. Outputs a chapter shell. |
| `hook-spawner` | 3 (structure) | Maintains the open-hook population at `hooks_active_target` (default 5). Plants new hooks, parks surplus, dedupes restatements. |
| `serial-memory-keeper` | 3 (quality) | Compresses old chapters into `novel.memory_log` entries. Default policy: keep last 3 chapters full, next 10 as per-chapter summaries, older merged 5-at-a-time. |

All three only activate when `novel.metadata.length_mode == "infinite_serial"`. The standard 47 agents are unchanged.

## The memory log — how the system stays bounded

When you've written 47 chapters, the `next-chapter-planner` does NOT load 47 chapters of prose. Instead:

```
Planner's input context:
├── full bible
├── full character roster (with voice cards)
├── novel.memory_log
│     ├── M001  covers ch01-ch05   (~500 word merged summary)
│     ├── M002  covers ch06-ch10   (~500 word merged summary)
│     ├── M003  covers ch11        (~300 word per-chapter summary)
│     ├── M004  covers ch12        (~300 word per-chapter summary)
│     │   ... 30 more per-chapter entries ...
│     └── M033  covers ch44
├── recent 3 chapters in FULL (ch45, ch46, ch47)
└── all OPEN hooks
```

Total: usually under 50,000 tokens even at chapter 50, under 100,000 at chapter 500 (if `n_chapters_merge` policy is used and merge intervals grow with age).

### Compaction policies

| Policy | What | When to use |
| --- | --- | --- |
| `default` | Last 3 full, next 10 per-chapter summary, older merged every 5 | The recommended baseline. |
| `summary_only` | Every old chapter gets its own summary entry, never merged | Highest fidelity, more tokens. Good up to ~100 chapters. |
| `n_chapters_merge` | All non-recent chapters merged in groups | Lowest tokens. Use for serials that hit 500+ chapters. |
| `custom` | You write a free-form instruction in `compaction_settings.custom_instructions` | Edge cases. The memory keeper executes whatever you write. |

You can switch policies at any time. The memory keeper will re-compact existing entries on its next run if the policy changed.

### When does compaction trigger?

The `/next-chapter` workflow's first step is `compress_check`. It triggers compaction if **either**:

- The estimated planner context > `metadata.serial.context_threshold_tokens` (default 100,000), OR
- `current_chapter_count % chapters_per_compression_check == 0` (default every 5 chapters)

You can also run `/compress-memory` manually any time, with `--policy <name>` to override.

## The hook ledger — kept healthy by the spawner

The serial reader is held by a rolling balance of open promises. The `hook-spawner` keeps the count near `hooks_active_target` (default 5):

- **Deficit** (open count < target − 1) → spawner adds extra hooks beyond what the planner suggested
- **Surplus** (open count > target + 1) → spawner reduces or "parks" (sets `low_priority: true` on) the planner's suggested new hooks
- **Mix discipline** — at any time, an ideal serial has:
  - 1-2 plot hooks (this chapter's engine)
  - 1-2 character hooks (who someone is becoming)
  - 0-1 mystery hooks (unsolved question)
  - 0-1 foreshadow hooks (planted for far later — chapter 100+)

`hook-auditor` runs after every chapter, so you can see at any moment which hooks have been open longest.

## Example: starting a serial

```bash
cd ~/projects/my-serial
claude
```

```
> /start
[welcome-agent] Where are you?
> nothing yet — just an idea about found family in a magical academy

[project-setup-agent] What's the working title?
> Bound

[author-profile-agent] (4-question conversation about your taste)
[genre-selection-agent] confirms genre: cozy / fantasy / web-serial
[manuscript-goal-agent]
  What length is this work?
  [1] Short story  [2] Novella  [3] Novel  [4] Infinite serial
> 4

[manuscript-goal-agent]
  Per-chapter target wordcount? (default 2,500)  > 2000
  Hooks-active target? (default 5)               > 6
  Compression policy?                            > default
  Context threshold for compression prompts?     > 100000
  Check for compression every N chapters?        > 5

[api-config-agent]
  Pick the model preset:
  [1] All Opus 4.7   [2] Balanced   [3] Budget   [4] Custom
> 2

> /start-serial
... runs the bootstrap workflow ...
✓ Chapter 1 published. 5 seed hooks open. Run /next-chapter when ready.
```

For chapter 2 onward:

```
> /next-chapter
... auto-checks context, plans chapter 2, spawns 1-2 new hooks,
... fills beats, opens HTML reviewer on chapter 2, writes prose,
... runs quality pass, reports.
✓ Chapter 2 published. 6 open hooks (1 advanced, 2 new).
```

Run `/next-chapter` once per posting cadence. Run `/compress-memory` whenever you want — usually unnecessary because the engine auto-triggers it.

## Publishing chapters as you go

You can compile any contiguous range of chapters to PDF at any time:

```bash
# Compile chapters 1-20 as a "Volume 1"
python3 output/pdf_compositor.py --novel novel.json --chapters-from ch001 --chapters-to ch020 --out volume1.pdf

# Or compile everything written so far
python3 output/pdf_compositor.py --novel novel.json
```

The PDF compositor respects whatever range you give it; it doesn't care that the novel is still being written.

## Editorial pass on a finished arc

When you reach a natural pause (end of a story arc, e.g. chapter 25), you can run a full quality pass on the arc:

```bash
# Quality pass on chapters 1-25 as if they were a complete novel
python3 orchestrator/runner.py workflow --workflow quality-pass --chapters ch001-ch025
```

The `chief-editor` agent will treat the arc as a unit and write a developmental letter for it.

## Limits / caveats

- **Pre-planning is intentionally minimal.** If you want a 3-act structure pre-built, use `/full-novel-pipeline` instead. The serial is "discovery writing with safety rails."
- **Older chapters are not freely editable.** Once a chapter is compressed into a `memory_log` entry, the planner stops loading its prose. If you go back and rewrite chapter 4 after publishing chapter 40, the memory entry covering chapter 4 is stale — run `/compress-memory --policy <same as before> --rerun-from ch004` to refresh.
- **Voice drift over thousands of chapters is real.** Periodically run `/audit-character-voice` against your voice cards. If the protagonist's voice has drifted, update the card; subsequent chapters will use the new card.

## File reference

- Agents: `agents/structure/next-chapter-planner.md`, `agents/structure/hook-spawner.md`, `agents/quality/serial-memory-keeper.md`
- Skills: `skills/single/{plan-next-chapter,spawn-hooks,compress-memory}/SKILL.md`, `skills/workflows/{start-serial,next-chapter}/SKILL.md`
- Workflows: `orchestrator/workflows/infinite-serial-bootstrap.yaml`, `orchestrator/workflows/infinite-serial-next-chapter.yaml`
- Data model: `novel.metadata.length_mode`, `novel.metadata.serial`, `novel.memory_log` (see `orchestrator/novel_tree.py`)
- Helpers: `serial_recent_chapters()`, `serial_chapters_needing_compaction()`, `serial_planner_context()`, `estimate_planner_context_tokens()`
