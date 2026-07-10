"""Tests for .template/onboard.py — marker processing, keep-set resolution, rename."""

from pathlib import Path

import onboard


# --- resolve_disabled -------------------------------------------------------

FEATURES = {
    "product": {"requires": []},
    "orchestrator": {"requires": []},
    "media-capture": {"requires": []},
    "mcp-server": {"requires": []},
}


def test_keep_all_disables_nothing():
    assert onboard.resolve_disabled(set(FEATURES), FEATURES) == set()


def test_keep_none_disables_everything():
    assert onboard.resolve_disabled(set(), FEATURES) == set(FEATURES)


def test_keep_subset():
    disabled = onboard.resolve_disabled({"product", "mcp-server"}, FEATURES)
    assert disabled == {"orchestrator", "media-capture"}


def test_requires_fixed_point():
    features = {
        "a": {"requires": []},
        "b": {"requires": ["a"]},
        "c": {"requires": ["b"]},
    }
    # keeping b and c without a cascades: dropping a drops b drops c
    assert onboard.resolve_disabled({"b", "c"}, features) == {"a", "b", "c"}


# --- marker processing: hash style ------------------------------------------

HASH_TEXT = """\
keep_always = 1
# sf:begin(media-capture)
[snippet]
glossary = {}
# sf:end(media-capture)
child_check()  # sf:keep-if(orchestrator)
tail = 2
"""


def test_hash_block_dropped_when_disabled():
    out = onboard.process_markers_text(HASH_TEXT, {"media-capture"}, onboard.HASH_RES)
    assert "glossary" not in out
    assert "sf:begin" not in out and "sf:end" not in out
    assert "child_check()" in out  # orchestrator kept: line survives, marker stripped
    assert "keep-if" not in out


def test_hash_block_kept_strips_markers():
    out = onboard.process_markers_text(HASH_TEXT, set(), onboard.HASH_RES)
    assert "glossary = {}" in out
    assert "sf:" not in out
    assert "child_check()" in out and "keep-if" not in out


def test_hash_keepif_dropped():
    out = onboard.process_markers_text(HASH_TEXT, {"orchestrator"}, onboard.HASH_RES)
    assert "child_check" not in out
    assert "tail = 2" in out


def test_hyphenated_feature_ids_match():
    text = "# sf:begin(mcp-server)\nx = 1\n# sf:end(mcp-server)\n"
    assert "x = 1" not in onboard.process_markers_text(
        text, {"mcp-server"}, onboard.HASH_RES)
    kept = onboard.process_markers_text(text, set(), onboard.HASH_RES)
    assert "x = 1" in kept and "sf:" not in kept


# --- marker processing: html style (markdown) --------------------------------

MD_TEXT = """\
# Heading

Trunk prose.

<!-- sf:begin(product) -->
## Decisions

- [[ADR-001]]
<!-- sf:end(product) -->

| a | b | <!-- sf:keep-if(orchestrator) -->
tail
"""


def test_html_block_dropped():
    out = onboard.process_markers_text(MD_TEXT, {"product"}, onboard.HTML_RES)
    assert "ADR-001" not in out and "Decisions" not in out
    assert "Trunk prose." in out


def test_html_block_kept_strips_markers():
    out = onboard.process_markers_text(MD_TEXT, set(), onboard.HTML_RES)
    assert "- [[ADR-001]]" in out
    assert "sf:" not in out
    assert "| a | b |" in out and "<!--" not in out


def test_html_keepif_dropped_and_stripped():
    dropped = onboard.process_markers_text(MD_TEXT, {"orchestrator"}, onboard.HTML_RES)
    assert "| a | b |" not in dropped
    kept = onboard.process_markers_text(MD_TEXT, set(), onboard.HTML_RES)
    assert "| a | b |" in kept and "keep-if" not in kept


def test_marker_style_chosen_by_suffix(tmp_path):
    assert onboard.marker_res_for(Path("x.md")) is onboard.HTML_RES
    assert onboard.marker_res_for(Path("x.py")) is onboard.HASH_RES
    assert onboard.marker_res_for(Path("kb.toml")) is onboard.HASH_RES
    assert onboard.marker_res_for(Path(".gitignore")) is onboard.HASH_RES
    assert onboard.marker_res_for(Path("x.json")) is None  # JSON: wholly-owned only


def test_docs_with_placeholder_ids_are_not_markers():
    # Prose documenting the syntax uses <id> placeholders; [\w-]+ must not match.
    text = "Wrap blocks in `# sf:begin(<id>)` ... `# sf:end(<id>)` markers.\n"
    assert onboard.process_markers_text(text, {"product"}, onboard.HASH_RES) == text


# --- rename ------------------------------------------------------------------

def test_rename_preserves_template_repo_pin(tmp_path):
    kb = tmp_path / "kb.toml"
    kb.write_text(
        '[kb]\nslug = "mycoforge"\nbrand = "MycoForge"\n\n'
        '[template]\nversion = "0.1.0"\n'
        'repo = "https://github.com/LukeMainwaring/mycoforge"\n',
        encoding="utf-8",
    )
    page = tmp_path / "page.md"
    page.write_text("MycoForge is a mycoforge instance.\n", encoding="utf-8")
    onboard.do_rename({"slug": "mycoforge", "brand": "MycoForge"},
                      "testkb", "TestKB", apply=True, root=tmp_path)
    kb_text = kb.read_text(encoding="utf-8")
    assert 'slug = "testkb"' in kb_text
    assert 'brand = "TestKB"' in kb_text
    assert 'repo = "https://github.com/LukeMainwaring/mycoforge"' in kb_text
    assert page.read_text(encoding="utf-8") == "TestKB is a testkb instance.\n"


def test_rename_defaults_brand_from_slug(tmp_path):
    page = tmp_path / "page.md"
    page.write_text("MycoForge / mycoforge\n", encoding="utf-8")
    onboard.do_rename({"slug": "mycoforge", "brand": "MycoForge"},
                      "notes", None, apply=True, root=tmp_path)
    assert page.read_text(encoding="utf-8") == "Notes / notes\n"


# --- delete_paths ------------------------------------------------------------

def test_delete_paths(tmp_path):
    (tmp_path / "mcp").mkdir()
    (tmp_path / "mcp/server.py").write_text("x\n", encoding="utf-8")
    (tmp_path / ".mcp.json").write_text("{}\n", encoding="utf-8")
    features = {"mcp-server": {"paths": ["mcp", ".mcp.json"]}}
    onboard.delete_paths({"mcp-server"}, features, apply=True, root=tmp_path)
    assert not (tmp_path / "mcp").exists()
    assert not (tmp_path / ".mcp.json").exists()


def test_delete_paths_dry_run(tmp_path):
    (tmp_path / ".mcp.json").write_text("{}\n", encoding="utf-8")
    features = {"mcp-server": {"paths": [".mcp.json"]}}
    onboard.delete_paths({"mcp-server"}, features, apply=False, root=tmp_path)
    assert (tmp_path / ".mcp.json").exists()
