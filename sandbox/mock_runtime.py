"""Sandbox runtime: shims `llm_backend.call` to return fixtures.

This module is imported (or its function patched in) when the orchestrator
runs with --sandbox. It does NOT touch the network. Returns canned outputs
from sandbox/fixtures/llm_cache.json keyed by (agent_name, input_hash) or
by agent_name as a generic fallback.

Usage:
    # programmatic
    from sandbox import mock_runtime
    mock_runtime.activate()

    # via runner
    python orchestrator/runner.py --sandbox
"""
from __future__ import annotations

import json
import os
from typing import Optional


FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
CACHE_PATH = os.path.join(FIXTURES_DIR, "llm_cache.json")


def load_cache() -> dict:
    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def get_response(agent_name: str, input_hash: Optional[str] = None) -> str:
    """Return cached output for (agent, input_hash) or agent-generic fallback."""
    cache = load_cache()
    if input_hash:
        key = f"{agent_name}:{input_hash}"
        if key in cache:
            return cache[key]
    if agent_name in cache:
        return cache[agent_name]
    return f"[SANDBOX_PLACEHOLDER for {agent_name}]"


def activate() -> None:
    """Force sandbox by unsetting ANTHROPIC_API_KEY in this process."""
    os.environ.pop("ANTHROPIC_API_KEY", None)


def load_demo_tree() -> dict:
    """Load the fully-populated demo tree for sandbox launches."""
    demo_path = os.path.join(os.path.dirname(__file__), "demo_novel.json")
    if not os.path.exists(demo_path):
        raise FileNotFoundError(f"missing {demo_path}")
    with open(demo_path, "r", encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    activate()
    cache = load_cache()
    print(f"Loaded sandbox cache with {len(cache)} entries.")
    tree = load_demo_tree()
    print(f"Loaded demo tree: title={tree['metadata'].get('title')}, "
          f"chapters={sum(len(a.get('chapters', [])) for a in tree['outline']['acts'])}")
