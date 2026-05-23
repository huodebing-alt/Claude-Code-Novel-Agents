---
name: full-novel-pipeline
type: workflow
description: All 6 phases end-to-end. The headline workflow.
workflow_yaml: orchestrator/workflows/full-novel-pipeline.yaml
mode_default: semi
---

# /full-novel-pipeline

All 6 phases end-to-end. The headline workflow.

## Steps

1. Ideation (brainstorm-themes → write-logline → draft-dramatic-question → set-stylistic-direction)
2. Worldbuilding (build-world-bible — fans out to geo/politics/magic/culture/timeline)
3. Characters (design-protagonist + design-antagonist + design-supporting-cast → write-backstory × N → calibrate-voice × N)
4. Structure (draft-outline → plan-chapter-beats × N → weave-subplot)
5. Writing (write-chapter × N chapters, fan-out parallelized; Opus for opener/midpoint/climax/finale, Sonnet for others)
6. Quality (critique-style + check-consistency + detect-ai-voice + developmental-edit → revise-from-notes × N)
7. Output (format-manuscript → write-cover-brief + write-blurb → compile-pdf)

## Configuration

Mode is taken from `config/novel_meta.yaml.mode_overrides`; CLI `--mode <full|semi|manual>` overrides config.

Skipping: any step whose target node already exists in the tree is skipped unless `--rerun <step_id>` is passed.

## DAG

See `full-novel-pipeline.yaml` for the full DAG with dependencies.
