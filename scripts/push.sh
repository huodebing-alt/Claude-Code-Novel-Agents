#!/usr/bin/env bash
# scripts/push.sh — push to github.com/huodebing-alt/Claude-Code-Novel-Agents
#
# Usage:
#   ./scripts/push.sh                   # incremental commit + push
#   ./scripts/push.sh --first           # first push (init repo, set remote, push --set-upstream)
#   ./scripts/push.sh --message "..."   # custom commit message
#
# Requires:
#   - GitHub repo huodebing-alt/Claude-Code-Novel-Agents created (public, empty or with README)
#   - `gh auth status` returns logged-in (or SSH key configured)

set -euo pipefail

REPO="huodebing-alt/Claude-Code-Novel-Agents"
DEFAULT_MSG="chore: update atelier"
FIRST=false
MSG="$DEFAULT_MSG"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --first)   FIRST=true; shift;;
    --message) MSG="$2"; shift 2;;
    --help|-h)
      grep '^# ' "$0" | sed 's/^# //'
      exit 0;;
    *) echo "unknown arg: $1" >&2; exit 2;;
  esac
done

# ensure we're at project root (folder containing CLAUDE.md)
cd "$(dirname "$0")/.."
if [[ ! -f CLAUDE.md || ! -d agents || ! -d skills ]]; then
  echo "ERROR: not at project root (no CLAUDE.md / agents/ / skills/)" >&2
  exit 1
fi

if $FIRST; then
  if [[ ! -d .git ]]; then
    git init -b main
    git remote add origin "https://github.com/$REPO.git"
  fi
  git add -A
  git commit -m "chore: initial commit — 45 agents, 62 skills, sandbox demo, pdf"
  git push --set-upstream origin main
  echo "✓ Initial push to https://github.com/$REPO"
  echo ""
  echo "Next:"
  echo "  1. Visit https://github.com/$REPO/settings to add description + topics"
  echo "  2. Open Claude Code in the cloned repo and run /start"
  exit 0
fi

# Incremental
if ! git rev-parse --git-dir >/dev/null 2>&1; then
  echo "ERROR: not a git repo. Run with --first to initialize." >&2
  exit 1
fi

# show what changed
git status --short

# stage everything
git add -A

# only commit if there's something staged
if git diff --cached --quiet; then
  echo "nothing to commit"
  exit 0
fi

git commit -m "$MSG"
git push
echo "✓ Pushed: $MSG"
