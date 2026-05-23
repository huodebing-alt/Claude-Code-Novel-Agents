---
name: world-bible-build
type: workflow
description: Phase 2a only — all worldbuilding agents.
workflow_yaml: orchestrator/workflows/world-bible-build.yaml
mode_default: semi
---

# /world-bible-build

Phase 2a only — all worldbuilding agents.

## Steps

1. worldbuilding-lead triages scope
2. Parallel: design-geography + design-political-system + (design-magic-system if applicable) + design-culture
3. build-timeline last (depends on the others)
4. Prune to load-bearing entries

## Configuration

Mode is taken from `config/novel_meta.yaml.mode_overrides`; CLI `--mode <full|semi|manual>` overrides config.

Skipping: any step whose target node already exists in the tree is skipped unless `--rerun <step_id>` is passed.

## DAG

See `world-bible-build.yaml` for the full DAG with dependencies.
