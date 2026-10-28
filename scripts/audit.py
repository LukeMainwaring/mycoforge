#!/usr/bin/env python3
"""MycoForge audit — the numbers behind the /audit report.

Read-only: runs the KB's own checks and prints what they found, so the report's
counts come from here and the agent only summarizes them. Pure stdlib.

Parts:
  * lint — ``scripts/lint.py`` output, as printed
  * vendored skills — ``scripts/check-vendored-skills.sh`` output, as printed
  * architecture — pages under ``architecture/`` whose ``watches:`` changed since
    their ``commit:``, rendered diagrams stale since their ``candidate.json``
    revision, uncommitted changes under watched paths, and files added under an
    overview's ``new_entries:`` since its commit
  * scout (``--scout``) — the latest run section of ``staging/scout.md`` and
    counts of open, approved and unreachable entries

Exit status: non-zero if lint reported an error; everything else exits 0.

Usage:
    python3 scripts/audit.py [--root <kb-root>]   # lint, vendored, architecture
    python3 scripts/audit.py --architecture        # architecture only
    python3 scripts/audit.py --scout               # scout ledger only
"""

from __future__ import annotations

import argparse
import json  # sf:keep-if(architecture)
import re  # sf:keep-if(architecture)
import subprocess
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent

# sf:begin(architecture)
DIAGRAM_LINK_RE = re.compile(r"Rendered with archify: \[[^\]]*\]\((diagrams/[^)]+?)/[^/)]+\.html\)")
# sf:end(architecture)


def run_cmd(root: Path, *cmd: str) -> tuple[int, str]:
    """Run a command in the KB root; return its exit code and combined output."""
    proc = subprocess.run(cmd, check=False, cwd=root, capture_output=True, text=True)
    return proc.returncode, (proc.stdout + proc.stderr).rstrip("\n")


def git(root: Path, *args: str) -> list[str]:
    code, out = run_cmd(root, "git", *args)
    return out.splitlines() if code == 0 and out else []


def lint_part(root: Path) -> tuple[int, str]:
    return run_cmd(root, sys.executable, str(SCRIPTS / "lint.py"), "--root", str(root))


def vendored_part(root: Path) -> str:
    code, out = run_cmd(root, "bash", str(SCRIPTS / "check-vendored-skills.sh"))
    return out if code == 0 else f"{out}\ncheck failed (exit {code})"


# sf:begin(architecture)
def commit_exists(root: Path, commit: str) -> bool:
    return run_cmd(root, "git", "cat-file", "-e", f"{commit}^{{commit}}")[0] == 0


def changed_since(root: Path, commit: str, paths: list[str]) -> list[str]:
    return git(root, "diff", "--name-only", commit, "HEAD", "--", *paths)


def diagram_revision(page_dir: Path, text: str) -> tuple[str, str] | None:
    """Return (diagram dir, revision) for a page with a rendered diagram."""
    m = DIAGRAM_LINK_RE.search(text)
    if not m:
        return None
    candidate = page_dir / m.group(1) / "candidate.json"
    try:
        revision = json.loads(candidate.read_text(encoding="utf-8"))["meta"]["repository"]["revision"]
    except (OSError, ValueError, KeyError, TypeError):
        return m.group(1), ""
    return m.group(1), revision


def architecture_part(root: Path) -> str:
    from lint import parse_frontmatter  # local: cut with the feature
    arch = root / "architecture"
    pages = sorted(arch.glob("*.md")) if arch.is_dir() else []
    pages = [(p, p.read_text(encoding="utf-8")) for p in pages]
    pages = [(p, text, parse_frontmatter(text)) for p, text in pages]
    pages = [(p, text, meta) for p, text, meta in pages if meta.get("type") == "architecture"]
    if not pages:
        return "architecture: no pages"

    stale, stale_diagrams, uncommitted, new = [], [], [], []
    for page, text, meta in pages:
        commit = meta.get("commit", "")
        watches = meta.get("watches") or []
        if not commit or not commit_exists(root, commit):
            stale.append(f"  stale {page.stem}: commit {commit or '(none)'} not found")
        elif changed := changed_since(root, commit, watches):
            stale.append(f"  stale {page.stem} (commit {commit}): {', '.join(changed)}")
        if watches and (dirty := git(root, "status", "--porcelain", "--", *watches)):
            uncommitted.append(f"  uncommitted under {page.stem}'s watches: "
                               f"{', '.join(line[3:] for line in dirty)}")
        if diagram := diagram_revision(page.parent, text):
            where, revision = diagram
            if not revision or not commit_exists(root, revision):
                stale_diagrams.append(f"  stale diagram {where}: revision {revision[:7] or '(none)'} not found")
            elif changed := changed_since(root, revision, watches):
                stale_diagrams.append(f"  stale diagram {where} (revision {revision[:7]}): {', '.join(changed)}")
        entries = meta.get("new_entries") or []
        if entries and commit and commit_exists(root, commit):
            added = git(root, "diff", "--name-only", "--diff-filter=A", commit, "HEAD", "--", *entries)
            if added:
                new.append(f"  new under {page.stem}'s new_entries since {commit}: {', '.join(added)}")

    head = (f"architecture: {len(pages)} page(s) — {len(stale)} stale, "
            f"{len(pages) - len(stale)} current, {len(stale_diagrams)} stale diagram(s)")
    return "\n".join([head, *stale, *stale_diagrams, *uncommitted, *new])
# sf:end(architecture)


# sf:begin(insight)
def status_cells(section: str) -> list[str]:
    """Last cell of every numbered ledger table row."""
    rows = [line for line in section.splitlines()
            if line.startswith("|") and line.split("|")[1].strip().isdigit()]
    return [row.rstrip(" |").rsplit("|", 1)[-1].strip() for row in rows]


def scout_part(root: Path) -> str:
    ledger = root / "staging" / "scout.md"
    if not ledger.exists():
        return "scout: no ledger at staging/scout.md"
    text = ledger.read_text(encoding="utf-8")
    runs = text.split("\n## [")
    if len(runs) < 2:
        return "scout: no runs in the ledger"
    latest = "## [" + runs[-1].strip()
    run_date = latest[4:14]
    statuses = status_cells(text)
    unreachable = [line for line in latest.splitlines() if line.startswith("unreachable:")]
    changed = "yes" if git(root, "status", "--porcelain", "--", "staging/scout.md") else "no"
    head = (f"scout: latest run {run_date} — "
            f"{status_cells(latest).count('candidate')} new candidate(s); "
            f"ledger-wide {statuses.count('candidate')} candidate, {statuses.count('approved')} approved "
            f"awaiting capture; {len(unreachable)} unreachable line(s); "
            f"ledger uncommitted changes: {changed}")
    return f"{head}\n\n{latest}"
# sf:end(insight)


def main() -> int:
    ap = argparse.ArgumentParser(description="Print the numbers behind the /audit report.")
    ap.add_argument("--root", type=Path,
                    default=Path(__file__).resolve().parent.parent,
                    help="KB root (default: the repo containing this script)")
    ap.add_argument("--architecture", action="store_true",  # sf:keep-if(architecture)
                    help="architecture staleness only")  # sf:keep-if(architecture)
    ap.add_argument("--scout", action="store_true",  # sf:keep-if(insight)
                    help="scout ledger only, after a /scout run")  # sf:keep-if(insight)
    args = ap.parse_args()
    root = args.root.resolve()

    if getattr(args, "architecture", False):
        print(architecture_part(root))  # sf:keep-if(architecture)
        return 0
    if getattr(args, "scout", False):
        print(scout_part(root))  # sf:keep-if(insight)
        return 0

    code, lint_out = lint_part(root)
    parts = [lint_out, vendored_part(root)]
    parts.append(architecture_part(root))  # sf:keep-if(architecture)
    print("\n\n".join(parts))
    return 1 if code else 0


if __name__ == "__main__":
    sys.exit(main())
