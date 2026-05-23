---
name: dialogue-polish
type: workflow
description: dialogue-specialist on a flat dialogue passage.
workflow_yaml: orchestrator/workflows/dialogue-polish.yaml
mode_default: semi
---

# /dialogue-polish

dialogue-specialist on a flat dialogue passage.

## Steps

1. Load passage + voice cards
2. write-dialogue (invokes dialogue-specialist)
3. Optional: audit-character-voice on the polished passage
4. Return revised dialogue

## Configuration

Mode is taken from `config/novel_meta.yaml.mode_overrides`; CLI `--mode <full|semi|manual>` overrides config.

Skipping: any step whose target node already exists in the tree is skipped unless `--rerun <step_id>` is passed.

## DAG

See `dialogue-polish.yaml` for the full DAG with dependencies.
