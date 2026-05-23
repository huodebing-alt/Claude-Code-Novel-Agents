"""Load agent definitions from agents/*/*.md (YAML frontmatter + body)."""
from __future__ import annotations

import glob
import os
import re
from typing import Any


_FRONT_RE = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.DOTALL)


def _parse_simple_yaml(text: str) -> dict:
    """Minimal YAML parser: scalar, list (- form), nested dicts via indent.

    No anchors, no flow style. Sufficient for our frontmatter.
    """
    out: dict = {}
    lines = text.splitlines()
    _parse_block(lines, 0, 0, out)
    return out


def _parse_block(lines: list[str], start: int, indent: int, out: dict) -> int:
    i = start
    while i < len(lines):
        raw = lines[i]
        if not raw.strip() or raw.lstrip().startswith("#"):
            i += 1
            continue
        cur_indent = len(raw) - len(raw.lstrip())
        if cur_indent < indent:
            return i
        if cur_indent > indent:
            # shouldn't happen at this level — caller handles nested
            i += 1
            continue

        stripped = raw.strip()
        if stripped.startswith("- "):
            # list item — but caller should have parsed list already
            return i

        if ":" not in stripped:
            i += 1
            continue
        key, _, rest = stripped.partition(":")
        key = key.strip()
        rest = rest.strip()
        if rest == "" or rest is None:
            # nested: peek next line
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j >= len(lines):
                out[key] = None
                i = j
                continue
            next_indent = len(lines[j]) - len(lines[j].lstrip())
            if next_indent > indent and lines[j].lstrip().startswith("- "):
                # list value
                items, i = _parse_list(lines, j, next_indent)
                out[key] = items
            elif next_indent > indent:
                sub: dict = {}
                i = _parse_block(lines, j, next_indent, sub)
                out[key] = sub
            else:
                out[key] = None
                i = j
        else:
            out[key] = _coerce(rest)
            i += 1
    return i


def _parse_list(lines: list[str], start: int, indent: int) -> tuple[list, int]:
    items: list = []
    i = start
    while i < len(lines):
        raw = lines[i]
        if not raw.strip():
            i += 1
            continue
        cur_indent = len(raw) - len(raw.lstrip())
        if cur_indent < indent:
            return items, i
        stripped = raw.lstrip()
        if not stripped.startswith("- "):
            return items, i
        body = stripped[2:].strip()
        if ":" in body and not body.startswith("\"") and not body.startswith("'"):
            # dict element — start a dict from this line, increment indent
            sub: dict = {}
            key, _, rest = body.partition(":")
            sub[key.strip()] = _coerce(rest.strip()) if rest.strip() else None
            j = i + 1
            inner_indent = indent + 2
            j = _parse_block(lines, j, inner_indent, sub)
            items.append(sub)
            i = j
        else:
            items.append(_coerce(body))
            i += 1
    return items, i


def _coerce(s: str) -> Any:
    if s == "":
        return None
    if s.lower() in ("true", "yes"):
        return True
    if s.lower() in ("false", "no"):
        return False
    if s.lower() in ("null", "none", "~"):
        return None
    # number?
    try:
        if "." in s:
            return float(s)
        return int(s)
    except ValueError:
        pass
    # quoted?
    if len(s) >= 2 and s[0] == s[-1] and s[0] in ("'", "\""):
        return s[1:-1]
    # inline list [a, b, c]
    if s.startswith("[") and s.endswith("]"):
        inner = s[1:-1].strip()
        if not inner:
            return []
        return [_coerce(p.strip()) for p in _split_commas(inner)]
    return s


def _split_commas(s: str) -> list[str]:
    """Split a comma-list respecting brackets and quotes (shallow)."""
    out: list[str] = []
    depth = 0
    buf = ""
    in_quote: str | None = None
    for c in s:
        if in_quote:
            buf += c
            if c == in_quote:
                in_quote = None
            continue
        if c in ("\"", "'"):
            in_quote = c
            buf += c
            continue
        if c in "[{(":
            depth += 1
        elif c in "]})":
            depth -= 1
        if c == "," and depth == 0:
            out.append(buf)
            buf = ""
        else:
            buf += c
    if buf.strip():
        out.append(buf)
    return out


def parse_agent_file(path: str) -> dict:
    """Read agents/*.md, return {frontmatter: dict, body: str, path: str}."""
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    m = _FRONT_RE.match(text)
    if not m:
        raise ValueError(f"missing frontmatter in {path}")
    front_text, body = m.group(1), m.group(2)
    front = _parse_simple_yaml(front_text)
    return {"frontmatter": front, "body": body, "path": path}


def load_all_agents(agents_dir: str | None = None) -> dict[str, dict]:
    """Scan for agent .md files and return {name: parsed}.

    Lookup order (first one that exists wins):
      1. Explicit `agents_dir` argument
      2. `.claude/agents` (Claude Code canonical location)
      3. `agents` (legacy / source-organized fallback)
    """
    candidates: list[str] = []
    if agents_dir:
        candidates.append(agents_dir)
    candidates += [".claude/agents", "agents"]

    chosen: str | None = None
    for c in candidates:
        if os.path.isdir(c):
            chosen = c
            break
    if not chosen:
        return {}

    out: dict[str, dict] = {}
    for path in sorted(glob.glob(os.path.join(chosen, "**", "*.md"), recursive=True)):
        parsed = parse_agent_file(path)
        name = parsed["frontmatter"].get("name") or os.path.splitext(os.path.basename(path))[0]
        out[name] = parsed
    return out


def build_system_prompt(agent: dict) -> str:
    """Compose a system prompt from agent body (drops frontmatter)."""
    return agent["body"].strip()


if __name__ == "__main__":
    agents = load_all_agents()
    print(f"loaded {len(agents)} agents:")
    for name, a in sorted(agents.items()):
        front = a["frontmatter"]
        print(f"  {name:32s} tier={front.get('tier')} dept={front.get('department')} model={front.get('model')}")
