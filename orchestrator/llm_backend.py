"""Thin Anthropic API client using urllib only (no pip dep on `anthropic`).

In sandbox mode (or when ANTHROPIC_API_KEY is unset), responses are returned
from `sandbox/fixtures/llm_cache.json` keyed by (agent_name, input_hash).

The default model across the project is `claude-opus-4-7`. Model selection is
done upstream in `workflow_engine._resolve_model()` which respects the user's
choice from `config/llm_config.yaml` (set during onboarding by api-config-agent).
"""
from __future__ import annotations

import hashlib
import json
import os
import time
import urllib.error
import urllib.request
from typing import Any


ANTHROPIC_BASE = "https://api.anthropic.com/v1/messages"
ANTHROPIC_VERSION = "2023-06-01"

_SANDBOX_CACHE: dict | None = None


def _input_hash(system: str, user: str, model: str) -> str:
    raw = f"{model}\n{system}\n{user}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:16]


def _load_sandbox_cache(path: str) -> dict:
    global _SANDBOX_CACHE
    if _SANDBOX_CACHE is None:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                _SANDBOX_CACHE = json.load(f)
        else:
            _SANDBOX_CACHE = {}
    return _SANDBOX_CACHE


def is_sandbox_mode(llm_config: dict) -> bool:
    if llm_config.get("sandbox", {}).get("enabled"):
        return True
    if not os.environ.get("ANTHROPIC_API_KEY"):
        return True
    return False


def call(
    *,
    agent_name: str,
    model: str,
    system: str,
    user: str,
    max_tokens: int = 4096,
    temperature: float = 0.7,
    llm_config: dict | None = None,
) -> str:
    """Make a single Claude API call. Returns plain-text content.

    In sandbox mode, returns cached output from llm_cache.json or a fallback
    placeholder if the (agent, input) pair is uncached.
    """
    cfg = llm_config or {}
    sandbox = is_sandbox_mode(cfg)
    h = _input_hash(system, user, model)

    if sandbox:
        cache_path = cfg.get("sandbox", {}).get(
            "llm_cache", "sandbox/fixtures/llm_cache.json"
        )
        cache = _load_sandbox_cache(cache_path)
        key = f"{agent_name}:{h}"
        if key in cache:
            return cache[key]
        # fallback to generic agent-level cached response
        if agent_name in cache:
            return cache[agent_name]
        # last resort: empty stub with a tag
        return f"[SANDBOX_PLACEHOLDER for {agent_name} hash={h}]"

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError(
            "ANTHROPIC_API_KEY not set and sandbox not enabled. "
            "Run with --sandbox or `export ANTHROPIC_API_KEY=...`"
        )

    payload = {
        "model": model,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "system": system,
        "messages": [{"role": "user", "content": user}],
    }
    req = urllib.request.Request(
        ANTHROPIC_BASE,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "x-api-key": api_key,
            "anthropic-version": ANTHROPIC_VERSION,
            "content-type": "application/json",
        },
        method="POST",
    )

    max_attempts = (cfg.get("retry", {}) or {}).get("max_attempts", 3)
    delay = (cfg.get("retry", {}) or {}).get("initial_delay_seconds", 2)
    backoff = (cfg.get("retry", {}) or {}).get("backoff_multiplier", 2)
    timeout = (cfg.get("timeout", {}) or {}).get("request_seconds", 120)

    last_err: Exception | None = None
    for attempt in range(1, max_attempts + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            # Anthropic format: {"content": [{"type":"text","text":"..."}], ...}
            parts = data.get("content", [])
            text = "".join(p.get("text", "") for p in parts if p.get("type") == "text")
            return text
        except urllib.error.HTTPError as e:
            last_err = e
            if e.code in (429, 500, 502, 503, 504) and attempt < max_attempts:
                time.sleep(delay)
                delay *= backoff
                continue
            raise
        except (urllib.error.URLError, TimeoutError) as e:
            last_err = e
            if attempt < max_attempts:
                time.sleep(delay)
                delay *= backoff
                continue
            raise
    if last_err:
        raise last_err
    return ""


def capture_to_cache(
    *,
    agent_name: str,
    model: str,
    system: str,
    user: str,
    output: str,
    cache_path: str,
) -> None:
    """Record a (agent, input) → output mapping for later sandbox replay."""
    h = _input_hash(system, user, model)
    key = f"{agent_name}:{h}"
    cache: dict = {}
    if os.path.exists(cache_path):
        with open(cache_path, "r", encoding="utf-8") as f:
            cache = json.load(f)
    cache[key] = output
    cache[agent_name] = output  # generic fallback
    os.makedirs(os.path.dirname(cache_path) or ".", exist_ok=True)
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    # Sandbox smoke test
    os.environ.pop("ANTHROPIC_API_KEY", None)
    out = call(
        agent_name="theme-brainstorm",
        model="claude-sonnet-4-6",
        system="You generate themes.",
        user="Seed: a synesthete prosecutor.",
        llm_config={"sandbox": {"enabled": True, "llm_cache": "/tmp/nonexistent.json"}},
    )
    print("sandbox call returned:", out[:80])
