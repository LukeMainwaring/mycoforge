---
type: decision
status: accepted
created: 2026-07-10
updated: 2026-07-10
related:
  - "[[ADR-001 Separate Repo with Product as Seam]]"
  - "[[Ingest Workflow]]"
tags: [adr, mcp]
---

# ADR-004 Read-Only MCP in v1

## Context

Product repos (and any other agent session) need to consult the KB without
opening it in an editor. MCP is the natural bridge. How much of the KB should it
expose — and in particular, should agents be able to write to the wiki remotely?

## Decision

The MCP server is **read-only and minimal in v1**: three tools —
`search_kb(query, scope?)` (ripgrep-backed full-text search), `read_page(name)`,
and `get_index()`. No write tools, no embeddings. Ingestion stays what it is in
the [[Ingest Workflow]]: an interactive, judgment-heavy workflow run in a harness
session inside the KB.

## Consequences

- A product repo attaches the KB with one `.mcp.json` line and can search and
  read it, but can never corrupt it — the trust boundary is structural, not
  behavioral.
- Search is ripgrep over markdown (with a pure-Python fallback): zero index to
  build or invalidate, which matches the index-first navigation bet in
  [[Why LLM Wikis Beat RAG]].
- Remote sessions that discover something wiki-worthy must hand it back to a KB
  session (or the user) rather than filing it themselves — mildly annoying,
  deliberately so.

## Alternatives

- **Write tools (`add_page`, `append_log`)** — rejected for v1: ingestion quality
  depends on the human-in-the-loop discussion; an API invites drive-by writes
  that erode the schema. Documented as a graduation path.
- **Embeddings/semantic search** — rejected for v1: personal-scale KBs navigate
  fine index-first; revisit if scale proves otherwise.
