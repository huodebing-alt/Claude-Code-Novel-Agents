# Deployment

How to push this project to GitHub and how to use it as a Claude Code project.

## Prerequisites

- A GitHub account (`huodebing-alt` is the canonical owner; replace with your own fork)
- `git` configured locally with that account's credentials
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) for running the slash commands
- Python 3.10+ for the orchestrator
- `pandoc` (recommended) for PDF output

## Push to GitHub

1. **Create the empty repository** on GitHub:
   - Name: `Claude-Code-Novel-Agents`
   - Visibility: public
   - Do not initialize with README/LICENSE/gitignore (this repo already has them)

2. **Push from your machine**:

   ```bash
   cd Claude-Code-Novel-Agents
   ./scripts/push.sh --first
   ```

   Or manually:

   ```bash
   git init -b main
   git remote add origin https://github.com/huodebing-alt/Claude-Code-Novel-Agents.git
   git add .
   git commit -m "initial commit"
   git push -u origin main
   ```

3. **Add description + topics** in the GitHub UI (Settings → General):
   - Description: *"The literary counterpart of Claude-Code-Game-Studios — 45 agents, 62 skills, a multi-agent atelier for long-form fiction."*
   - Topics (paste at once):
     ```
     ai-novel-writing multi-agent claude-code claude-code-plugin
     fiction-writing creative-writing python pandoc
     pdf-generation save-the-cat three-act-structure character-bible
     worldbuilding claude-agents subagents authoring-tool
     novel-writing-software ai-fiction-writer ai-storytelling
     ```

## Use as a Claude Code project (primary path — no API key needed)

```bash
git clone https://github.com/huodebing-alt/Claude-Code-Novel-Agents.git my-novel
cd my-novel
claude
# In Claude Code:
/start
```

Claude Code auto-discovers the 47 agents in `.claude/agents/` and the 65 skills in `.claude/skills/`. The slash commands (`/start`, `/full-novel-pipeline`, `/write-chapter`, etc.) appear immediately after the session opens.

**No `ANTHROPIC_API_KEY` is required.** Subagents run inside your Claude Code session, which is already authenticated by whatever you set up when you installed CC (subscription, your own key, etc.). The model preset (all_opus / balanced / budget) you pick during onboarding determines which Anthropic model each subagent uses; usage is billed to your CC plan.

If your `/start` command does not appear, your repo is probably missing the `.claude/` mirror — see "Re-mirror `.claude/`" below.

## Optional: use as a standalone Python orchestrator (only path that needs an API key)

This is a secondary, optional path for users who want to drive the pipeline from a Python CLI (for scripting, CI, or just preference) rather than from inside a Claude Code session. The orchestrator makes API calls directly.

```bash
cp config/novel_meta.example.yaml config/novel_meta.yaml
cp config/llm_config.example.yaml config/llm_config.yaml

# Sandbox demo (no key — uses cached fixtures)
python3 orchestrator/runner.py workflow --workflow sandbox-demo --sandbox

# Real run (this path DOES need ANTHROPIC_API_KEY)
export ANTHROPIC_API_KEY=sk-ant-...
python3 orchestrator/runner.py workflow --workflow full-novel-pipeline --mode semi
```

## Compile the PDF

```bash
python output/pdf_compositor.py --novel sandbox/demo_novel.json
# Output → manuscripts/the-trial-of-memory.{html,pdf}
```

The compositor tries pandoc/WeasyPrint/wkhtmltopdf/Chromium in that order and falls back to "open the HTML in a browser and Print to PDF" if no PDF engine is present.

## GitHub Actions CI

`.github/workflows/verify.yml` runs on every push/PR:

- `scripts/verify.sh` — structural integrity (counts, files, smoke tests)

Add a status badge to `README.md`:

```markdown
![CI](https://github.com/huodebing-alt/Claude-Code-Novel-Agents/actions/workflows/verify.yml/badge.svg)
```

## Re-mirror `.claude/`

The repo ships with `.claude/agents/` and `.claude/skills/` populated. If you add a new agent or skill, re-mirror them so Claude Code picks it up:

```bash
mkdir -p .claude/agents .claude/skills
cp -r agents/* .claude/agents/
cp -r skills/single/* skills/workflows/* .claude/skills/
```

This is the same command you run if you cloned an older version of the repo that didn't include the `.claude/` directories.

## Optional: GitHub Pages for docs

If you want the `docs/*.md` browsable on GitHub Pages:

1. Settings → Pages → Source: `Deploy from a branch` → `main` → `/docs`
2. Add a `docs/_config.yml` with `theme: minima` (or another Jekyll theme)
