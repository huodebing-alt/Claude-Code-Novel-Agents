---
name: from-existing-draft
type: workflow
description: User pastes a draft. Skip Phase 1-4. Run Phase 5 → 6.
workflow_yaml: orchestrator/workflows/from-existing-draft.yaml
mode_default: semi
---

# /from-existing-draft

User pastes a draft. Skip Phase 1-4. Run Phase 5 → 6.

## Steps

1. Import draft as flat chapter list (no beats — synthesized after)
2. manuscript-doctor diagnoses which phases are broken
3. critique-style + check-consistency + detect-ai-voice
4. developmental-edit (chief-editor)
5. revise-from-notes
6. format-manuscript → compile-pdf

## Configuration

Mode is taken from `config/novel_meta.yaml.mode_overrides`; CLI `--mode <full|semi|manual>` overrides config.

Skipping: any step whose target node already exists in the tree is skipped unless `--rerun <step_id>` is passed.

## DAG

See `from-existing-draft.yaml` for the full DAG with dependencies.
