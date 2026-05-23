---
name: short-story-pipeline
type: workflow
description: Phases 1, minimal 2, single-act 3, 4, 5, 6. Target: 3k-15k words.
workflow_yaml: orchestrator/workflows/short-story-pipeline.yaml
mode_default: semi
---

# /short-story-pipeline

Phases 1, minimal 2, single-act 3, 4, 5, 6. Target: 3k-15k words.

## Steps

1. Ideation (same as full pipeline, but logline target 15-20 words)
2. Minimal worldbuilding (one-page bible)
3. Single-act outline with 3-7 chapters
4. Per-chapter writing
5. Quality pass
6. Output (PDF; no copyright page for personal use)

## Configuration

Mode is taken from `config/novel_meta.yaml.mode_overrides`; CLI `--mode <full|semi|manual>` overrides config.

Skipping: any step whose target node already exists in the tree is skipped unless `--rerun <step_id>` is passed.

## DAG

See `short-story-pipeline.yaml` for the full DAG with dependencies.
