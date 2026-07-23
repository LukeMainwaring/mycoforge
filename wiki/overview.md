---
type: overview
created: 2026-07-10
updated: 2026-07-23
tags: [meta]
---

# Overview

This knowledge base documents **the LLM-wiki pattern itself** — it is the example
content shipped with the MycoForge template, and it eats its own dog food: every
page obeys the schema in `AGENTS.md`, carries provenance, and is indexed and
logged. When you onboard, this content gets replaced by your domain; until then,
it's both the worked example and the documentation.

Start here:

- [[Three-Layer Architecture]] — the raw / wiki / schema split and its ownership rules
- [[Ingest Workflow]] — how knowledge gets in (one source per session)
- [[Subtractive Onboarding]] — the template philosophy: everything on, prune down
- [[Fractal Federation]] — how KBs nest without a special "parent" repo type
- [[Andrej Karpathy]] — author of the source pattern
- [[Why LLM Wikis Beat RAG]] — the synthesis, with its claims marked
- [[AI-Native Company]] — the AI-native cluster: the pattern applied at company
  scale (loops, legibility, company brain, software factories)

Raw sources so far: Karpathy's founding gist
[[2026-04-04 LLM Wiki (Karpathy)]], two YC talks on AI-native companies
(Diana Hu, Tom Blomfield), and the Claude Code team's first-party account
[[2026-06-03 Running an AI-native Engineering Org (Anthropic)]]. One Anthropic
PDF (The Founders Playbook) remains captured in `raw/articles/` awaiting
ingest. The catalog lives in [[index]]; the history in [[log]].
