#!/usr/bin/env python3
"""Carve podcast snippet files from `==highlights==` in a full-episode transcript,
or regenerate the Summary + Cleaned Transcript of an existing snippet.

Two-phase contract: `plan` is read-only and emits a JSON manifest to stdout for
Claude to fill in (topic / summary / cleaned_transcript); `write` reads the
filled manifest from stdin and writes the actual files. This keeps the LLM
phase and the I/O phase cleanly separated.

Usage:
    carve.py plan <input.md>
        Read-only. Emits a JSON plan to stdout.
        Mode auto-detected from the input file's frontmatter:
          - full episode (no `clip:`, no `podcast-clip` tag) → N highlights
          - snippet (has `clip:` or `podcast-clip` tag)       → single entry

    carve.py write <input.md> --plan-stdin [--force]
        Reads filled plan from stdin. For full episodes: writes N new snippet
        files alongside the source. For snippets: rewrites in place, preserving
        the Notes section and Raw Transcript byte-identical.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

# Reuse helpers from the sibling /transcript skill so naming, YAML escaping,
# project-root anchoring, and clock-string parsing stay in one place.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "transcript"))
from fetch import (  # type: ignore  # noqa: E402
    find_project_root,
    parse_clock,
    safe_stem,
    yaml_dq,
)


# --- frontmatter parsing (hand-parsed; no PyYAML dependency) ----------------

def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Parse the YAML frontmatter subset that fetch.py emits. Returns (dict, body).

    Handles top-level scalar `key: value` (with optional double-quotes) and
    list-valued `key:` followed by indented `  - item` lines. Anything more
    exotic is YAML-illegal in our schema and we'd rather fail loudly than try
    to be clever.
    """
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}, text
    fm_text = text[4:end]
    body = text[end + 5:]

    fm: dict = {}
    cur_list_key: str | None = None
    for line in fm_text.splitlines():
        if not line.strip():
            cur_list_key = None
            continue
        # Indented list item under the most recent list-valued key.
        if line.startswith("  - ") and cur_list_key is not None:
            val = line[4:].strip()
            if val.startswith('"') and val.endswith('"'):
                val = val[1:-1]
            fm[cur_list_key].append(val)
            continue
        if ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip()
            if not val:
                fm[key] = []
                cur_list_key = key
            else:
                cur_list_key = None
                if val.startswith('"') and val.endswith('"'):
                    val = val[1:-1]
                fm[key] = val
    return fm, body


# --- anchor handling --------------------------------------------------------

# Matches [MM:SS] or [H:MM:SS] anywhere on a line. The leading `— ` em-dash
# (when present on turn-2+ paragraphs) is not part of the anchor itself; we
# locate the anchor by absolute position and let the em-dash live where it is.
ANCHOR_RE = re.compile(r"\[(\d{1,2}(?::\d{2}){1,2})\]")
# Match a paragraph-start anchor, tolerating leading `==` (Obsidian highlight
# wrap), `— ` (em-dash turn marker), or any combination thereof. The trailing
# lookahead enforces that the anchor is followed by a space or a closing `==`,
# so we don't accidentally match a `[…]` token deep in the prose.
PARAGRAPH_ANCHOR_RE = re.compile(
    r"^(?:==)?(?:— )?(?:==)?(\[\d{1,2}(?::\d{2}){1,2}\])(?=\s|==)"
)


def anchor_at_paragraph_start(paragraph: str) -> str | None:
    """Return the bracketed anchor token at the start of a paragraph, or None
    when the paragraph has no anchor (shouldn't happen for `/transcript`-output
    files, but possible for hand-edited files)."""
    m = PARAGRAPH_ANCHOR_RE.match(paragraph)
    return m.group(1)[1:-1] if m else None  # strip the [ ]


def detect_anchor_fmt(body: str, duration_str: str | None) -> str:
    """Decide whether anchors are MM:SS or H:MM:SS. First check the duration
    field; fall back to inspecting the first anchor encountered."""
    if duration_str:
        # duration is "H:MM:SS" or "M:SS" from fetch.fmt_duration
        if duration_str.count(":") == 2:
            return "hmmss"
        return "mmss"
    m = ANCHOR_RE.search(body)
    if m:
        return "hmmss" if m.group(1).count(":") == 2 else "mmss"
    return "mmss"


# --- highlight & paragraph location -----------------------------------------

HIGHLIGHT_RE = re.compile(r"==(.+?)==", re.DOTALL)


def find_highlights(body: str) -> list[dict]:
    """Find logical highlights in the body. Consecutive `==…==` marks separated
    only by paragraph breaks are merged into a single highlight — Obsidian's
    toggle-highlight hotkey wraps each paragraph independently when applied to
    a multi-paragraph selection, but the user's intent is one continuous span.
    A non-whitespace gap between two `==…==` marks (plain prose, another
    sentence, etc.) keeps them as independent highlights.

    Returns dicts with: start, end (offsets into body, encompassing all merged
    `==` marks), and text (the highlighted content with intervening paragraph
    breaks preserved and the artifact `==` markers stripped out).
    """
    matches = list(HIGHLIGHT_RE.finditer(body))
    if not matches:
        return []

    groups: list[list[re.Match]] = [[matches[0]]]
    for m in matches[1:]:
        prev = groups[-1][-1]
        gap = body[prev.end():m.start()]
        # Merge if the gap is whitespace-only and crosses at least one
        # paragraph break — the Obsidian hotkey artifact.
        if gap.strip() == "" and "\n\n" in gap:
            groups[-1].append(m)
        else:
            groups.append([m])

    out: list[dict] = []
    for group in groups:
        start = group[0].start()
        end = group[-1].end()
        if len(group) == 1:
            text = group[0].group(1)
        else:
            # Splice captured groups together, preserving the paragraph-break
            # gap text between adjacent matches so the merged text reads as
            # continuous prose.
            parts: list[str] = []
            for i, m in enumerate(group):
                parts.append(m.group(1))
                if i < len(group) - 1:
                    parts.append(body[m.end():group[i + 1].start()])
            text = "".join(parts)
        out.append({"start": start, "end": end, "text": text})
    return out


def split_paragraphs(body: str) -> list[tuple[int, int, str]]:
    """Split body into (start_offset, end_offset, text) paragraphs on `\\n\\n`.
    Offsets are into the original body string."""
    out: list[tuple[int, int, str]] = []
    pos = 0
    for chunk in body.split("\n\n"):
        start = pos
        end = pos + len(chunk)
        out.append((start, end, chunk))
        pos = end + 2  # skip the \n\n
    return out


def paragraph_index_at(paragraphs: list[tuple[int, int, str]], offset: int) -> int:
    """Return the index of the paragraph that contains `offset`."""
    for i, (s, e, _) in enumerate(paragraphs):
        if s <= offset <= e:
            return i
    # Past the end of the last paragraph — return the last index.
    return len(paragraphs) - 1


# --- plan-mode logic --------------------------------------------------------

def build_full_episode_plan(
    source_path: Path,
    fm: dict,
    body: str,
    project_root: Path,
) -> dict:
    """Scan `==highlights==` in the body and emit a manifest with one entry
    per highlight. Each entry carries enough context for Claude to fill in the
    topic / summary / cleaned_transcript and for `write` to compute the target
    path and assemble the snippet file."""
    # Use a stripped body throughout so paragraph offsets and HIGHLIGHT_RE
    # match offsets are in the same coordinate space.
    body = body.strip("\n")
    paragraphs = split_paragraphs(body)
    anchor_fmt = detect_anchor_fmt(body, fm.get("duration"))

    # Map each paragraph index to its anchor (parsed seconds). Some paragraphs
    # may legitimately lack an anchor — only the very first paragraph in a
    # hand-edited file, or transcripts produced before the anchor change.
    para_anchors_s: list[int | None] = []
    for _, _, text in paragraphs:
        a = anchor_at_paragraph_start(text)
        para_anchors_s.append(parse_clock(a) if a else None)

    duration_total_s = _duration_to_seconds(fm.get("duration"))

    out_dir = project_root / "raw" / "podcasts"
    source_stem = source_path.stem

    highlights: list[dict] = []
    for hi, hl in enumerate(find_highlights(body)):
        h_start = hl["start"]
        h_end = hl["end"]
        h_text = hl["text"]

        if re.search(r"(?<!=)==(?!=)", h_text):
            # find_highlights merges Obsidian-hotkey paragraph artifacts, so an
            # `==` left in h_text is a genuine nested-marker case that would
            # break framing. Warn the user.
            print(
                f"warning: highlight #{hi} contains nested `==` markers; "
                f"output may misparse — fix in source",
                file=sys.stderr,
            )

        p_start = paragraph_index_at(paragraphs, h_start)
        p_end = paragraph_index_at(paragraphs, h_end)
        spans_paragraphs = p_end - p_start + 1

        preceding_s = _resolve_preceding_anchor(para_anchors_s, p_start)
        following_s = _resolve_following_anchor(
            para_anchors_s, p_end, duration_total_s
        )

        clip_range = (
            f"{_fmt_clip(preceding_s, anchor_fmt)}-"
            f"{_fmt_clip(following_s, anchor_fmt)}"
        )

        # raw_text = the full text of all paragraphs the highlight touches,
        # joined with the same `\n\n` separator they had in the source. This
        # preserves the source's `[MM:SS]` anchors so the carved snippet's
        # Raw Transcript section reads identically to the source's spliced view.
        raw_text = "\n\n".join(
            paragraphs[i][2] for i in range(p_start, p_end + 1)
        )

        highlights.append({
            "id": hi,
            "raw_text": raw_text,
            "highlight_text": h_text.strip(),
            "preceding_anchor": _fmt_clip(preceding_s, anchor_fmt),
            "following_anchor": _fmt_clip(following_s, anchor_fmt),
            "clip_range": clip_range,
            "spans_paragraphs": spans_paragraphs,
            "topic_inferred": None,
            "topic_user_confirmed": None,
            "summary": None,
            "cleaned_transcript": None,
            # `exists` is best-effort; the real path depends on the topic Claude
            # picks, so we mark False here and recompute in `write`.
            "exists": False,
            "_target_dir": str(out_dir.relative_to(project_root)),
        })

    return {
        "mode": "full-episode",
        "source_path": str(source_path.relative_to(project_root)),
        "source_stem": source_stem,
        "anchor_fmt": anchor_fmt,
        "frontmatter_inherit": fm,
        "highlights": highlights,
    }


def build_snippet_plan(
    source_path: Path,
    fm: dict,
    body: str,
    project_root: Path,
) -> dict:
    """For an existing snippet file (or a fresh `/transcript --clip` output
    that hasn't been structured yet), emit a single-entry manifest. The
    `raw_text` is the existing Raw Transcript section if present; otherwise
    the entire body after the H1 heading is treated as raw."""
    raw_text = _extract_raw_transcript_section(body) or _strip_h1(body)

    # If the file already has a Notes section, refuse to operate when ==…==
    # markers appear there (the user is using highlights for their own notes
    # and we'd misparse them as carve targets).
    notes_section = _extract_section(body, "Notes")
    if notes_section and HIGHLIGHT_RE.search(notes_section):
        sys.exit(
            "error: ==highlight== markers found inside the Notes section. "
            "Notes is user-owned; remove the highlights or rename the section "
            "to disambiguate before regenerating."
        )

    clip = fm.get("clip")
    if clip and "-" in clip:
        clip_pre, clip_post = clip.split("-", 1)
    else:
        clip_pre = clip_post = None

    return {
        "mode": "snippet-regen",
        "source_path": str(source_path.relative_to(project_root)),
        "source_stem": source_path.stem,
        "anchor_fmt": detect_anchor_fmt(raw_text, fm.get("duration")),
        "frontmatter_inherit": fm,
        "highlights": [{
            "id": 0,
            "raw_text": raw_text.strip(),
            "highlight_text": raw_text.strip(),
            "preceding_anchor": clip_pre,
            "following_anchor": clip_post,
            "clip_range": clip,
            "spans_paragraphs": raw_text.count("\n\n") + 1,
            "topic_inferred": fm.get("clip_topic"),
            "topic_user_confirmed": None,
            "summary": None,
            "cleaned_transcript": None,
            "exists": True,
        }],
    }


# --- helpers ----------------------------------------------------------------

def _duration_to_seconds(s: str | None) -> int | None:
    if not s:
        return None
    parts = [int(p) for p in s.split(":")]
    if len(parts) == 2:
        return parts[0] * 60 + parts[1]
    if len(parts) == 3:
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    return None


def _fmt_clip(seconds: int | None, fmt: str) -> str:
    """Render seconds as `MM:SS` or `H:MM:SS` for clip-range strings (no
    surrounding brackets — those are for body anchors)."""
    if seconds is None:
        return "0:00"
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    if fmt == "hmmss":
        return f"{h}:{m:02d}:{s:02d}"
    # MM:SS — but if H is non-zero (clip is past the 1-hour mark in a sub-1hr
    # episode, which shouldn't happen, but…), promote to HH:MM:SS gracefully.
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def _resolve_preceding_anchor(
    anchors: list[int | None], p_start_idx: int
) -> int:
    """Walk backward from p_start_idx to find the first anchor; default 0."""
    for i in range(p_start_idx, -1, -1):
        if anchors[i] is not None:
            return anchors[i]  # type: ignore
    return 0


def _resolve_following_anchor(
    anchors: list[int | None], p_end_idx: int, duration_s: int | None
) -> int:
    """Walk forward from p_end_idx + 1 to find the next anchor. Defaults to
    episode duration when no later anchor exists; falls back to last known
    anchor + 60 when even duration is missing."""
    for i in range(p_end_idx + 1, len(anchors)):
        if anchors[i] is not None:
            return anchors[i]  # type: ignore
    if duration_s is not None:
        return duration_s
    # Final fallback: anchor at p_end_idx + 60s.
    if anchors[p_end_idx] is not None:
        return anchors[p_end_idx] + 60  # type: ignore
    return 60


SECTION_HEADING_RE = re.compile(r"^## (.+?)\s*$", re.MULTILINE)


def _extract_section(body: str, name: str) -> str | None:
    """Return the text of `## <name>` ... up to the next `## ` or `---` or EOF.
    Returns None when the section isn't present."""
    pattern = re.compile(
        rf"^## {re.escape(name)}\s*$\n(.*?)(?=^## |^---\s*$|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    m = pattern.search(body)
    return m.group(1).strip() if m else None


def _extract_raw_transcript_section(body: str) -> str | None:
    return _extract_section(body, "Raw Transcript")


def _strip_h1(body: str) -> str:
    """Drop a leading `# Title` line from a body, return the rest."""
    lines = body.splitlines()
    out: list[str] = []
    skipped_h1 = False
    for ln in lines:
        if not skipped_h1 and ln.startswith("# "):
            skipped_h1 = True
            continue
        out.append(ln)
    return "\n".join(out).lstrip("\n")


# --- write-mode logic -------------------------------------------------------

_DEFAULT_NOTES = (
    "<!-- Personal takeaways, connections to wiki pages, follow-up "
    "questions, contradictions. The agent never edits this section. -->"
)


def _is_snippet(fm: dict) -> bool:
    return bool(fm.get("clip")) or "podcast-clip" in (fm.get("tags") or [])


def write_full_episode_snippets(
    plan: dict, project_root: Path, force: bool
) -> None:
    fm_inherit = plan["frontmatter_inherit"]
    out_dir = project_root / "raw" / "podcasts"
    out_dir.mkdir(parents=True, exist_ok=True)

    written: list[str] = []
    skipped: list[str] = []

    for h in plan["highlights"]:
        topic = h.get("topic_user_confirmed") or h.get("topic_inferred")
        if not topic:
            sys.exit(f"error: highlight #{h['id']} missing topic; cannot write")
        if h.get("summary") is None or h.get("cleaned_transcript") is None:
            sys.exit(
                f"error: highlight #{h['id']} missing summary or cleaned_transcript; "
                f"plan must be filled before write"
            )

        # Compose target_stem from the already-safe source_stem and a separately-
        # cleaned topic. Don't run safe_stem on the combined form: source_stem is
        # already at the 80-char default cap from /transcript, and re-truncating
        # would drop the "(clip - topic)" suffix and collide with the source
        # filename. Topics are kebab-case by convention but we still sanitize
        # them defensively (cap at 60 chars; strip path-breakers).
        topic_safe = safe_stem(topic, max_len=60)
        target_stem = f"{plan['source_stem']} (clip - {topic_safe})"
        target_path = out_dir / f"{target_stem}.md"

        if target_path.exists() and not force:
            skipped.append(str(target_path.relative_to(project_root)))
            continue

        content = _assemble_snippet_file(
            fm_inherit=fm_inherit,
            source_stem=plan["source_stem"],
            topic=topic,
            clip_range=h["clip_range"],
            summary=h["summary"],
            cleaned=h["cleaned_transcript"],
            raw=h["raw_text"],
        )
        target_path.write_text(content, encoding="utf-8")
        written.append(str(target_path.relative_to(project_root)))

    # Report. One line per file for easy chat relay.
    for p in written:
        print(f"wrote: {p}")
    for p in skipped:
        print(f"skipped (exists): {p}")


def write_snippet_regen(plan: dict, project_root: Path) -> None:
    """Rewrite a single snippet file's Summary + Cleaned sections in place.
    Frontmatter is preserved (except ensuring `derived_from` if applicable);
    Notes and Raw Transcript are byte-identical."""
    h = plan["highlights"][0]
    if h.get("summary") is None or h.get("cleaned_transcript") is None:
        sys.exit("error: plan missing summary or cleaned_transcript")

    source_path = project_root / plan["source_path"]
    fm_inherit = plan["frontmatter_inherit"]
    existing_text = source_path.read_text(encoding="utf-8")
    existing_fm, existing_body = parse_frontmatter(existing_text)

    # Preserve Notes verbatim. Empty default when the file doesn't have one yet
    # (e.g. fresh `/transcript --clip` output being structured for the first
    # time).
    notes_section = _extract_section(existing_body, "Notes") or _DEFAULT_NOTES

    # Raw Transcript: prefer the existing section (byte-identical preservation);
    # else use raw_text from the plan (covers fresh `--clip` output case).
    raw = _extract_raw_transcript_section(existing_body) or h["raw_text"]

    # Reuse existing frontmatter wholesale — that pins `created` and any user
    # edits. Only the body sections are regenerated.
    title = existing_fm.get("title", fm_inherit.get("title", "untitled"))
    topic = (
        existing_fm.get("clip_topic")
        or h.get("topic_user_confirmed")
        or h.get("topic_inferred")
        or ""
    )

    new_content = (
        _emit_frontmatter(existing_fm)
        + f"\n\n# {title}"
        + (f" — {topic}" if topic else "")
        + "\n\n## Summary\n\n"
        + h["summary"].strip()
        + "\n\n## Cleaned Transcript\n\n"
        + h["cleaned_transcript"].strip()
        + "\n\n## Notes\n\n"
        + notes_section.strip()
        + "\n\n---\n\n## Raw Transcript\n\n"
        + raw.strip()
        + "\n"
    )
    source_path.write_text(new_content, encoding="utf-8")
    print(f"wrote: {source_path.relative_to(project_root)}")


def _assemble_snippet_file(
    fm_inherit: dict,
    source_stem: str,
    topic: str,
    clip_range: str,
    summary: str,
    cleaned: str,
    raw: str,
) -> str:
    """Compose a fresh snippet file from inherited frontmatter + per-clip data."""
    fm = dict(fm_inherit)
    fm["created"] = date.today().isoformat()
    fm["clip"] = clip_range
    fm["clip_topic"] = topic
    fm["derived_from"] = f"[[{source_stem}]]"
    # Tags: merge `podcast-clip` in (preserve any existing tags).
    tags = list(fm.get("tags") or [])
    if "podcast-clip" not in tags:
        tags.append("podcast-clip")
    fm["tags"] = tags

    title = fm.get("title", "untitled")

    return (
        _emit_frontmatter(fm)
        + f"\n\n# {title} — {topic}\n\n"
        + "## Summary\n\n"
        + summary.strip()
        + "\n\n## Cleaned Transcript\n\n"
        + cleaned.strip()
        + "\n\n## Notes\n\n"
        + _DEFAULT_NOTES
        + "\n\n---\n\n## Raw Transcript\n\n"
        + raw.strip()
        + "\n"
    )


# Field ordering for emitted frontmatter — matches fetch.py's order so a
# carved snippet sits naturally next to a `/transcript`-fetched full episode.
_FIELD_ORDER = [
    "title", "source", "show", "published", "created", "duration",
    "captions_source", "clip", "clip_topic", "derived_from", "tags",
]


def _emit_frontmatter(fm: dict) -> str:
    """Render a frontmatter dict back to the YAML subset we accept. Quotes
    string scalars; emits lists as indented `  - item` blocks."""
    lines: list[str] = ["---"]
    seen: set[str] = set()
    for key in _FIELD_ORDER:
        if key in fm and fm[key] is not None and fm[key] != "":
            lines.extend(_emit_field(key, fm[key]))
            seen.add(key)
    # Append any extra keys we don't know about (forward-compat).
    for key, val in fm.items():
        if key in seen or val is None or val == "":
            continue
        lines.extend(_emit_field(key, val))
    lines.append("---")
    return "\n".join(lines)


def _emit_field(key: str, val) -> list[str]:
    if isinstance(val, list):
        out = [f"{key}:"]
        for item in val:
            out.append(f"  - {item}")
        return out
    # String scalars get quoted unless they look like a bare URL / date / number
    # we know fetch.py emits unquoted.
    sval = str(val)
    if key in {"source", "published", "created", "captions_source"}:
        return [f"{key}: {sval}"]
    if key == "duration":
        return [f'duration: "{sval}"']
    if key == "clip":
        return [f'clip: "{sval}"']
    if key == "derived_from":
        # Wikilink — must be quoted per the YAML wikilink rule in AGENTS.md.
        return [f'derived_from: "{sval}"']
    # Default: double-quote.
    return [f"{key}: {yaml_dq(sval)}"]


# --- main -------------------------------------------------------------------

def cmd_plan(args) -> None:
    project_root = find_project_root()
    source_path = Path(args.input).resolve()
    if not source_path.is_file():
        sys.exit(f"error: not a file: {source_path}")
    text = source_path.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)

    if _is_snippet(fm):
        plan = build_snippet_plan(source_path, fm, body, project_root)
    else:
        plan = build_full_episode_plan(source_path, fm, body, project_root)
        if not plan["highlights"]:
            sys.exit(
                "error: no `==highlights==` found in source. Mark passages "
                "with Obsidian highlight syntax first, then re-run."
            )

    json.dump(plan, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")


def cmd_write(args) -> None:
    project_root = find_project_root()
    plan = json.load(sys.stdin)
    if plan.get("mode") == "snippet-regen":
        write_snippet_regen(plan, project_root)
    else:
        write_full_episode_snippets(plan, project_root, force=args.force)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_plan = sub.add_parser("plan", help="Read-only: emit a JSON plan to stdout.")
    p_plan.add_argument("input", help="Path to a full-episode or snippet .md file")
    p_plan.set_defaults(func=cmd_plan)

    p_write = sub.add_parser("write", help="Write snippet file(s) from a filled plan on stdin.")
    p_write.add_argument("input", help="Same input the plan was generated from")
    p_write.add_argument(
        "--plan-stdin", action="store_true", required=True,
        help="Read filled plan JSON from stdin (only mode supported).",
    )
    p_write.add_argument(
        "--force", action="store_true",
        help="Overwrite existing snippet files in full-episode mode.",
    )
    p_write.set_defaults(func=cmd_write)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
