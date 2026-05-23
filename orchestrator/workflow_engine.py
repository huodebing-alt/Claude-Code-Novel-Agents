"""DAG workflow engine.

Reads a workflow YAML, resolves dependencies, dispatches per-step skill calls.
Supports `fan_out: per_chapter` (or per_character) which expands one step into N.

The engine is synchronous by design — parallelism is achieved by the LLM backend
batching internally (Anthropic's `batches` API can be plugged in later) or by
running multiple engine instances on different chapters.
"""
from __future__ import annotations

import json
import os
import sys
import time
from collections import deque
from dataclasses import dataclass, field
from typing import Any, Callable

if __name__ == "__main__" and __package__ is None:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from orchestrator import novel_tree as nt
from orchestrator.agent_loader import load_all_agents, build_system_prompt
from orchestrator.llm_backend import call as llm_call, is_sandbox_mode
from orchestrator.mode_selector import resolve_mode, Mode
from orchestrator.skill_loader import load_all_skills, load_workflow_yaml


@dataclass
class StepResult:
    step_id: str
    mode: Mode
    status: str  # "done", "skipped", "stub", "error"
    output_paths: list[str] = field(default_factory=list)
    elapsed_seconds: float = 0.0
    note: str = ""


@dataclass
class EngineConfig:
    cli_mode: Mode | None = None
    novel_meta_path: str = "config/novel_meta.yaml"
    llm_config_path: str = "config/llm_config.yaml"
    tree_path: str = "novel.json"
    capture_cache: str | None = None  # if set, capture LLM outputs here
    dry_run: bool = False             # skip LLM calls, log what would happen


def _load_yaml(path: str) -> dict:
    if not os.path.exists(path):
        return {}
    from orchestrator.agent_loader import _parse_simple_yaml
    with open(path, "r", encoding="utf-8") as f:
        return _parse_simple_yaml(f.read())


def _fan_out_inputs(step: dict, tree: dict) -> list[dict[str, Any]]:
    """Given a step with `fan_out`, produce per-instance input dicts."""
    fan = step.get("fan_out")
    if not fan:
        return [{}]
    if fan == "per_chapter":
        return [{"chapter_id": ch.get("id"), "chapter": ch} for ch in nt.iter_chapters(tree)]
    if fan == "per_character":
        return [{"character_id": c.get("id"), "character": c} for c in tree.get("characters", [])]
    if fan == "per_principal_character":
        principals = [
            c for c in tree.get("characters", [])
            if c.get("role") in ("protagonist", "antagonist")
        ]
        return [{"character_id": c.get("id"), "character": c} for c in principals]
    if fan == "per_speaking_character":
        # heuristic — all named characters
        return [
            {"character_id": c.get("id"), "character": c}
            for c in tree.get("characters", []) if c.get("name")
        ]
    return [{}]


def _build_user_prompt(step: dict, skill: dict, agent: dict, tree: dict, instance: dict) -> str:
    """Build the per-call user prompt for the agent.

    Important: the chapter-writer agent is rendered as a *parallel* subagent —
    its `context_isolation: strict` frontmatter flag tells us to ONLY load its
    own chapter (with beats) and a one-paragraph summary of every other chapter.
    No other chapter's prose text is exposed. This is what lets us run 12
    chapter-writers in parallel without blowing the context budget.
    """
    skill_name = step.get("skill", "")
    skill_desc = (skill.get("frontmatter") or {}).get("description", "")
    agent_name = (skill.get("frontmatter") or {}).get("agent") or ""
    dept = (agent["frontmatter"].get("department") or "") if agent else ""

    isolation = (agent["frontmatter"].get("context_isolation") or "") if agent else ""

    ctx: dict[str, Any] = {
        "skill": skill_name,
        "skill_description": skill_desc,
        "novel_metadata": tree.get("metadata", {}),
        "ideation": tree.get("ideation", {}),
    }

    # ---- Chapter-writer (or any agent with strict isolation) ----
    if isolation == "strict" and instance.get("chapter"):
        # Full bible
        ctx["world_bible"] = tree.get("world_bible", {})
        # Full character roster (voice cards + psychology + arc)
        ctx["characters"] = tree.get("characters", [])
        # Hook registry (so the writer knows what to plant / pay off)
        ctx["hooks"] = tree.get("hooks", [])
        # Style brief
        ctx["style_brief"] = tree.get("ideation", {}).get("stylistic_direction")
        # ONLY THIS chapter (full detail)
        ctx["my_chapter"] = instance["chapter"]
        # Sibling chapters: STRIPPED — only id, title, POV, summary. NO beats text, NO compiled_text.
        my_id = instance["chapter"].get("id")
        prior_summary: list[dict] = []
        future_summary: list[dict] = []
        seen_me = False
        for act in tree.get("outline", {}).get("acts", []):
            for ch in act.get("chapters", []) or []:
                if ch.get("id") == my_id:
                    seen_me = True
                    continue
                stripped = {
                    "id": ch.get("id"),
                    "title": ch.get("title"),
                    "POV": ch.get("POV"),
                    "summary": ch.get("summary"),
                }
                (future_summary if seen_me else prior_summary).append(stripped)
        ctx["prior_chapters_summary"] = prior_summary
        ctx["future_chapters_summary"] = future_summary

    else:
        # Non-isolated agents: load what they declare they need by department/skill heuristic
        if "world" in skill_name or "world" in dept or "location" in skill_name:
            ctx["world_bible"] = tree.get("world_bible", {})
        if "character" in skill_name or "character" in dept:
            ctx["characters"] = tree.get("characters", [])
        if instance.get("chapter"):
            ctx["chapter"] = instance["chapter"]
            ctx["world_bible"] = tree.get("world_bible", {})
            ctx["characters"] = tree.get("characters", [])
            ctx["style_brief"] = tree.get("ideation", {}).get("stylistic_direction")
        if instance.get("character"):
            ctx["character"] = instance["character"]
        # Quality + structure agents need to see the hook ledger
        if dept in ("quality", "structure") or "hook" in skill_name:
            ctx["hooks"] = tree.get("hooks", [])

    return (
        f"# /{skill_name}\n\n"
        f"## Instance context\n```json\n{json.dumps(ctx, ensure_ascii=False, indent=2)}\n```\n\n"
        "## Task\n"
        f"Produce the output described in your role for skill `/{skill_name}`. "
        "Output the deliverable directly. If you produce JSON, output only the JSON in a fenced block."
    )


def _apply_output(step: dict, instance: dict, output_text: str, tree: dict) -> list[str]:
    """Naively write the agent output into the tree at the skill's output paths.

    For prose outputs (chapter text), routes to the chapter's beat texts (joined).
    For structured outputs, attempts JSON parse and writes the dict.
    """
    outputs = step.get("outputs") or []
    paths_written: list[str] = []
    for raw_path in outputs:
        path = raw_path
        # substitute fan-out wildcards
        if instance.get("chapter_id"):
            path = path.replace("*", instance["chapter_id"], 1)
        if instance.get("character_id"):
            path = path.replace("*", instance["character_id"], 1)
        # try JSON
        parsed: Any
        s = output_text.strip()
        if s.startswith("```"):
            # strip fenced block
            s = "\n".join(s.splitlines()[1:-1])
        try:
            parsed = json.loads(s)
        except Exception:
            parsed = output_text
        try:
            nt.set_path(tree, path, parsed)
            paths_written.append(path)
        except Exception:
            # graceful — store under a side-channel
            nt.set_path(tree, f"manuscript._unsorted.{step.get('id', 'unknown')}", parsed)
            paths_written.append(f"manuscript._unsorted.{step.get('id', 'unknown')}")
    return paths_written


def _resolve_model(agent_name: str, agent: dict, instance: dict, llm_config: dict) -> str:
    """Decide which model to use for this dispatch.

    Priority (highest first) — user config wins so the onboarding preset choice is honored:
      1. config.agent_model_overrides["<agent>-<context_tag>"]   # e.g. chapter-writer-climax
      2. config.agent_model_overrides["<agent>"]
      3. config.models[<tier>]  based on agent.frontmatter.tier   # USER PRESET WINS HERE
      4. agent.frontmatter.model_overrides[<context_tag>_chapter] # static fallback
      5. agent.frontmatter.model                                   # static fallback
      6. global default: claude-opus-4-7
    """
    overrides = (llm_config.get("agent_model_overrides") or {}) if llm_config else {}
    models_cfg = (llm_config.get("models") or {}) if llm_config else {}
    fm = agent.get("frontmatter") or {}
    ch = instance.get("chapter") or {}

    # Determine context tag for chapter-writer instances
    context_tag = None
    if agent_name == "chapter-writer" and ch:
        if ch.get("is_climax") or "climax" in (ch.get("title") or "").lower():
            context_tag = "climax"
        elif ch.get("is_midpoint") or "midpoint" in (ch.get("title") or "").lower():
            context_tag = "midpoint"
        elif ch.get("is_opener"):
            context_tag = "opener"
        elif ch.get("is_final"):
            context_tag = "final"

    # Priority 1
    if context_tag and overrides.get(f"{agent_name}-{context_tag}"):
        return overrides[f"{agent_name}-{context_tag}"]
    # Priority 2
    if overrides.get(agent_name):
        return overrides[agent_name]
    # Priority 3 — tier-based config (user preset)
    tier = fm.get("tier")
    if tier in (1, "1") and models_cfg.get("director"):
        return models_cfg["director"]
    if tier in (2, "2") and models_cfg.get("lead"):
        return models_cfg["lead"]
    if tier in (3, "3") and models_cfg.get("specialist"):
        return models_cfg["specialist"]
    if tier in (4, "4") and models_cfg.get("onboarding"):
        return models_cfg["onboarding"]
    # Priority 4 — agent frontmatter chapter overrides
    fm_overrides = fm.get("model_overrides") or {}
    if context_tag and fm_overrides.get(f"{context_tag}_chapter"):
        return fm_overrides[f"{context_tag}_chapter"]
    # Priority 5 — agent frontmatter
    if fm.get("model"):
        return fm["model"]
    # Priority 6 — global default
    return "claude-opus-4-7"


def _topological_order(steps: list[dict]) -> list[dict]:
    """Kahn's algorithm for DAG ordering."""
    by_id = {s["id"]: s for s in steps}
    indeg = {s["id"]: 0 for s in steps}
    edges: dict[str, list[str]] = {s["id"]: [] for s in steps}
    for s in steps:
        for dep in s.get("depends_on", []) or []:
            indeg[s["id"]] = indeg.get(s["id"], 0) + 1
            edges.setdefault(dep, []).append(s["id"])
    queue = deque([sid for sid, d in indeg.items() if d == 0])
    out: list[dict] = []
    while queue:
        sid = queue.popleft()
        out.append(by_id[sid])
        for child in edges.get(sid, []):
            indeg[child] -= 1
            if indeg[child] == 0:
                queue.append(child)
    if len(out) != len(steps):
        raise ValueError("workflow DAG has a cycle")
    return out


def execute_workflow(
    workflow_name: str,
    cfg: EngineConfig,
    *,
    interactive_pause: Callable[[str, str, str], str] | None = None,
) -> list[StepResult]:
    """Execute a workflow end-to-end. Returns per-step results.

    `interactive_pause(step_id, mode, draft)` is called in semi mode to gather
    user input. Return 'accept' to write draft, anything else replaces.
    """
    workflow = load_workflow_yaml(workflow_name)
    skills = load_all_skills()
    agents = load_all_agents()
    novel_meta = _load_yaml(cfg.novel_meta_path)
    llm_config = _load_yaml(cfg.llm_config_path)
    tree = nt.load_tree(cfg.tree_path)

    results: list[StepResult] = []
    steps = workflow.get("steps", []) or []
    ordered = _topological_order(steps)

    for step in ordered:
        start = time.time()
        sid = step["id"]
        skill_name = step.get("skill")
        skill = skills.get(skill_name) if skill_name else None
        agent_name = (skill.get("frontmatter") or {}).get("agent") if skill else None
        agent = agents.get(agent_name) if agent_name else None
        action = step.get("action") or ""
        mode = resolve_mode(
            sid,
            cli_mode=cfg.cli_mode,
            novel_meta=novel_meta,
            skill=skill,
            agent=agent,
            workflow=workflow,
        )

        # ---- Non-LLM step types ----
        if action == "wait_for_review":
            # In `full` mode, skip the user review entirely.
            if mode == "full":
                results.append(StepResult(sid, mode, "skipped", note="full mode — skipped user review"))
                continue
            # Otherwise launch the outline reviewer and block until /api/done.
            from orchestrator.runner import launch_outline_reviewer  # late import to avoid circular
            try:
                params = step.get("params") or {}
                port = int(params.get("port") or 7878)
                open_browser = bool(params.get("open_browser", True) if "open_browser" in params else True)
                if cfg.dry_run:
                    note = f"DRY_RUN — would launch outline reviewer on :{port}"
                else:
                    launch_outline_reviewer(novel_path=cfg.tree_path, port=port, open_browser=open_browser)
                    note = "user reviewed outline, signaled Done"
                    # reload tree (user may have edited it in the UI)
                    tree = nt.load_tree(cfg.tree_path)
                results.append(StepResult(sid, mode, "done", note=note,
                                          elapsed_seconds=time.time() - start))
            except Exception as e:
                results.append(StepResult(sid, mode, "error",
                                          note=f"wait_for_review failed: {type(e).__name__}: {e}"))
            continue

        if action == "print":
            msg = (step.get("params") or {}).get("message", "")
            print(msg)
            results.append(StepResult(sid, mode, "done", note="printed"))
            continue

        # Implicit skip: outputs already exist
        if skill and mode != "skip":
            from orchestrator.mode_selector import should_skip_existing
            synthetic = {"outputs": (skill.get("frontmatter") or {}).get("outputs") or []}
            if should_skip_existing(synthetic, tree):
                results.append(StepResult(sid, mode, "skipped", note="outputs already present"))
                nt.save_tree(tree, cfg.tree_path)
                continue

        if mode == "skip":
            results.append(StepResult(sid, mode, "skipped", note="config skip"))
            continue
        if mode == "manual":
            results.append(StepResult(
                sid, mode, "stub",
                note=f"manual mode — user to produce {skill_name} output",
            ))
            continue

        if not skill or not agent:
            results.append(StepResult(sid, mode, "error", note=f"missing skill or agent: {skill_name}"))
            continue

        # fan-out per instance
        instances = _fan_out_inputs(step, tree)
        for inst in instances:
            system = build_system_prompt(agent)
            user = _build_user_prompt(step, skill, agent, tree, inst)
            model = _resolve_model(agent_name, agent, inst, llm_config)
            temperature = float(agent["frontmatter"].get("temperature", 0.7) or 0.7)

            if cfg.dry_run:
                output = f"[DRY_RUN output for {agent_name} on {sid}]"
            else:
                try:
                    output = llm_call(
                        agent_name=agent_name,
                        model=model,
                        system=system,
                        user=user,
                        max_tokens=int(agent["frontmatter"].get("max_tokens", 4096)),
                        temperature=temperature,
                        llm_config=llm_config,
                    )
                except Exception as e:
                    results.append(StepResult(
                        sid, mode, "error",
                        note=f"LLM call failed: {type(e).__name__}: {e}",
                    ))
                    continue
                if cfg.capture_cache and not is_sandbox_mode(llm_config):
                    from orchestrator.llm_backend import capture_to_cache
                    capture_to_cache(
                        agent_name=agent_name,
                        model=model,
                        system=system,
                        user=user,
                        output=output,
                        cache_path=cfg.capture_cache,
                    )

            # semi-auto pause
            if mode == "semi" and interactive_pause:
                final = interactive_pause(sid, mode, output)
                if final and final != "accept":
                    output = final

            # write output
            synthetic_step = {
                "id": sid,
                "outputs": (skill.get("frontmatter") or {}).get("outputs") or [],
            }
            written = _apply_output(synthetic_step, inst, output, tree)
            results.append(StepResult(
                sid, mode, "done", output_paths=written,
                elapsed_seconds=time.time() - start,
            ))
            nt.save_tree(tree, cfg.tree_path)

    return results


if __name__ == "__main__":
    cfg = EngineConfig(cli_mode="full", dry_run=True, tree_path="/tmp/_test_novel.json")
    nt.save_tree(nt.empty_tree("Smoke Test"), cfg.tree_path)
    results = execute_workflow("outline-only", cfg)
    for r in results:
        print(f"  [{r.status:8s}] {r.step_id:24s} mode={r.mode}  note={r.note}")
