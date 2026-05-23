"""Resolve the mode (full / semi / manual / skip) for each step.

Resolution priority:
  1. CLI --mode flag (applies to all steps)
  2. config.mode_overrides[step_id]
  3. config.skip[step_id]
  4. skill.mode_default
  5. agent.mode_default
  6. workflow.mode_default
  7. global default: 'semi'
"""
from __future__ import annotations

from typing import Literal


Mode = Literal["full", "semi", "manual", "skip"]
VALID_MODES: tuple[Mode, ...] = ("full", "semi", "manual", "skip")


def resolve_mode(
    step_id: str,
    *,
    cli_mode: Mode | None = None,
    novel_meta: dict | None = None,
    skill: dict | None = None,
    agent: dict | None = None,
    workflow: dict | None = None,
) -> Mode:
    """Resolve the mode for a single step."""
    if cli_mode and cli_mode in VALID_MODES:
        return cli_mode

    meta = novel_meta or {}
    overrides = meta.get("mode_overrides") or {}
    skip = meta.get("skip") or {}

    if skip.get(step_id) is True:
        return "skip"
    if step_id in overrides:
        m = overrides[step_id]
        if m in VALID_MODES:
            return m

    if skill:
        m = (skill.get("frontmatter") or {}).get("mode_default")
        if m in VALID_MODES:
            return m
    if agent:
        m = (agent.get("frontmatter") or {}).get("mode_default")
        if m in VALID_MODES:
            return m
    if workflow:
        m = workflow.get("mode_default")
        if m in VALID_MODES:
            return m

    return "semi"


def should_skip_existing(step: dict, tree: dict) -> bool:
    """If the output node already exists, skip unless rerun is forced."""
    from orchestrator.novel_tree import is_node_present
    outputs = (step.get("outputs") or []) if isinstance(step, dict) else []
    if not outputs:
        return False
    return all(is_node_present(tree, o) for o in outputs)


if __name__ == "__main__":
    # quick test
    skill = {"frontmatter": {"mode_default": "full"}}
    print(resolve_mode("compile_pdf", cli_mode=None, skill=skill))  # full
    print(resolve_mode("chapters", cli_mode="manual", skill=skill))  # manual
    print(resolve_mode("any", novel_meta={"skip": {"any": True}}))  # skip
    print(resolve_mode("any", novel_meta={"mode_overrides": {"any": "full"}}))  # full
    print(resolve_mode("any"))  # semi (default)
