---
name: audit-hooks
description: Verify every hook the story opens has a resolution beat
agent: hook-auditor
mode_default: full
mode_compatible: [full, semi, manual]
inputs: []
outputs:
  - novel.quality_reports.hook_audit
---

# /audit-hooks

Mechanical audit: cross-reference every `hooks_opened` / `hooks_resolved` across all beats against the `novel.hooks` registry. Flag unresolved promises, dangling references, orphan resolutions, out-of-order resolutions.

Run after `beat-planner` (catches outline-level holes) and again after `chapter-writer` (catches hooks that drifted in revision).

## Workflow

1. Walk all beats; build `{hook_id: {opened_at, resolved_at}}` index.
2. Cross-reference with `novel.hooks` registry.
3. Classify each hook: resolved / open / dangling / orphan_resolution / out_of_order.
4. Apply severity: plot+mystery = high, character+thematic = medium, foreshadow = low.
5. Write `novel.quality_reports.hook_audit`.

## Verdict

- `clean`: no high-severity issues
- `warn`: medium issues only
- `block`: at least one unresolved high (plot/mystery left open)

## Owning agent

`hook-auditor` — see `agents/quality/hook-auditor.md`.
