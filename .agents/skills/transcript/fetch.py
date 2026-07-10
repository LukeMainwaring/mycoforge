#!/usr/bin/env python3
"""Fetch a YouTube/podcast transcript into raw/podcasts/ as dated markdown.

Shells out to yt-dlp for metadata and (auto-)subtitles, converts them to a
markdown transcript with [MM:SS] timestamp anchors, and writes
``raw/podcasts/YYYY-MM-DD <Title>.md`` with source frontmatter.

Capture only: this populates raw/ and never touches the wiki.

Usage:
    python3 .agents/skills/transcript/fetch.py <url> [--out raw/podcasts]
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

KB_ROOT = Path(__file__).resolve().parents[3]
FORBIDDEN = '[]#^|:/\\'  # characters that break Obsidian links or file systems
ANCHOR_EVERY_S = 30


def sanitize(title: str) -> str:
    cleaned = "".join(c for c in title if c not in FORBIDDEN)
    return re.sub(r"\s+", " ", cleaned).strip()


def ytdlp(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(["yt-dlp", *args], capture_output=True, text=True)


def get_metadata(url: str) -> dict:
    proc = ytdlp(["--dump-json", "--skip-download", url])
    if proc.returncode != 0:
        sys.exit(f"yt-dlp metadata fetch failed:\n{proc.stderr.strip()}")
    return json.loads(proc.stdout.splitlines()[0])


def get_subtitles(url: str, workdir: Path) -> Path | None:
    """Download the best English subtitle track as json3; return its path."""
    proc = ytdlp([
        "--skip-download", "--write-subs", "--write-auto-subs",
        "--sub-langs", "en.*,en", "--sub-format", "json3",
        "-o", str(workdir / "sub"), url,
    ])
    if proc.returncode != 0:
        sys.exit(f"yt-dlp subtitle fetch failed:\n{proc.stderr.strip()}")
    hits = sorted(workdir.glob("sub*.json3"))
    return hits[0] if hits else None


def mmss(ms: int) -> str:
    s = ms // 1000
    if s >= 3600:
        return f"[{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}]"
    return f"[{s // 60:02d}:{s % 60:02d}]"


def json3_to_markdown(path: Path) -> str:
    """Flatten a json3 subtitle track into anchored paragraphs."""
    data = json.loads(path.read_text(encoding="utf-8"))
    lines: list[tuple[int, str]] = []
    for event in data.get("events", []):
        text = "".join(seg.get("utf8", "") for seg in event.get("segs", []))
        text = re.sub(r"\s+", " ", text).strip()
        if not text:
            continue
        if lines and lines[-1][1] == text:  # rolling-caption duplicate
            continue
        lines.append((int(event.get("tStartMs", 0)), text))

    paragraphs: list[str] = []
    current: list[str] = []
    anchor_ms = None
    for start_ms, text in lines:
        if anchor_ms is None:
            anchor_ms = start_ms
        current.append(text)
        if start_ms - anchor_ms >= ANCHOR_EVERY_S * 1000:
            paragraphs.append(f"{mmss(anchor_ms)} {' '.join(current)}")
            current, anchor_ms = [], None
    if current:
        paragraphs.append(f"{mmss(anchor_ms or 0)} {' '.join(current)}")
    return "\n\n".join(paragraphs)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Fetch a YouTube/podcast transcript into raw/podcasts/.")
    ap.add_argument("url", help="video/podcast URL (anything yt-dlp understands)")
    ap.add_argument("--out", type=Path, default=KB_ROOT / "raw" / "podcasts",
                    help="output directory (default: raw/podcasts/)")
    args = ap.parse_args()

    meta = get_metadata(args.url)
    title = sanitize(meta.get("title") or "Untitled")
    upload = meta.get("upload_date")  # YYYYMMDD
    date = (f"{upload[:4]}-{upload[4:6]}-{upload[6:]}" if upload
            else dt.date.today().isoformat())

    with tempfile.TemporaryDirectory() as tmp:
        sub_path = get_subtitles(args.url, Path(tmp))
        if sub_path is None:
            sys.exit("no English subtitles/auto-captions available for this URL")
        body = json3_to_markdown(sub_path)

    out_dir = args.out
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{date} {title}.md"
    duration = int(meta.get("duration") or 0)
    front = "\n".join([
        "---",
        "type: podcast",
        f"title: {title}",
        f"channel: {meta.get('uploader') or meta.get('channel') or 'unknown'}",
        f"published: {date}",
        f"retrieved: {dt.date.today().isoformat()}",
        f"url: {meta.get('webpage_url') or args.url}",
        f"duration: {duration // 60}m{duration % 60:02d}s",
        "---",
    ])
    out.write_text(f"{front}\n\n# {title}\n\n{body}\n", encoding="utf-8")
    print(f"wrote {out.relative_to(KB_ROOT) if out.is_relative_to(KB_ROOT) else out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
