"""Load skill definitions from skills/{single,workflows}/<name>/SKILL.md.

Skills are how the orchestrator and Claude Code expose user-facing actions.
"""
from __future__ import annotations

import glob
import os
import sys

if __name__ == "__main__" and __package__ is None:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from orchestrator.agent_loader import parse_agent_file  # frontmatter parser is generic


def load_all_skills(skills_dir: str | None = None) -> dict[str, dict]:
    """Scan for SKILL.md files and return {name: parsed}.

    Lookup order:
      1. Explicit `skills_dir`
      2. `.claude/skills` (Claude Code canonical location)
      3. `skills` (source-organized fallback with single/ and workflows/ subdirs)
    """
    candidates: list[str] = []
    if skills_dir:
        candidates.append(skills_dir)
    candidates += [".claude/skills", "skills"]

    chosen: str | None = None
    for c in candidates:
        if os.path.isdir(c):
            chosen = c
            break
    if not chosen:
        return {}

    out: dict[str, dict] = {}
    for path in sorted(glob.glob(os.path.join(chosen, "**", "SKILL.md"), recursive=True)):
        parsed = parse_agent_file(path)
        name = parsed["frontmatter"].get("name") or os.path.basename(os.path.dirname(path))
        parsed["category"] = "workflow" if "/workflows/" in path else "single"
        out[name] = parsed
    return out


def load_workflow_yaml(name: str, workflows_dir: str = "orchestrator/workflows") -> dict:
    """Load a workflow YAML by name."""
    path = os.path.join(workflows_dir, f"{name}.yaml")
    if not os.path.exists(path):
        raise FileNotFoundError(f"workflow not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    from orchestrator.agent_loader import _parse_simple_yaml
    return _parse_simple_yaml(text)


if __name__ == "__main__":
    skills = load_all_skills()
    single = [n for n, s in skills.items() if s["category"] == "single"]
    workflows = [n for n, s in skills.items() if s["category"] == "workflow"]
    print(f"loaded {len(skills)} skills: {len(single)} single + {len(workflows)} workflows")
    print("\nWorkflows:")
    for w in sorted(workflows):
        print(f"  /{w}")
    print("\nSample single skills:")
    for s in sorted(single)[:10]:
        print(f"  /{s}")
    # try loading a workflow yaml
    full = load_workflow_yaml("full-novel-pipeline")
    print(f"\nfull-novel-pipeline has {len(full.get('steps', []))} steps")
