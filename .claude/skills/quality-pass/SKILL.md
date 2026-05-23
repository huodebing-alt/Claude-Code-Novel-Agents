---
name: quality-pass
type: workflow
description: Phase 5 only — all quality agents, but no revision applied.
workflow_yaml: orchestrator/workflows/quality-pass.yaml
mode_default: semi
---

# /quality-pass

Phase 5 only — all quality agents, but no revision applied.

## Steps

Parallel:
- critique-style
- check-consistency
- audit-continuity
- detect-ai-voice
- audit-character-voice
- hunt-plot-holes
- review-pacing
Then developmental-edit (chief-editor synthesis).
Output: revision_plan.json (not applied).

## Configuration

Mode is taken from `config/novel_meta.yaml.mode_overrides`; CLI `--mode <full|semi|manual>` overrides config.

Skipping: any step whose target node already exists in the tree is skipped unless `--rerun <step_id>` is passed.

## DAG

See `quality-pass.yaml` for the full DAG with dependencies.
