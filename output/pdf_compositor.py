#!/usr/bin/env python3
"""PDF compositor — assembles a print-ready PDF from a novel tree.

Pipeline:
  1. Read novel.json (or sandbox/demo_novel.json)
  2. Render chapter markdown → HTML paragraphs
  3. Substitute into output/template.html
  4. Write the standalone HTML to manuscripts/<slug>.html
  5. Attempt PDF generation via, in order:
        a. weasyprint (if installed)
        b. wkhtmltopdf (if installed)
        c. pandoc + xelatex (if installed)
        d. Chromium headless (if installed)
        e. fallback: print instructions for browser "Save as PDF"

The fallback path is deliberate — in many environments you only need the
HTML; the user prints to PDF from their browser, which gives them control
over the page count and the print settings.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from typing import Any


HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(HERE)
DEFAULT_TEMPLATE = os.path.join(HERE, "template.html")
DEFAULT_CSS = os.path.join(HERE, "styles", "manuscript.css")


# ---------------- helpers ----------------

def slugify(s: str) -> str:
    s = re.sub(r"[^\w\s-]", "", (s or "untitled")).strip().lower()
    return re.sub(r"[\s_-]+", "-", s)


def markdown_to_html(text: str) -> str:
    """Tiny markdown → HTML converter (paragraphs + scene-break `## §`).

    Sufficient for our chapter text (we control the input format).
    """
    out: list[str] = []
    paras = re.split(r"\n\s*\n", text.strip())
    for p in paras:
        p = p.strip()
        if not p:
            continue
        if p.startswith("# "):
            continue  # chapter title is handled by the template
        if p in ("## §", "## §"):
            out.append('<div class="scenebreak">§</div>')
        elif p.startswith("## "):
            out.append(f'<div class="scenebreak">{p[3:].strip()}</div>')
        else:
            out.append(f"<p>{p.replace(chr(10), ' ')}</p>")
    return "\n".join(out)


def render_template(template: str, ctx: dict[str, Any]) -> str:
    """Tiny mustache-ish renderer: {{KEY}}, {{#LIST}}...{{/LIST}}, {{#IF}}...{{/IF}}."""
    # Sections {{#NAME}}...{{/NAME}} — list or truthy
    def section_replace(m: re.Match) -> str:
        name = m.group(1)
        body = m.group(2)
        val = ctx.get(name)
        if not val:
            return ""
        if isinstance(val, list):
            out: list[str] = []
            for item in val:
                sub_ctx = {**ctx, **(item if isinstance(item, dict) else {"VALUE": item})}
                out.append(render_template(body, sub_ctx))
            return "".join(out)
        if isinstance(val, dict):
            return render_template(body, {**ctx, **val})
        # truthy scalar
        return body

    sec_re = re.compile(r"\{\{#([A-Z_]+)\}\}(.*?)\{\{/\1\}\}", re.DOTALL)
    while True:
        new = sec_re.sub(section_replace, template)
        if new == template:
            break
        template = new

    # Scalars {{NAME}}
    def scalar_replace(m: re.Match) -> str:
        key = m.group(1)
        if key in ctx:
            return str(ctx[key]) if ctx[key] is not None else ""
        return ""
    return re.sub(r"\{\{([A-Z_]+)\}\}", scalar_replace, template)


# ---------------- main compose ----------------

def compose_html(novel: dict, *, template_path: str = DEFAULT_TEMPLATE) -> tuple[str, dict]:
    meta = novel.get("metadata", {})
    title = meta.get("title", "Untitled")
    title_zh = meta.get("title_zh") or ""
    author = meta.get("author", "Anonymous")
    genre = meta.get("genre", "")
    year = 2026

    blurb = (novel.get("manuscript", {}) or {}).get("blurb") or ""
    if isinstance(blurb, dict):
        blurb = blurb.get("text") or json.dumps(blurb, ensure_ascii=False)

    acknowledgments = (
        "Generated end-to-end by the Claude Code Novel Agents atelier. "
        "Forty-five agents, sixty-two skills, six phases. The atelier is the "
        "literary counterpart of Claude Code Game Studios. For the full pipeline, see "
        "github.com/huodebing-alt/Claude-Code-Novel-Agents."
    )

    chapters_ctx = []
    for act_idx, act in enumerate(novel.get("outline", {}).get("acts", [])):
        for ch_idx, ch in enumerate(act.get("chapters", [])):
            num = sum(
                len(a.get("chapters", []))
                for a in novel["outline"]["acts"][:act_idx]
            ) + ch_idx + 1
            body_text = ch.get("compiled_text") or ""
            if not body_text:
                # assemble from beats
                body_text = "\n\n".join((b.get("text") or "") for b in ch.get("beats", []))
            html_body = markdown_to_html(body_text)
            chapters_ctx.append({
                "NUM": num,
                "TITLE": ch.get("title", f"Chapter {num}"),
                "BODY": html_body,
            })

    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    ctx = {
        "TITLE": title,
        "TITLE_ZH": title_zh,
        "AUTHOR": author,
        "GENRE": genre,
        "YEAR": year,
        "CHAPTERS": chapters_ctx,
        "BLURB": blurb,
        "ACKNOWLEDGMENTS": acknowledgments,
    }
    html = render_template(template, ctx)
    return html, {
        "chapter_count": len(chapters_ctx),
        "wordcount": sum(
            len((ch.get("compiled_text") or "").split())
            for act in novel.get("outline", {}).get("acts", [])
            for ch in act.get("chapters", [])
        ),
    }


# ---------------- PDF backends ----------------

def try_weasyprint(html_path: str, pdf_path: str) -> bool:
    try:
        from weasyprint import HTML  # type: ignore
    except Exception:
        return False
    HTML(filename=html_path).write_pdf(pdf_path)
    return True


def try_wkhtmltopdf(html_path: str, pdf_path: str) -> bool:
    if not shutil.which("wkhtmltopdf"):
        return False
    cmd = ["wkhtmltopdf", "--enable-local-file-access", "-q",
           "-T", "18mm", "-B", "20mm", "-L", "14mm", "-R", "14mm",
           html_path, pdf_path]
    subprocess.run(cmd, check=True)
    return True


def try_chromium(html_path: str, pdf_path: str) -> bool:
    for binary in ("chromium", "chromium-browser", "google-chrome", "chrome"):
        if shutil.which(binary):
            url = "file://" + os.path.abspath(html_path)
            cmd = [binary, "--headless=new", "--no-sandbox", "--disable-gpu",
                   f"--print-to-pdf={pdf_path}", url]
            try:
                subprocess.run(cmd, check=True, capture_output=True, timeout=60)
                return os.path.exists(pdf_path)
            except Exception:
                continue
    return False


def try_pandoc(html_path: str, pdf_path: str) -> bool:
    if not shutil.which("pandoc"):
        return False
    try:
        cmd = ["pandoc", html_path, "-o", pdf_path,
               "--pdf-engine=xelatex",
               "-V", "geometry:paperwidth=5.5in,paperheight=8.5in,margin=0.7in",
               "-V", "mainfont=Cormorant Garamond"]
        subprocess.run(cmd, check=True, capture_output=True, timeout=120)
        return os.path.exists(pdf_path)
    except Exception:
        return False


# ---------------- CLI ----------------

def main() -> int:
    ap = argparse.ArgumentParser(description="Compile a novel tree to print-ready PDF")
    ap.add_argument("--novel", default="sandbox/demo_novel.json")
    ap.add_argument("--out", default=None, help="Output PDF path (default: manuscripts/<slug>.pdf)")
    ap.add_argument("--html-only", action="store_true", help="Only produce HTML; skip PDF")
    ap.add_argument("--template", default=DEFAULT_TEMPLATE)
    args = ap.parse_args()

    if not os.path.exists(args.novel):
        print(f"novel not found: {args.novel}", file=sys.stderr)
        return 2

    with open(args.novel, "r", encoding="utf-8") as f:
        novel = json.load(f)

    title = novel.get("metadata", {}).get("title", "Untitled")
    slug = slugify(title)
    out_dir = "manuscripts"
    os.makedirs(out_dir, exist_ok=True)

    html_path = os.path.join(out_dir, f"{slug}.html")
    pdf_path = args.out or os.path.join(out_dir, f"{slug}.pdf")

    print(f"▶ Composing HTML → {html_path}")
    html, stats = compose_html(novel, template_path=args.template)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    # Copy CSS next to HTML for relative <link> to work
    css_dst_dir = os.path.join(out_dir, "styles")
    os.makedirs(css_dst_dir, exist_ok=True)
    shutil.copy(DEFAULT_CSS, css_dst_dir)
    print(f"  chapters: {stats['chapter_count']} · words: {stats['wordcount']:,}")

    if args.html_only:
        print(f"✓ HTML ready. Open {html_path} in a browser and Print → Save as PDF.")
        return 0

    print(f"▶ Attempting PDF generation → {pdf_path}")
    for fn in (try_weasyprint, try_wkhtmltopdf, try_chromium, try_pandoc):
        try:
            if fn(html_path, pdf_path):
                print(f"✓ PDF written via {fn.__name__} → {pdf_path}")
                return 0
        except Exception as e:
            print(f"  {fn.__name__}: {type(e).__name__}: {e}")
            continue

    print()
    print("No PDF backend available in this environment.")
    print(f"The HTML is ready at: {html_path}")
    print("Options:")
    print("  1. Open the HTML in Chrome/Firefox/Safari → Print → Save as PDF")
    print("  2. pip install weasyprint  →  re-run this script")
    print("  3. Install wkhtmltopdf      →  re-run this script")
    return 0


if __name__ == "__main__":
    sys.exit(main())
