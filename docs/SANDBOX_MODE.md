# Sandbox Mode

A complete, pre-baked novel pipeline output. Lets anyone explore what the system produces without committing to writing their own novel.

> Note: when used **inside Claude Code** (the primary path), the project does not need an `ANTHROPIC_API_KEY` at all — subagents run inside your CC session. Sandbox mode is therefore not about avoiding an API key; it's about loading pre-baked fixture content so you can inspect every phase's output without running the pipeline. For the **standalone Python orchestrator** path (which does call the Anthropic API directly), sandbox mode also doubles as the fallback when no key is set.

## What it is

*The Trial of Memory* — a ~10,000-word sci-fi short novel, generated end-to-end by the pipeline, with every intermediate artifact stored as a fixture.

**Logline**: In a near-future republic where memory is admissible evidence, a synesthete prosecutor discovers her own missing year is the key to the case she's prosecuting.

**Dramatic question**: Will Lin Wei choose to remember — knowing the cost of remembering?

## How it works

When the orchestrator runs in sandbox mode (`--sandbox` or `ANTHROPIC_API_KEY` unset):

1. `llm_backend.call()` is shimmed: instead of POSTing to the API, it looks up
   `(agent_name, input_hash)` in `sandbox/fixtures/llm_cache.json` and returns
   the cached response.
2. Every node in the tree is filled from pre-baked output.
3. The visual editor labels each node with a `(demo)` tag.

You can:

- **Inspect** any node — see what the agent produced
- **Re-run** any node in sandbox mode (returns the same cached output)
- **Export** the PDF (uses the pre-baked manuscript)

You can NOT, in sandbox mode:

- Generate new text
- Run an agent on input that isn't in the cache
- Change the novel to a different story

## File layout

```
sandbox/
├── demo_novel.json              # the tree, fully populated
├── mock_runtime.py              # the shim that intercepts llm_backend.call()
└── fixtures/
    ├── 00_metadata.json         # title, author, target, mode trace
    ├── 01_ideation.json         # theme, logline, dramatic question, style brief
    ├── 02_world_bible.md        # geography, politics, the Mneme law
    ├── 03_characters.json       # roster + backstories + arc maps
    ├── 04_outline.json          # 3 acts, 12 chapters, beat plan
    ├── 05_chapters/
    │   ├── ch01.md
    │   ├── ch02.md
    │   ...
    │   └── ch12.md
    ├── 06_editorial.json        # critiques, plan, revision diffs
    ├── 07_compiled.pdf          # the final PDF (committed)
    └── llm_cache.json           # the (agent, input) → output map
```

## How the fixtures were generated

In the canonical run, the pipeline was driven by the **all_opus** preset — every agent on `claude-opus-4-7`. Token / dollar budget approximate (Opus 4.7 pricing varies; below uses a typical premium-tier rate):

- Phase 1: ~3k tokens
- Phase 2: ~12k tokens
- Phase 3: ~8k tokens
- Phase 4: ~45k tokens (twelve chapters × ~3.5k tokens each)
- Phase 5: ~10k tokens
- Phase 6: <1k tokens
- **Total**: ~80k tokens, ~$8

The `llm_cache.json` was captured during this run. To regenerate fixtures:

```bash
export ANTHROPIC_API_KEY=sk-ant-...
python orchestrator/runner.py \
  --workflow full-novel-pipeline \
  --novel sandbox/demo_novel_seed.yaml \
  --capture-cache sandbox/fixtures/llm_cache.json
```

This produces fresh fixtures. Old fixtures are preserved by `git`.

## Inspecting the demo

```bash
# CLI walk
python orchestrator/runner.py --sandbox --replay

# Inspect a specific fixture
cat sandbox/fixtures/01_ideation.json | jq .
less sandbox/fixtures/05_chapters/ch06.md

# Open the pre-rendered PDF
open sandbox/fixtures/07_compiled.pdf
```

## Why this story

*The Trial of Memory* was chosen as the demo because:

- **Short** (10k words = ~40 PDF pages, easy to inspect end-to-end)
- **Genre-balanced** (sci-fi premise + courtroom drama + literary prose) — exercises every category of agent
- **Character-driven** (single protagonist with deep arc, exercises character agents)
- **Worldbuilt** (the Mneme law and its synesthete jurists give the worldbuilding agents real work)
- **Structurally clean** (12 chapters, 3-act, easy to follow the structural agents' output)

## Disabling sandbox mode

```bash
export ANTHROPIC_API_KEY=sk-ant-...
# OR set in config/llm_config.yaml
```

The orchestrator will no longer intercept calls. Sandbox fixtures are preserved
but not used.
