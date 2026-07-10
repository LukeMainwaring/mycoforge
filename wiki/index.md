# Index

The catalog: every wiki page, one line each. Updated on every ingest.

## Meta

- [[overview]] — what this KB is and where to start

## Concepts

- [[Three-Layer Architecture]] — raw / wiki / schema, and why the ownership boundary matters
- [[Ingest Workflow]] — the write path: integrate, don't index; one source per session
- [[Subtractive Onboarding]] — ship with everything on, prune down deterministically
- [[Fractal Federation]] — nesting KBs: orchestrator as a feature, children as independent repos

## People

- [[Andrej Karpathy]] — author of the LLM Wiki gist this KB implements

## Syntheses

- [[Why LLM Wikis Beat RAG]] — compile-at-ingest vs retrieve-at-query, claims marked

## Raw sources

- [[2026-04-04 LLM Wiki (Karpathy)]] — the founding gist (article, 2026-04-04)

<!-- sf:begin(product) -->
## Decisions

- [[ADR-001 Separate Repo with Product as Seam]] — KB and software live apart, bridged by MCP
- [[ADR-002 Fractal Federation for Nested KBs]] — orchestrator as a cuttable feature
- [[ADR-003 Copy-and-Own with Config-Code Split]] — vendored tooling, instance data in kb.toml
- [[ADR-004 Read-Only MCP in v1]] — search/read/index only; writes stay interactive
<!-- sf:end(product) -->
