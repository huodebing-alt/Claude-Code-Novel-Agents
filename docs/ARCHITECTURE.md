# Architecture

## The novel as a tree

Every artifact lives in one tree:

```
Novel
├── metadata: {title, author, genre, target_wordcount, target_pages, mode_overrides, ...}
├── ideation: {theme, logline, dramatic_question, stylistic_direction}
├── world_bible:
│   ├── geography
│   ├── politics
│   ├── magic_or_tech
│   ├── culture
│   ├── timeline
│   └── locations: [Location, ...]                  # NEW (P1)
│         Location = {id: "L001", name, description,
│                     sensory_anchors: {sight, sound, smell, touch, taste},
│                     parent_region, first_appearance_chapter}
├── characters: [Character, ...]
│   Character = {name, role, want, need, lie, ghost, arc, voice_card, backstory, psychology}
├── outline:
│   acts: [Act, Act, Act]
│     Act = {name, summary, central_image, stc_beats, wordcount_target, chapters: [Chapter, ...]}
│     Chapter = {id, title, POV, location_id, time, opening_image, summary, length_target,
│                stc_beats_in_chapter, beats: [Beat, ...]}
│     Beat = {id, emotion, function, length_target, opening_trigger, closing_image,
│             facts: [{actor, action, object?, detail?}],     # NEW (P1) — atomic events
│             location_id,                                     # NEW (P1) — ref to world_bible.locations
│             emotions: [{character, emotion}],                # NEW (P1) — per-character weather
│             state_changes: [{character, before, after}],     # NEW (P1) — character delta
│             hooks_opened: ["H001", ...],                     # NEW (P1) — promises planted
│             hooks_resolved: ["H002", ...],                   # NEW (P1) — promises paid off
│             text}
│   subplots: [...]
├── hooks: [Hook, ...]                                          # NEW (P1) — promise/payoff ledger
│   Hook = {id: "H001", label, kind, opened_at_beat, resolved_at_beat, status}
│   kind ∈ {plot, character, thematic, mystery, foreshadow}
│   status ∈ {open, resolved, abandoned}
├── quality_reports: {style_critique, consistency_audit, ai_voice_score,
│                     hook_audit, chief_editor_letter, revision_plan}
└── manuscript: {compiled_md, compiled_html, pdf_path, cover_brief, blurb}
```

Implemented in `orchestrator/novel_tree.py` (with `empty_tree()`, `empty_beat()`, `empty_hook()`, `empty_location()`, `audit_hooks()`). Serialized as JSON.

## Phase / agent / skill / mode / step-action

Five orthogonal axes:

- **Phase**: 1-6 (ideation → output)
- **Agent**: the actor (47 named)
- **Skill**: the action (65 named)
- **Mode**: full / semi / manual
- **Step action**: `skill` (default — invoke an LLM agent) | `wait_for_review` (block on user review) | `print`

A skill invokes one or more agents to produce output for a specific node. A workflow chains multiple skills with dependency edges and non-LLM action steps.

## Workflow engine

`orchestrator/workflow_engine.py` is a small DAG executor with two important wrinkles:

### Context isolation for `chapter-writer`

Chapter-writer's frontmatter declares `context_isolation: strict`. When the engine dispatches a chapter-writer:

| Context slice | Loaded? |
| --- | --- |
| `world_bible` (geography, politics, magic, culture, timeline, **locations**) | ✓ full |
| `characters` (with voice_card, psychology, arc) | ✓ full |
| `hooks` registry | ✓ full |
| `style_brief` (from ideation) | ✓ |
| **This chapter** (metadata + beats[] with all detailed fields) | ✓ full |
| **Other chapters' detailed beats** | ✗ stripped — only id/title/POV/summary |
| **Other chapters' compiled prose** | ✗ never |

This saves ~80% of context tokens in a 12-chapter novel and lets 12 chapter-writers run in parallel without one polluting another. The trade-off: continuity that matters lives in the bible (location sensory anchors), in voice cards (character speech rules), and in beat `facts`/`hooks_*` (what happened earlier that this chapter must reference) — not in the prose of prior chapters.

### `wait_for_review` step type

A workflow step can declare `action: wait_for_review` instead of `skill: <name>`. When the engine reaches such a step:

- In `full` mode → step is skipped.
- In `semi` mode → engine calls `runner.launch_outline_reviewer()`, which boots a local stdlib `http.server` on `localhost:7878` and opens the browser. The engine blocks until the user clicks Done in the UI (POST /api/done). Then the tree is reloaded from disk (the UI may have edited it) and the next step proceeds.
- In `manual` mode → same as `semi` but the UI launches against a tree with beats pre-emptied.

```python
- id: review_outline
  action: wait_for_review
  params: {port: 7878, open_browser: true}
  depends_on: [hook_audit_pre]
```

### DAG executor

```python
workflow = {
    "name": "full-novel-pipeline",
    "steps": [
        {"id": "outline_acts",      "skill": "draft-outline", "params": {"mode": "act_level"}},
        {"id": "outline_chapters",  "skill": "draft-outline", "params": {"mode": "chapter_level"},
                                     "depends_on": ["outline_acts"]},
        {"id": "beats",             "skill": "plan-chapter-beats", "fan_out": "per_chapter",
                                     "depends_on": ["outline_chapters"]},
        {"id": "hook_audit_pre",    "skill": "audit-hooks", "depends_on": ["beats"]},
        {"id": "review_outline",    "action": "wait_for_review", "depends_on": ["hook_audit_pre"]},
        {"id": "chapters",          "skill": "write-chapter", "fan_out": "per_chapter", "parallelism": 4,
                                     "depends_on": ["review_outline"]},
        ...
    ]
}
```

Steps with `fan_out: per_chapter` are dispatched in parallel (one chapter per call). `depends_on` controls execution order. The engine respects `mode_overrides` from `novel_meta.yaml`.

## Mode selector

`orchestrator/mode_selector.py` resolves the mode for each step:

1. CLI `--mode <full|semi|manual>` flag (applies to all steps)
2. `mode_overrides: { <step_id>: <mode> }` in `config/novel_meta.yaml`
3. The skill's `mode_default`
4. The agent's `mode_default`
5. The workflow's `mode_default`
6. Global default: `semi`

Plus: if `skip: { <step_id>: true }` → `skip`, and if all the skill's declared output nodes already exist in the tree → implicit skip (load existing).

## LLM backend

`orchestrator/llm_backend.py` is a thin wrapper around the Anthropic API using `urllib` only (no pip dep on `anthropic`).

Default model: `claude-opus-4-7` (every agent). Users can opt into a `balanced` (Opus / Sonnet / Haiku per tier) or `budget` (all Sonnet) preset during `/start` onboarding via `api-config-agent`. The engine's `_resolve_model()` honors `config/llm_config.yaml` over agent frontmatter.

## Sandbox mode

When `ANTHROPIC_API_KEY` is unset OR `--sandbox` is passed:

- `llm_backend.call()` returns pre-baked responses from `sandbox/fixtures/llm_cache.json`
- Allows the full pipeline to "run" without spending a token
- Sandbox fixtures are *The Trial of Memory* (~13k-word sci-fi short with 10 locations, 12 hooks, 40 detailed beats)

## File layout (deeper)

```
orchestrator/
├── runner.py              # CLI: workflow / skill / init / review-outline
├── workflow_engine.py     # DAG executor + context isolation + wait_for_review
├── mode_selector.py       # full / semi / manual / skip
├── llm_backend.py         # urllib-based Anthropic client + sandbox shim
├── novel_tree.py          # tree data model + hook audit + factories
├── agent_loader.py        # reads .claude/agents (then agents/) + frontmatter parser
├── skill_loader.py        # reads .claude/skills (then skills/)
└── workflows/             # 14 workflow YAMLs

output/
├── pdf_compositor.py
├── outline_reviewer.py    # NEW (P4): Python stdlib http.server for outline review
├── outline_review.html    # NEW (P4): single-page reviewer UI (vanilla JS + SortableJS CDN)
├── template.html
└── styles/manuscript.css
```

## Extension points

- **Add an agent**: drop `agents/<dept>/<name>.md` and mirror to `.claude/agents/<dept>/<name>.md`.
- **Add a skill**: drop `skills/single/<name>/SKILL.md` and mirror to `.claude/skills/<name>/SKILL.md`.
- **Add a workflow**: drop a YAML in `orchestrator/workflows/`.
- **Add a step action**: edit `workflow_engine.py:execute_workflow` to handle a new `action: <type>`.
- **Change context isolation for an agent**: set `context_isolation: strict` in the agent's frontmatter; the engine's `_build_user_prompt` will respect it.
