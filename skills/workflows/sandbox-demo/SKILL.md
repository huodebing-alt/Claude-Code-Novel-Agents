---
name: sandbox-demo
type: workflow
description: Load The Trial of Memory fixtures; replay the full pipeline output without API calls.
workflow_yaml: orchestrator/workflows/sandbox-demo.yaml
mode_default: full
---

# /sandbox-demo

Load *The Trial of Memory* fixtures and walk through the pre-baked output of every phase. No API key required.

## Steps

1. Set `sandbox.enabled = true` (also auto-enabled when `ANTHROPIC_API_KEY` is unset).
2. Copy `sandbox/demo_novel.json` → `novel.json`.
3. Walk the tree: metadata → ideation → world_bible → characters → outline → 12 chapters → quality_reports → manuscript.
4. Optionally re-render the PDF: `python output/pdf_compositor.py --novel sandbox/demo_novel.json`.

## What you can inspect

| Fixture | Content |
| --- | --- |
| `sandbox/fixtures/00_metadata.json` | title, author, target wordcount, mode trace |
| `sandbox/fixtures/01_ideation.json` | theme, logline, dramatic question, style brief |
| `sandbox/fixtures/02_world_bible.md` | geography, politics, the Mneme law |
| `sandbox/fixtures/03_characters.json` | full roster + backstories + voice cards |
| `sandbox/fixtures/04_outline.json` | 3 acts, 12 chapters, beat-level granularity |
| `sandbox/fixtures/05_chapters/ch*.md` | 12 written chapters (~13k words total) |
| `sandbox/fixtures/06_editorial.json` | style critique, consistency audit, chief-editor letter |
| `sandbox/fixtures/07_compiled.pdf` | the final print-ready PDF |

## DAG

See `orchestrator/workflows/sandbox-demo.yaml` for the full DAG.
