#!/usr/bin/env bash
# Build-verify matrix for the onboarding prune.
#
# Copies the working tree into throwaway dirs, runs onboard.py for representative
# feature combos, and asserts each pruned/renamed KB still lints clean, carries
# zero leftover markers, keeps its symlinks and references consistent, and passes
# the tooling checks. This is the safety net that guarantees the subtractive
# prune never produces a broken KB.
#
# Usage: bash .template/verify_matrix.sh
set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
EXCLUDES=(
  --exclude .git --exclude __pycache__ --exclude '*.pyc'
  --exclude .pytest_cache --exclude .ruff_cache --exclude .obsidian
  --exclude BUILD_SPEC.md
)

fail=0

# Post-prune consistency the linter can't see:
#   1. CLAUDE.md -> AGENTS.md and .claude/skills -> .agents/skills symlinks intact
#   2. no surviving file references a pruned skill directory
#   3. .mcp.json present iff mcp/server.py present (the mcp-server feature seam)
#   4. every surviving skill dir still has its SKILL.md
check_consistency() {
  python3 - "$1" <<'PY'
import re, sys, pathlib
root = pathlib.Path(sys.argv[1])
problems = []

for link, target in (("CLAUDE.md", "AGENTS.md"), (".claude/skills", ".agents/skills")):
    p = root / link
    if not p.is_symlink() or not p.exists():
        problems.append(f"symlink broken: {link}")

ref_re = re.compile(r"\.agents/skills/([\w-]+)")
skip = {".git", ".template", "raw", ".obsidian", "__pycache__"}
for p in root.rglob("*"):
    parts = p.relative_to(root).parts
    if p.is_dir() or p.is_symlink() or any(s in parts for s in skip):
        continue
    if p.suffix not in {".md", ".toml", ".json"}:
        continue
    for name in set(ref_re.findall(p.read_text(encoding="utf-8", errors="ignore"))):
        if not (root / ".agents/skills" / name).is_dir():
            problems.append(f"{p.relative_to(root)} references deleted skill: {name}")

has_json = (root / ".mcp.json").exists()
has_server = (root / "mcp/server.py").exists()
if has_json != has_server:
    problems.append(f".mcp.json present={has_json} but mcp/server.py present={has_server}")

skills_dir = root / ".agents/skills"
if skills_dir.exists():
    for d in skills_dir.iterdir():
        if d.is_dir() and not (d / "SKILL.md").exists():
            problems.append(f"skill dir without SKILL.md: {d.relative_to(root)}")

if problems:
    for msg in problems:
        print(f"  {msg}")
    sys.exit(1)
print("  config consistent: symlinks, skill refs, mcp seam OK")
PY
}

run_case() {
  local name="$1"; shift
  local tmp; tmp="$(mktemp -d)"
  local case_fail=0
  echo "=== case: ${name}  [onboard $*] ==="
  rsync -a "${EXCLUDES[@]}" "$ROOT/" "$tmp/" >/dev/null

  if ! python3 "$tmp/.template/onboard.py" "$@" --apply >/dev/null; then
    echo "  ❌ onboard.py failed"; fail=1; rm -rf "$tmp"; return
  fi

  if ! (cd "$tmp" && python3 scripts/lint.py); then
    echo "  ❌ ${name}: lint FAILED"; case_fail=1
  fi

  local leftovers
  leftovers="$(grep -rI "sf:begin\|sf:end\|sf:keep-if" "$tmp" \
      --exclude-dir=.template --exclude-dir=.git 2>/dev/null)"
  if [ -n "$leftovers" ]; then
    echo "  ❌ ${name}: leftover markers:"; echo "$leftovers" | head -5; case_fail=1
  fi

  if ! check_consistency "$tmp"; then
    echo "  ❌ ${name}: config consistency FAILED"; case_fail=1
  fi

  if ! (cd "$tmp" && uvx ruff check --quiet scripts .template); then
    echo "  ❌ ${name}: ruff FAILED"; case_fail=1
  fi
  if ! (cd "$tmp" && uvx --with pytest pytest -q scripts .template >/dev/null); then
    echo "  ❌ ${name}: pytest FAILED"; case_fail=1
  fi

  if [ -f "$tmp/mcp/server.py" ]; then
    if ! (cd "$tmp" && uv run --quiet mcp/server.py --help >/dev/null); then
      echo "  ❌ ${name}: mcp server --help FAILED"; case_fail=1
    fi
  fi

  if [ $case_fail -eq 0 ]; then
    echo "  ✅ ${name}: lint + markers + consistency + tooling OK"
  else
    fail=1
  fi
  rm -rf "$tmp"
  echo
}

run_case "full + rename"  --keep product,orchestrator,media-capture,mcp-server --slug testkb --brand TestKB
run_case "research-only"  --keep orchestrator,media-capture,mcp-server
run_case "leaf"           --keep product,media-capture,mcp-server
run_case "minimal"        --keep ""

if [ $fail -eq 0 ]; then echo "ALL CASES PASSED"; else echo "SOME CASES FAILED"; fi
exit $fail
