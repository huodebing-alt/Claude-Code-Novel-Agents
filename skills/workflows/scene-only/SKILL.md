---
name: scene-only
type: workflow
description: scene-builder for one scene from a beat plan.
workflow_yaml: orchestrator/workflows/scene-only.yaml
mode_default: semi
---

# /scene-only

scene-builder for one scene from a beat plan.

## Steps

1. Load beat range (input)
2. write-scene
3. Optional: detect-ai-voice on output
4. Return revised passage

## Configuration

Mode is taken from `config/novel_meta.yaml.mode_overrides`; CLI `--mode <full|semi|manual>` overrides config.

Skipping: any step whose target node already exists in the tree is skipped unless `--rerun <step_id>` is passed.

## DAG

See `scene-only.yaml` for the full DAG with dependencies.
