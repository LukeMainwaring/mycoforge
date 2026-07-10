#!/usr/bin/env python3
"""Carve ==highlighted== passages out of a transcript into a clip scaffold.

Reads a transcript from raw/, extracts every passage the user marked with
Obsidian ``==highlight==`` syntax (keeping the nearest preceding [MM:SS] anchor),
applies the ASR-correction glossary from ``kb.toml [snippet].glossary``, and
writes a structured clip file next to the source with sections:
Summary -> Cleaned Transcript -> Notes -> Raw Transcript.

The script fills Cleaned Transcript (glossary-corrected) and Raw Transcript
(verbatim); Summary and Notes are placeholders the /snippet skill fills — the
user's own notes go in verbatim.

Usage:
    python3 .agents/skills/snippet/carve.py <transcript.md> [--out <file>]
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
import tomllib
from pathlib import Path

KB_ROOT = Path(__file__).resolve().parents[3]
HIGHLIGHT_RE = re.compile(r"==(.+?)==", re.DOTALL)
ANCHOR_RE = re.compile(r"\[(?:\d+:)?\d{1,2}:\d{2}\]")


def load_glossary(root: Path) -> dict[str, str]:
    kb_toml = root / "kb.toml"
    if not kb_toml.exists():
        return {}
    config = tomllib.loads(kb_toml.read_text(encoding="utf-8"))
    return config.get("snippet", {}).get("glossary", {})


def apply_glossary(text: str, glossary: dict[str, str]) -> str:
    for wrong, right in glossary.items():
        text = re.sub(re.escape(wrong), right, text, flags=re.IGNORECASE)
    return text


def carve(text: str) -> list[tuple[str, str]]:
    """Return (anchor, passage) per highlight, anchor = nearest [MM:SS] before it."""
    passages = []
    for m in HIGHLIGHT_RE.finditer(text):
        anchors = ANCHOR_RE.findall(text[:m.start()])
        anchor = anchors[-1] if anchors else "[??:??]"
        passage = re.sub(r"\s+", " ", m.group(1)).strip()
        passages.append((anchor, passage))
    return passages


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Carve ==highlights== from a transcript into a clip file.")
    ap.add_argument("source", type=Path, help="transcript markdown file in raw/")
    ap.add_argument("--out", type=Path, default=None,
                    help="clip file path (default: '<source stem> (Clip).md' beside it)")
    args = ap.parse_args()

    if not args.source.exists():
        sys.exit(f"no such file: {args.source}")
    text = args.source.read_text(encoding="utf-8")
    passages = carve(text)
    if not passages:
        sys.exit("no ==highlights== found in the source — mark some passages first")

    glossary = load_glossary(KB_ROOT)
    today = dt.date.today().isoformat()
    raw_block = "\n\n".join(f"{a} {p}" for a, p in passages)
    cleaned_block = apply_glossary(raw_block, glossary)

    out = args.out or args.source.with_name(f"{args.source.stem} (Clip).md")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join([
        "---",
        "type: clip",
        f'source: "[[{args.source.stem}]]"',
        f"created: {today}",
        f"highlights: {len(passages)}",
        "---",
        "",
        f"# {args.source.stem} (Clip)",
        "",
        "## Summary",
        "",
        "<!-- filled by /snippet -->",
        "",
        "## Cleaned Transcript",
        "",
        cleaned_block,
        "",
        "## Notes",
        "",
        "<!-- the user's own notes, verbatim -->",
        "",
        "## Raw Transcript",
        "",
        raw_block,
        "",
    ]), encoding="utf-8")
    rel = out.relative_to(KB_ROOT) if out.is_relative_to(KB_ROOT) else out
    print(f"wrote {rel} ({len(passages)} highlight(s), "
          f"{len(glossary)} glossary rule(s) applied)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
