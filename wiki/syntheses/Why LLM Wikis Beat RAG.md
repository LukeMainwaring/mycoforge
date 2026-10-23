---
type: synthesis
created: 2026-07-10
updated: 2026-10-23
sources:
  - "[[2026-04-04 LLM Wiki (Karpathy)]]"
  - "[[2026-05-21 Y Combinator - How to Build a Self-Improving Company with AI]]"
  - "[[2026-08-20 The Claude Code Guide For Startups]]"
  - "[[2026-08-27 WikiSkill - Compiling Agent Experience into Persistent Knowledge for Skill Evolution]]"
  - "[[2026-10-22 ar9av obsidian-wiki (repo)]]"
raw:
  - raw/articles/2026-04-04 LLM Wiki (Karpathy).md
  - raw/podcasts/2026-05-21 Y Combinator - How to Build a Self-Improving Company with AI.md
  - raw/articles/2026-08-20 The Claude Code Guide For Startups.pdf
  - raw/papers/2026-08-27 WikiSkill - Compiling Agent Experience into Persistent Knowledge for Skill Evolution.md
  - raw/articles/2026-10-22 ar9av obsidian-wiki (repo).md
related:
  - "[[Provenance Tags]]"
  - "[[Skill Evolution]]"
  - "[[Three-Layer Architecture]]"
  - "[[Ingest Workflow]]"
  - "[[Prototype, Dogfood, Productionize]]"
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
> that cost once, at ingest. Independently corroborated at organizational scale:
> "you cannot pump in 100,000 hours worth of recordings into a context window…
> synthesize it into the important parts, and give the AI breadcrumbs" —
> [[2026-05-21 Y Combinator - How to Build a Self-Improving Company with AI]];
> YC's regenerated, monthly-refreshed user manual (see
> [[Organizational Legibility]]) is this pattern running live.
> First controlled evidence, from a different setting ([[Skill Evolution]]):
> in WikiSkill's ablation a skill proposer that reads a wiki compiled from
> past iterations averages 63.7%, against 48.7% when "persistent knowledge
> accumulation across iterations" is removed and it works from the latest
> traces alone, re-deriving each time — [[2026-08-27 WikiSkill - Compiling Agent Experience into Persistent Knowledge for Skill Evolution]].
> Four benchmarks, one model (Gemini-3.5-Flash), three runs. The compounding
> artifact there is patterns from traces, not documents, so it supports the
> mechanism rather than the personal-corpus case.

> [!claim] Index-first navigation makes embeddings unnecessary at personal scale
> confidence: medium · status: supported
> evidence: Karpathy reports index-then-drill "works surprisingly well at moderate
> scale (~100 sources, ~hundreds of pages)" — [[2026-04-04 LLM Wiki (Karpathy)]].
> Untested here beyond that scale; embeddings remain the documented graduation
> path (see `roadmap.md` in instances that keep the product layer).
> Practitioner corroboration in product, not personal, context: Omni "took
> inspiration from [Anthropic's] file vs embedding approach, which emboldened
> us to keep things simple in our own product. We avoided a lot of complexity
> that would have come from a RAG pipeline" (Chris Merrick) —
> [[2026-08-20 The Claude Code Guide For Startups]]. No scale figure given, so
> it widens the claim's plausible range without pinning it; see
> [[Prototype, Dogfood, Productionize]].
> Machine-scale data point: WikiSkill's Skill Proposer is handed `index.md`
> and reads pattern pages and traces on demand, and the maintainer prompt
> calls index entries "the MOST IMPORTANT part of the wiki" because they
> decide whether a page gets opened — [[2026-08-27 WikiSkill - Compiling Agent Experience into Persistent Knowledge for Skill Evolution]]. Its wikis hold 4–10 patterns,
> so this corroborates the mechanism at the low end, not the scale question.
> Second practitioner implementation making the same bet: obsidian-wiki ships
> with "no embedding model, no vector store, no network", claims "titles,
> tags, and summaries get read before page bodies. 20 pages or 2000, roughly
> the same cost", and offers QMD semantic search as an opt-in config, which is
> the same graduation path — [[2026-10-22 ar9av obsidian-wiki (repo)]]. The
> 2000-page figure is asserted, not shown; its one measurement is a 38-page
> vault. One qualification from that measurement: the index is a routing
> aid, not a graph edge, since an agent that reasoned over links through
> `index.md` "found a short path that means nothing" (see
> [[Progressive Disclosure]]).

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
