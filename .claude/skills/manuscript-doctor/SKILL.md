---
name: manuscript-doctor
type: workflow
description: Diagnostic only: identifies which phase is broken.
workflow_yaml: orchestrator/workflows/manuscript-doctor.yaml
mode_default: semi
---

# /manuscript-doctor

Diagnostic only: identifies which phase is broken.

## Steps

1. Inspect the manuscript for what is present vs. absent (logline, outline, beats, voice cards, etc.)
2. For each phase, score completeness 0-100
3. Identify the earliest weak phase
4. Recommend the targeted workflow to fix it
5. Output: a 1-page diagnosis + workflow recommendation

## Configuration

Mode is taken from `config/novel_meta.yaml.mode_overrides`; CLI `--mode <full|semi|manual>` overrides config.

Skipping: any step whose target node already exists in the tree is skipped unless `--rerun <step_id>` is passed.

## DAG

See `manuscript-doctor.yaml` for the full DAG with dependencies.
