# Skill Catalog

62 skills total: 48 single-action + 14 workflows. Slash command in left column.

## Workflows (chained, 14)

| Command | Pipeline |
| --- | --- |
| `/full-novel-pipeline` | All 6 phases end-to-end |
| `/short-story-pipeline` | Phase 1 → 4 → 5 → 6 (skips heavy worldbuilding) |
| `/outline-only` | Phase 1 → 2 → 3, stops before writing |
| `/character-bible-build` | Phase 2b only (all character agents) |
| `/world-bible-build` | Phase 2a only (all world agents) |
| `/chapter-revision` | Phase 4 (one chapter) → Phase 5 → Phase 4 (rewrite) |
| `/from-existing-draft` | Phase 5 → 6 starting from a pasted manuscript |
| `/quality-pass` | Phase 5 only (all quality agents in sequence) |
| `/style-rescue` | style-critic → ai-voice-detector → reviser (loop until clean) |
| `/manuscript-doctor` | Diagnostic pass: detects which phase a draft is broken at and recommends |
| `/scene-only` | scene-builder for a single scene from a beat plan |
| `/dialogue-polish` | dialogue-specialist on a passage of flat dialogue |
| `/blurb-and-cover` | blurb-writer + cover-brief-writer for marketing collateral |
| `/sandbox-demo` | Loads The Trial of Memory fixtures, runs the visual editor against them |

## Single-action skills (48)

### Ideation (4)

| Command | Agent | Output |
| --- | --- | --- |
| `/brainstorm-themes` | theme-brainstorm | 5-10 theme directions |
| `/write-logline` | logline-specialist | One 25-word sentence |
| `/draft-dramatic-question` | dramatic-question-coach | A yes/no question that drives the novel |
| `/set-stylistic-direction` | style-director | Voice, tense, POV, register decision |

### Worldbuilding (6)

| Command | Agent | Output |
| --- | --- | --- |
| `/build-world-bible` | world-builder | Full bible (orchestrates 5 below) |
| `/design-geography` | world-builder | Region map + climate + key locations |
| `/design-political-system` | world-builder | Polities, succession, conflict lines |
| `/design-magic-system` | magic-system-designer | Rules, costs, cultural impact |
| `/design-culture` | cultural-anthropologist | Customs, food, religion, calendar |
| `/build-timeline` | world-builder | World history relevant to the plot |

### Character (7)

| Command | Agent | Output |
| --- | --- | --- |
| `/design-protagonist` | protagonist-specialist | Want/need/lie/ghost/arc |
| `/design-antagonist` | antagonist-specialist | Wound/justification/collision |
| `/design-supporting-cast` | character-designer | Roster of named NPCs |
| `/write-backstory` | backstory-writer | Per-character biography |
| `/profile-psychology` | psychology-profiler | Attachment, trauma, defense |
| `/map-character-arc` | protagonist-specialist | Arc beats mapped to outline |
| `/calibrate-voice` | voice-coach | Per-character voice card |

### Structure (6)

| Command | Agent | Output |
| --- | --- | --- |
| `/draft-outline` | outline-architect | 3-act outline with chapter list |
| `/apply-three-act` | outline-architect | Identifies/repairs act breaks |
| `/apply-save-the-cat` | outline-architect | Maps existing outline to STC beats |
| `/weave-subplot` | subplot-weaver | B/C plot interlocked with main |
| `/analyze-pacing` | outline-architect | Pacing audit + repair notes |
| `/plan-chapter-beats` | beat-planner | Per-chapter beat list w/ length targets |

### Writing (5)

| Command | Agent | Output |
| --- | --- | --- |
| `/write-chapter` | chapter-writer | Full chapter from beat plan |
| `/write-scene` | scene-builder | Single scene |
| `/write-dialogue` | dialogue-specialist | Dialogue exchange |
| `/write-action` | scene-builder | Action sequence |
| `/write-description` | description-painter | Sensory passage |

### Quality (7)

| Command | Agent | Output |
| --- | --- | --- |
| `/check-consistency` | consistency-checker | Inconsistency report w/ line refs |
| `/audit-continuity` | consistency-checker | Timeline + geography + character-knowledge audit |
| `/detect-ai-voice` | ai-voice-detector | AI-tell density score + flagged passages |
| `/review-pacing` | style-critic | Pacing critique |
| `/audit-character-voice` | voice-coach | Per-character voice drift report |
| `/hunt-plot-holes` | consistency-checker | Plot-hole list w/ severity |
| `/critique-style` | style-critic | Prose-level critique with examples |

### Editing (4)

| Command | Agent | Output |
| --- | --- | --- |
| `/developmental-edit` | chief-editor | Macro-level edit letter |
| `/line-edit` | reviser | Sentence-level pass |
| `/copy-edit` | formatter | Grammar/punctuation/style-guide pass |
| `/revise-from-notes` | reviser | Applies an explicit revision plan |

### Output (4)

| Command | Agent | Output |
| --- | --- | --- |
| `/format-manuscript` | formatter | Print-ready manuscript file |
| `/write-cover-brief` | cover-brief-writer | Cover designer brief |
| `/write-blurb` | blurb-writer | Back-cover blurb |
| `/compile-pdf` | pdf-compositor | Print-ready PDF |

### Project / onboarding (5)

| Command | Agent | Output |
| --- | --- | --- |
| `/start` | welcome-agent | Routes to the right next agent |
| `/project-stage-detect` | welcome-agent | Detects where you are in the process |
| `/setup-novel` | project-setup-agent | Creates `config/novel_meta.yaml` |
| `/profile-author` | author-profile-agent | Captures your taste |
| `/select-genre` | genre-selection-agent | Picks/confirms genre |

---

## Skill file format

Each skill lives in `skills/<single|workflows>/<command-name>/SKILL.md`:

```yaml
---
name: write-chapter
description: Write a full chapter from a beat plan
agent: chapter-writer
inputs:
  - chapter_id: required
  - mode: optional, default=semi
outputs:
  - novel.outline.acts.*.chapters.*.beats.*.text
mode_compatible: [full, semi, manual]
---

# /write-chapter

Workflow:
1. Load the chapter node from the novel tree
2. Load the world bible, character roster, prior chapters
3. Invoke chapter-writer with the beat plan
4. ...
```

See `skills/single/write-chapter/SKILL.md` for the canonical example.

---

## Added in P3 (detailed-beats upgrade)

| Command | Agent | Output |
| --- | --- | --- |
| `/build-location-bible` | location-designer | `novel.world_bible.locations[]` (8-12 typical) |
| `/audit-hooks`          | hook-auditor     | `novel.quality_reports.hook_audit` (verdict: clean/warn/block) |
| `/review-outline`       | — (tool)         | Launches `http://localhost:7878` for user editing of detailed outline; blocks pipeline until Done |

The upgraded `/plan-chapter-beats` now writes the **canonical beat schema** (facts / location_id / emotions / state_changes / hooks_opened / hooks_resolved) — see `agents/structure/beat-planner.md`.
