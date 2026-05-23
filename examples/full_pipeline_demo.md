# Example: full pipeline run

This is the canonical end-to-end demo. It traces what *The Trial of Memory* —
the sandbox demo — looks like at each pipeline step.

## Phase 1 — Ideation

**Input**: a seed — *"a synesthete prosecutor in a near-future republic."*

**theme-brainstorm** generates ten candidate themes; the recommended is *"memory and complicity."*

**logline-specialist** writes:

> In a republic where memory is admissible evidence, a synesthete prosecutor discovers her own missing year is the key to the case she's prosecuting.

**dramatic-question-coach** writes:

> Will Lin Wei choose to remember — knowing the cost of remembering?

**style-director** brief:

- POV: close third
- Tense: past
- Register: literary, clinical, with synesthete lapses
- Voice anchors: Han Kang (primary), Ishiguro, Ogawa, Anne Carson
- Banned: "delve", "tapestry", filtering verbs, rhetorical questions
- Encouraged: sensory inventory in lieu of explanation; period over comma

**creative-director** signs off on the Phase 1 brief.

## Phase 2 — Worldbuilding & Characters

**world-builder** + **magic-system-designer** + **cultural-anthropologist** compile a minimal bible:

- Geography: one coastal capital, three places (Reader College, Court of Mneme, Eastern Quarter)
- Magic/Tech: the Mneme protocol (memory extraction, 72hr window, synesthete jurists)
- Culture: defining taboo (Reader-touch), defining ceremony (Retirement gowning)
- Timeline: ten events from 2018-2061

**character-designer** rosters five characters: protagonist (Lin Wei), antagonist (Han Bo), mentor (Tao), ally (Mei), ghost (Lin Yan). No function overlaps.

**protagonist-specialist** + **antagonist-specialist** + **backstory-writer** + **psychology-profiler** + **voice-coach** flesh out each.

## Phase 3 — Structure

**outline-architect** drafts a 3-act outline with 12 chapters. **beat-planner** fans out per chapter and produces 3-4 beats each. **subplot-weaver** adds the two subplots: Mei's defection (B) and the father's letter (C).

Total beat-target wordcount: 9,820 (within 2% of the 10k target).

## Phase 4 — Execution

**writing-lead** dispatches **chapter-writer** per chapter. Opus is used for the opener (ch.1), midpoint (ch.6), climax (ch.11), and finale (ch.12); Sonnet for the rest.

The compiled manuscript runs 13,123 words — a hair over target but consistent with the prose density chosen by the style-director.

## Phase 5 — Quality

In parallel:
- **style-critic**: per-chapter metrics on cliché/adverb/filtering density. Two warn-level chapters (5, 9); rest clean.
- **consistency-checker** + **continuity-director**: 0 high, 2 medium issues. Verdict: warn.
- **ai-voice-detector**: manuscript score 11 / clean. Per-chapter range 4-18.
- **voice-coach**: dialogue audit per character — Lin Wei has 4 flagged passages of voice drift; the rest of the cast is in voice.

**chief-editor** writes the 6-section letter. Surgery in order: 4 revisions proposed.

## Phase 6 — Output

**reviser** applies 2 of 4 revisions (user accepted r01 — trim ch.9 — and r03 — add bleed-clarification line to ch.6; declined r02 and r04).

**formatter** applies 8 mechanical passes (smart quotes, em-dash hygiene, scene breaks, etc.).

**cover-brief-writer** produces a brief for an illustrator:
- Mood: cold, intimate, watchful
- Palette: ivory, oxblood, dusty teal, slate, matte gold
- Focal: gloved hand on sealed evidence envelope
- References: *Klara and the Sun*, *The Memory Police*
- Avoid: magnifying glass + gavel

**blurb-writer** produces the back-cover:

> In a near-future republic where memory is admissible evidence, the prosecutor Lin Wei has spent her career not consulting her own past. When a witness's testimony arrives in a synesthetic palette she recognizes as her own, the case turns on a year of her ninth life she has spent twenty-nine years not remembering. To win, she must keep forgetting. To remember, she must lose everything she has built.

**pdf-compositor** renders the print PDF:
- 5.5×8.5 trim
- Cormorant Garamond + Noto Serif SC + Inter
- Cover, copyright, TOC, body with drop caps, blurb, acknowledgments
- ~52 pages

## What this run cost

In the canonical run on Anthropic's API:

| Phase | Tokens (approx) | Notes |
| --- | --- | --- |
| 1 | 3,000 | Mostly Sonnet; one Opus call for director sign-off |
| 2 | 12,000 | Sonnet across worldbuilding + character |
| 3 | 8,000 | Sonnet |
| 4 | 45,000 | Sonnet for 8 chapters + Opus for 4 |
| 5 | 10,000 | Sonnet across critique agents |
| 6 | 2,000 | Mostly Haiku (formatting + PDF) + one Opus (blurb) |
| **Total** | **~80,000** | **~$8 at current rates** |

## Reproducing

```bash
export ANTHROPIC_API_KEY=sk-ant-...
python orchestrator/runner.py \
    --workflow full-novel-pipeline \
    --novel sandbox/demo_novel_seed.yaml \
    --capture-cache sandbox/fixtures/llm_cache.json
```

The `--capture-cache` flag records every (agent, input) → output pair so future
runs in sandbox mode can replay this exact pipeline without spending tokens.
