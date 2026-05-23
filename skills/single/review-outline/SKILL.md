---
name: review-outline
description: Launch local HTML reviewer for the outline (drag/edit/save before chapter writing starts)
agent: null
mode_default: semi
mode_compatible: [full, semi, manual]
inputs:
  - port: optional, default=7878
  - open_browser: optional, default=true
outputs:
  - novel.outline  (in-place edits from the UI)
  - novel.hooks    (in-place edits from the UI)
---

# /review-outline

Launches a local HTTP server on `http://localhost:7878` that renders the full outline (acts → chapters → beats with all detailed fields) and the hook ledger as an editable page. You can:

- Edit any beat field (facts, location_id, emotions, state_changes, hooks_opened/resolved, length_target, etc.)
- Drag beats to reorder within a chapter, or chapters to reorder within an act
- Delete a beat or chapter
- Add a fresh beat (canonical empty schema) at any position
- Inspect the hook panel: every hook with its opening / resolution beats and current status
- Save back to `novel.json` (atomic write)

This is the user-review checkpoint between Phase 3 (detailed outline) and Phase 4 (parallel chapter writing). Once you click **Done** in the UI, the server shuts down and the workflow engine continues.

## Workflow

1. Validate `novel.outline.acts[*].chapters[*].beats` exists.
2. Run `audit-hooks` first; surface issues in the UI's hook panel.
3. Start `output/outline_reviewer.py --port <port> --novel <tree_path>`.
4. Open the browser (unless `open_browser=false`).
5. Block the workflow until the user clicks **Done** (POST /done; server exits cleanly).

## Mode behavior

- **full**: skips the review — chapter writing starts immediately on the auto-generated outline.
- **semi**: invokes the reviewer; pipeline halts until user signs off.
- **manual**: invokes the reviewer with all beats pre-emptied; user fills them in by hand.

## CLI standalone use

```bash
python orchestrator/runner.py review-outline
# Or directly:
python output/outline_reviewer.py --novel novel.json --port 7878
```
