#!/usr/bin/env python3
"""MycoForge wiki linter — deterministic health checks over the KB.

Pure stdlib. All per-instance data (candidate terms, link allowlists, staleness
threshold, children) comes from ``kb.toml`` — never hard-code instance data here.

Checks:
  * index audit — every wiki page has an entry in wiki/index.md, no ghost entries
  * wikilink resolution — code blocks stripped first; piped links and section
    anchors supported; ``intentional_forward_links`` suppressed
  * ``raw:`` frontmatter references point at existing files
  * orphan pages (no inbound link outside index.md/log.md) — warning
  * stale pages — file mtime more than ``stale_after_days`` newer than ``updated:``
  * concept candidates — configured terms recurring without a page of their own
  * child KBs exist and carry their own kb.toml; cross-KB links are warnings

Exit status: non-zero if any ERROR was found; warnings alone exit 0.

Usage:
    python3 scripts/lint.py [--root <kb-root>]
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

FENCE_RE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE_RE = re.compile(r"`[^`\n]+`")
# [[Target]], [[Target|shown]], [[Target#Heading]], ![[embed.png]] — group 1 = target.
# The target class permits a trailing backslash so Obsidian's table-escaped pipe
# — [[Target\|Display]], required inside markdown table cells — is captured as
# `Target\`; wikilinks() strips that escaping backslash back off.
WIKILINK_RE = re.compile(r"!?\[\[([^\[\]|#]+?)(?:#[^\[\]|]*)?(?:\\?\|[^\[\]]*)?\]\]")

# Directories never scanned (not KB content).
SKIP_DIRS = {".git", ".obsidian", ".template", ".agents", ".claude", "__pycache__",
             "node_modules", ".pytest_cache", ".ruff_cache"}
# Repo-level docs, not KB content — never scanned for links or indexed.
SKIP_FILES = {"AGENTS.md", "CLAUDE.md", "README.md", "BUILD_SPEC.md"}


@dataclass
class Issues:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def error(self, where: str, msg: str) -> None:
        self.errors.append(f"{where}: {msg}")

    def warn(self, where: str, msg: str) -> None:
        self.warnings.append(f"{where}: {msg}")


def load_config(root: Path) -> dict:
    kb_toml = root / "kb.toml"
    if not kb_toml.exists():
        return {}
    return tomllib.loads(kb_toml.read_text(encoding="utf-8"))


def strip_code(text: str) -> str:
    """Remove fenced code blocks and inline code so examples aren't scanned."""
    return INLINE_CODE_RE.sub("", FENCE_RE.sub("", text))


def parse_frontmatter(text: str) -> dict:
    """Minimal YAML-subset frontmatter parser: scalars, inline and block lists."""
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    meta: dict = {}
    key = None
    for line in text[4:end].split("\n"):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        item = line.strip()
        if item.startswith("- ") and key is not None:
            meta.setdefault(key, [])
            if isinstance(meta[key], list):
                meta[key].append(_unquote(item[2:]))
            continue
        if ":" in line and not line.startswith((" ", "\t")):
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip()
            if not value:
                meta[key] = []  # block list (or intentionally empty)
            elif value.startswith("[") and value.endswith("]"):
                inner = value[1:-1].strip()
                meta[key] = [_unquote(v.strip()) for v in inner.split(",")] if inner else []
            else:
                meta[key] = _unquote(value)
    return meta


def _unquote(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def nested_kb_dirs(root: Path) -> list[Path]:
    """Directories that are KBs of their own (they carry a kb.toml) — e.g. child
    KBs physically nested in this folder. Their files are never OUR content."""
    return [p.parent for p in root.rglob("kb.toml")
            if p.parent != root and ".git" not in p.parts]


def _excluded(root: Path, p: Path, nested: list[Path]) -> bool:
    rel_parts = p.relative_to(root).parts
    if any(part in SKIP_DIRS for part in rel_parts):
        return True
    return any(p.is_relative_to(n) for n in nested)


def iter_md(root: Path) -> list[Path]:
    """All markdown files that count as KB content (raw/ included as link targets)."""
    nested = nested_kb_dirs(root)
    out = []
    for p in sorted(root.rglob("*.md")):
        if _excluded(root, p, nested):
            continue
        if p.is_symlink() or p.name in SKIP_FILES:
            continue
        out.append(p)
    return out


def scannable(root: Path) -> list[Path]:
    """The LLM-owned layer we lint for links/frontmatter — everything but raw/."""
    return [p for p in iter_md(root) if p.relative_to(root).parts[0] != "raw"]


def rel(root: Path, p: Path) -> str:
    return str(p.relative_to(root))


def wikilinks(text: str) -> list[str]:
    # rstrip("\\") drops a table-escaped-pipe backslash the regex may leave on the
    # target (see WIKILINK_RE); page names never legitimately end in a backslash.
    return [m.group(1).strip().rstrip("\\").strip()
            for m in WIKILINK_RE.finditer(strip_code(text))]


# sf:begin(orchestrator)
def cross_kb_roots(config: dict, root: Path) -> list[Path]:
    """Directories of related KBs (parent + children) declared in kb.toml."""
    orch = config.get("orchestrator", {})
    roots = []
    if orch.get("parent"):
        roots.append((root / orch["parent"]).resolve())
    for child in orch.get("children", []):
        roots.append((root / child.get("path", "")).resolve())
    return [r for r in roots if r.is_dir()]


def find_cross_kb(target: str, config: dict, root: Path) -> Path | None:
    """Resolve a wikilink inside a related KB (parent/children). Warn-only match."""
    for kb_root in cross_kb_roots(config, root):
        for p in kb_root.rglob(f"{target}.md"):
            if ".git" not in p.parts:
                return p
    return None


def check_children(config: dict, root: Path, issues: Issues) -> None:
    """Every declared child path must exist and be a KB (carry its own kb.toml)."""
    for child in config.get("orchestrator", {}).get("children", []):
        path = child.get("path", "")
        child_dir = root / path
        if not child_dir.is_dir():
            issues.error("kb.toml", f"child KB path does not exist: {path}")
        elif not (child_dir / "kb.toml").exists():
            issues.error("kb.toml", f"child KB has no kb.toml of its own: {path}")
# sf:end(orchestrator)


def check_wikilinks(root: Path, config: dict, targets: set[str], issues: Issues) -> None:
    forward = set(config.get("lint", {}).get("intentional_forward_links", []))
    for page in scannable(root):
        for target in wikilinks(page.read_text(encoding="utf-8")):
            name = Path(target).name  # Obsidian resolves path-ish links by basename
            if name in targets or Path(name).stem in targets or target in forward:
                continue
            cross = None
            cross = find_cross_kb(name, config, root)  # sf:keep-if(orchestrator)
            if cross:
                issues.warn(rel(root, page),
                            f"cross-KB link [[{target}]] leaves this repo ({cross})")
            else:
                issues.error(rel(root, page), f"broken wikilink [[{target}]]")


def check_index(root: Path, targets: set[str], issues: Issues) -> None:
    index = root / "wiki" / "index.md"
    if not index.exists():
        issues.error("wiki/index.md", "missing — the index is mandatory")
        return
    indexed = set(wikilinks(index.read_text(encoding="utf-8")))
    for page in iter_md(root):
        parts = page.relative_to(root).parts
        if parts[0] != "wiki" or page.name in {"index.md", "log.md", "overview.md"}:
            continue  # overview.md is a structural meta page, not a catalog entry
        if page.stem not in indexed:
            issues.error(rel(root, page), "missing from wiki/index.md")
    # Ghost entries (index links to nowhere) surface via check_wikilinks, since
    # index.md is part of the scannable set.


def check_raw_refs(root: Path, targets: set[str], issues: Issues) -> None:
    """Resolve `raw:` frontmatter references in either supported form:

    - a repo-relative **path** (`raw/articles/x.md`) — checked for existence
    - an Obsidian **wikilink** (`[[x]]`, `[[x.pdf]]`) — resolved by file
      name/stem, the same way body wikilinks are (this is the vault-native form
      the hand-built KBs use)
    """
    for page in scannable(root):
        meta = parse_frontmatter(page.read_text(encoding="utf-8"))
        refs = meta.get("raw", [])
        if isinstance(refs, str):
            refs = [refs]
        for ref in refs:
            link = WIKILINK_RE.match(ref)
            if link:
                name = Path(link.group(1).strip()).name
                if name not in targets and Path(name).stem not in targets:
                    issues.error(rel(root, page), f"raw: reference not found: {ref}")
            elif not (root / ref).exists():
                issues.error(rel(root, page), f"raw: reference not found: {ref}")


def check_orphans(root: Path, issues: Issues) -> None:
    structural = {"index.md", "log.md", "overview.md"}
    inbound: set[str] = set()
    for page in scannable(root):
        if page.name in {"index.md", "log.md"}:
            continue  # the catalog/log linking a page doesn't make it non-orphan
        inbound.update(Path(t).stem for t in wikilinks(page.read_text(encoding="utf-8")))
    for page in iter_md(root):
        parts = page.relative_to(root).parts
        if parts[0] != "wiki" or page.name in structural:
            continue
        if page.stem not in inbound:
            issues.warn(rel(root, page), "orphan page — no inbound links outside index/log")


def check_stale(root: Path, config: dict, issues: Issues) -> None:
    days = int(config.get("lint", {}).get("stale_after_days", 0) or 0)
    if days <= 0:
        return
    for page in scannable(root):
        meta = parse_frontmatter(page.read_text(encoding="utf-8"))
        updated = meta.get("updated")
        if not isinstance(updated, str):
            continue
        try:
            updated_date = dt.date.fromisoformat(updated)
        except ValueError:
            issues.error(rel(root, page), f"unparseable updated: date {updated!r}")
            continue
        mtime = dt.date.fromtimestamp(page.stat().st_mtime)
        if (mtime - updated_date).days > days:
            issues.warn(rel(root, page),
                        f"stale: edited {mtime} but frontmatter says updated: {updated}")


def check_concept_candidates(root: Path, config: dict, targets: set[str],
                             issues: Issues, threshold: int = 3) -> None:
    terms = config.get("lint", {}).get("concept_candidate_terms", [])
    if not terms:
        return
    corpus = "\n".join(strip_code(p.read_text(encoding="utf-8")) for p in scannable(root))
    titles = {t.lower() for t in targets}
    for term in terms:
        if any(term.lower() in title for title in titles):
            continue  # a page title already covers this term
        count = len(re.findall(rf"\b{re.escape(term)}\b", corpus, re.IGNORECASE))
        if count >= threshold:
            issues.warn("wiki", f"concept candidate: {term!r} appears {count}x "
                                "with no page of its own — consider promoting it")


def run(root: Path) -> Issues:
    issues = Issues()
    config = load_config(root)
    all_md = iter_md(root)
    targets = {p.stem for p in all_md}
    # Non-markdown files (images etc.) are valid embed targets by full name.
    nested = nested_kb_dirs(root)
    for p in sorted(root.rglob("*")):
        if p.is_file() and not p.is_symlink() and p.suffix != ".md" \
                and not _excluded(root, p, nested) \
                and not p.name.startswith("."):
            targets.add(p.name)
            targets.add(p.stem)

    check_index(root, targets, issues)
    check_wikilinks(root, config, targets, issues)
    check_raw_refs(root, targets, issues)
    check_orphans(root, issues)
    check_stale(root, config, issues)
    check_concept_candidates(root, config, targets, issues)
    check_children(config, root, issues)  # sf:keep-if(orchestrator)
    return issues


def main() -> int:
    ap = argparse.ArgumentParser(description="Lint this knowledge base.")
    ap.add_argument("--root", type=Path,
                    default=Path(__file__).resolve().parent.parent,
                    help="KB root (default: the repo containing this script)")
    args = ap.parse_args()
    root = args.root.resolve()

    issues = run(root)
    for line in issues.errors:
        print(f"ERROR {line}")
    for line in issues.warnings:
        print(f"WARN  {line}")
    n_pages = len([p for p in iter_md(root) if p.relative_to(root).parts[0] != "raw"])
    print(f"lint: {n_pages} page(s) scanned — "
          f"{len(issues.errors)} error(s), {len(issues.warnings)} warning(s)")
    return 1 if issues.errors else 0


if __name__ == "__main__":
    sys.exit(main())
