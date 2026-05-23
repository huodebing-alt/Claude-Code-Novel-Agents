---
name: outline-only
type: workflow
description: Phases 1-3 only. Stops before writing. For writers who do their own prose.
workflow_yaml: orchestrator/workflows/outline-only.yaml
mode_default: semi
---

# /outline-only

Phases 1-3 only. Stops before writing. For writers who do their own prose.

## Steps

1. Ideation
2. Worldbuilding + Characters (parallel)
3. Structure (outline + beat plan)
Result: a complete planning package the user can hand-write from.

## Configuration

Mode is taken from `config/novel_meta.yaml.mode_overrides`; CLI `--mode <full|semi|manual>` overrides config.

Skipping: any step whose target node already exists in the tree is skipped unless `--rerun <step_id>` is passed.

## DAG

See `outline-only.yaml` for the full DAG with dependencies.
