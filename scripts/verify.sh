#!/usr/bin/env bash
# scripts/verify.sh — sanity-check the project structure
set -e
cd "$(dirname "$0")/.."

GREEN='\033[32m'; RED='\033[31m'; GOLD='\033[33m'; RESET='\033[0m'
ok()   { echo -e "  ${GREEN}✓${RESET} $1"; }
fail() { echo -e "  ${RED}✗${RESET} $1"; exit 1; }

echo -e "${GOLD}── Project structure verification ──${RESET}"

# count agents (we have 47; minimum 30)
n_agents=$(find agents -name "*.md" | wc -l)
[[ "$n_agents" -ge 30 ]] && ok "agents: $n_agents (>= 30 required)" || fail "only $n_agents agents (need 30+)"

# count skills (we have 65; minimum 60)
n_single=$(find skills/single -name "SKILL.md" | wc -l)
n_workflows=$(find skills/workflows -name "SKILL.md" | wc -l)
total=$((n_single + n_workflows))
[[ "$total" -ge 60 ]] && ok "skills: $total ($n_single single + $n_workflows workflows)" || fail "only $total skills (need 60+)"

# workflow YAMLs ≥ workflow skills
n_yaml=$(find orchestrator/workflows -name "*.yaml" | wc -l)
[[ "$n_yaml" -ge "$n_workflows" ]] && ok "workflow YAMLs: $n_yaml (≥ $n_workflows workflow skills)" || fail "yaml/skill mismatch"

# core files
for f in README.md LICENSE CLAUDE.md \
         orchestrator/runner.py orchestrator/workflow_engine.py orchestrator/novel_tree.py \
         sandbox/demo_novel.json sandbox/fixtures/llm_cache.json \
         sandbox/fixtures/02_locations.json sandbox/fixtures/05_hooks.json \
         output/pdf_compositor.py output/styles/manuscript.css \
         output/outline_reviewer.py output/outline_review.html \
         .claude/settings.json; do
  [[ -f "$f" ]] && ok "$f" || fail "$f missing"
done

# .claude mirror present
n_claude_agents=$(find .claude/agents -name "*.md" 2>/dev/null | wc -l)
n_claude_skills=$(find .claude/skills -name "SKILL.md" 2>/dev/null | wc -l)
[[ "$n_claude_agents" -ge 30 ]] && ok ".claude/agents mirror: $n_claude_agents" || fail ".claude/agents missing or too few ($n_claude_agents)"
[[ "$n_claude_skills" -ge 60 ]] && ok ".claude/skills mirror: $n_claude_skills" || fail ".claude/skills missing or too few ($n_claude_skills)"
[[ -f .claude/skills/start/SKILL.md ]] && ok ".claude/skills/start/SKILL.md present (so /start appears in Claude Code)" || fail ".claude/skills/start/SKILL.md missing"

# New (P1-P7) artifacts
[[ -f .claude/agents/quality/hook-auditor.md ]] && ok "agent hook-auditor present" || fail "missing hook-auditor agent"
[[ -f .claude/agents/worldbuilding/location-designer.md ]] && ok "agent location-designer present" || fail "missing location-designer agent"
[[ -f .claude/skills/audit-hooks/SKILL.md ]] && ok "skill /audit-hooks present" || fail "missing /audit-hooks"
[[ -f .claude/skills/build-location-bible/SKILL.md ]] && ok "skill /build-location-bible present" || fail "missing /build-location-bible"
[[ -f .claude/skills/review-outline/SKILL.md ]] && ok "skill /review-outline present" || fail "missing /review-outline"

echo ""
echo -e "${GOLD}── Orchestrator smoke ──${RESET}"
python3 orchestrator/novel_tree.py >/dev/null && ok "novel_tree.py runs (incl. hook audit)"
python3 -c "import sys; sys.path.insert(0,'.'); from orchestrator.agent_loader import load_all_agents; n=len(load_all_agents()); assert n >= 30, n; print(n)" >/dev/null && ok "agent_loader loads $(python3 -c "import sys; sys.path.insert(0,'.'); from orchestrator.agent_loader import load_all_agents; print(len(load_all_agents()))") agents"
python3 -c "import sys; sys.path.insert(0,'.'); from orchestrator.skill_loader import load_all_skills; n=len(load_all_skills()); assert n >= 60, n" && ok "skill_loader loads enough skills"
python3 -c "import sys; sys.path.insert(0,'.'); from orchestrator.runner import launch_outline_reviewer" && ok "runner.launch_outline_reviewer importable"

# sandbox + hook audit on the demo
python3 -c "
import sys, json; sys.path.insert(0,'.')
from sandbox import mock_runtime
from orchestrator import novel_tree as nt
t = mock_runtime.load_demo_tree()
assert t['metadata']['title'] == 'The Trial of Memory', t['metadata']['title']
assert len(t.get('hooks', [])) >= 10, 'too few hooks'
assert len(t.get('world_bible', {}).get('locations', [])) >= 8, 'too few locations'
audit = nt.audit_hooks(t)
assert audit['summary']['verdict'] == 'clean', json.dumps(audit['summary'])
print(f'  hooks: {len(t[\"hooks\"])} all resolved; locations: {len(t[\"world_bible\"][\"locations\"])}')
" && ok "sandbox demo: hooks resolved, locations present, audit clean"

# PDF compose
python3 output/pdf_compositor.py --novel sandbox/demo_novel.json --html-only >/dev/null 2>&1 && ok "pdf_compositor compiles HTML"
[[ -f manuscripts/the-trial-of-memory.html ]] && ok "manuscripts/the-trial-of-memory.html exists"

echo ""
echo -e "${GREEN}All checks passed.${RESET}"
