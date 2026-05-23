# Onboarding

The first thing a new user does is run `/start`. The onboarding agents handle the rest. **No `ANTHROPIC_API_KEY` is asked for at any step** — this project runs inside Claude Code, which already has auth.

## The 7 onboarding agents

```
welcome-agent
   ↓
project-setup-agent
   ↓
author-profile-agent ─→ genre-selection-agent ─→ manuscript-goal-agent
   ↓
api-config-agent  (model preset choice — NOT an API key)
   ↓
(first work skill: /brainstorm-themes, /draft-dramatic-question, /plan-chapter-beats, /quality-pass, etc.)

sandbox-mode-agent (separate path — triggered only if user picks "Show me the demo" at welcome)
```

## Welcome flow

`welcome-agent` asks one question:

> Where are you?
>   a. I have nothing — just a feeling, a mood, an image
>   b. I have a logline or a one-line concept
>   c. I have an outline and characters
>   d. I have a draft I want to polish
>   e. I have a finished manuscript that needs an editorial pass

Then routes:

- a → `/brainstorm-themes` (full pipeline)
- b → `/draft-dramatic-question` (skips theme brainstorm)
- c → `/plan-chapter-beats` (skips Phase 1, 2)
- d → `/quality-pass` (Phase 5)
- e → `/manuscript-doctor` (diagnostic first)

## Project setup

`project-setup-agent` creates:

```
config/novel_meta.yaml      # title, author, genre, target_wordcount, mode_overrides
config/llm_config.yaml      # API key (or sandbox flag), model preferences, budget
novel.json                  # the tree, initialized empty
```

It asks the minimum: title (can be "Untitled"), author name, target wordcount.

## Author profile

`author-profile-agent` is conversational. It asks:

- Have you written long-form before? (yes/no/in-progress)
- Three favourite novels (for style anchoring)
- Three writers whose voice you'd like to learn from
- Anything you specifically *don't* want (tropes you hate, formats you avoid)

Stores in `novel.metadata.author_profile`. Used by the writing agents as a
style anchor.

## Genre selection

`genre-selection-agent` confirms genre. If unsure, it asks:

- Setting (contemporary / historical / SF / fantasy / horror)
- Length (short / novella / novel)
- Audience (literary / commercial / YA / MG)
- Mood (light / dark / mixed)

And maps to a genre that determines defaults: STC vs. McKee, average chapter
length, POV conventions, expected world-bible depth.

## Manuscript goal

`manuscript-goal-agent` captures:

- Target wordcount (default by genre)
- Target page count (default by trim size)
- Trim size (5×8 / 5.5×8.5 / 6×9)
- Target audience age range
- Market (trad / indie / personal)

These flow into the PDF compositor's defaults.

## Model preset

`api-config-agent` (legacy name; today it's effectively a *model-preset agent*) handles:

- Picks a model preset: `all_opus` (default, every agent → opus-4-7), `balanced` (Opus for directors + climax / Sonnet for specialists / Haiku for onboarding), `budget` (all Sonnet), or `custom`.
- Optionally records a soft usage cap.
- **Does NOT ask for an `ANTHROPIC_API_KEY`** — the Claude Code session is already authenticated by the user's CC login. The key is only needed for the optional standalone Python orchestrator (`python orchestrator/runner.py`), which is documented separately in `docs/DEPLOYMENT.md`.

Writes `config/llm_config.yaml` and hands off to the first work skill.

## Sandbox mode

Users can also pick "Show me the demo first" at the welcome question. That routes to `sandbox-mode-agent`:

> *The Trial of Memory* is loaded — a 13k-word sci-fi short novel generated
> end-to-end by the pipeline. Every phase's output is in `sandbox/fixtures/`.
> Inspect any chapter, the outline, the editorial report, the compiled PDF.
> When ready to start your own novel, delete or rename `novel.json` and
> run `/start` again.

Sandbox mode is purely about **loading pre-baked content for inspection**. It is unrelated to API key configuration.

## Re-entry

If a user closes their session and comes back, `welcome-agent` detects the
existing `novel.json` and asks:

> You're working on **<title>** (genre: <genre>, words: <current>/<target>).
> Want to continue from where you left off? (last step: <last_step_id>)

Picks up exactly where they stopped.
