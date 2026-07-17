# Log

Append-only. Most recent at the bottom. Entry format:
`## [YYYY-MM-DD] <prefix> | <Title>` with prefixes
`ingest | query | lint | decision | schema | discovered`.

## [2026-07-10] schema | Initial schema established

Wrote `AGENTS.md`: three-layer architecture, frontmatter schema, claim callouts,
Ingest/Query/Lint workflows, log conventions, template contract.

## [2026-07-10] ingest | 2026-04-04 LLM Wiki (Karpathy)

Ingested the founding gist from `raw/articles/`. Created
[[Three-Layer Architecture]], [[Ingest Workflow]], [[Andrej Karpathy]], and the
synthesis [[Why LLM Wikis Beat RAG]] (three claims marked, all currently
supported). Seeded [[index]] and [[overview]].

## [2026-07-10] discovered | Template concepts are wiki-worthy

The template's own design ideas kept coming up while writing the schema, so they
became pages: [[Subtractive Onboarding]] and [[Fractal Federation]]. No raw
source behind them — provenance is the design session itself.

<!-- sf:begin(product) -->
## [2026-07-10] decision | Founding ADRs 001–004 accepted

Filed the four decisions from the template design session:
[[ADR-001 Separate Repo with Product as Seam]],
[[ADR-002 Fractal Federation for Nested KBs]],
[[ADR-003 Copy-and-Own with Config-Code Split]],
[[ADR-004 Read-Only MCP in v1]]. All `status: accepted`.
<!-- sf:end(product) -->

<!-- sf:begin(product) -->
## [2026-07-17] schema | Roadmap drops Now and Done sections

`roadmap.md` now holds Next / Later only — shipped items are removed rather
than archived (the log and git history are the record). Cleared the completed
v0.1–v0.3 items and updated the Roadmap-upkeep rule in AGENTS.md.
<!-- sf:end(product) -->
