#!/usr/bin/env python3
"""CLI entrypoint for Claude Code Novel Agents.

Examples:

  # Run the full pipeline in semi mode (default)
  python orchestrator/runner.py --workflow full-novel-pipeline

  # Run only Phase 5 (quality) on an existing draft, full-auto
  python orchestrator/runner.py --workflow quality-pass --mode full

  # Sandbox demo — no API key required
  python orchestrator/runner.py --sandbox

  # Single skill against a single chapter
  python orchestrator/runner.py --skill write-chapter --chapter ch04

  # Dry run — no LLM calls; print what would happen
  python orchestrator/runner.py --workflow full-novel-pipeline --dry-run
"""
from __future__ import annotations

import argparse
import os
import sys
from typing import Optional

# Make `orchestrator.*` importable when run as a script
HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(HERE)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from orchestrator import novel_tree as nt
from orchestrator.workflow_engine import EngineConfig, execute_workflow
from orchestrator.skill_loader import load_all_skills


# ---------- ANSI (cheap, no rich dep) ----------

DIM = "\033[2m"
BOLD = "\033[1m"
RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
GOLD = "\033[33m"

def color(s: str, c: str) -> str:
    if not sys.stdout.isatty():
        return s
    return f"{c}{s}{RESET}"


def banner() -> None:
    print()
    print(color("┌──────────────────────────────────────────────────┐", GOLD))
    print(color("│  Claude Code Novel Agents — orchestrator         │", GOLD))
    print(color("│  45 agents · 62 skills · 6 phases                │", GOLD))
    print(color("└──────────────────────────────────────────────────┘", GOLD))
    print()


def interactive_pause_terminal(step_id: str, mode: str, draft: str) -> str:
    """Semi-mode terminal pause: show draft, accept/edit/reject."""
    print(color(f"\n— Semi-auto pause @ {step_id} —", BLUE))
    print(color("Draft:", DIM))
    preview = draft[:1200] + ("\n…(truncated)" if len(draft) > 1200 else "")
    print(preview)
    print(color("\n[a]ccept  [r]eplace (paste; end with EOF/Ctrl-D)  [s]kip", DIM))
    try:
        choice = input("> ").strip().lower()
    except EOFError:
        return "accept"
    if choice == "r":
        print(color("Paste replacement, end with Ctrl-D:", DIM))
        try:
            replacement = sys.stdin.read()
        except KeyboardInterrupt:
            return "accept"
        return replacement.strip() or "accept"
    if choice == "s":
        return "[USER_SKIPPED]"
    return "accept"


def cmd_workflow(args: argparse.Namespace) -> int:
    cfg = EngineConfig(
        cli_mode=args.mode,
        novel_meta_path=args.config or "config/novel_meta.yaml",
        llm_config_path=args.llm_config or "config/llm_config.yaml",
        tree_path=args.novel or "novel.json",
        capture_cache=args.capture_cache,
        dry_run=args.dry_run,
    )
    if args.sandbox:
        os.environ.pop("ANTHROPIC_API_KEY", None)  # force sandbox
    workflow_name = args.workflow or "full-novel-pipeline"
    print(color(f"▶ workflow: {workflow_name}  mode: {args.mode or 'auto'}  tree: {cfg.tree_path}", BLUE))
    results = execute_workflow(
        workflow_name, cfg,
        interactive_pause=interactive_pause_terminal if args.mode != "full" and not args.dry_run else None,
    )
    print()
    print(color("─ Results ─", GOLD))
    total = len(results)
    done = sum(1 for r in results if r.status == "done")
    skipped = sum(1 for r in results if r.status == "skipped")
    errored = sum(1 for r in results if r.status == "error")
    for r in results:
        status_color = {"done": GREEN, "skipped": DIM, "stub": YELLOW, "error": RED}.get(r.status, "")
        marker = {"done": "✓", "skipped": "−", "stub": "○", "error": "✗"}.get(r.status, "?")
        line = f"  {color(marker, status_color)} {r.step_id:24s} {r.mode:6s}  {r.note}"
        print(line)
    print()
    print(color(f"  {done}/{total} done, {skipped} skipped, {errored} errored", GOLD))
    return 0 if errored == 0 else 1


def cmd_skill(args: argparse.Namespace) -> int:
    """Run a single skill (one-step workflow)."""
    skills = load_all_skills()
    if args.skill not in skills:
        print(color(f"unknown skill: /{args.skill}", RED))
        return 2
    # Build a tiny one-step workflow on the fly
    one_step_wf = {
        "name": f"single-{args.skill}",
        "mode_default": args.mode or "semi",
        "steps": [{"id": args.skill, "skill": args.skill}],
    }
    # Write it to a temp file and reuse the engine
    import tempfile, json as _json
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False, dir="orchestrator/workflows")
    # write as our minimalist YAML — actually json works as a yaml subset if we keep it flat
    tmp.write(_to_yaml(one_step_wf))
    tmp.close()
    workflow_name = os.path.splitext(os.path.basename(tmp.name))[0]
    try:
        cfg = EngineConfig(
            cli_mode=args.mode,
            tree_path=args.novel or "novel.json",
            dry_run=args.dry_run,
        )
        results = execute_workflow(workflow_name, cfg)
        for r in results:
            print(f"  [{r.status}] {r.step_id} {r.note}")
        return 0 if all(r.status != "error" for r in results) else 1
    finally:
        os.unlink(tmp.name)


def _to_yaml(d: dict) -> str:
    """Minimal dict→YAML for our flat workflow format."""
    lines: list[str] = []
    for k, v in d.items():
        if isinstance(v, list):
            lines.append(f"{k}:")
            for el in v:
                if isinstance(el, dict):
                    first = True
                    for ek, ev in el.items():
                        prefix = "  - " if first else "    "
                        lines.append(f"{prefix}{ek}: {ev}")
                        first = False
                else:
                    lines.append(f"  - {el}")
        else:
            lines.append(f"{k}: {v}")
    return "\n".join(lines) + "\n"


def launch_outline_reviewer(novel_path: str, port: int = 7878,
                            open_browser: bool = True) -> None:
    """Launch the HTML reviewer and block until the user clicks Done.

    Called by workflow_engine's `wait_for_review` step. Also reachable via
    `python orchestrator/runner.py review-outline`.
    """
    # late import: output/ is not a package but a script directory
    import importlib.util
    here = os.path.dirname(os.path.abspath(__file__))
    spec_path = os.path.join(os.path.dirname(here), "output", "outline_reviewer.py")
    spec = importlib.util.spec_from_file_location("outline_reviewer", spec_path)
    if not spec or not spec.loader:
        raise RuntimeError(f"cannot load outline_reviewer at {spec_path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.serve(novel_path, port=port, open_browser=open_browser)


def cmd_review_outline(args: argparse.Namespace) -> int:
    novel = args.novel or "novel.json"
    if not os.path.exists(novel):
        print(color(f"novel.json not found at {novel}", RED))
        print(color(f"  → tip: try --novel sandbox/demo_novel.json for the pre-baked demo", DIM))
        return 2
    launch_outline_reviewer(
        novel_path=novel,
        port=args.port,
        open_browser=not args.no_browser,
    )
    return 0


def cmd_init(args: argparse.Namespace) -> int:
    """Initialize a new novel project (creates novel.json + configs)."""
    novel_path = args.novel or "novel.json"
    if os.path.exists(novel_path) and not args.force:
        print(color(f"{novel_path} exists. Use --force to overwrite.", YELLOW))
        return 1
    tree = nt.empty_tree(args.title or "Untitled", args.author or "Anonymous", args.wordcount or 80000)
    nt.save_tree(tree, novel_path)
    print(color(f"✓ Created {novel_path}", GREEN))
    for src, dst in (
        ("config/novel_meta.example.yaml", "config/novel_meta.yaml"),
        ("config/llm_config.example.yaml", "config/llm_config.yaml"),
    ):
        if not os.path.exists(dst) and os.path.exists(src):
            import shutil
            shutil.copy(src, dst)
            print(color(f"✓ Created {dst}", GREEN))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Claude Code Novel Agents orchestrator")
    sub = parser.add_subparsers(dest="cmd")

    # workflow (default)
    p_wf = sub.add_parser("workflow", help="run a workflow")
    p_wf.add_argument("--workflow", "-w", default="full-novel-pipeline")
    p_wf.add_argument("--mode", choices=["full", "semi", "manual"], default=None)
    p_wf.add_argument("--novel", default=None)
    p_wf.add_argument("--config", default=None)
    p_wf.add_argument("--llm-config", default=None)
    p_wf.add_argument("--sandbox", action="store_true")
    p_wf.add_argument("--dry-run", action="store_true")
    p_wf.add_argument("--capture-cache", default=None,
                      help="capture LLM outputs to this JSON path for later sandbox replay")

    # skill (one-shot)
    p_sk = sub.add_parser("skill", help="run a single skill")
    p_sk.add_argument("--skill", "-s", required=True)
    p_sk.add_argument("--mode", choices=["full", "semi", "manual"], default=None)
    p_sk.add_argument("--novel", default=None)
    p_sk.add_argument("--dry-run", action="store_true")

    # init
    p_in = sub.add_parser("init", help="initialize a new novel project")
    p_in.add_argument("--title", default=None)
    p_in.add_argument("--author", default=None)
    p_in.add_argument("--wordcount", type=int, default=None)
    p_in.add_argument("--novel", default=None)
    p_in.add_argument("--force", action="store_true")

    # review-outline (launch HTML reviewer standalone)
    p_rev = sub.add_parser("review-outline", help="launch the HTML outline reviewer (blocking)")
    p_rev.add_argument("--novel", default=None,
                       help="path to novel.json (default: ./novel.json)")
    p_rev.add_argument("--port", type=int, default=7878)
    p_rev.add_argument("--no-browser", action="store_true",
                       help="do not auto-open the browser")

    # Backward-compatible: if no subcommand, treat top-level flags as `workflow`
    if len(sys.argv) > 1 and sys.argv[1] not in {"workflow", "skill", "init", "review-outline"}:
        sys.argv.insert(1, "workflow")

    args = parser.parse_args()
    banner()
    if args.cmd == "workflow":
        return cmd_workflow(args)
    if args.cmd == "skill":
        return cmd_skill(args)
    if args.cmd == "init":
        return cmd_init(args)
    if args.cmd == "review-outline":
        return cmd_review_outline(args)
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
