#!/usr/bin/env python3
"""MycoForge onboarding helper — deterministic prune + rename.

Reads ``.template/features.toml`` and turns the full scaffold into the subset
you want: deletes features you don't keep, strips the ``sf:`` markers, and
optionally renames the instance slug/brand. Pure stdlib, idempotent, dry-run by
default. Adapted from sporeforge's onboard.py; the KB twist is that markdown is
marker-eligible too, via HTML-comment markers invisible in Obsidian and GitHub.

Examples
--------
    # List the cuttable features:
    python3 .template/onboard.py --list

    # Preview a pure research KB (drop the product layer):
    python3 .template/onboard.py --keep orchestrator,media-capture,mcp-server

    # Apply it, and rename the instance:
    python3 .template/onboard.py --keep media-capture,mcp-server \\
            --slug mykb --brand MyKB --apply

    # Minimal wiki core (drop all four features):
    python3 .template/onboard.py --keep "" --apply

The deterministic prune covers code + config + marked prose. Whole docs
(README, AGENTS.md domain prose, seed pages) are refreshed by the /onboard
skill, not here.
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # repo root (.template/..)
MANIFEST = Path(__file__).resolve().parent / "features.toml"

# Directories we never walk for marker-processing or renaming.
EXCLUDE_DIRS = {
    ".git", ".obsidian", "__pycache__", ".pytest_cache", ".ruff_cache",
    "node_modules", ".template",
}
# Hash-comment marker style applies to these…
HASH_SUFFIXES = {".py", ".toml", ".sh", ".yml", ".yaml"}
HASH_NAMES = {".gitignore", ".env.sample"}
# …HTML-comment style to these (invisible in Obsidian reading view and GitHub).
HTML_SUFFIXES = {".md"}
# Skip these when renaming (binary).
BINARY_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".ico", ".webp", ".pdf",
                   ".woff", ".woff2", ".ttf", ".mp3", ".mp4", ".m4a", ".wav"}

# Feature ids may contain hyphens (media-capture, mcp-server): [\w-]+
HASH_RES = {
    "begin": re.compile(r"#\s*sf:begin\(([\w-]+)\)"),
    "end": re.compile(r"#\s*sf:end\(([\w-]+)\)"),
    "keepif": re.compile(r"#\s*sf:keep-if\(([\w-]+)\)"),
    "keepif_strip": re.compile(r"[ \t]*#\s*sf:keep-if\([\w-]+\)[ \t]*$"),
}
HTML_RES = {
    "begin": re.compile(r"<!--\s*sf:begin\(([\w-]+)\)\s*-->"),
    "end": re.compile(r"<!--\s*sf:end\(([\w-]+)\)\s*-->"),
    "keepif": re.compile(r"<!--\s*sf:keep-if\(([\w-]+)\)\s*-->"),
    "keepif_strip": re.compile(r"[ \t]*<!--\s*sf:keep-if\([\w-]+\)\s*-->[ \t]*$"),
}
SLUG_RE = re.compile(r"^[a-z][a-z0-9_]*$")


def log(msg: str = "") -> None:
    print(msg)


def load_manifest(manifest: Path = MANIFEST) -> tuple[dict, dict]:
    data = tomllib.loads(manifest.read_text(encoding="utf-8"))
    return data.get("project", {}), data.get("features", {})


def resolve_disabled(kept: set[str], features: dict) -> set[str]:
    """Features to drop = everything not kept, plus anything requiring a dropped one."""
    all_ids = set(features)
    disabled = all_ids - (kept & all_ids)
    changed = True
    while changed:
        changed = False
        for fid, spec in features.items():
            if fid in disabled:
                continue
            if set(spec.get("requires", [])) & disabled:
                disabled.add(fid)
                changed = True
    return disabled


def iter_walk_files(root: Path):
    for p in root.rglob("*"):
        if p.is_dir() or p.is_symlink():
            continue
        if any(part in EXCLUDE_DIRS for part in p.relative_to(root).parts):
            continue
        yield p


def marker_res_for(p: Path) -> dict | None:
    if p.suffix in HTML_SUFFIXES:
        return HTML_RES
    if p.suffix in HASH_SUFFIXES or p.name in HASH_NAMES:
        return HASH_RES
    return None


def process_markers_text(text: str, disabled: set[str], res: dict) -> str:
    """Drop disabled marker blocks / keep-if lines; strip markers for kept features."""
    out: list[str] = []
    skipping: str | None = None
    for line in text.split("\n"):
        if skipping is not None:
            m = res["end"].search(line)
            if m and m.group(1) == skipping:
                skipping = None
            continue  # drop everything inside a disabled block (incl. the end marker)
        mb = res["begin"].search(line)
        if mb:
            if mb.group(1) in disabled:
                skipping = mb.group(1)
            continue  # drop the begin marker line either way
        if res["end"].search(line):
            continue  # drop a kept-feature's end marker line
        mi = res["keepif"].search(line)
        if mi:
            if mi.group(1) in disabled:
                continue  # drop the whole annotated line
            line = res["keepif_strip"].sub("", line)  # keep content, strip the marker
        out.append(line)
    return "\n".join(out)


def collect_deleted_paths(disabled: set[str], features: dict) -> set[str]:
    return {rel for fid in disabled for rel in features[fid].get("paths", [])}


def delete_paths(disabled: set[str], features: dict, apply: bool, root: Path = ROOT) -> None:
    for fid in sorted(disabled):
        for rel in features[fid].get("paths", []):
            target = root / rel
            if not target.exists():
                continue
            log(f"  rm {rel}")
            if apply:
                if target.is_dir():
                    shutil.rmtree(target)
                else:
                    target.unlink()


def process_markers(disabled: set[str], apply: bool, root: Path = ROOT) -> None:
    n = 0
    for p in iter_walk_files(root):
        res = marker_res_for(p)
        if res is None:
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if "sf:" not in text:
            continue
        new = process_markers_text(text, disabled, res)
        if new != text:
            n += 1
            if apply:
                p.write_text(new, encoding="utf-8")
    log(f"  markers stripped/pruned in {n} file(s)")


def check_links(root: Path = ROOT) -> list[str]:
    """Post-prune sanity: symlinks intact, no reference to a deleted skill dir.

    The sporeforge analog rewired hook configs; a KB has nothing to rewire, so
    this verifies and reports instead (verify_matrix.sh enforces it in CI).
    """
    problems: list[str] = []
    for link, expect_dir in (("CLAUDE.md", False), (".claude/skills", True)):
        p = root / link
        if not p.is_symlink() or not p.exists():
            problems.append(f"symlink broken or missing: {link}")
        elif expect_dir and not p.resolve().is_dir():
            problems.append(f"symlink does not resolve to a directory: {link}")
    ref_re = re.compile(r"\.agents/skills/([\w-]+)")
    for p in iter_walk_files(root):
        if p.suffix not in {".md", ".toml", ".json"}:
            continue
        if p.relative_to(root).parts[0] == "raw":
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for name in set(ref_re.findall(text)):
            if not (root / ".agents/skills" / name).is_dir():
                problems.append(
                    f"{p.relative_to(root)} references deleted skill: {name}")
    for msg in problems:
        log(f"  WARNING {msg}")
    if not problems:
        log("  links OK: symlinks intact, no dangling skill references")
    return problems


def do_rename(project: dict, slug: str, brand: str | None, apply: bool,
              root: Path = ROOT) -> None:
    """Pure text substitution of slug/brand across non-binary files.

    kb.toml's `[template]` repo pin must keep pointing at the *template* repo,
    so its `repo = ...` line is restored after substitution.
    """
    old_slug = project.get("slug", "mycoforge")
    old_brand = project.get("brand", "MycoForge")
    brand = brand or (slug[:1].upper() + slug[1:])
    log(f"rename: {old_slug} -> {slug} | {old_brand} -> {brand}")

    repo_line_re = re.compile(r"(?m)^(repo\s*=\s*.*)$")
    n = 0
    for p in iter_walk_files(root):
        if p.suffix in BINARY_SUFFIXES:
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if old_brand not in text and old_slug not in text:
            continue
        new = text.replace(old_brand, brand).replace(old_slug, slug)
        if p == root / "kb.toml":
            old_repo = repo_line_re.search(text)
            if old_repo:
                new = repo_line_re.sub(old_repo.group(1).replace("\\", "\\\\"),
                                       new, count=1)
        if new != text:
            n += 1
            if apply:
                p.write_text(new, encoding="utf-8")
    log(f"  identity token updated in {n} file(s)")


def print_next_steps(disabled: set[str]) -> None:
    log("")
    log("Applied. Next steps:")
    log("  - run the linter:  python3 scripts/lint.py")
    log("  - regenerate the prose to match — schema domain text, seed wiki pages,")
    log("    README (the /onboard skill owns this half)")
    log("  - remove the .template/ directory once you're done onboarding")


def main() -> int:
    ap = argparse.ArgumentParser(
        description="MycoForge onboarding: deterministic prune + rename.")
    ap.add_argument("--keep", default=None,
                    help="comma list of features to KEEP (default: keep all), "
                         "e.g. 'media-capture,mcp-server'")
    ap.add_argument("--slug", default=None,
                    help="new instance slug (renames the 'mycoforge' token)")
    ap.add_argument("--brand", default=None,
                    help="new display name (renames 'MycoForge'); defaults from --slug")
    ap.add_argument("--apply", action="store_true",
                    help="make changes (default: dry run)")
    ap.add_argument("--list", action="store_true", help="list features and exit")
    args = ap.parse_args()

    project, features = load_manifest()

    if args.list:
        for fid, spec in features.items():
            req = spec.get("requires") or []
            suffix = f"  (requires: {', '.join(req)})" if req else ""
            log(f"{fid}: {spec.get('description', '')}{suffix}")
        return 0

    if args.slug is not None and not SLUG_RE.match(args.slug):
        ap.error(f"--slug must match {SLUG_RE.pattern}")

    if args.keep is None:
        kept = set(features)
    else:
        kept = {s.strip() for s in args.keep.split(",") if s.strip()}
        unknown = kept - set(features)
        if unknown:
            ap.error(f"unknown features: {sorted(unknown)}; valid: {sorted(features)}")

    disabled = resolve_disabled(kept, features)
    log(f"keep: {sorted(set(features) - disabled) or '(none)'}   "
        f"drop: {sorted(disabled) or '(none)'}")
    log("")

    delete_paths(disabled, features, args.apply)
    process_markers(disabled, args.apply)
    if args.apply:
        check_links()
    if args.slug:
        do_rename(project, args.slug, args.brand, args.apply)

    if not args.apply:
        log("")
        log("DRY RUN — re-run with --apply to make these changes.")
    else:
        print_next_steps(disabled)
    return 0


if __name__ == "__main__":
    sys.exit(main())
