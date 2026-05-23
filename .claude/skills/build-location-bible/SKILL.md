---
name: build-location-bible
description: Build the location bible — every place a scene happens, with sensory anchors
agent: location-designer
mode_default: semi
mode_compatible: [full, semi, manual]
inputs:
  - count_target: optional, default=12
outputs:
  - novel.world_bible.locations
---

# /build-location-bible

Build the location bible: 6-12 named locations for a short novel, 15-30 for long. Each location has an `id` (L001, L002, ...), name, description, parent_region, first_appearance_chapter, and five sensory anchors (sight / sound / smell / touch / taste).

## Workflow

1. Load `novel.outline` (if exists) and `novel.world_bible.geography` (if exists).
2. Invoke `location-designer`.
3. Verify every id is unique; every first_appearance_chapter exists in the outline (or is being planned).
4. Write to `novel.world_bible.locations`.

## Mode behavior

- **full**: agent produces the full bible end-to-end.
- **semi**: agent produces draft + alternatives, pauses for user accept/edit per location.
- **manual**: agent suggests a list of locations to design; you fill in the sensory anchors.

## Owning agent

`location-designer` — see `agents/worldbuilding/location-designer.md`.
