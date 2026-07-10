"""Tests for scripts/lint.py against synthetic KB fixtures."""

from pathlib import Path

import lint


def make_kb(root: Path, kb_toml: str = "", pages: dict[str, str] | None = None) -> Path:
    """Build a minimal KB tree: kb.toml + wiki/ + any extra pages given."""
    (root / "wiki").mkdir(parents=True, exist_ok=True)
    (root / "kb.toml").write_text(kb_toml or "[kb]\nslug = 'testkb'\n", encoding="utf-8")
    defaults = {
        "wiki/index.md": "# Index\n",
        "wiki/log.md": "# Log\n",
    }
    for relpath, text in {**defaults, **(pages or {})}.items():
        p = root / relpath
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    return root


def test_clean_kb_has_no_issues(tmp_path):
    make_kb(tmp_path, pages={
        "wiki/index.md": "# Index\n- [[Alpha]] — a page\n- [[overview]]\n",
        "wiki/overview.md": "Start at [[Alpha]].\n",
        "wiki/Alpha.md": "Linked from [[overview]].\n",
    })
    issues = lint.run(tmp_path)
    assert issues.errors == []
    assert issues.warnings == []


def test_broken_wikilink_is_error(tmp_path):
    make_kb(tmp_path, pages={
        "wiki/index.md": "- [[Alpha]]\n",
        "wiki/Alpha.md": "See [[Nowhere]]. Inbound: [[Alpha]] from index only.\n",
    })
    issues = lint.run(tmp_path)
    assert any("broken wikilink [[Nowhere]]" in e for e in issues.errors)


def test_code_blocks_and_inline_code_are_stripped(tmp_path):
    make_kb(tmp_path, pages={
        "wiki/index.md": "- [[Alpha]]\n- [[overview]]\n",
        "wiki/overview.md": "hub [[Alpha]]\n",
        "wiki/Alpha.md": (
            "Linking works like `[[Not A Page]]` in Obsidian.\n"
            "```\n[[Also Not A Page]]\n```\n"
        ),
    })
    issues = lint.run(tmp_path)
    assert issues.errors == []


def test_piped_links_and_anchors_resolve(tmp_path):
    make_kb(tmp_path, pages={
        "wiki/index.md": "- [[Alpha]]\n- [[overview]]\n",
        "wiki/overview.md": "hub [[Alpha]]\n",
        "wiki/Alpha.md": "See [[Alpha|this very page]] and [[Alpha#Heading]] "
                         "and [[Alpha#Heading|both]].\n",
    })
    issues = lint.run(tmp_path)
    assert issues.errors == []


def test_intentional_forward_links_suppressed(tmp_path):
    make_kb(
        tmp_path,
        kb_toml='[lint]\nintentional_forward_links = ["Future Page"]\n',
        pages={
            "wiki/index.md": "- [[Alpha]]\n- [[overview]]\n",
            "wiki/overview.md": "hub [[Alpha]]\n",
            "wiki/Alpha.md": "Will write [[Future Page]] eventually.\n",
        },
    )
    issues = lint.run(tmp_path)
    assert issues.errors == []


def test_index_audit_missing_and_ghost(tmp_path):
    make_kb(tmp_path, pages={
        "wiki/index.md": "- [[Ghost Page]]\n",
        "wiki/Alpha.md": "Some page. [[Alpha]] inbound comes from overview.\n",
        "wiki/overview.md": "hub [[Alpha]]\n",
    })
    issues = lint.run(tmp_path)
    assert any("wiki/Alpha.md: missing from wiki/index.md" in e for e in issues.errors)
    assert any("broken wikilink [[Ghost Page]]" in e for e in issues.errors)
    assert any("wiki/overview.md: missing from" in e for e in issues.errors)


def test_raw_frontmatter_refs(tmp_path):
    (tmp_path / "raw/articles").mkdir(parents=True)
    (tmp_path / "raw/articles/2026-01-01 Real.md").write_text("src\n", encoding="utf-8")
    make_kb(tmp_path, pages={
        "wiki/index.md": "- [[Alpha]] - [[Beta]]\n",
        "wiki/overview.md": "hub [[Alpha]] [[Beta]]\n",
        "wiki/Alpha.md": (
            "---\ntype: concept\nraw:\n  - raw/articles/2026-01-01 Real.md\n---\nok\n"
        ),
        "wiki/Beta.md": (
            "---\ntype: concept\nraw:\n  - raw/articles/2026-01-01 Missing.md\n---\nbad\n"
        ),
    })
    issues = lint.run(tmp_path)
    assert not any("Alpha" in e and "raw:" in e for e in issues.errors)
    assert any("Beta" in e and "raw: reference not found" in e for e in issues.errors)


def test_orphan_detection(tmp_path):
    make_kb(tmp_path, pages={
        "wiki/index.md": "- [[Alpha]]\n- [[Lonely]]\n- [[overview]]\n",
        "wiki/overview.md": "hub [[Alpha]]\n",
        "wiki/Alpha.md": "content\n",
        "wiki/Lonely.md": "nobody links here except the index\n",
    })
    issues = lint.run(tmp_path)
    assert any("Lonely" in w and "orphan" in w for w in issues.warnings)
    assert not any("Alpha" in w and "orphan" in w for w in issues.warnings)


def test_stale_check(tmp_path):
    make_kb(
        tmp_path,
        kb_toml="[lint]\nstale_after_days = 30\n",
        pages={
            "wiki/index.md": "- [[Old]]\n- [[overview]]\n",
            "wiki/overview.md": "hub [[Old]]\n",
            "wiki/Old.md": "---\ntype: concept\nupdated: 2020-01-01\n---\nold\n",
        },
    )
    issues = lint.run(tmp_path)
    assert any("Old" in w and "stale" in w for w in issues.warnings)


def test_stale_disabled_by_default(tmp_path):
    make_kb(tmp_path, pages={
        "wiki/index.md": "- [[Old]]\n- [[overview]]\n",
        "wiki/overview.md": "hub [[Old]]\n",
        "wiki/Old.md": "---\ntype: concept\nupdated: 2020-01-01\n---\nold\n",
    })
    issues = lint.run(tmp_path)
    assert not any("stale" in w for w in issues.warnings)


def test_concept_candidate_fires_and_is_satisfied_by_title(tmp_path):
    make_kb(
        tmp_path,
        kb_toml='[lint]\nconcept_candidate_terms = ["entropy", "gravity"]\n',
        pages={
            "wiki/index.md": "- [[Alpha]]\n- [[Gravity Well]]\n- [[overview]]\n",
            "wiki/overview.md": "hub [[Alpha]] [[Gravity Well]]\n",
            "wiki/Alpha.md": "entropy rises. entropy falls. entropy stays.\n",
            "wiki/Gravity Well.md": "gravity gravity gravity gravity\n",
        },
    )
    issues = lint.run(tmp_path)
    assert any("'entropy'" in w and "concept candidate" in w for w in issues.warnings)
    # "gravity" recurs too, but the "Gravity Well" page title covers it.
    assert not any("'gravity'" in w for w in issues.warnings)


# sf:begin(orchestrator)
def test_child_kb_checks(tmp_path):
    (tmp_path / "kids/real").mkdir(parents=True)
    (tmp_path / "kids/real/kb.toml").write_text("[kb]\nslug='child'\n", encoding="utf-8")
    (tmp_path / "kids/bare").mkdir(parents=True)
    make_kb(
        tmp_path,
        kb_toml=(
            "[orchestrator]\nparent = ''\n"
            '[[orchestrator.children]]\npath = "kids/real"\nscope = "ok"\n'
            '[[orchestrator.children]]\npath = "kids/bare"\nscope = "no kb.toml"\n'
            '[[orchestrator.children]]\npath = "kids/ghost"\nscope = "missing"\n'
        ),
    )
    issues = lint.run(tmp_path)
    assert any("kids/bare" in e and "no kb.toml" in e for e in issues.errors)
    assert any("kids/ghost" in e and "does not exist" in e for e in issues.errors)
    assert not any("kids/real" in e for e in issues.errors)


def test_cross_kb_link_is_warning_not_error(tmp_path):
    child = tmp_path / "kids/real"
    (child / "wiki").mkdir(parents=True)
    (child / "kb.toml").write_text("[kb]\nslug='child'\n", encoding="utf-8")
    (child / "wiki/Child Page.md").write_text("hello\n", encoding="utf-8")
    make_kb(
        tmp_path,
        kb_toml=(
            "[orchestrator]\nparent = ''\n"
            '[[orchestrator.children]]\npath = "kids/real"\nscope = "ok"\n'
        ),
        pages={
            "wiki/index.md": "- [[Alpha]]\n- [[overview]]\n",
            "wiki/overview.md": "hub [[Alpha]]\n",
            "wiki/Alpha.md": "See [[Child Page]] over in the child KB.\n",
        },
    )
    # The child is its own repo; the parent must not scan into it as own content.
    issues = lint.run(tmp_path)
    assert not any("Child Page" in e for e in issues.errors)
    assert any("cross-KB link [[Child Page]]" in w for w in issues.warnings)
# sf:end(orchestrator)


def test_exit_codes(tmp_path):
    import subprocess
    import sys as _sys
    script = Path(lint.__file__)
    make_kb(tmp_path, pages={
        "wiki/index.md": "- [[Alpha]]\n- [[overview]]\n",
        "wiki/overview.md": "hub [[Alpha]]\n",
        "wiki/Alpha.md": "fine\n",
    })
    ok = subprocess.run([_sys.executable, str(script), "--root", str(tmp_path)],
                        capture_output=True, text=True)
    assert ok.returncode == 0, ok.stdout
    (tmp_path / "wiki/Alpha.md").write_text("See [[Nowhere]].\n", encoding="utf-8")
    bad = subprocess.run([_sys.executable, str(script), "--root", str(tmp_path)],
                         capture_output=True, text=True)
    assert bad.returncode == 1, bad.stdout
    assert "broken wikilink" in bad.stdout
