#!/usr/bin/env python3
"""MycoForge audit — the numbers behind the /audit report.

Read-only: runs the KB's own checks and prints what they found, so the report's
counts come from here and the agent only summarizes them. Pure stdlib.

Parts, each printed as soon as it finishes:
  * lint — ``scripts/lint.py`` output, as printed
  * vendored skills — the KB's ``scripts/check-vendored-skills.sh`` output, as printed
  * architecture — pages under ``architecture/`` whose ``watches:`` changed since  # sf:keep-if(architecture)
    their ``commit:``, rendered diagrams stale since their ``candidate.json``  # sf:keep-if(architecture)
    revision, uncommitted changes under watched paths, and files added under an  # sf:keep-if(architecture)
    overview's ``new_entries:`` since its commit; a page whose check could not  # sf:keep-if(architecture)
    run is ``incomplete``, never ``current``  # sf:keep-if(architecture)
  * scout (``--scout``) — the latest run section of ``staging/scout.md`` and  # sf:keep-if(insight)
    counts of open, approved and unreachable entries  # sf:keep-if(insight)

Exit status: non-zero if lint reported an error or a part crashed.

Usage:
    python3 scripts/audit.py [--root <kb-root>]   # every part but scout
    python3 scripts/audit.py --architecture        # architecture only  # sf:keep-if(architecture)
    python3 scripts/audit.py --scout               # scout ledger only  # sf:keep-if(insight)
"""

from __future__ import annotations

import argparse
import datetime as dt  # sf:keep-if(insight)
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


def git(root: Path, *args: str) -> list[str] | None:
    """Output lines of a git command, or None if it failed."""
    code, out = run_cmd(root, "git", "-c", "core.quotePath=false", *args)
    if code != 0:
        return None
    return out.splitlines() if out else []


def lint_part(root: Path) -> tuple[int, str]:
    return run_cmd(root, sys.executable, str(SCRIPTS / "lint.py"), "--root", str(root))


def vendored_part(root: Path) -> str:
    check = root / "scripts" / "check-vendored-skills.sh"
    if not check.exists():
        return "vendored skills: no scripts/check-vendored-skills.sh in this KB"
    code, out = run_cmd(root, "bash", str(check))
    return out if code == 0 else f"{out}\nvendored check failed (exit {code})"


# sf:begin(architecture)
def as_list(value: object) -> list[str]:
    """A frontmatter field as a list: a bare scalar is one entry."""
    if isinstance(value, list):
        return [v for v in value if v]
    return [value] if isinstance(value, str) and value else []


def commit_exists(root: Path, commit: str) -> bool:
    return run_cmd(root, "git", "cat-file", "-e", f"{commit}^{{commit}}")[0] == 0


def diagram_revision(page_dir: Path, text: str) -> tuple[str, str] | None:
    """Return (diagram dir, revision) for a page with a rendered diagram; revision is
    empty when candidate.json is missing or carries no usable revision."""
    m = DIAGRAM_LINK_RE.search(text)
    if not m:
        return None
    candidate = page_dir / m.group(1) / "candidate.json"
    try:
        revision = json.loads(candidate.read_text(encoding="utf-8"))["meta"]["repository"]["revision"]
    except (OSError, ValueError, KeyError, TypeError):
        revision = None
    return m.group(1), revision if isinstance(revision, str) else ""


def architecture_part(root: Path) -> str:
    from lint import parse_frontmatter  # local: cut with the feature
    arch = root / "architecture"
    pages = sorted(arch.glob("*.md")) if arch.is_dir() else []
    pages = [(p, p.read_text(encoding="utf-8")) for p in pages]
    pages = [(p, text, parse_frontmatter(text)) for p, text in pages]
    pages = [(p, text, meta) for p, text, meta in pages if meta.get("type") == "architecture"]
    if not pages:
        return "architecture: no pages"

    state: dict[str, str] = {}  # page -> stale | incomplete | current
    stale, incomplete, stale_diagrams, uncommitted, new = [], [], [], [], []
    for page, text, meta in pages:
        state[page.stem] = "current"
        commit = meta.get("commit") if isinstance(meta.get("commit"), str) else ""
        watches = as_list(meta.get("watches"))
        if not watches:
            state[page.stem] = "incomplete"
            incomplete.append(f"  incomplete {page.stem}: no watches")
            continue
        if not commit or not commit_exists(root, commit):
            state[page.stem] = "stale"
            stale.append(f"  stale {page.stem}: commit {commit or '(none)'} not found")
        else:
            changed = git(root, "diff", "--name-only", commit, "HEAD", "--", *watches)
            if changed is None:
                state[page.stem] = "incomplete"
                incomplete.append(f"  incomplete {page.stem}: git diff failed over {', '.join(watches)}")
            elif changed:
                state[page.stem] = "stale"
                stale.append(f"  stale {page.stem} (commit {commit}): {', '.join(changed)}")
        dirty = (git(root, "diff", "--name-only", "HEAD", "--", *watches) or []) \
            + (git(root, "ls-files", "--others", "--exclude-standard", "--", *watches) or [])
        if dirty:
            uncommitted.append(f"  uncommitted under {page.stem}'s watches: {', '.join(dirty)}")
        if diagram := diagram_revision(page.parent, text):
            where, revision = diagram
            if not revision:
                stale_diagrams.append(f"  stale diagram {where}: no revision in candidate.json")
            elif not commit_exists(root, revision):
                stale_diagrams.append(f"  stale diagram {where}: revision {revision[:7]} not found")
            else:
                changed = git(root, "diff", "--name-only", revision, "HEAD", "--", *watches)
                if changed is None:
                    incomplete.append(f"  incomplete diagram {where}: git diff failed")
                elif changed:
                    stale_diagrams.append(f"  stale diagram {where} (revision {revision[:7]}): "
                                          f"{', '.join(changed)}")
        entries = as_list(meta.get("new_entries"))
        if entries and commit and commit_exists(root, commit):
            added = git(root, "diff", "--name-only", "--diff-filter=A", commit, "HEAD", "--", *entries)
            if added is None:
                incomplete.append(f"  incomplete {page.stem}: git diff failed over new_entries")
            elif added:
                new.append(f"  new under {page.stem}'s new_entries since {commit}: {', '.join(added)}")

    counts = list(state.values())
    head = (f"architecture: {len(pages)} page(s) — {counts.count('stale')} stale, "
            f"{counts.count('current')} current, {counts.count('incomplete')} incomplete, "
            f"{len(stale_diagrams)} stale diagram(s)")
    return "\n".join([head, *stale, *incomplete, *stale_diagrams, *uncommitted, *new])
# sf:end(architecture)


# sf:begin(insight)
def status_cells(section: str) -> list[str]:
    """Last cell of every numbered ledger table row."""
    rows = [line for line in section.splitlines()
            if line.startswith("|") and line.split("|")[1].strip().isdigit()]
    return [row.rstrip(" |").rsplit("|", 1)[-1].strip() for row in rows]


def is_run_header(chunk: str) -> bool:
    """True when a chunk split on '## [' opens with a dated run header."""
    try:
        dt.date.fromisoformat(chunk[:10])
    except ValueError:
        return False
    return chunk[10:11] == "]"


def scout_part(root: Path) -> str:
    ledger = root / "staging" / "scout.md"
    if not ledger.exists():
        return "scout: no ledger at staging/scout.md"
    text = ledger.read_text(encoding="utf-8")
    runs = [chunk for chunk in ("\n" + text).split("\n## [")[1:] if is_run_header(chunk)]
    if not runs:
        return "scout: no runs in the ledger"
    latest = "## [" + runs[-1].strip()
    statuses = status_cells(text)
    unreachable = [line for line in latest.splitlines() if line.startswith("unreachable:")]
    dirty = git(root, "status", "--porcelain", "--", "staging/scout.md")
    changed = "unknown (git failed)" if dirty is None else "yes" if dirty else "no"
    head = (f"scout: latest run {runs[-1][:10]} — "
            f"{status_cells(latest).count('candidate')} new candidate(s); "
            f"ledger-wide {statuses.count('candidate')} candidate, {statuses.count('approved')} approved "
            f"awaiting capture; {len(unreachable)} unreachable line(s); "
            f"ledger uncommitted changes: {changed}")
    return f"{head}\n\n{latest}"
# sf:end(insight)


def emit(name: str, part) -> bool:
    """Print one part as soon as it finishes; a crash is reported, not fatal."""
    try:
        print(part(), flush=True)
    except Exception as exc:  # noqa: BLE001 — one broken part must not hide the rest
        print(f"{name}: check crashed: {exc!r}", flush=True)
        return False
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description="Print the numbers behind the /audit report.")
    ap.add_argument("--root", type=Path,
                    default=Path(__file__).resolve().parent.parent,
                    help="KB root (default: the repo containing this script)")
    ap.add_argument("--architecture", action="store_true",  # sf:keep-if(architecture)
                    help="architecture staleness only")  # sf:keep-if(architecture)
    ap.add_argument("--scout", action="store_true",  # sf:keep-if(insight)
                    help="scout ledger only")  # sf:keep-if(insight)
    args = ap.parse_args()
    root = args.root.resolve()

    if args.architecture:  # sf:keep-if(architecture)
        return 0 if emit("architecture", lambda: architecture_part(root)) else 1  # sf:keep-if(architecture)
    if args.scout:  # sf:keep-if(insight)
        return 0 if emit("scout", lambda: scout_part(root)) else 1  # sf:keep-if(insight)

    code, lint_out = lint_part(root)
    print(lint_out + "\n", flush=True)
    ok = emit("vendored skills", lambda: vendored_part(root))
    print(flush=True)  # sf:keep-if(architecture)
    ok = emit("architecture", lambda: architecture_part(root)) and ok  # sf:keep-if(architecture)
    return 1 if code or not ok else 0


if __name__ == "__main__":
    sys.exit(main())
