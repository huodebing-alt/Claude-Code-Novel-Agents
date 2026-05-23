"""Novel tree data model — the single source of truth.

The novel is a tree. Every artifact lives at a stable dotted path.
Serialized as JSON for both UI and orchestrator consumption.

Schema (informal):
    novel
      metadata: {title, author, genre, target_wordcount, target_pages, ...}
      ideation: {theme, logline, dramatic_question, stylistic_direction}
      world_bible: {geography, politics, magic_or_tech, culture, timeline}
      characters: [Character, ...]
      outline:
        grammar: str
        acts: [Act, ...]
          chapters: [Chapter, ...]
            beats: [Beat, ...]
        subplots: [Subplot, ...]
      quality_reports: {style_critique, consistency_audit, ai_voice_score, ...}
      manuscript: {compiled_md, compiled_html, pdf_path, cover_brief, blurb}
"""
from __future__ import annotations

import json
import os
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any, Iterator


def empty_tree(title: str = "Untitled", author: str = "Anonymous", target_wordcount: int = 80000) -> dict:
    """Build a fresh empty novel tree."""
    return {
        "metadata": {
            "title": title,
            "author": author,
            "genre": "",
            "length_mode": "novel",      # "short_story" | "novella" | "novel" | "infinite_serial"
            "target_wordcount": target_wordcount,
            "target_pages": max(1, target_wordcount // 240),
            "trim_size": "5.5x8.5",
            "style": {},
            "author_profile": {},
            "mode_overrides": {},
            # Serial mode block — only active when length_mode == "infinite_serial".
            # Ignored otherwise. See docs/INFINITE_SERIAL.md.
            "serial": {
                "enabled": False,
                "current_chapter_count": 0,
                "chapter_target_words": 2500,           # words per published chapter
                "hooks_active_target": 5,                # recommended open hooks at any time
                "chapters_per_compression_check": 5,    # check memory size every N chapters
                "context_threshold_tokens": 100000,     # auto-suggest compress above this
                "compaction_policy": "default",         # default | summary_only | n_chapters_merge | custom
                "compaction_settings": {
                    "keep_recent_full": 3,              # last N chapters keep full text
                    "keep_medium_summary": 10,          # next N chapters compressed to per-chapter summary
                    "merge_distant_every": 5,           # older chapters merged N-at-a-time into one memory entry
                    "custom_instructions": "",
                },
            },
        },
        "ideation": {
            "theme": None,
            "logline": None,
            "dramatic_question": None,
            "stylistic_direction": None,
        },
        "world_bible": {
            "geography": None,
            "politics": None,
            "magic_or_tech": None,
            "culture": None,
            "timeline": None,
            "locations": [],   # [{id: "L001", name, description, sensory_anchors, parent_region}]
        },
        "characters": [],
        "outline": {
            "grammar": None,
            "acts": [],
            "subplots": [],
        },
        # Hook ledger — every promise the story opens, and where it pays off.
        # [{id: "H001", label, kind, opened_at_beat, resolved_at_beat, status}]
        # status: "open" | "resolved" | "abandoned"
        "hooks": [],
        # Memory log — used by infinite_serial mode to keep the next-chapter
        # planner's context bounded. As the chapter count grows, older chapters
        # are compressed by the serial-memory-keeper agent into entries here.
        # Each entry covers one or more contiguous chapters.
        # [{id: "M001", covers_chapters, summary, hooks_still_open, key_facts,
        #   state_snapshot, created_at_chapter, compaction_level}]
        # compaction_level: "per_chapter" (one chapter → one entry) |
        #                   "n_chapters_merge" (multiple chapters merged into one)
        "memory_log": [],
        "quality_reports": {},
        "manuscript": {
            "compiled_md": None,
            "compiled_html": None,
            "pdf_path": None,
            "cover_brief": None,
            "blurb": None,
        },
    }


def load_tree(path: str) -> dict:
    """Load a tree from disk. If missing, returns an empty tree."""
    if not os.path.exists(path):
        return empty_tree()
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_tree(tree: dict, path: str) -> None:
    """Atomically save a tree to disk."""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(tree, f, ensure_ascii=False, indent=2)
    os.replace(tmp, path)


# ---------- Path access (dotted with [index], [?key=value] selectors) ----------

def get_path(tree: dict, dotted: str) -> Any:
    """Get a value by dotted path. Supports list indices [i] and [?id=value]."""
    node: Any = tree
    for part in _split_path(dotted):
        node = _step(node, part)
        if node is None:
            return None
    return node


def set_path(tree: dict, dotted: str, value: Any) -> None:
    """Set a value by dotted path. Creates intermediate dicts; lists must exist."""
    parts = _split_path(dotted)
    node: Any = tree
    for part in parts[:-1]:
        nxt = _step(node, part)
        if nxt is None:
            if isinstance(node, dict):
                node[part] = {}
                nxt = node[part]
            else:
                raise KeyError(f"cannot create path through non-dict at {part}")
        node = nxt
    last = parts[-1]
    if isinstance(node, dict):
        node[last] = value
    elif isinstance(node, list) and last.startswith("["):
        idx = _parse_bracket(last)
        if isinstance(idx, int):
            node[idx] = value
        else:
            # selector-based set: replace matching element or append
            for i, el in enumerate(node):
                if isinstance(el, dict) and idx and el.get(idx[0]) == idx[1]:
                    node[i] = value
                    return
            node.append(value)
    else:
        raise KeyError(f"cannot set {dotted}")


def _split_path(p: str) -> list[str]:
    """Split 'a.b[0].c[?id=x]' → ['a', 'b', '[0]', 'c', '[?id=x]']."""
    out: list[str] = []
    buf = ""
    i = 0
    while i < len(p):
        c = p[i]
        if c == ".":
            if buf:
                out.append(buf)
                buf = ""
        elif c == "[":
            if buf:
                out.append(buf)
                buf = ""
            j = p.index("]", i)
            out.append(p[i:j + 1])
            i = j
        else:
            buf += c
        i += 1
    if buf:
        out.append(buf)
    return out


def _parse_bracket(part: str) -> Any:
    """Parse '[0]' → 0, '[?id=lin-wei]' → ('id', 'lin-wei'), '[*]' → '*'."""
    inner = part[1:-1]
    if inner == "*":
        return "*"
    if inner.startswith("?"):
        k, v = inner[1:].split("=", 1)
        return (k.strip(), v.strip())
    return int(inner)


def _step(node: Any, part: str) -> Any:
    if part.startswith("["):
        idx = _parse_bracket(part)
        if not isinstance(node, list):
            return None
        if idx == "*":
            return node
        if isinstance(idx, int):
            return node[idx] if 0 <= idx < len(node) else None
        if isinstance(idx, tuple):
            k, v = idx
            for el in node:
                if isinstance(el, dict) and str(el.get(k)) == v:
                    return el
            return None
    if isinstance(node, dict):
        return node.get(part)
    return None


# ---------- Tree queries used by the workflow engine ----------

def is_node_present(tree: dict, dotted: str) -> bool:
    val = get_path(tree, dotted)
    if val is None:
        return False
    if isinstance(val, (list, dict, str)) and len(val) == 0:
        return False
    return True


def iter_chapters(tree: dict) -> Iterator[dict]:
    for act in tree.get("outline", {}).get("acts", []) or []:
        for ch in act.get("chapters", []) or []:
            yield ch


def iter_beats(tree: dict, chapter_id: str | None = None) -> Iterator[dict]:
    for ch in iter_chapters(tree):
        if chapter_id and ch.get("id") != chapter_id:
            continue
        for b in ch.get("beats", []) or []:
            yield b


def total_wordcount(tree: dict) -> int:
    n = 0
    for b in iter_beats(tree):
        text = b.get("text") or ""
        n += len(text.split())
    return n


# ---------- Hooks: promise/payoff ledger ----------

def collect_hook_refs(tree: dict) -> tuple[dict, dict]:
    """Walk all beats and return (opened_index, resolved_index) — hook_id → list of beat refs."""
    opened: dict[str, list[str]] = {}
    resolved: dict[str, list[str]] = {}
    for b in iter_beats(tree):
        bid = b.get("id") or ""
        for h in (b.get("hooks_opened") or []):
            opened.setdefault(h, []).append(bid)
        for h in (b.get("hooks_resolved") or []):
            resolved.setdefault(h, []).append(bid)
    return opened, resolved


def audit_hooks(tree: dict) -> dict:
    """Run a hook audit. Returns {open, dangling, resolved, orphan_resolutions, summary}.

    - open:               hooks declared in `novel.hooks` that have an open beat but no resolution
    - dangling:           beats `.hooks_opened` references that never appear in `novel.hooks` registry
    - resolved:           hooks that have both open beat and resolve beat
    - orphan_resolutions: beats `.hooks_resolved` that have no opening beat
    """
    registry = {h.get("id"): h for h in (tree.get("hooks") or []) if h.get("id")}
    opened, resolved = collect_hook_refs(tree)

    open_unresolved: list[dict] = []
    dangling: list[dict] = []
    resolved_ok: list[dict] = []
    orphans: list[dict] = []

    seen = set()
    for hid, beats in opened.items():
        seen.add(hid)
        reg = registry.get(hid)
        if hid not in resolved:
            (open_unresolved if reg else dangling).append({
                "id": hid,
                "opened_at": beats,
                "registered": bool(reg),
                "label": (reg or {}).get("label"),
            })
        else:
            resolved_ok.append({
                "id": hid,
                "opened_at": beats,
                "resolved_at": resolved[hid],
                "label": (reg or {}).get("label"),
            })

    for hid, beats in resolved.items():
        if hid not in opened:
            orphans.append({"id": hid, "resolved_at": beats, "label": (registry.get(hid) or {}).get("label")})

    # also flag registered hooks with no opening beat at all
    for hid, reg in registry.items():
        if hid not in opened:
            dangling.append({
                "id": hid,
                "registered": True,
                "label": reg.get("label"),
                "issue": "registered_but_never_opened",
            })

    return {
        "summary": {
            "registered": len(registry),
            "resolved": len(resolved_ok),
            "open": len(open_unresolved),
            "dangling": len(dangling),
            "orphan_resolutions": len(orphans),
            "verdict": "clean" if not open_unresolved and not dangling and not orphans else "warn",
        },
        "resolved": resolved_ok,
        "open": open_unresolved,
        "dangling": dangling,
        "orphan_resolutions": orphans,
    }


# ---------- Empty beat factory (canonical schema) ----------

def empty_beat(beat_id: str = "") -> dict:
    """A beat with the full schema, all fields present (default to empty)."""
    return {
        "id": beat_id,
        "emotion": "",
        "function": "",
        "length_target": 0,
        "opening_trigger": "",
        "closing_image": "",
        # New richer fields (added in P1):
        "facts": [],              # [{actor, action, object?, detail?}]
        "location_id": None,       # ref to novel.world_bible.locations[].id, e.g. "L003"
        "emotions": [],            # [{character, emotion}]  — per-character emotional weather
        "state_changes": [],       # [{character, before, after}]
        "hooks_opened": [],        # ["H001", "H004", ...]
        "hooks_resolved": [],      # ["H002", ...]
        "text": "",
    }


def empty_hook(hook_id: str, label: str = "", kind: str = "plot") -> dict:
    """A canonical hook entry.

    kind: 'plot' | 'character' | 'thematic' | 'mystery' | 'foreshadow'
    """
    return {
        "id": hook_id,
        "label": label,
        "kind": kind,
        "opened_at_beat": "",
        "resolved_at_beat": "",
        "status": "open",
    }


def empty_location(loc_id: str, name: str = "") -> dict:
    return {
        "id": loc_id,
        "name": name,
        "description": "",
        "sensory_anchors": {     # what the POV character cannot help noticing
            "sight": "",
            "sound": "",
            "smell": "",
            "touch": "",
            "taste": "",
        },
        "parent_region": "",     # e.g. "the Eastern Quarter"
        "first_appearance_chapter": "",
    }


def empty_memory_entry(mem_id: str, covers: list[str], created_at_chapter: str = "") -> dict:
    """A canonical entry in `novel.memory_log` (used by infinite_serial mode).

    - covers_chapters: list of chapter ids this entry summarizes
    - summary: prose-level recap (~300 words per chapter at per_chapter level,
               ~500 words for N-chapters-merged level)
    - hooks_still_open: ids of hooks that were planted in these chapters and
                        had not yet been paid off as of this entry's creation
    - key_facts: durable facts the next-chapter planner must know
    - state_snapshot: per-character state at the end of the covered range
    - created_at_chapter: id of the chapter that was the latest when this
                          memory was created (for provenance)
    - compaction_level: "per_chapter" if covers exactly one chapter,
                        "n_chapters_merge" if it merges multiple
    """
    return {
        "id": mem_id,
        "covers_chapters": list(covers),
        "summary": "",
        "hooks_still_open": [],
        "key_facts": [],
        "state_snapshot": {},
        "created_at_chapter": created_at_chapter,
        "compaction_level": "per_chapter" if len(covers) == 1 else "n_chapters_merge",
    }


# ---------- Serial-mode helpers ----------

def serial_recent_chapters(tree: dict, n: int = 3) -> list[dict]:
    """Return the last N chapters (with full beats/text). For serial mode."""
    chapters = list(iter_chapters(tree))
    return chapters[-n:] if len(chapters) >= n else chapters


def serial_chapters_needing_compaction(tree: dict) -> list[str]:
    """Decide which chapter ids should be compacted into memory_log next.

    Default policy:
      - Keep most-recent `keep_recent_full` chapters fully present.
      - Chapters older than that BUT not yet in memory_log → ripe for per-chapter
        summary (or merge if depth > keep_medium_summary).
    Returns chapter ids ripe for compaction (oldest-first).
    """
    cfg = (tree.get("metadata", {}).get("serial") or {}).get("compaction_settings", {})
    keep_full = int(cfg.get("keep_recent_full", 3) or 3)

    all_chs = list(iter_chapters(tree))
    if len(all_chs) <= keep_full:
        return []
    already_compacted = set()
    for m in (tree.get("memory_log") or []):
        for cid in (m.get("covers_chapters") or []):
            already_compacted.add(cid)

    candidates: list[str] = []
    # All chapters EXCEPT the last `keep_full` are eligible
    for ch in all_chs[:-keep_full]:
        cid = ch.get("id")
        if cid and cid not in already_compacted:
            candidates.append(cid)
    return candidates


def serial_planner_context(tree: dict) -> dict:
    """The compact context the next-chapter planner sees in serial mode.

    Excludes full prose of all but the recent few chapters; instead, includes
    the memory_log + per-character state snapshot.
    """
    cfg = (tree.get("metadata", {}).get("serial") or {}).get("compaction_settings", {})
    keep_full = int(cfg.get("keep_recent_full", 3) or 3)

    open_hooks = [h for h in (tree.get("hooks") or []) if h.get("status") == "open"]
    recent = serial_recent_chapters(tree, n=keep_full)

    return {
        "world_bible": tree.get("world_bible", {}),
        "characters":  tree.get("characters", []),
        "memory_log":  tree.get("memory_log", []),
        "open_hooks":  open_hooks,
        "recent_chapters_full": [
            {
                "id": ch.get("id"),
                "title": ch.get("title"),
                "POV": ch.get("POV"),
                "summary": ch.get("summary"),
                "compiled_text": ch.get("compiled_text") or "",
                "beats": ch.get("beats", []),
            } for ch in recent
        ],
        "current_chapter_count": (tree.get("metadata", {}).get("serial") or {}).get(
            "current_chapter_count", len(list(iter_chapters(tree)))
        ),
    }


def estimate_planner_context_tokens(tree: dict) -> int:
    """Rough token estimate (chars/4) of what the planner would see today.

    Used to decide whether to prompt the user to run /compress-memory.
    """
    import json as _json
    ctx = serial_planner_context(tree)
    s = _json.dumps(ctx, ensure_ascii=False)
    return len(s) // 4


# ---------- Convenience ----------

def deep_merge(base: dict, override: dict) -> dict:
    """Recursive merge — override wins on conflict."""
    out = deepcopy(base)
    for k, v in override.items():
        if k in out and isinstance(out[k], dict) and isinstance(v, dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = deepcopy(v)
    return out


if __name__ == "__main__":
    # Smoke test
    t = empty_tree("Test", "Lei", 10000)
    set_path(t, "metadata.genre", "literary sci-fi")
    set_path(t, "ideation.logline", "A test logline.")
    assert get_path(t, "ideation.logline") == "A test logline."
    assert get_path(t, "metadata.genre") == "literary sci-fi"

    # Hook audit smoke test
    t["hooks"] = [
        empty_hook("H001", "The mother's missing year", kind="mystery"),
        empty_hook("H002", "The father's letter", kind="plot"),
        empty_hook("H003", "Mei's defection", kind="character"),
    ]
    t["world_bible"]["locations"] = [
        empty_location("L001", "Reader College, dawn garden"),
        empty_location("L002", "Court of Mneme, central hall"),
    ]
    # fake one act / one chapter / two beats
    b1 = empty_beat("ch01.b01")
    b1["hooks_opened"] = ["H001"]
    b1["location_id"] = "L001"
    b2 = empty_beat("ch12.b03")
    b2["hooks_resolved"] = ["H001"]
    b2["location_id"] = "L001"
    t["outline"]["acts"] = [{
        "id": "act1", "name": "Setup",
        "chapters": [{"id": "ch01", "title": "Opening", "beats": [b1]}],
    }, {
        "id": "act3", "name": "Resolution",
        "chapters": [{"id": "ch12", "title": "End", "beats": [b2]}],
    }]
    audit = audit_hooks(t)
    print("hook audit:", json.dumps(audit["summary"], indent=2))
    assert audit["summary"]["resolved"] == 1, audit
    assert audit["summary"]["open"] == 0, audit
    # H002 and H003 are registered but never opened — should be dangling
    assert audit["summary"]["dangling"] == 2, audit

    print("novel_tree smoke test passed")
