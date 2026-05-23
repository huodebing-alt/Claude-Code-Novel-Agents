---
name: chapter-revision
type: workflow
description: One chapter: write → quality → revision plan → rewrite. Loops until clean.
workflow_yaml: orchestrator/workflows/chapter-revision.yaml
mode_default: semi
---

# /chapter-revision

One chapter: write → quality → revision plan → rewrite. Loops until clean.

## Steps

1. write-chapter
2. critique-style + detect-ai-voice + audit-character-voice (parallel)
3. If ai_voice_score > threshold OR consistency_issues > 0:
   - developmental-edit on this chapter
   - revise-from-notes
   - GOTO step 2
4. Else exit clean.

## Configuration

Mode is taken from `config/novel_meta.yaml.mode_overrides`; CLI `--mode <full|semi|manual>` overrides config.

Skipping: any step whose target node already exists in the tree is skipped unless `--rerun <step_id>` is passed.

## DAG

See `chapter-revision.yaml` for the full DAG with dependencies.
