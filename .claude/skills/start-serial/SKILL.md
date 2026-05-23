---
name: start-serial
type: workflow
description: Bootstrap an infinite-serial novel — ideation + minimal world + protagonist + chapter 1 plan + chapter 1 prose
workflow_yaml: orchestrator/workflows/infinite-serial-bootstrap.yaml
mode_default: semi
---

# /start-serial

Run this once per serial novel to lay the seed. After this, use `/next-chapter` for each new chapter.

## What it does (vs. /full-novel-pipeline)

Unlike the finite pipeline (which plans 12-30 chapters end-to-end before any prose is written), `/start-serial` **does not** pre-plan the future. It establishes only:

1. Ideation: theme, logline, dramatic question, stylistic direction
2. Minimal world bible — only what's needed for chapter 1 (you can grow it organically)
3. Minimal location bible — only locations chapter 1 needs
4. Protagonist + 1-2 supporting characters with voice cards
5. **3-5 initial hooks** (the bait — what drives readers to chapter 2 onwards)
6. Chapter 1 shell + detailed beats + prose

Subplot weaver, full-cast roster, and structure-lead's 3-act outline are **skipped**. In a serial, structure emerges chapter by chapter.

## Workflow

See `orchestrator/workflows/infinite-serial-bootstrap.yaml`.

## After bootstrap

Run `/next-chapter` to plan + write each subsequent chapter. The engine will:

- Reuse the same world / characters / hooks
- Build the planner context from `memory_log` + last N chapters (not the full history)
- Run `/compress-memory` automatically every `chapters_per_compression_check` chapters

## Modes

`/start-serial` honors `--mode <full|semi|manual>` the same way `/full-novel-pipeline` does.
