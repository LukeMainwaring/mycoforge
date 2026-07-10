#!/usr/bin/env python3
"""Fetch a YouTube podcast transcript and save it to raw/podcasts/.

Capture only: this populates raw/ and never ingests into the wiki.

Usage:
    fetch.py <url>
    fetch.py <url> --clip 30:20-31:50 --topic "key argument"
    fetch.py <url> --clip 1:05:30-1:07:00 --topic "methodology"
    fetch.py <url> --show "Acquired"

Requires: yt-dlp (`brew install yt-dlp`, or `pip install -U yt-dlp`).
"""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path


# --- locating the project ---------------------------------------------------

def find_project_root() -> Path:
    """Walk up from this file looking for the schema file + raw/ to anchor on.
    AGENTS.md is canonical; CLAUDE.md is its symlink, so either identifies a KB."""
    here = Path(__file__).resolve()
    for ancestor in [here, *here.parents]:
        has_schema = (ancestor / "AGENTS.md").is_file() or (ancestor / "CLAUDE.md").is_file()
        if has_schema and (ancestor / "raw").is_dir():
            return ancestor
    sys.exit(
        "error: could not locate the KB root "
        "(no AGENTS.md/CLAUDE.md + raw/ found above this script)"
    )


def require_yt_dlp() -> None:
    if shutil.which("yt-dlp") is None:
        sys.exit(
            "error: yt-dlp is not installed.\n"
            "  install with: brew install yt-dlp\n"
            "  or:           pip install -U yt-dlp"
        )


# --- yt-dlp wrappers --------------------------------------------------------

def get_metadata(url: str) -> dict:
    res = subprocess.run(
        ["yt-dlp", "--dump-json", "--skip-download", "--no-warnings", url],
        capture_output=True, text=True,
    )
    if res.returncode != 0:
        sys.exit(f"yt-dlp metadata fetch failed:\n{res.stderr.strip()}")
    return json.loads(res.stdout)


def fetch_captions(url: str, lang: str) -> tuple[str | None, str | None]:
    """Fetch captions via yt-dlp. Returns (vtt_text, source_label)."""
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        cmd = [
            "yt-dlp",
            "--write-sub", "--write-auto-sub",
            "--skip-download",
            "--sub-format", "vtt",
            "--sub-langs", lang,
            "--no-warnings",
            "-o", str(td_path / "%(id)s.%(ext)s"),
            url,
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            sys.exit(f"yt-dlp caption fetch failed:\n{res.stderr.strip()}")

        vtt_files = list(td_path.glob("*.vtt"))
        if not vtt_files:
            return None, None

        log = (res.stderr + res.stdout).lower()
        # yt-dlp writes manual subs preferentially; the log line tells us which.
        if "writing video subtitles" in log:
            source = "youtube-manual"
        elif "writing video automatic" in log or "writing automatic" in log:
            source = "youtube-auto"
        else:
            source = "youtube-unknown"
        return vtt_files[0].read_text(encoding="utf-8"), source


# --- VTT parsing ------------------------------------------------------------

CUE_TIME_RE = re.compile(
    r"^(\d{2}:\d{2}:\d{2}\.\d{3})\s+-->\s+(\d{2}:\d{2}:\d{2}\.\d{3})"
)
INLINE_TAG_RE = re.compile(r"<[^>]+>")


def vtt_time_to_seconds(s: str) -> float:
    h, m, rest = s.split(":")
    sec, ms = rest.split(".")
    return int(h) * 3600 + int(m) * 60 + int(sec) + int(ms) / 1000


def parse_vtt(vtt_text: str) -> list[tuple[float, float, list[str]]]:
    """Parse VTT to a list of (start_s, end_s, lines) cues, inline tags stripped.

    Lines within a cue are kept as a list (not pre-joined) so downstream dedup can
    operate at the line level — YouTube auto-captions emit a rolling window where
    each cue contains one or two prior lines plus a new line, and cue-level dedup
    misses that pattern entirely.
    """
    cues: list[tuple[float, float, list[str]]] = []
    cur_start: float | None = None
    cur_end: float | None = None
    cur_lines: list[str] = []

    def flush():
        nonlocal cur_start, cur_end, cur_lines
        if cur_start is not None and cur_lines:
            cues.append((cur_start, cur_end or cur_start, list(cur_lines)))
        cur_start = cur_end = None
        cur_lines = []

    for line in vtt_text.splitlines():
        m = CUE_TIME_RE.match(line)
        if m:
            flush()
            cur_start = vtt_time_to_seconds(m.group(1))
            cur_end = vtt_time_to_seconds(m.group(2))
            continue
        if not line.strip():
            continue
        if line.startswith(("WEBVTT", "Kind:", "Language:", "NOTE")):
            continue
        # Bare cue numbers between cues
        if cur_start is None and line.strip().isdigit():
            continue
        # Order matters: unescape FIRST so HTML-encoded inline tags like
        # `&lt;c&gt;` become visible `<c>`, then strip them.
        cleaned = INLINE_TAG_RE.sub("", html.unescape(line)).strip()
        if cleaned and cur_start is not None:
            cur_lines.append(cleaned)

    flush()
    return cues


def cues_to_timed_lines(
    cues: list[tuple[float, float, list[str]]],
) -> list[tuple[float, str]]:
    """Flatten cues to (start_s, line) tuples in transcript order, deduping at
    the line level to absorb YouTube's rolling-window repetition. The earliest
    start_s wins per unique line — that's the cue when the line first appeared,
    which is the most accurate moment to anchor on."""
    seen: set[str] = set()
    out: list[tuple[float, str]] = []
    for start_s, _, lines in cues:
        for ln in lines:
            if ln in seen:
                continue
            seen.add(ln)
            out.append((start_s, ln))
    return out


def split_into_turns(
    timed_lines: list[tuple[float, str]],
) -> list[list[tuple[float, str]]]:
    """Split timed lines on `>>` speaker-turn markers (YouTube manual-caption
    convention). Each `>>` boundary opens a new turn; both halves of a `>>`
    that falls mid-line keep the parent cue's start_s. Auto-caption transcripts
    have no `>>` markers and collapse to a single turn (no behavior change)."""
    turns: list[list[tuple[float, str]]] = [[]]
    for start_s, line in timed_lines:
        parts = re.split(r"\s*>>\s*", line)
        for i, part in enumerate(parts):
            part = part.strip()
            if i > 0:
                # `>>` boundary — open a new turn.
                turns.append([])
            if part:
                turns[-1].append((start_s, part))
    return [t for t in turns if t]


def _break_runons(sent: str, max_words: int = 120, target: int = 60) -> list[str]:
    """If a 'sentence' (text between two [.!?]\\s+ boundaries) exceeds max_words,
    fall back to comma-boundary splits coalesced into ~target-word fragments.
    Catches long un-punctuated monologues that survive the speaker-turn split."""
    if len(sent.split()) <= max_words:
        return [sent]
    sub = re.split(r"(?<=,)\s+", sent)
    if len(sub) == 1:
        return [sent]  # no commas either; nothing we can do
    out: list[str] = []
    cur: list[str] = []
    cur_words = 0
    for s in sub:
        cur.append(s)
        cur_words += len(s.split())
        if cur_words >= target:
            out.append(" ".join(cur))
            cur = []
            cur_words = 0
    if cur:
        out.append(" ".join(cur))
    return out


def _merge_unterminated(
    timed_sents: list[tuple[float, str]],
) -> list[tuple[float, str]]:
    """Merge consecutive (t, sent) tuples where the prior sentence doesn't end
    with .!? — handles sentences that straddle two cues. The first occurrence's
    start_s is preserved (it's when the speech started)."""
    merged: list[tuple[float, str]] = []
    for start_s, sent in timed_sents:
        if merged and not merged[-1][1].rstrip().endswith((".", "!", "?")):
            ps, ps_sent = merged[-1]
            merged[-1] = (ps, ps_sent + " " + sent)
        else:
            merged.append((start_s, sent))
    return merged


def select_anchor_format(duration_s: float | int | None) -> str:
    """Return 'hmmss' for episodes >= 1 hour, else 'mmss'. Fallback 'mmss'
    when duration is unknown."""
    if duration_s and duration_s >= 3600:
        return "hmmss"
    return "mmss"


def fmt_anchor(start_s: float, fmt: str) -> str:
    """Render `[MM:SS]` or `[H:MM:SS]`. Integer seconds (floor)."""
    total = int(start_s)
    h, rem = divmod(total, 3600)
    m, s = divmod(rem, 60)
    if fmt == "hmmss":
        return f"[{h}:{m:02d}:{s:02d}]"
    return f"[{m}:{s:02d}]"


def lines_to_paragraphs(
    timed_fragments: list[tuple[float, str]],
    target_words: int = 200,
    anchor_fmt: str = "mmss",
) -> str:
    """Sentence-split timed fragments (carrying start_s through), apply
    _break_runons to long sentences, merge unterminated-sentence straddles,
    then wrap into ~target_words paragraphs. Each paragraph starts with
    `[MM:SS] ` (or `[H:MM:SS] `) using the start_s of its first sentence."""
    timed_sents: list[tuple[float, str]] = []
    for start_s, frag in timed_fragments:
        for sent in re.split(r"(?<=[.!?])\s+", frag):
            sent = sent.strip()
            if not sent:
                continue
            chunks = _break_runons(sent)
            for chunk in chunks:
                timed_sents.append((start_s, chunk))

    timed_sents = _merge_unterminated(timed_sents)

    paragraphs: list[str] = []
    cur_sents: list[str] = []
    cur_words = 0
    cur_anchor: float | None = None
    for start_s, sent in timed_sents:
        if cur_anchor is None:
            cur_anchor = start_s
        cur_sents.append(sent)
        cur_words += len(sent.split())
        if cur_words >= target_words:
            paragraphs.append(
                f"{fmt_anchor(cur_anchor, anchor_fmt)} " + " ".join(cur_sents)
            )
            cur_sents = []
            cur_words = 0
            cur_anchor = None
    if cur_sents:
        paragraphs.append(
            f"{fmt_anchor(cur_anchor or 0.0, anchor_fmt)} " + " ".join(cur_sents)
        )
    return "\n\n".join(paragraphs)


def cues_to_prose(
    cues: list[tuple[float, float, list[str]]],
    anchor_fmt: str = "mmss",
) -> str:
    """Flatten cues to prose. Dedups at the line level (rolling-window absorption),
    splits on `>>` speaker-turn markers, paragraph-wraps each turn with `[MM:SS]`
    anchors at paragraph starts, and prefixes turns 2+ with `— ` (em-dash).
    Auto-caption transcripts (no `>>`) collapse to a single turn — anchors still
    fire."""
    timed = cues_to_timed_lines(cues)
    turns = split_into_turns(timed)
    formatted: list[str] = []
    for i, turn in enumerate(turns):
        wrapped = lines_to_paragraphs(turn, anchor_fmt=anchor_fmt)
        if i > 0:
            wrapped = "— " + wrapped
        formatted.append(wrapped)
    return "\n\n".join(formatted)


# --- clip handling ----------------------------------------------------------

CLIP_RE = re.compile(r"^(\d{1,2}(?::\d{2}){1,2})-(\d{1,2}(?::\d{2}){1,2})$")


def parse_clock(s: str) -> int:
    parts = [int(p) for p in s.split(":")]
    if len(parts) == 2:
        return parts[0] * 60 + parts[1]
    if len(parts) == 3:
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    raise ValueError(f"bad time: {s!r}")


def slice_cues(
    cues: list[tuple[float, float, list[str]]], start_s: float, end_s: float
) -> list[tuple[float, float, list[str]]]:
    return [c for c in cues if c[1] >= start_s and c[0] <= end_s]


# --- filename / formatting --------------------------------------------------

_TRAILING_STOPWORDS = frozenset({
    "a", "an", "and", "the", "of", "in", "on", "at", "to", "for", "with",
    "by", "from", "as", "but", "or", "is", "it",
})


def safe_stem(s: str, max_len: int = 80) -> str:
    """Apply the schema's Obsidian path-breaker rules. Replace `/` with `-` (no
    spaces), `:` with ` -` (so "Show: Episode" reads naturally as "Show -
    Episode"), and strip the rest (`#`, `?`, `|`, `[`, `]`). Truncate at word
    boundaries — and drop trailing stopwords ("on", "the", "and", ...) — so
    titles don't end on a visibly-truncated preposition like "...Journey to"."""
    s = s.replace("/", "-")
    s = s.replace(":", " -")
    s = re.sub(r"[?#|\[\]]", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    s = s.rstrip("-").strip()
    if len(s) > max_len:
        cut = s.rfind(" ", 0, max_len + 1)
        # Guard against pathological cases (giant compound word with no space
        # in the first half of the budget) by falling back to the hard cut.
        if cut > max_len // 2:
            s = s[:cut]
        else:
            s = s[:max_len]
        # Drop trailing punctuation and any stopwords left dangling at the end.
        # Stop after one stopword pass so "on the" → "" doesn't strip the whole
        # title; in practice titles end with at most one trailing stopword.
        s = s.rstrip().rstrip("-,").rstrip()
        words = s.split(" ")
        if words and words[-1].lower() in _TRAILING_STOPWORDS:
            s = " ".join(words[:-1]).rstrip().rstrip("-,").rstrip()
    return s


def fmt_duration(seconds: int | float | None) -> str:
    if not seconds:
        return ""
    total = int(seconds)
    h, rem = divmod(total, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def yaml_dq(s: str) -> str:
    """Escape a string for use as a YAML double-quoted scalar."""
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


# --- main -------------------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser(
        description="Fetch a YouTube podcast transcript to raw/podcasts/."
    )
    ap.add_argument("url")
    ap.add_argument("--clip", help="Time range MM:SS-MM:SS or HH:MM:SS-HH:MM:SS")
    ap.add_argument("--topic", help="Topic label for the snippet filename")
    ap.add_argument("--lang", default="en", help="Caption language (default: en)")
    ap.add_argument("--show", help="Override the show / channel name")
    args = ap.parse_args()

    require_yt_dlp()
    project_root = find_project_root()
    out_dir = project_root / "raw" / "podcasts"
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"fetching metadata for {args.url} ...", file=sys.stderr)
    meta = get_metadata(args.url)
    title = (meta.get("title") or "untitled").strip()
    show = (args.show or meta.get("uploader") or meta.get("channel") or "unknown").strip()
    upload = meta.get("upload_date")  # YYYYMMDD
    if upload and len(upload) == 8 and upload.isdigit():
        published = f"{upload[:4]}-{upload[4:6]}-{upload[6:]}"
    else:
        published = ""
    duration_s = meta.get("duration")

    print("fetching captions ...", file=sys.stderr)
    vtt, source = fetch_captions(args.url, lang=args.lang)
    if vtt is None:
        sys.exit(
            "no captions available for this video.\n"
            "fall back to whisper:\n"
            f"  yt-dlp -x --audio-format mp3 \"{args.url}\"\n"
            "  whisper-cpp -m models/ggml-large-v3.bin -f <audio>.mp3 -otxt"
        )

    cues = parse_vtt(vtt)
    if not cues:
        sys.exit("captions file parsed to zero cues; bailing")

    anchor_fmt = select_anchor_format(duration_s)

    if args.clip:
        m = CLIP_RE.match(args.clip)
        if not m:
            sys.exit(
                f"bad --clip format: {args.clip!r} "
                "(expected MM:SS-MM:SS or HH:MM:SS-HH:MM:SS)"
            )
        start_s = parse_clock(m.group(1))
        end_s = parse_clock(m.group(2))
        if end_s <= start_s:
            sys.exit(f"--clip end ({m.group(2)}) must be after start ({m.group(1)})")
        sliced = slice_cues(cues, start_s, end_s)
        if not sliced:
            sys.exit(f"no captions found in time range {args.clip}")
        body = cues_to_prose(sliced, anchor_fmt=anchor_fmt)
        topic_label = args.topic or f"{m.group(1)}-{m.group(2)}"
        suffix = f" (clip - {topic_label})"
        is_clip = True
    else:
        body = cues_to_prose(cues, anchor_fmt=anchor_fmt)
        suffix = ""
        is_clip = False

    stem_raw = (
        f"{published} {show} - {title}{suffix}"
        if published
        else f"{show} - {title}{suffix}"
    )
    stem = safe_stem(stem_raw)
    out_path = out_dir / f"{stem}.md"

    fm: list[str] = ["---"]
    fm.append(f"title: {yaml_dq(title)}")
    fm.append(f"source: {args.url}")
    fm.append(f"show: {yaml_dq(show)}")
    if published:
        fm.append(f"published: {published}")
    fm.append(f"created: {date.today().isoformat()}")
    if duration_s:
        fm.append(f'duration: "{fmt_duration(duration_s)}"')
    fm.append(f"captions_source: {source}")
    if is_clip:
        fm.append(f'clip: "{args.clip}"')
        if args.topic:
            fm.append(f"clip_topic: {yaml_dq(args.topic)}")
    fm.append("tags:")
    fm.append("  - podcast")
    if is_clip:
        fm.append("  - podcast-clip")
    fm.append("---")

    content = "\n".join(fm) + f"\n\n# {title}\n\n{body}\n"
    out_path.write_text(content, encoding="utf-8")

    # Single-line summary on stdout for the calling skill to relay.
    summary_bits = [
        f"saved: {out_path.relative_to(project_root)}",
        f"show: {show}",
        f"duration: {fmt_duration(duration_s) or 'unknown'}",
        f"captions: {source}",
    ]
    if is_clip:
        summary_bits.append(f"clip: {args.clip}")
    print(" · ".join(summary_bits))


if __name__ == "__main__":
    main()
