---
name: blurb-and-cover
type: workflow
description: Marketing collateral for a finished manuscript.
workflow_yaml: orchestrator/workflows/blurb-and-cover.yaml
mode_default: semi
---

# /blurb-and-cover

Marketing collateral for a finished manuscript.

## Steps

Parallel:
- write-blurb
- write-cover-brief
Then: format-manuscript (if not done) + present both artifacts.

## Configuration

Mode is taken from `config/novel_meta.yaml.mode_overrides`; CLI `--mode <full|semi|manual>` overrides config.

Skipping: any step whose target node already exists in the tree is skipped unless `--rerun <step_id>` is passed.

## DAG

See `blurb-and-cover.yaml` for the full DAG with dependencies.
