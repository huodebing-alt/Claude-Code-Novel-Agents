---
name: character-bible-build
type: workflow
description: Phase 2b only — all character agents in parallel.
workflow_yaml: orchestrator/workflows/character-bible-build.yaml
mode_default: semi
---

# /character-bible-build

Phase 2b only — all character agents in parallel.

## Steps

Parallel:
- design-protagonist
- design-antagonist
- design-supporting-cast
Then per-character (parallel):
- write-backstory
- profile-psychology
- calibrate-voice
Then character-lead audits the constellation for function-overlap.

## Configuration

Mode is taken from `config/novel_meta.yaml.mode_overrides`; CLI `--mode <full|semi|manual>` overrides config.

Skipping: any step whose target node already exists in the tree is skipped unless `--rerun <step_id>` is passed.

## DAG

See `character-bible-build.yaml` for the full DAG with dependencies.
