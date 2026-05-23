#!/usr/bin/env python3
"""Outline Reviewer — local HTTP server for user review of the detailed outline.

Renders novel.outline as an editable HTML page. The user can:
  - Edit any beat field (facts / location_id / emotions / state_changes / hooks_*)
  - Drag beats to reorder within a chapter, and chapters within an act
  - Delete a beat or chapter; add a new (empty) beat anywhere
  - Inspect hook audit (opened-but-unresolved, dangling refs, etc.)
  - Save back to novel.json (atomic)
  - Click Done to shut the server down and continue the pipeline

Stdlib only (http.server + threading). No pip dependencies.

CLI:
    python output/outline_reviewer.py --novel novel.json --port 7878

Endpoints:
    GET  /                 → the HTML page
    GET  /api/novel        → current novel tree JSON
    GET  /api/audit        → hook audit report
    POST /api/save         → save the (modified) novel tree
    POST /api/done         → signal the workflow to continue (server exits)
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(HERE)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from orchestrator import novel_tree as nt

DEFAULT_HTML = os.path.join(HERE, "outline_review.html")


class _State:
    novel_path: str = "novel.json"
    html_path: str = DEFAULT_HTML
    done_event = threading.Event()


def _read(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()


def _json_response(handler: BaseHTTPRequestHandler, status: int, payload: Any) -> None:
    body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
    handler.send_response(status)
    handler.send_header("content-type", "application/json; charset=utf-8")
    handler.send_header("content-length", str(len(body)))
    handler.send_header("cache-control", "no-store")
    handler.end_headers()
    handler.wfile.write(body)


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt: str, *args: Any) -> None:
        # quieter logs
        sys.stderr.write("[reviewer] " + fmt % args + "\n")

    # GET endpoints ------------------------------------------------
    def do_GET(self) -> None:
        if self.path == "/" or self.path == "/index.html":
            body = _read(_State.html_path)
            self.send_response(200)
            self.send_header("content-type", "text/html; charset=utf-8")
            self.send_header("content-length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if self.path == "/api/novel":
            tree = nt.load_tree(_State.novel_path)
            return _json_response(self, 200, tree)
        if self.path == "/api/audit":
            tree = nt.load_tree(_State.novel_path)
            return _json_response(self, 200, nt.audit_hooks(tree))
        if self.path == "/api/health":
            return _json_response(self, 200, {"ok": True, "novel": _State.novel_path})
        self.send_response(404); self.end_headers()

    # POST endpoints -----------------------------------------------
    def do_POST(self) -> None:
        length = int(self.headers.get("content-length", "0") or 0)
        raw = self.rfile.read(length) if length else b""

        if self.path == "/api/save":
            try:
                tree = json.loads(raw.decode("utf-8")) if raw else {}
                nt.save_tree(tree, _State.novel_path)
                audit = nt.audit_hooks(tree)
                return _json_response(self, 200, {"saved": True, "audit": audit["summary"]})
            except Exception as e:
                return _json_response(self, 400, {"saved": False, "error": str(e)})

        if self.path == "/api/done":
            _State.done_event.set()
            return _json_response(self, 200, {"done": True})

        self.send_response(404); self.end_headers()


def serve(novel_path: str, port: int = 7878, open_browser: bool = True,
          html_path: str = DEFAULT_HTML) -> None:
    _State.novel_path = novel_path
    _State.html_path = html_path
    _State.done_event = threading.Event()

    if not os.path.exists(html_path):
        print(f"outline_review.html not found at {html_path}", file=sys.stderr)
        sys.exit(2)
    if not os.path.exists(novel_path):
        print(f"novel.json not found at {novel_path}", file=sys.stderr)
        sys.exit(2)

    httpd = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    url = f"http://127.0.0.1:{port}/"
    print(f"▶ Outline Reviewer at {url}")
    print(f"  novel: {novel_path}")
    print(f"  When you are done editing, click 'Done — continue pipeline' in the UI.")
    print(f"  Or press Ctrl-C to abort.")

    server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    server_thread.start()
    if open_browser:
        try:
            webbrowser.open(url)
        except Exception:
            pass

    try:
        # Block until /api/done is hit
        while not _State.done_event.wait(timeout=0.5):
            pass
        print("✓ User signaled Done. Shutting down reviewer.")
    except KeyboardInterrupt:
        print("\n× Aborted by user (Ctrl-C). Outline has not been finalized.")
    finally:
        httpd.shutdown()
        httpd.server_close()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--novel", default="novel.json")
    ap.add_argument("--port", type=int, default=7878)
    ap.add_argument("--no-browser", action="store_true")
    ap.add_argument("--html", default=DEFAULT_HTML)
    args = ap.parse_args()
    serve(args.novel, port=args.port, open_browser=not args.no_browser, html_path=args.html)
    return 0


if __name__ == "__main__":
    sys.exit(main())
