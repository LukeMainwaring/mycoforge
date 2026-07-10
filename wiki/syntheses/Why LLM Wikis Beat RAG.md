---
type: synthesis
created: 2026-07-10
updated: 2026-07-10
sources:
  - "[[2026-04-04 LLM Wiki (Karpathy)]]"
raw:
  - raw/articles/2026-04-04 LLM Wiki (Karpathy).md
related:
  - "[[Three-Layer Architecture]]"
  - "[[Ingest Workflow]]"
confidence: medium
tags: [synthesis, rag]
---

# Why LLM Wikis Beat RAG

RAG retrieves fragments at query time and re-derives understanding from scratch on
every question. An LLM wiki moves that work to ingest time: knowledge is compiled
once, cross-referenced, and *kept current* — see [[Three-Layer Architecture]] for
the structure and [[Ingest Workflow]] for the write path. This page synthesizes
why that trade wins for a personal, curated corpus.

> [!claim] Compounding beats re-derivation
> confidence: high · status: supported
> evidence: "the wiki is a persistent, compounding artifact… the contradictions
> have already been flagged" — [[2026-04-04 LLM Wiki (Karpathy)]]. A question
> spanning five sources costs RAG a five-way synthesis per query; the wiki paid
> that cost once, at ingest.

> [!claim] Index-first navigation makes embeddings unnecessary at personal scale
> confidence: medium · status: supported
> evidence: Karpathy reports index-then-drill "works surprisingly well at moderate
> scale (~100 sources, ~hundreds of pages)" — [[2026-04-04 LLM Wiki (Karpathy)]].
> Untested here beyond that scale; embeddings remain the documented graduation
> path (see `roadmap.md` in instances that keep the product layer).

> [!claim] The economics are about maintenance, not retrieval
> confidence: high · status: supported
> evidence: humans abandon wikis because "the maintenance burden grows faster than
> the value"; the LLM makes maintenance near-free, which is the actual unlock —
> [[2026-04-04 LLM Wiki (Karpathy)]]. Retrieval quality is a side effect of a
> maintained artifact.

The honest caveat: a wiki is only as good as its ingest discipline. Skip the
bookkeeping and you get a stale cache with confident prose — strictly worse than
RAG, which at least never pretends to remember. The schema and lint tooling exist
to hold that discipline.
