#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.14"
# dependencies = ["mcp>=2.3,<3"]
# ///
"""Read-only MCP server for this MycoForge knowledge base.

Exposes three tools over stdio — search_kb, read_page, get_index — so product
repos and other agent sessions can consult the KB. Deliberately read-only:
ingestion stays an interactive workflow inside the KB (see ADR-004).

Run:      uv run mcp/server.py
Register: .mcp.json in this repo; for a product repo, point the same command at
          this file by absolute path (see README).
Deps:     pinned in mcp/server.py.lock; `uv lock --script mcp/server.py --upgrade` to bump.
"""

import argparse
import shutil
import subprocess
import tomllib
from pathlib import Path

from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

KB_ROOT = Path(__file__).resolve().parent.parent
SEARCH_DIRS = ("wiki", "raw")
MAX_HITS = 50


def _kb_identity() -> tuple[str, str, str]:
    """(slug, version, instructions) from kb.toml; safe defaults if it's missing."""
    try:
        cfg = tomllib.loads((KB_ROOT / "kb.toml").read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError):
        cfg = {}
    kb = cfg.get("kb", {})
    slug = kb.get("slug", KB_ROOT.name)
    brand = kb.get("brand", slug)
    description = kb.get("description", "")
    version = cfg.get("template", {}).get("version", "0")
    instructions = (
        f"{brand} knowledge base — {description}. " if description else f"{brand} knowledge base. "
    ) + "Read-only: start with get_index for the page catalog, search_kb for full-text hits, read_page for a page."
    return slug, version, instructions


_SLUG, _VERSION, _INSTRUCTIONS = _kb_identity()
mcp = MCPServer(_SLUG, version=_VERSION, instructions=_INSTRUCTIONS)


def _search_dirs(scope: str | None) -> list[Path]:
    names = SEARCH_DIRS if scope in (None, "", "all") else (scope,)
    dirs = [KB_ROOT / n for n in names if (KB_ROOT / n).is_dir()]
    if not dirs:
        raise ToolError(f"scope must be one of {('all', *SEARCH_DIRS)}, got {scope!r}")
    return dirs


def _rg_search(query: str, dirs: list[Path]) -> list[str]:
    proc = subprocess.run(
        ["rg", "--no-heading", "--line-number", "--ignore-case",
         "--fixed-strings", "--max-count", "5", query, *(str(d) for d in dirs)],
        check=False, capture_output=True, text=True, cwd=KB_ROOT,
    )
    if proc.returncode not in (0, 1):  # 1 = no matches; anything else is an error
        raise RuntimeError(proc.stderr.strip())
    return proc.stdout.splitlines()


def _py_search(query: str, dirs: list[Path]) -> list[str]:
    needle = query.lower()
    hits: list[str] = []
    for d in dirs:
        for p in sorted(d.rglob("*.md")):
            try:
                lines = p.read_text(encoding="utf-8").splitlines()
            except (UnicodeDecodeError, OSError):
                continue
            per_file = 0
            for i, line in enumerate(lines, 1):
                if needle in line.lower():
                    hits.append(f"{p}:{i}:{line.strip()}")
                    per_file += 1
                    if per_file >= 5:
                        break
    return hits


@mcp.tool()
def search_kb(query: str, scope: str | None = None) -> str:
    """Full-text search over the KB. scope: 'wiki', 'raw', or 'all' (default)."""
    dirs = _search_dirs(scope)
    hits = _rg_search(query, dirs) if shutil.which("rg") else _py_search(query, dirs)
    if not hits:
        return f"no matches for {query!r}"
    shown = [h.replace(f"{KB_ROOT}/", "", 1) for h in hits[:MAX_HITS]]
    suffix = f"\n… {len(hits) - MAX_HITS} more (narrow the query)" \
        if len(hits) > MAX_HITS else ""
    return "\n".join(shown) + suffix


@mcp.tool()
def read_page(name: str) -> str:
    """Read a page by name ('Ingest Workflow') or repo-relative path."""
    direct = KB_ROOT / name
    if direct.is_file() and direct.resolve().is_relative_to(KB_ROOT):
        return direct.read_text(encoding="utf-8")
    stem = Path(name).stem.lower()
    candidates = [p for d in _search_dirs("all")
                  for p in sorted(d.rglob("*.md")) if p.stem.lower() == stem]
    if not candidates:
        raise ToolError(f"no page named {name!r} — try search_kb, or get_index for the "
                        "catalog of page names")
    best = min(candidates,
               key=lambda p: 0 if p.relative_to(KB_ROOT).parts[0] == "wiki" else 1)
    header = f"<!-- {best.relative_to(KB_ROOT)} -->\n"
    return header + best.read_text(encoding="utf-8")


@mcp.tool()
def get_index() -> str:
    """Return wiki/index.md — the catalog of every page, one line each."""
    index = KB_ROOT / "wiki" / "index.md"
    if not index.exists():
        return "this KB has no wiki/index.md"
    return index.read_text(encoding="utf-8")


if __name__ == "__main__":
    argparse.ArgumentParser(
        description="Read-only MCP server (stdio) for this knowledge base: "
                    "search_kb, read_page, get_index.",
    ).parse_args()
    mcp.run()
