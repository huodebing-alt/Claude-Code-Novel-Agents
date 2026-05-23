<div align="center">

# Claude Code Novel Agents

### The literary counterpart of [Claude Code Game Studios](https://github.com/Donchitos/Claude-Code-Game-Studios)
### 一个由 50 个 AI 智能体协作完成长篇小说和无限连载的多智能体写作工坊

**Turn a single Claude Code session into a full novel atelier.**
**50 agents · 70 skills · 6-phase pipeline · detailed beat planner · hook auditor · HTML outline reviewer · PDF compositor · infinite-serial mode for long-running web-serials.**

[![MIT License](https://img.shields.io/badge/license-MIT-7a1f1f.svg)](LICENSE)
[![50 Agents](https://img.shields.io/badge/agents-50-7a1f1f)](agents/)
[![70 Skills](https://img.shields.io/badge/skills-70-c9a96b)](skills/)
[![6 Phases](https://img.shields.io/badge/phases-6-2c2c2c)](docs/ARCHITECTURE.md)
[![Three Modes](https://img.shields.io/badge/modes-full%20%7C%20semi%20%7C%20manual-2c2c2c)](docs/WORKFLOWS.md)
[![Built for Claude Code](https://img.shields.io/badge/built%20for-Claude%20Code-7a1f1f?logo=anthropic)](https://docs.anthropic.com/en/docs/claude-code)

</div>

> A multi-agent atelier for novelists. Whether you have nothing but a feeling, or a 300-page draft that needs surgery — assemble a roster of specialized agents, hand them the parts you want done, and keep the parts you want to write yourself.

---

## Why this exists

Writing a novel alone with one general-purpose AI is like writing one alone with no AI: you still have to be the protagonist *and* the antagonist, the worldbuilder *and* the line editor, the architect *and* the bricklayer. You burn out at the wrong layer, you patch story holes with prose, you call the climax a midpoint.

Real publishing houses don't work that way. There is a **developmental editor** who never touches a comma, and a **copy editor** who never touches the plot. There is a **continuity reader** whose only job is to remember the eye colour you gave Mei in chapter 2. There is a **brand voice** consultant who never appears in the author bio.

**Claude Code Novel Agents** ports that division of labour into a Claude Code session. Forty-seven named agents, each with a specific seat at the table. Six phases. Three levels of human control. One tree of beats that anyone — human or agent — can rearrange.

You stay the author. The atelier becomes your invisible staff.

---

## Table of Contents

- [What's included](#whats-included)
- [The 6-phase pipeline](#the-6-phase-pipeline)
- [The three modes](#the-three-modes)
- [Studio hierarchy](#studio-hierarchy)
- [The atomic unit is the *beat*](#the-atomic-unit-is-the-beat)
- [Slash commands](#slash-commands)
- [Quick start](#quick-start)
- [Sandbox demo: *The Trial of Memory*](#sandbox-demo-the-trial-of-memory)
- [PDF output](#pdf-output)
- [Project structure](#project-structure)
- [Tech stack](#tech-stack)
- [SEO & discoverability](#seo--discoverability)
- [Acknowledgments](#acknowledgments)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## What's included

| Category | Count | Description |
| --- | --- | --- |
| **Agents** | 50 | Markdown + YAML frontmatter, organized into 10 departments |
| **Skills** | 70 | 54 single-action + 16 workflow skills (slash commands) |
| **Length modes** | 4 | short story · novella · novel · **infinite serial** (web-serial / light-novel pattern; see [docs/INFINITE_SERIAL.md](docs/INFINITE_SERIAL.md)) |
| **Orchestrator** | 1 | Python workflow engine with pluggable LLM backend |
| **Modes** | 3 | Full-auto · Semi-auto · Manual (per step, per agent) |
| **Sandbox demo** | 1 | *The Trial of Memory* — a complete sci-fi short novel, all phases pre-baked |
| **PDF compositor** | 1 | Cover · copyright · TOC · body · blurb, print-ready |
| **Onboarding agents** | 7 | Welcome → Profile → Genre → Goal → API → Sandbox |

---

## The 6-phase pipeline

```
Phase 1 — IDEATION
  Theme Brainstorm  →  Logline  →  Dramatic Question  →  Stylistic Direction

Phase 2 — WORLD & CHARACTERS
  World Bible  →  Location Bible  →  Character Roster  →  Backstory & Bio

Phase 3 — STRUCTURE  (three-pass + hook audit + USER REVIEW)
  3.1  3-act outline (acts, midpoint, climax)
  3.2  Chapter list (one logline + summary + metadata per chapter)
  3.3  Detailed beats per chapter — each beat carries:
         · facts[]          (atomic actor/action/object/detail)
         · location_id      (ref to world_bible.locations[].id)
         · emotions[]       (per-character emotional weather)
         · state_changes[]  (before/after for each affected character)
         · hooks_opened[]   (promises this beat plants)
         · hooks_resolved[] (promises this beat pays off)
  3.4  hook-auditor: verify every hook has both an opening beat and a resolution
  ===  USER REVIEW CHECKPOINT  ===
       Local HTML reviewer (drag-reorder, edit, delete, add)
       → user clicks Done → pipeline continues

Phase 4 — EXECUTION (parallel subagents, strict context isolation)
  One chapter-writer per chapter, in parallel.
  Each writer sees: full bible + full characters + hook ledger + own chapter detail.
  Each writer does NOT see: other chapters' prose (~80% context window saved).

Phase 5 — QUALITY
  Style Critic · Consistency Checker · AI-Voice Detector · Hook Auditor
  → Chief Editor · Reviser

Phase 6 — OUTPUT
  Formatter  →  Cover Brief  →  Blurb  →  PDF Compositor
```

**You can skip any phase.** Already have an outline? Jump to Phase 4. Already have a draft? Run Phase 5 alone for an editorial pass.

See [docs/WORKFLOWS.md](docs/WORKFLOWS.md) for the full DAG and the skip-rules.

### The outline reviewer (the user-review checkpoint between Phase 3 and Phase 4)

After beat-planner has produced detailed beats and hook-auditor has flagged any unclosed promises, the pipeline halts and launches a local HTTP server at `http://localhost:7878`. You see the full outline as an editable tree: acts → chapters → beats with all detailed fields. You can:

- Edit any beat field (facts, location, emotions, state changes, hooks)
- Drag beats to reorder within a chapter (HTML5 drag-drop via SortableJS)
- Delete or insert beats anywhere
- Watch the hook ledger update live in the side panel (verdict: clean / warn / block)
- Save at any time (`Cmd/Ctrl + S`); the file writes atomically to `novel.json`
- Click **Done** to shut the server down and let the chapter-writers start

In `full` mode the review is skipped automatically. In `manual` mode the reviewer launches with all beats pre-emptied for you to fill in by hand.

### Infinite-serial mode (for web-serials and long-running fiction)

If your work is a web-serial, light novel, or any ongoing fiction that grows chapter-by-chapter rather than being pre-planned end-to-end, pick **`infinite_serial`** as the length mode during onboarding. This swaps the finite 6-phase pipeline for a different loop:

```
/start-serial       ← run once: ideation + minimal bible + protagonist +
                                3-5 seed hooks + chapter 1

/next-chapter       ← run per chapter (forever):
                       auto-check: compress memory if context > threshold
                       → plan next chapter (next-chapter-planner)
                       → spawn / balance hooks (hook-spawner)
                       → plan detailed beats
                       → user review (HTML reviewer, scoped to this chapter)
                       → write chapter (with strict context isolation)
                       → quality pass + hook audit
                       → done — N+1 chapters in the can
```

Key adaptations:

- **`next-chapter-planner`** plans only the next chapter, never the rest of the novel.
- **`hook-spawner`** keeps an active-hook population at your target (default 5) — plants new hooks when running low, parks surplus when planted too many.
- **`serial-memory-keeper`** compresses old chapters into `novel.memory_log` entries so the planner's context stays bounded even at chapter 500. Default policy: last 3 full, next 10 as per-chapter summaries, older merged 5-at-a-time. Custom policies supported.
- **Auto-triggered compression** when the planner's loaded context exceeds your configured threshold (default 100,000 tokens).

Full documentation: **[docs/INFINITE_SERIAL.md](docs/INFINITE_SERIAL.md)**.

---

## The three modes

Every step of every phase can run in any of three modes — and you can mix them. Plan the outline yourself, let agents draft chapters, then run the editorial pass full-auto:

| Mode | What the agent does | What you do |
| --- | --- | --- |
| **Full-auto** | Produces the deliverable end-to-end | Review at the end |
| **Semi-auto** | Produces a draft, presents options | Edit, accept, or request another pass |
| **Manual** | Suggests, critiques, checks — but does not write | You write; agents review |

The mode is set per-step in `config/novel_meta.yaml`, or live via the visual editor.

---


## Models · pick your preset at onboarding

Every agent runs on **`claude-opus-4-7`** by default. During `/start` onboarding the `api-config-agent` presents four presets:

| Preset | What runs where | Cost estimate per 80k-word novel |
| --- | --- | --- |
| **all_opus** (default) | Every agent → `claude-opus-4-7` | ~$30-50 |
| **balanced** | Directors + climax chapters → Opus 4.7 · leads + most specialists → Sonnet 4.6 · onboarding + formatter → Haiku 4.5 | ~$8-12 |
| **budget** | Every agent → Sonnet 4.6 | ~$3-5 |
| **custom** | Set the model per tier (director / lead / specialist / onboarding) or per agent (`agent_model_overrides`) | varies |

The preset is recorded in `config/llm_config.yaml`. The orchestrator's `_resolve_model()` resolves at dispatch time:

1. `config.agent_model_overrides["<agent>-<context>"]`  ← most specific (e.g. `chapter-writer-climax`)
2. `config.agent_model_overrides["<agent>"]`
3. `config.models[<tier>]`  ← **user preset wins here**
4. Agent frontmatter (`model:` and `model_overrides`)  ← fallback
5. Global default `claude-opus-4-7`

After onboarding you can hand-edit `config/llm_config.yaml` any time — the engine reloads it per run.

---

## Studio hierarchy

Mirroring [Claude Code Game Studios](https://github.com/Donchitos/Claude-Code-Game-Studios), agents are tiered:

```
Tier 1 — DIRECTORS (Opus 4.7 default)
  chief-editor       creative-director       continuity-director

Tier 2 — DEPARTMENT LEADS (Opus 4.7 default)
  ideation-lead      worldbuilding-lead      character-lead
  structure-lead     writing-lead            quality-lead
  output-lead

Tier 3 — SPECIALISTS (Opus 4.7 default)
  theme-brainstorm   logline-specialist      dramatic-question-coach
  style-director     world-builder           magic-system-designer
  cultural-anthropologist  character-designer  protagonist-specialist
  antagonist-specialist    backstory-writer    psychology-profiler
  voice-coach        outline-architect       beat-planner
  subplot-weaver     chapter-writer          scene-builder
  dialogue-specialist  description-painter   style-critic
  consistency-checker  ai-voice-detector     reviser
  formatter          cover-brief-writer      blurb-writer
  pdf-compositor

Tier 4 — ONBOARDING (Opus 4.7 default)
  welcome-agent      project-setup-agent     author-profile-agent
  genre-selection-agent  manuscript-goal-agent  api-config-agent
  sandbox-mode-agent
```

Full table in [docs/AGENT_CATALOG.md](docs/AGENT_CATALOG.md).

---

## The atomic unit is the *beat*

Everything in this system reduces to a **beat** — a single emotional or narrative unit, typically 200-1500 words. A chapter is a sequence of beats. An act is a sequence of chapters. A novel is a tree.

```
Novel
├── Metadata (title, author, genre, target_pages, target_wordcount, ...)
├── World Bible
├── Character Roster
│   ├── Protagonist
│   ├── Antagonist
│   └── ...
├── Outline
│   ├── Act 1
│   │   ├── Chapter 1
│   │   │   ├── Metadata (POV, location, time, opening_image, midpoint, climax)
│   │   │   ├── Beat 1.1 (emotion, function, length_target)
│   │   │   ├── Beat 1.2
│   │   │   └── ...
│   │   └── Chapter 2
│   ├── Act 2
│   └── Act 3
└── Final Manuscript (compiled output)
```

Every node carries metadata. Whether a beat is written by a human or by a Chapter Writer agent, it lands in the same slot in the same tree.

---

## Slash commands

Type `/` in Claude Code (or use the corresponding skill via the orchestrator):

### Workflows (chained)
`/full-novel-pipeline` · `/outline-only` · `/chapter-revision` · `/character-bible-build` · `/world-bible-build` · `/quality-pass` · `/style-rescue` · `/manuscript-doctor` · `/from-existing-draft` · `/short-story-pipeline` · `/scene-only` · `/dialogue-polish` · `/blurb-and-cover` · `/sandbox-demo`

### Ideation
`/brainstorm-themes` · `/write-logline` · `/draft-dramatic-question` · `/set-stylistic-direction`

### Worldbuilding
`/build-world-bible` · `/design-geography` · `/design-political-system` · `/design-magic-system` · `/design-culture` · `/build-timeline`

### Characters
`/design-protagonist` · `/design-antagonist` · `/design-supporting-cast` · `/write-backstory` · `/profile-psychology` · `/map-character-arc` · `/calibrate-voice`

### Structure
`/draft-outline` · `/apply-three-act` · `/apply-save-the-cat` · `/weave-subplot` · `/analyze-pacing` · `/plan-chapter-beats`

### Writing
`/write-chapter` · `/write-scene` · `/write-dialogue` · `/write-action` · `/write-description`

### Quality
`/check-consistency` · `/audit-continuity` · `/detect-ai-voice` · `/review-pacing` · `/audit-character-voice` · `/hunt-plot-holes` · `/critique-style`

### Editing
`/developmental-edit` · `/line-edit` · `/copy-edit` · `/revise-from-notes`

### Output
`/format-manuscript` · `/write-cover-brief` · `/write-blurb` · `/compile-pdf`

Full catalog in [docs/SKILL_CATALOG.md](docs/SKILL_CATALOG.md).

---

## Quick start

### Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code): `npm install -g @anthropic-ai/claude-code` and signed in (Claude subscription or API key — whatever you already use Claude Code with). **The project itself does NOT need an `ANTHROPIC_API_KEY`** — subagents run inside your existing Claude Code session.
- `pandoc` (optional, for PDF output)
- Python 3.10+ (optional, only if you want to run the standalone Python orchestrator instead of slash commands)

### Use as a Claude Code project

```bash
git clone https://github.com/huodebing-alt/Claude-Code-Novel-Agents.git my-novel
cd my-novel
claude
# Inside Claude Code:
/start
```

`/start` runs the onboarding agents: figures out where you are in the process, what genre you're writing, what your output target is, and which **model preset** you want (`all_opus` default, or `balanced` / `budget` for cost control). **No API key step** — your Claude Code session already has auth.

**Note**: agents and skills are mirrored at `.claude/agents/` and `.claude/skills/` (where Claude Code discovers them) and at root-level `agents/` and `skills/` (where they are organized by department for human browsing).

### Launch the outline reviewer on the sandbox demo (no setup needed)

```bash
python3 orchestrator/runner.py review-outline --novel sandbox/demo_novel.json
# Opens http://localhost:7878 — explore the 12-chapter outline with detailed
# beats and 12 fully-resolved hooks. Pure local Python, no LLM call.
```

### Compile the sandbox demo to PDF

```bash
python3 output/pdf_compositor.py --novel sandbox/demo_novel.json
# Output → manuscripts/the-trial-of-memory.{html,pdf}. No LLM call.
```

### Optional: run the standalone Python orchestrator (only if NOT using Claude Code)

If you want to drive the pipeline from a Python CLI instead of from inside a Claude Code session — for scripting, CI, or just preference — the orchestrator can make API calls directly:

```bash
export ANTHROPIC_API_KEY=sk-ant-...     # only needed for THIS path
cp config/novel_meta.example.yaml config/novel_meta.yaml
cp config/llm_config.example.yaml config/llm_config.yaml
python3 orchestrator/runner.py workflow --workflow full-novel-pipeline --mode semi
```

This is a secondary path. The primary, intended use is **inside Claude Code with slash commands**, where no `ANTHROPIC_API_KEY` is needed.

---

## Sandbox demo: *The Trial of Memory*

A complete short novel (~10,000 words, ~40 PDF pages) generated end-to-end by the pipeline, shipped as fixtures so anyone can see what the system produces without spending a token.

**Logline:** *In a near-future republic where memory is admissible evidence, a synesthete prosecutor discovers her own missing year is the key to the case she's prosecuting.*

**Dramatic question:** *Will Lin Wei choose to remember — knowing the cost of remembering?*

You'll find:

- `sandbox/fixtures/00_metadata.json` — title, author, target wordcount, mode trace
- `sandbox/fixtures/01_ideation.json` — theme, logline, dramatic question, style brief
- `sandbox/fixtures/02_world_bible.md` — geography, politics, the "Mneme" memory-evidence law
- `sandbox/fixtures/03_characters.json` — protagonist, antagonist, supporting cast, full backstories
- `sandbox/fixtures/04_outline.json` — 3 acts, 12 chapters, beat-level granularity
- `sandbox/fixtures/05_chapters/` — 12 written chapters
- `sandbox/fixtures/06_editorial.json` — style critique, consistency audit, chief editor notes, revision diff
- `sandbox/fixtures/07_compiled.pdf` — the final PDF

Run `python orchestrator/runner.py --sandbox --resume-from <step>` to step through.

See [docs/SANDBOX_MODE.md](docs/SANDBOX_MODE.md).

---

## PDF output

Print-ready PDF via Pandoc + HTML/CSS `@page` rules:

- Cover (generated from cover-brief-writer)
- Copyright page
- Table of contents
- Body (Cormorant for body text · Noto Serif SC for Chinese · Inter for metadata)
- Acknowledgments
- Blurb (back-cover paragraph)

Configurable: trim size (5×8 / 5.5×8.5 / 6×9), margins, page numbers, drop caps, chapter-opening style.

```bash
python output/pdf_compositor.py --novel sandbox/fixtures --trim 5.5x8.5 --out my_novel.pdf
```

---

## Project structure

```
claude-code-novel-agents/
├── README.md
├── LICENSE
├── CLAUDE.md                       # Master config: tells Claude Code about the agents
├── .gitignore
│
├── .claude/                        # Claude Code discovery location
│   ├── agents/                     # 45 agents (mirrored from agents/)
│   ├── skills/                     # 62 SKILL.md (mirrored from skills/single + skills/workflows)
│   └── settings.json               # Permissions + allowlist for orchestrator calls
│
├── agents/                         # 45 agents organized by department (for browsing)
│   ├── ideation/
│   ├── worldbuilding/
│   ├── character/
│   ├── structure/
│   ├── writing/
│   ├── quality/
│   ├── editing/
│   ├── output/
│   ├── onboarding/
│   └── orchestrator/
│
├── skills/                         # 62 skills organized by category (for browsing)
│   ├── single/                     # 48 single-action skills
│   └── workflows/                  # 14 chained workflow skills
│
├── orchestrator/                   # Multi-agent coordinator
│   ├── runner.py                   # CLI entrypoint
│   ├── workflow_engine.py          # DAG executor
│   ├── mode_selector.py            # full / semi / manual logic
│   ├── llm_backend.py              # urllib-based Anthropic client (no SDK dep)
│   ├── novel_tree.py               # tree data model + serialization
│   └── workflows/                  # 14 workflow YAML definitions
│
├── sandbox/                        # Demo data + mock LLM
│   ├── demo_novel.json
│   ├── mock_runtime.py
│   └── fixtures/                   # The Trial of Memory, pre-baked
│
├── output/                         # PDF generation
│   ├── pdf_compositor.py
│   ├── template.html
│   └── styles/
│       └── manuscript.css
│
├── config/
│   ├── novel_meta.example.yaml
│   └── llm_config.example.yaml
│
├── docs/
│   ├── ARCHITECTURE.md
│   ├── AGENT_CATALOG.md
│   ├── SKILL_CATALOG.md
│   ├── ONBOARDING.md
│   ├── SANDBOX_MODE.md
│   ├── WORKFLOWS.md
│   ├── DEPLOYMENT.md
│   └── PROMPT_DESIGN.md
│
└── examples/
    ├── full_pipeline_demo.md
    └── chapter_only_demo.md
```

---

## Tech stack

- **Agents/skills**: Markdown + YAML frontmatter (Claude Code native format)
- **Orchestrator**: Python 3.10 + `urllib` (zero pip deps for portability)
- **LLM**: `claude-opus-4-7` for every agent by default; api-config-agent during onboarding offers a "balanced" (Opus/Sonnet/Haiku per tier) or "budget" (all Sonnet) preset; per-agent overrides supported via `config/llm_config.yaml.agent_model_overrides`
- **PDF**: Pandoc + HTML/CSS `@page` (with WeasyPrint / wkhtmltopdf / Chromium fallbacks)
- **Typography**: Cormorant Garamond (Latin body) · Noto Serif SC (CJK body) · Inter (metadata)
- **Palette**: warm ivory `#f7f2e7`, deep oxblood `#7a1f1f`, matte gold `#c9a96b`, charcoal `#2c2c2c`

---

## SEO & discoverability

This project targets the intersection of three search terrains:

- **AI novel writing**: "AI fiction writer", "automated novel writing", "multi-agent storytelling", "AI novelist"
- **Claude Code ecosystem**: "Claude Code agents", "Claude Code skills", "Claude Code plugin", "subagents"
- **Authoring workflow**: "novel outline generator", "Save the Cat beats", "character bible", "writing pipeline"

GitHub topics: `ai-novel-writing` · `multi-agent` · `claude-code` · `claude-code-plugin` · `fiction-writing` · `creative-writing` · `python` · `pandoc` · `weasyprint` · `pdf-generation` · `save-the-cat` · `three-act-structure` · `character-bible` · `worldbuilding` · `claude-agents` · `subagents` · `authoring-tool` · `novel-writing-software` · `ai-fiction-writer` · `ai-storytelling`

---

## Acknowledgments

- [Donchitos/Claude-Code-Game-Studios](https://github.com/Donchitos/Claude-Code-Game-Studios) — the template this project mirrors, ported from game dev to fiction.
- Blake Snyder, *Save the Cat!* — beat grammar that underpins our structure agents.
- Robert McKee, *Story* — the dramatic-question framing in our ideation agents.
- Stephen King, *On Writing* — the AI-voice detector's rubric draws heavily on King's prose anti-patterns.
- The Anthropic team for Claude and Claude Code.

---

## Contributing

Open an issue or PR. Especially welcome:

- New agents for genres we don't cover well (literary, romance, MG, picture book)
- Localizations of the agent prompts (Spanish, French, Japanese, Russian)
- Alternative beat-grammar plug-ins (Dan Harmon's Story Circle, Hero's Journey, Kishōtenketsu)
- Better PDF templates (literary trim sizes, art-book layouts)
- A future web UI (none ships in this repo by design — the orchestrator is CLI/SDK-first)

---

## License

MIT. See [LICENSE](LICENSE).

---

## Citation

```bibtex
@software{claude_code_novel_agents,
  title  = {Claude Code Novel Agents: A Multi-Agent Atelier for Long-Form Fiction},
  author = {huodebing-alt and contributors},
  year   = {2026},
  url    = {https://github.com/huodebing-alt/Claude-Code-Novel-Agents}
}
```
