---
type: roadmap
created: 2026-07-10
updated: 2026-07-10
tags: [product]
---

# Roadmap

Now / Next / Later / Done. Items move down as they land; prune Done occasionally.

## Now

- Publish the template repo and mark it as a GitHub template.
- Dogfood: instantiate the first real KB from the template.

## Next

- **Retrofit the two existing hand-built KBs** via `/sync-upstream` — adopt
  `kb.toml`, replace their diverged `lint.py`/skills with template copies. (Run
  from within each KB — not part of the template itself.)
- **Books KB**: a reading-library instance (`books/authors/themes` taxonomy).

## Later

- **Vault parent instance**: an orchestrator KB for the whole Obsidian vault,
  registering the existing per-project KBs and folders as children. (The vault
  root is not currently a git repo; placement and scope are an open decision.)
- **MCP write tools** — ingest via API, superseding part of
  [[ADR-004 Read-Only MCP in v1]] if the interactive-only rule proves too strict.
- **Embeddings / semantic search** — if index-first navigation stops scaling.
- **Installable `kb-lint` package** — only if `/sync-upstream` proves
  insufficient for keeping vendored tooling current.
- **Podcast/briefing generation** — script-first: a markdown dialogue or
  briefing built from a topic's wiki pages, filed as a query artifact; audio
  rendering (TTS, config in `kb.toml`) only if the script version earns it.

## Done

- Template v0.2: `insight` feature — `/research` source discovery and
  `/connect` novel-connection syntheses. (2026-07-10)
- Template v0.1: wiki core, four cuttable features, deterministic onboarding,
  verify matrix, read-only MCP server. (2026-07-10)
