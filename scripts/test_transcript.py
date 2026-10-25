"""Tests for the pure helpers in .agents/skills/transcript/fetch.py (no network)."""

import importlib.util
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
FETCH = REPO / ".agents" / "skills" / "transcript" / "fetch.py"

# Loaded by path: the skill directory isn't a package.
_spec = importlib.util.spec_from_file_location("transcript_fetch", FETCH)
fetch = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(fetch)


def test_pick_prefers_regional_manual_track():
    meta = {
        "subtitles": {"en-US": [{}], "live_chat": [{}]},
        "automatic_captions": {"en-orig": [{}], "en": [{}]},
    }
    assert fetch.pick_caption_track(meta, "en") == ("en-US", "subtitles", "youtube-manual")


def test_pick_exact_manual_before_regional():
    meta = {"subtitles": {"en-GB": [{}], "en": [{}]}}
    assert fetch.pick_caption_track(meta, "en")[0] == "en"


def test_pick_original_language_asr():
    meta = {"subtitles": {}, "automatic_captions": {"en-orig": [{}], "en": [{}], "fr": [{}]}}
    assert fetch.pick_caption_track(meta, "en") == (
        "en-orig", "automatic_captions", "youtube-auto")


def test_pick_flags_machine_translation():
    meta = {"automatic_captions": {"es-orig": [{}], "es": [{}], "en": [{}]}}
    assert fetch.pick_caption_track(meta, "en")[2] == "youtube-auto-translated"


def test_pick_none_when_language_missing():
    assert fetch.pick_caption_track({"automatic_captions": {"de-orig": [{}]}}, "en") is None
    assert fetch.pick_caption_track({}, "en") is None


VTT = """WEBVTT
Kind: captions
Language: en

00:00:01.000 --> 00:00:03.000
hello &lt;c&gt;there&lt;/c&gt;

00:00:03.000 --> 00:00:05.000 align:start position:0%
hello there
<00:00:03.500><c>general</c> kenobi

00:00:05.000 --> 00:00:07.000
general kenobi
"""


def test_parse_vtt_strips_tags_and_keeps_lines():
    cues = fetch.parse_vtt(VTT)
    assert [c[2] for c in cues] == [
        ["hello there"], ["hello there", "general kenobi"], ["general kenobi"]]
    assert cues[1][0] == 3.0


def test_rolling_window_repeats_collapse():
    timed = fetch.cues_to_timed_lines(fetch.parse_vtt(VTT))
    assert timed == [(1.0, "hello there"), (3.0, "general kenobi")]


def test_distant_repeat_is_kept():
    cues = [(0.0, 1.0, ["Yeah."]), (1.0, 2.0, ["so the point is"]),
            (2.0, 3.0, ["it compounds"]), (3.0, 4.0, ["right"]),
            (4.0, 5.0, ["Yeah."])]
    lines = [ln for _, ln in fetch.cues_to_timed_lines(cues)]
    assert lines.count("Yeah.") == 2
