---
name: style-rescue
type: workflow
description: Loop style-critic → ai-voice-detector → reviser until clean.
workflow_yaml: orchestrator/workflows/style-rescue.yaml
mode_default: semi
---

# /style-rescue

Loop style-critic → ai-voice-detector → reviser until clean.

## Steps

1. critique-style on the target text
2. detect-ai-voice on the target text
3. If clean: exit
4. Else: revise-from-notes (using the critique + detector reports)
5. GOTO 1 (max 3 iterations)

## Configuration

Mode is taken from `config/novel_meta.yaml.mode_overrides`; CLI `--mode <full|semi|manual>` overrides config.

Skipping: any step whose target node already exists in the tree is skipped unless `--rerun <step_id>` is passed.

## DAG

See `style-rescue.yaml` for the full DAG with dependencies.
