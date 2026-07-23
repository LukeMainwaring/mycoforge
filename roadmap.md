---
type: roadmap
created: 2026-07-10
updated: 2026-07-23
tags: [product]
---

# Roadmap

Next / Later. Completed items are removed, not archived — `wiki/log.md` and git
history are the record of what shipped.

## Next

- **Dogfood the playbook preset** — instantiate for Luke's own venture(s); fold
  findings back into the preset before calling it stable.

## Later

- **MCP write tools** — ingest via API, superseding part of
  [[ADR-004 Read-Only MCP in v1]] if the interactive-only rule proves too strict.
- **Embeddings / semantic search** — if index-first navigation stops scaling.
- **Installable `kb-lint` package** — only if `/sync-upstream` proves
  insufficient for keeping vendored tooling current.
- **Podcast/briefing generation** — script-first: a markdown dialogue or
  briefing built from a topic's wiki pages, filed as a query artifact; audio
  rendering (TTS, config in `kb.toml`) only if the script version earns it.
