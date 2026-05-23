---
name: compress-memory
description: (infinite_serial mode) Compress older chapters into novel.memory_log to keep the next-chapter planner's context bounded
agent: serial-memory-keeper
mode_default: semi
mode_compatible: [full, semi, manual]
inputs:
  - policy: optional, overrides metadata.serial.compaction_policy for this run
outputs:
  - novel.memory_log
---

# /compress-memory

Triggered manually by the user OR automatically by the engine when the
planner's loaded context exceeds `metadata.serial.context_threshold_tokens`.

## Workflow

1. Confirm `novel.metadata.length_mode == "infinite_serial"`. Otherwise refuse.
2. Use `orchestrator.novel_tree.serial_chapters_needing_compaction(tree)` to enumerate which chapter ids are ripe.
3. Resolve the compaction policy:
   - CLI / skill input `--policy <name>` (highest priority)
   - `novel.metadata.serial.compaction_policy`
   - default: `default`
4. Invoke `serial-memory-keeper` with the chapter ids + policy + settings.
5. Append the returned entries to `novel.memory_log`.
6. Report: how many chapters compressed, how many memory entries added, before/after estimated planner context tokens.

## Modes

- **full**: compresses without asking.
- **semi**: shows the user the new memory entries before writing back.
- **manual**: agent only emits suggested entries; user copies+edits.

## When this runs

- The user runs `/compress-memory` explicitly.
- The `/next-chapter` workflow runs it implicitly every `metadata.serial.chapters_per_compression_check` chapters, **and** when the live planner context estimate exceeds the threshold.
- The user can force a re-compaction with `--policy n_chapters_merge` to merge older per-chapter entries into bigger blocks.

## Owning agent

`serial-memory-keeper` — see `agents/quality/serial-memory-keeper.md`.
