# Workflows

A workflow is a chain of skills with dependency edges and mode handling. 14 workflows ship with the project.

## The 6 phases

```
Phase 1: Ideation
Phase 2: Worldbuilding + Characters (parallel)
Phase 3: Structure (outline + beats)
Phase 4: Execution (per-chapter writing)
Phase 5: Quality (critique + revision)
Phase 6: Output (format + PDF)
```

Each phase can be entered, exited, or skipped independently.

## /full-novel-pipeline (the headline workflow)

```mermaid
graph TD
  A[/brainstorm-themes/] --> B[/write-logline/]
  B --> C[/draft-dramatic-question/]
  C --> D[/set-stylistic-direction/]
  D --> E[/build-world-bible/]
  D --> F[/design-protagonist/]
  D --> G[/design-antagonist/]
  F --> H[/design-supporting-cast/]
  G --> H
  H --> I[/write-backstory/ × N]
  E --> J[/draft-outline/]
  H --> J
  J --> K[/plan-chapter-beats/ × N chapters]
  K --> L[/write-chapter/ × N chapters]
  L --> M[/critique-style/]
  L --> N[/check-consistency/]
  L --> O[/detect-ai-voice/]
  M --> P[/developmental-edit/]
  N --> P
  O --> P
  P --> Q[/revise-from-notes/ × N chapters]
  Q --> R[/format-manuscript/]
  R --> S[/write-cover-brief/]
  R --> T[/write-blurb/]
  R --> U[/compile-pdf/]
```

Steps marked × N fan out per chapter (or per character).

## Skip rules

The orchestrator checks the tree before running each step. If the node already exists:

| Step | Skips if |
| --- | --- |
| `/brainstorm-themes` | `novel.ideation.theme` exists |
| `/write-logline` | `novel.ideation.logline` exists |
| `/build-world-bible` | `novel.world_bible` exists |
| `/design-protagonist` | A character with `role: protagonist` exists |
| `/draft-outline` | `novel.outline.acts` has ≥3 elements |
| `/plan-chapter-beats` | The chapter has ≥3 beats |
| `/write-chapter` | All beats in the chapter have non-empty `text` |
| `/check-consistency` | Always runs unless explicitly skipped |
| `/compile-pdf` | `novel.manuscript.pdf_path` exists |

You can force a re-run with `--rerun <step_id>`.

## Mode resolution per step

Modes resolve in this priority:

1. `--mode <full|semi|manual>` CLI flag (applies to all steps)
2. `mode_overrides: { <step_id>: <mode> }` in `config/novel_meta.yaml`
3. The skill's `mode_default`
4. The agent's `mode_default`
5. Global default: `semi`

## The 14 workflows

### 1. `/full-novel-pipeline`
All 6 phases. The default for greenfield projects.

### 2. `/short-story-pipeline`
Phase 1 → minimal Phase 2 → Phase 3 (single-act outline) → Phase 4 → Phase 5 → Phase 6.
Target: 3,000-15,000 words.

### 3. `/outline-only`
Phase 1 → 2 → 3. Stops before writing. For writers who do their own prose.

### 4. `/character-bible-build`
All character agents, parallelized. Produces a full roster with backstories.

### 5. `/world-bible-build`
All worldbuilding agents. Produces geography, politics, magic/tech, culture, timeline.

### 6. `/chapter-revision`
For a single chapter: write → quality pass → revision plan → rewrite.
Loops until the AI-voice score < threshold and no consistency issues remain.

### 7. `/from-existing-draft`
Skip Phase 1-4. User pastes a full manuscript. Runs Phase 5 → 6.
A useful diagnostic for writers shopping a finished MS.

### 8. `/quality-pass`
Phase 5 only. Runs style-critic, consistency-checker, ai-voice-detector,
chief-editor, then writes the revision plan (does NOT apply it).

### 9. `/style-rescue`
Loops style-critic → ai-voice-detector → reviser until clean.
For prose that is structurally fine but reads as AI-generated.

### 10. `/manuscript-doctor`
Diagnostic only. Inspects a draft and reports which phase is broken:
"This manuscript has a clear protagonist but no dramatic question; we recommend
re-running /draft-dramatic-question and propagating the change forward."

### 11. `/scene-only`
scene-builder for one scene. Useful for hand-writing while delegating one stuck spot.

### 12. `/dialogue-polish`
dialogue-specialist on a passage. Most useful when prose is fine but dialogue
sounds wooden.

### 13. `/blurb-and-cover`
blurb-writer + cover-brief-writer. For marketing collateral on a finished MS.

### 14. `/sandbox-demo`
Loads The Trial of Memory fixtures and walks the visual editor through them.
No API call required.

## Workflow YAML format

```yaml
name: full-novel-pipeline
description: All 6 phases end-to-end
mode_default: semi
steps:
  - id: ideation_themes
    skill: brainstorm-themes
  - id: ideation_logline
    skill: write-logline
    depends_on: [ideation_themes]
  ...
```

See `orchestrator/workflows/*.yaml` for the canonical files.
