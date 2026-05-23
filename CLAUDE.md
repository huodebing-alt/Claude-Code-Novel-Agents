# CLAUDE.md — Claude Code Novel Agents

> Master configuration. Claude Code reads this file at session start.

You are working inside **Claude Code Novel Agents**, a multi-agent atelier for writing long-form fiction. This file orients you. The specialized agents in `agents/` do the actual work.

## What this project is

A Claude Code project that turns a single session into a 32-agent fiction-writing studio organized into 10 departments and 6 pipeline phases. The atomic unit is the *beat* (an emotional/narrative unit, 200-1500 words). Beats compose chapters; chapters compose acts; acts compose the novel tree.

## How sessions begin

Run `/start`. The onboarding agents (welcome → project-setup → author-profile → genre → goal → model-preset) figure out:

1. Where the user is — nothing, a feeling, a logline, an outline, a draft, a finished manuscript needing revision
2. What genre and target wordcount
3. Which **model preset** to use (`all_opus` default, or `balanced` / `budget` / `custom` to manage Claude Code usage)
4. Which mode per phase: full-auto / semi-auto / manual

There is **no `ANTHROPIC_API_KEY` step**. This project runs inside Claude Code; the user's CC session already has auth. (An API key would only be needed if the user wants to run the standalone Python orchestrator at `orchestrator/runner.py` — see `docs/DEPLOYMENT.md`.)

Never assume. Always route through `/start` for new sessions, or jump directly to a specific skill if the user knows what they want.

## The collaboration protocol (binding for all agents)

Every agent in this project follows this protocol. Do not break it:

1. **Ask** — clarify before proposing. Agents ask 2-4 specific questions before doing real work.
2. **Present options** — when there are multiple defensible directions, show 2-4 with pros/cons.
3. **The user decides** — agents never make a binding creative or structural choice without sign-off.
4. **Draft, then approve** — show work in progress before finalizing.
5. **Stay in lane** — agents only edit files in their domain. Cross-domain changes route through `chief-editor` (creative) or `continuity-director` (structural).

## Tiering and delegation

```
Directors (Opus 4.7 by default)        : creative vision, final approval
   ↓
Department Leads (Opus 4.7 by default): own a phase, coordinate specialists
   ↓
Specialists (Opus 4.7 by default): atomic skills
```

- Vertical delegation: leads delegate to specialists.
- Horizontal consultation: same-tier agents can consult but cannot bind each other.
- Conflict resolution: escalate to the shared parent director.

## The mode system

Every step can run in one of three modes (configurable per phase, per step, per agent):

- **Full-auto**: agent produces deliverable end-to-end; user reviews at the end.
- **Semi-auto**: agent produces a draft + alternatives; user edits or accepts.
- **Manual**: agent only suggests, critiques, checks. User writes.

If the user does not specify a mode, default to **semi-auto** for all writing/structure agents and **full-auto** for quality/onboarding agents.

## The skip system

Any phase or step can be skipped. If a user has:

- A logline → skip ideation
- A world bible → skip worldbuilding
- A character roster → skip character phase
- An outline → skip structure
- A draft → skip to Phase 5 (quality)
- A revised manuscript → skip to Phase 6 (output)

Use `/project-stage-detect` to figure out where to start.

## Tree-first thinking

Every artifact lives in the **novel tree** (`novel_tree.py`):

```
Novel
  metadata (title, author, genre, target_wordcount, mode_overrides, ...)
  ├── world_bible
  ├── characters[]
  ├── outline
  │   acts[]
  │     chapters[]
  │       metadata (POV, location, time, opening_image, midpoint, climax_beat)
  │       beats[]
  │         metadata (emotion, function, length_target, mode)
  │         text
  └── manuscript (compiled)
```

When an agent produces output, it writes to a specific node. Always think of yourself as editing a node, not a file.

## Files agents may touch

| Agent family | Editable paths |
| --- | --- |
| ideation | `novel.metadata`, `novel.ideation` |
| worldbuilding | `novel.world_bible.*` |
| character | `novel.characters[*]` |
| structure | `novel.outline.*` (acts, chapters, beats — structural only) |
| writing | `novel.outline.acts[*].chapters[*].beats[*].text` |
| quality | read-only on tree, writes to `novel.quality_reports.*` |
| editing | applies diffs to `*.text` based on quality reports |
| output | `novel.manuscript`, `manuscripts/*.pdf` |
| onboarding | `config/novel_meta.yaml`, `config/llm_config.yaml` |

Agents that touch files outside their lane must request delegation through a director.

## Sandbox mode

Sandbox mode loads the pre-baked demo (*The Trial of Memory*) instead of generating a new novel. Useful for exploring what the pipeline produces. Triggered by the user picking the "Show me the demo first" option at the welcome prompt, or by running `python3 orchestrator/runner.py review-outline --novel sandbox/demo_novel.json`.

Sandbox mode is unrelated to API keys. **There is no API key step for the Claude Code path** — subagents run inside the user's CC session. An `ANTHROPIC_API_KEY` is only relevant for the optional standalone Python orchestrator path; in that case, when the key is missing, the orchestrator falls back to fixtures from `sandbox/fixtures/llm_cache.json` so the pipeline can still "run" without spending tokens.

## PDF output

`output/pdf_compositor.py` reads the manuscript node and renders to PDF via Pandoc + HTML/CSS. Cover, copyright, TOC, body, blurb. Cormorant + Noto Serif SC + Inter. Palette: ivory `#f7f2e7`, oxblood `#7a1f1f`, gold `#c9a96b`, charcoal `#2c2c2c`.

## Style baseline (project-wide voice)

Even when agents are not actively writing prose, project-wide outputs (commentary, critiques, briefs) should be:

- **Specific over vague** ("Mei's eyes go from grey to grey-green in chapter 4" not "watch the eye colour")
- **Concrete over abstract** (cite line numbers, page numbers, beat IDs)
- **Constructive over judgmental** (every critique includes a suggested fix)
- **Restrained in formatting** (prose over bullets, unless the user asks otherwise)

## Engaging the user

This is a collaborative atelier, not a content factory. Treat the user as the author. Ask them what they want to write next. Surface options. Defer to their taste. Provide the structure that lets their voice survive the pipeline.
