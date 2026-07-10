---
type: concept
created: 2026-07-10
updated: 2026-07-10
sources:
  - "[[2026-04-04 LLM Wiki (Karpathy)]]"
raw:
  - raw/articles/2026-04-04 LLM Wiki (Karpathy).md
related:
  - "[[Three-Layer Architecture]]"
confidence: high
tags: [workflow]
---

# Ingest Workflow

The core write path of an LLM wiki: a new source arrives in `raw/`, and the LLM
**integrates** it rather than merely indexing it — reading it in full, extracting
what matters, and updating every wiki page it touches. A single source might touch
10–15 pages: entity pages gain facts, syntheses get strengthened or challenged,
contradictions with older claims get flagged instead of papered over.

The MycoForge house style, following Karpathy's own practice: **one source per
session**, with the user in the loop. Ingestion is judgment-heavy — what to
emphasize, what to contest, what to promote to its own page — so it stays
interactive. (This is also why the MCP server is read-only: capture and search
can be mechanical; integration can't.)

Every ingest ends with bookkeeping: an `index.md` entry per new page and an
`ingest |` line in `log.md`. Companion workflows: [[Query Workflow]] (the read
path) and [[Lint Workflow]] (the health check) — see `AGENTS.md` until those
pages are written.
