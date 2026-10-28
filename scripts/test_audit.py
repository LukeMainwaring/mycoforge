"""Tests for scripts/audit.py against synthetic KB fixtures in a throwaway git repo."""

import subprocess
from pathlib import Path

import audit


def git(root: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=root, check=True,
                          capture_output=True, text=True).stdout.strip()


def make_repo(root: Path, files: dict[str, str]) -> str:
    """Init a repo with the given files committed; return the commit sha."""
    git(root, "init", "-q")
    git(root, "config", "user.email", "t@example.com")
    git(root, "config", "user.name", "t")
    write(root, files)
    git(root, "add", "-A")
    git(root, "commit", "-qm", "init")
    return git(root, "rev-parse", "--short", "HEAD")


def write(root: Path, files: dict[str, str]) -> None:
    for relpath, text in files.items():
        p = root / relpath
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")


def commit_all(root: Path, msg: str) -> None:
    git(root, "add", "-A")
    git(root, "commit", "-qm", msg)


def test_lint_part_passes_lint_output_through(tmp_path):
    write(tmp_path, {"kb.toml": "[kb]\nslug = 'testkb'\n", "wiki/index.md": "- [[Nowhere]]\n",
                     "wiki/log.md": "# Log\n"})
    code, out = audit.lint_part(tmp_path)
    assert code == 1
    assert "ERROR" in out and "1 error(s)" in out


# sf:begin(architecture)
def arch_page(commit: str, extra: str = "") -> str:
    return (f"---\ntype: architecture\ncommit: {commit}\nwatches:\n  - wiki/Alpha.md\n{extra}---\n"
            "# Page\n")


def test_architecture_current_then_stale(tmp_path):
    sha = make_repo(tmp_path, {"wiki/Alpha.md": "a\n", "wiki/Beta.md": "b\n"})
    write(tmp_path, {"architecture/Page.md": arch_page(sha)})
    commit_all(tmp_path, "page")
    assert "0 stale, 1 current" in audit.architecture_part(tmp_path)

    write(tmp_path, {"wiki/Beta.md": "b2\n"})  # unwatched change
    commit_all(tmp_path, "beta")
    assert "0 stale, 1 current" in audit.architecture_part(tmp_path)

    write(tmp_path, {"wiki/Alpha.md": "a2\n"})
    out = audit.architecture_part(tmp_path)
    assert "uncommitted under Page's watches: wiki/Alpha.md" in out
    commit_all(tmp_path, "alpha")
    out = audit.architecture_part(tmp_path)
    assert "1 stale, 0 current" in out
    assert f"stale Page (commit {sha}): wiki/Alpha.md" in out


def test_missing_commit_is_stale(tmp_path):
    make_repo(tmp_path, {"wiki/Alpha.md": "a\n", "architecture/Page.md": arch_page("deadbee")})
    assert "stale Page: commit deadbee not found" in audit.architecture_part(tmp_path)


def test_diagram_stale_from_its_own_revision(tmp_path):
    sha = make_repo(tmp_path, {"wiki/Alpha.md": "a\n"})
    full = git(tmp_path, "rev-parse", "HEAD")
    write(tmp_path, {
        "architecture/diagrams/page/candidate.json":
            f'{{"meta": {{"repository": {{"revision": "{full}"}}}}}}',
        "wiki/Alpha.md": "a2\n",
    })
    commit_all(tmp_path, "render, then alpha changes")
    head = git(tmp_path, "rev-parse", "--short", "HEAD")
    write(tmp_path, {"architecture/Page.md": arch_page(head) + (
        "Rendered with archify: [diagrams/page](diagrams/page/page.html) (open locally).\n")})
    commit_all(tmp_path, "page updated, diagram not re-rendered")
    out = audit.architecture_part(tmp_path)
    assert "0 stale, 1 current, 1 stale diagram(s)" in out
    assert f"stale diagram diagrams/page (revision {sha[:7]}): wiki/Alpha.md" in out


def test_new_entries_listed(tmp_path):
    sha = make_repo(tmp_path, {"wiki/Alpha.md": "a\n"})
    write(tmp_path, {"architecture/Overview.md": arch_page(sha, "new_entries:\n  - wiki\n"),
                     "wiki/Gamma.md": "g\n"})
    commit_all(tmp_path, "gamma")
    assert f"new under Overview's new_entries since {sha}: wiki/Gamma.md" \
        in audit.architecture_part(tmp_path)
# sf:end(architecture)


# sf:begin(insight)
LEDGER = """# Scout ledger

## [2026-10-01] window 2026-07-01 → 2026-10-01

| # | source | date | kind | adds | status |
|---|--------|------|------|------|--------|
| 1 | [A](https://a.example) | 2026-09-30 | article | a | approved |
| 2 | [B](https://b.example) | 2026-09-29 | article | b | rejected |

## [2026-10-20] window 2026-10-01 → 2026-10-20

unreachable: https://c.example (timed out); window stays open from 2026-10-01

| # | source | date | kind | adds | status |
|---|--------|------|------|------|--------|
| 1 | [D](https://d.example) | 2026-10-19 | repo | d | candidate |
| 2 | [E](https://e.example) | 2026-10-18 | article | e | captured → raw/articles/2026-10-18 E.md |
"""


def test_scout_counts_and_latest_section(tmp_path):
    make_repo(tmp_path, {"staging/scout.md": LEDGER})
    out = audit.scout_part(tmp_path)
    assert out.startswith("scout: latest run 2026-10-20 — 1 new candidate(s); "
                          "ledger-wide 1 candidate, 1 approved awaiting capture; "
                          "1 unreachable line(s); ledger uncommitted changes: no")
    assert "[D](https://d.example)" in out
    assert "[A](https://a.example)" not in out

    write(tmp_path, {"staging/scout.md": LEDGER + "\n## [2026-10-28] window 2026-10-20 → 2026-10-28\n\nnothing new\n"})
    out = audit.scout_part(tmp_path)
    assert "latest run 2026-10-28 — 0 new candidate(s)" in out
    assert "ledger uncommitted changes: yes" in out
# sf:end(insight)
