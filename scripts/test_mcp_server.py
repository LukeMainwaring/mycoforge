"""Smoke test for mcp/server.py: connect in-process and call all three tools.

Needs the mcp SDK in the test env. Run it against the server's locked deps, as
the template's verify_matrix does:
    uv export --script mcp/server.py --no-hashes --quiet > /tmp/mcp-reqs.txt
    uvx --with pytest --with-requirements /tmp/mcp-reqs.txt pytest -q scripts
"""

import importlib.util
from pathlib import Path

import pytest

mcp_sdk = pytest.importorskip("mcp")
from mcp import Client

REPO = Path(__file__).resolve().parent.parent
SERVER = REPO / "mcp" / "server.py"
TOOLS = {"search_kb", "read_page", "get_index"}


def _load_server():
    # Loaded by path: the `mcp/` directory would shadow the `mcp` package on import.
    spec = importlib.util.spec_from_file_location("mycoforge_mcp_server", SERVER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.mcp


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def client():
    async with Client(_load_server(), raise_exceptions=True) as c:
        yield c


def _text(result) -> str:
    return "".join(c.text for c in result.content if hasattr(c, "text"))


@pytest.mark.anyio
async def test_lists_exactly_the_three_read_only_tools(client):
    tools = await client.list_tools()
    assert {t.name for t in tools.tools} == TOOLS


@pytest.mark.anyio
async def test_get_index_returns_the_catalog(client):
    result = await client.call_tool("get_index", {})
    assert not result.is_error
    assert _text(result) == (REPO / "wiki" / "index.md").read_text(encoding="utf-8")


@pytest.mark.anyio
async def test_search_kb_finds_a_known_term(client):
    result = await client.call_tool("search_kb", {"query": "index", "scope": "wiki"})
    assert not result.is_error
    assert "wiki/" in _text(result)


@pytest.mark.anyio
async def test_search_kb_rejects_bad_scope(client):
    result = await client.call_tool("search_kb", {"query": "x", "scope": "nope"})
    assert result.is_error
    assert "scope must be one of" in _text(result)


@pytest.mark.anyio
async def test_read_page_by_name_and_by_path(client):
    by_path = await client.call_tool("read_page", {"name": "wiki/index.md"})
    assert not by_path.is_error
    first = next(
        p for p in sorted((REPO / "wiki").rglob("*.md")) if p.name not in ("index.md", "log.md")
    )
    by_name = await client.call_tool("read_page", {"name": first.stem})
    assert not by_name.is_error
    assert _text(by_name).startswith(f"<!-- {first.relative_to(REPO)} -->")


@pytest.mark.anyio
async def test_read_page_missing_is_a_tool_error(client):
    result = await client.call_tool("read_page", {"name": "No Such Page Ever"})
    assert result.is_error
    assert "no page named" in _text(result)
