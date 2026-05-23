# Agent Catalog

47 agents across 10 departments. Each row: name · tier · model · one-line job · primary skills it owns.

> All agents run on `claude-opus-4-7` by default. During `/start` onboarding, `api-config-agent` lets you pick a different preset:
> - **all_opus**: every agent → opus-4-7 (default, highest quality, ~$30-50 per 80k-word novel)
> - **balanced**: Opus for directors + climax chapters, Sonnet for leads/specialists, Haiku for onboarding (~$8-12)
> - **budget**: Sonnet for everything (~$3-5)
> - **custom**: set per tier or per agent

> The model column below shows the *frontmatter default*; the runtime model is the user's config preset unless overridden.

## Tier 1 — Directors (Opus 4.7 by default, 3 agents)

| Agent | Job | Owns |
| --- | --- | --- |
| `creative-director` | Guards the novel's vision — theme, voice, market fit | Approves Phase 1 outputs; arbitrates creative disputes |
| `chief-editor` | Macro pacing, theme depth, market readability | Phase 5 final pass; revision orders |
| `continuity-director` | Hard logical/timeline/character consistency across the whole tree | Approves any cross-chapter change |

## Tier 2 — Department Leads (Opus 4.7 by default, 7 agents)

| Agent | Department | Owns |
| --- | --- | --- |
| `ideation-lead` | Ideation | Phase 1: theme, logline, dramatic question, style |
| `worldbuilding-lead` | Worldbuilding | Phase 2a: world bible (geography, politics, magic/tech, culture, timeline) |
| `character-lead` | Character | Phase 2b: roster, backstories, arcs, voices |
| `structure-lead` | Structure | Phase 3: outline, acts, chapter list, beat planning |
| `writing-lead` | Writing | Phase 4: assigns chapter writers, monitors prose quality |
| `quality-lead` | Quality | Phase 5: dispatches critique agents, compiles report |
| `output-lead` | Output | Phase 6: format, cover brief, blurb, PDF |

## Tier 3 — Specialists (Opus 4.7 by default, 22 agents)

### Ideation

| Agent | Model | Job |
| --- | --- | --- |
| `theme-brainstorm` | Opus 4.7 | Generate 5-10 theme directions from a seed (mood, image, what-if) |
| `logline-specialist` | Opus 4.7 | Compress story into a single 25-word sentence (protagonist, want, obstacle, stakes) |
| `dramatic-question-coach` | Opus 4.7 | Frame the core yes/no question that drives the reader for 300 pages |
| `style-director` | Opus 4.7 | Decide voice (1st/3rd/close/omniscient), tense, register, genre conventions |

### Worldbuilding

| Agent | Model | Job |
| --- | --- | --- |
| `world-builder` | Opus 4.7 | Assembles full world bible from genre + theme; orchestrates specialists below |
| `magic-system-designer` | Opus 4.7 | Hard or soft magic; rules, costs, cultural impact (Sanderson's laws) |
| `cultural-anthropologist` | Opus 4.7 | Customs, food, religion, kinship, calendar, taboos |

### Character

| Agent | Model | Job |
| --- | --- | --- |
| `character-designer` | Opus 4.7 | Roster: how many, what role, what relationship topology |
| `protagonist-specialist` | Opus 4.7 | Want vs. need, lie they believe, ghost, arc shape |
| `antagonist-specialist` | Opus 4.7 | Wound, justification, why their goal collides with the protagonist's |
| `backstory-writer` | Opus 4.7 | Childhood, turning points, syndromes, the secret they'd never tell |
| `psychology-profiler` | Opus 4.7 | Attachment style, MBTI/Big5 if helpful, defense mechanisms, trauma response |
| `voice-coach` | Opus 4.7 | Dialect, idiolect, sentence rhythm — for each named character |

### Structure

| Agent | Model | Job |
| --- | --- | --- |
| `outline-architect` | Opus 4.7 | 3-act outline; identifies act breaks, midpoint, climax, denouement |
| `beat-planner` | Opus 4.7 | Chapter → scenes → beats with emotion/function/length per beat |
| `subplot-weaver` | Opus 4.7 | B and C plots, when they enter, when they intersect main plot |

### Writing

| Agent | Model | Job |
| --- | --- | --- |
| `chapter-writer` | Opus 4.7 (Opus for all chapters by default) | Writes a full chapter from the beat plan |
| `scene-builder` | Opus 4.7 | One scene (multiple beats) — useful when revising or filling a single hole |
| `dialogue-specialist` | Opus 4.7 | Replaces flat dialogue with character-voiced exchange |
| `description-painter` | Opus 4.7 | Sensory rendering of place/object/face when prose is going gray |

### Quality

| Agent | Model | Job |
| --- | --- | --- |
| `style-critic` | Opus 4.7 | Voice consistency, AI tells, purple prose, cliché density |
| `consistency-checker` | Opus 4.7 | Timeline, geography, hair colour, who knows what when |
| `ai-voice-detector` | Opus 4.7 | Flags AI tells (em-dash addiction, "It's not X, it's Y", "delve", "tapestry") |
| `reviser` | Opus 4.7 | Applies a revision plan to text, surgically |

### Output

| Agent | Model | Job |
| --- | --- | --- |
| `formatter` | Opus 4.7 | Smart quotes, em-dash hygiene, chapter numbering, consistent scene breaks |
| `cover-brief-writer` | Opus 4.7 | Brief for a cover designer (or for an AI image gen): mood, palette, focal element |
| `blurb-writer` | Opus 4.7 | Back-cover paragraph (3 sentences: setup, hook, stakes) |
| `pdf-compositor` | Opus 4.7 | Runs the PDF pipeline; not a writer, an executor |

## Tier 4 — Onboarding (Opus 4.7 by default, 7 agents)

| Agent | Job |
| --- | --- |
| `welcome-agent` | First-touch greeting; routes to the right next agent |
| `project-setup-agent` | Creates `config/novel_meta.yaml`, initializes the tree |
| `author-profile-agent` | Captures user's writing experience, taste, references |
| `genre-selection-agent` | Picks/confirms genre, applies genre-conventions defaults |
| `manuscript-goal-agent` | Target wordcount, page count, audience, market |
| `api-config-agent` | Sets up `ANTHROPIC_API_KEY`, model preferences, budget caps |
| `sandbox-mode-agent` | Enables sandbox; explains what's pre-baked vs. live |

---

## Agent file format

Each agent is a single markdown file with YAML frontmatter:

```yaml
---
name: chapter-writer
tier: 3
department: writing
model: claude-opus-4-7
escalates_to: writing-lead
consults: [voice-coach, dialogue-specialist, description-painter]
edits: [novel.outline.acts.*.chapters.*.beats.*.text]
mode_default: semi
---

# Chapter Writer

You are a Chapter Writer in the atelier. Given a beat plan...
```

See `agents/writing/chapter-writer.md` for the full canonical example.

---

## Added in P2 (detailed-beats upgrade)

| Agent | Tier | Department | Job |
| --- | --- | --- | --- |
| `location-designer` | 3 | worldbuilding | Builds the location bible (L001…) with five sensory anchors per location |
| `hook-auditor` | 3 | quality | Verifies every hook the story opens has a resolution beat; runs pre-review and post-write |

These two agents work hand-in-hand with the upgraded `beat-planner` and the new `wait_for_review` step in `full-novel-pipeline.yaml`.
