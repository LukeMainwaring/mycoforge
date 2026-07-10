---
type: dashboard
created: 2026-07-10
updated: 2026-07-10
tags: [meta]
---

# MycoForge

The dashboard — a map of content, kept current by the LLM.

## The wiki

- [[overview]] — what this KB is and where to start
- [[index]] — the full catalog · [[log]] — the append-only history
- Highlights: [[Three-Layer Architecture]] · [[Why LLM Wikis Beat RAG]] ·
  [[Fractal Federation]]

## The product layer

- [[Vision]] — why this template exists
- [[MVP]] — what v0.1 ships
- [[roadmap]] — Now / Next / Later / Done
- Decisions: [[ADR-001 Separate Repo with Product as Seam]] ·
  [[ADR-002 Fractal Federation for Nested KBs]] ·
  [[ADR-003 Copy-and-Own with Config-Code Split]] ·
  [[ADR-004 Read-Only MCP in v1]]
- Software: [[KB Stats Dashboard (Example)]] — the embedded-prompt convention,
  by example

## Operating this KB

The schema is `AGENTS.md` (start there). Health check: `python3 scripts/lint.py`.
