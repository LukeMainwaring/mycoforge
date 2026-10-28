---
type: architecture
kind: content
created: 2026-10-28
updated: 2026-10-28
commit: 4b7c704
watches:
  - wiki/concepts/Three-Layer Architecture.md
  - wiki/concepts/Ingest Workflow.md
  - wiki/syntheses/Why LLM Wikis Beat RAG.md
  - wiki/concepts/Progressive Disclosure.md
  - wiki/concepts/Skill Evolution.md
  - wiki/concepts/Belief Ledger.md
  - wiki/concepts/Provenance Tags.md
  - wiki/concepts/Unattended Agent State.md
  - wiki/concepts/Fractal Federation.md
  - wiki/concepts/Subtractive Onboarding.md
sources:
  - "[[2026-04-04 LLM Wiki (Karpathy)]]"
  - "[[2026-05-21 Y Combinator - How to Build a Self-Improving Company with AI]]"
  - "[[2026-08-20 The Claude Code Guide For Startups]]"
  - "[[2026-08-27 WikiSkill - Compiling Agent Experience into Persistent Knowledge for Skill Evolution]]"
  - "[[2026-09-06 The AI Daily Brief - How to Build an AI-Native Company Today]]"
  - "[[2026-10-08 Building Effective Agent Automations (Anthropic)]]"
  - "[[2026-10-15 gbrain Belief Ledger Design (Garry Tan)]]"
  - "[[2026-10-22 ar9av obsidian-wiki (repo)]]"
  - "[[2026-10-22 langchain-ai openwiki (repo)]]"
raw:
  - raw/articles/2026-04-04 LLM Wiki (Karpathy).md
  - raw/podcasts/2026-05-21 Y Combinator - How to Build a Self-Improving Company with AI.md
  - raw/articles/2026-08-20 The Claude Code Guide For Startups.pdf
  - raw/papers/2026-08-27 WikiSkill - Compiling Agent Experience into Persistent Knowledge for Skill Evolution.md
  - raw/podcasts/2026-09-06 The AI Daily Brief - How to Build an AI-Native Company Today.md
  - raw/articles/2026-10-08 Building Effective Agent Automations (Anthropic).md
  - raw/articles/2026-10-15 gbrain Belief Ledger Design (Garry Tan).md
  - raw/articles/2026-10-22 ar9av obsidian-wiki (repo).md
  - raw/articles/2026-10-22 langchain-ai openwiki (repo).md
related:
  - "[[The Knowledge Map]]"
  - "[[The Machinery]]"
  - "[[Three-Layer Architecture]]"
  - "[[Why LLM Wikis Beat RAG]]"
  - "[[Ingest Workflow]]"
tags: [architecture, content, knowledge-capture, provenance]
---

# Map - The Knowledge Layer

## Summary

Ten pages on the LLM-wiki pattern as the sources describe it, as opposed to how [[The Machinery]] implements it. [[Three-Layer Architecture]] is the hub, [[Why LLM Wikis Beat RAG]] the thesis, and [[Ingest Workflow]] the write path; the other pages are comparators that each test one part of the pattern against another implementation (WikiSkill, gbrain, obsidian-wiki, OpenWiki, Anthropic's automations). The one idea to remember: the compounding thesis has exactly one controlled measurement behind it, and every comparator so far changes the gate, not the layers.

## Diagram

Rendered with archify: [diagrams/map-the-knowledge-layer](diagrams/map-the-knowledge-layer/map-the-knowledge-layer.html) (open from a local checkout).

```mermaid
flowchart TB
    karpathy["Karpathy gist (2026-04)<br/>thesis: a persistent, compounding wiki"]
    three["Three-Layer Architecture<br/>raw · wiki · schema"]
    why["Why LLM Wikis Beat RAG<br/>compile at ingest, not per query"]
    ingest["Ingest Workflow<br/>one source per session"]
    pd["Progressive Disclosure<br/>index routes, never reasons"]
    skill["Skill Evolution (WikiSkill)<br/>the one controlled measurement"]
    ledger["Belief Ledger (gbrain)<br/>what git does not record"]
    prov["Provenance Tags (obsidian-wiki, OpenWiki)<br/>marking where a claim came from"]
    unattended["Unattended Agent State (Anthropic)<br/>memory for a scheduled reader"]
    fed["Fractal Federation"]
    sub["Subtractive Onboarding"]

    karpathy -->|states| why
    karpathy -->|defines| three
    why -->|requires| ingest
    three -->|read side| pd
    skill -->|63.7% vs 48.7% supports| why
    skill -->|swaps the top layer| three
    ledger -->|a property of the wiki layer| three
    prov -->|callouts vs tags vs ranges| ingest
    unattended -->|a different gate| ingest
    pd -.->|index misleads reasoning| why
    sub -->|template shape| fed
    fed -->|nests| three
```

## How it works

[[Why LLM Wikis Beat RAG]] states the thesis: synthesis moves to ingest time, so knowledge compounds instead of being re-derived per query, and the economics are about maintenance rather than retrieval. [[Three-Layer Architecture]] is the shape that makes it safe: immutable `raw/`, an agent-owned `wiki/`, and a schema that disciplines the agent. [[Ingest Workflow]] is the write path, one source per session with the user in the loop, and [[Progressive Disclosure]] the read side: metadata and `index.md` route an agent to the right pages but are not where it reasons.

The comparators each probe one piece. [[Skill Evolution]] (WikiSkill) swaps documents for execution traces and skills for the schema, and supplies the only controlled evidence for compounding: 63.7% with a compiled wiki against 48.7% without, from one paper and one model. [[Belief Ledger]] (gbrain) asks what markdown plus git fails to record, belief history rather than file history, and the page files that as a wiki-layer property rather than a fourth layer. [[Provenance Tags]] sets obsidian-wiki's origin tags and OpenWiki's versioned evidence ranges against this KB's claim callouts. [[Unattended Agent State]] takes Anthropic's scheduled daily brief as the discipline a timer-driven `/scout` would need. [[Fractal Federation]] and [[Subtractive Onboarding]] are template design, not pattern claims: they have no sources and no callouts.

## Where the tensions are

- **Interactive gate vs mechanical maintenance.** [[Ingest Workflow]] keeps ingest interactive; the maintenance-economics claim in [[Why LLM Wikis Beat RAG]] rests on OpenWiki and WikiSkill, which maintain with no human at ingest. [[Ingest Workflow]] files the reconciliation as `speculative`: one-source-per-session is a choice of gate, not of scale.
- **Who reads the wiki.** [[Skill Evolution]] measured that giving the executing agent wiki access lowered skill quality (63.7% to 60.9%), which sits awkwardly with the read-time-asset premise of [[Why LLM Wikis Beat RAG]]. The page says the result does not decide who should read a wiki that trains nothing.
- **Index as replacement for embeddings.** [[Why LLM Wikis Beat RAG]] leans on index-first navigation; [[Progressive Disclosure]]'s obsidian-wiki measurement (44% vs 83% on graph questions) shows the index misleads reasoning and is a routing aid only.
- **Inference lint cannot see prose.** [[Provenance Tags]]'s speculative claim is that origin-mark lint only counts inference the agent admitted to, and it cites the low-confidence "bookkeeping lapse makes a wiki worse than RAG" line as the kind of claim that hides.
- **One paper carries the thesis.** Everything resting on WikiSkill is medium confidence from one paper, one model, three runs; obsidian-wiki's "2000 pages, same cost" is asserted, not shown. A second controlled study on a document corpus would move the compounding claim most.

## How to explain this

**In a few sentences:**

> This is what the sources say about the pattern the KB runs on. Karpathy's gist states it: read each source once, compile it into a wiki, and answer from the wiki so knowledge compounds. The layers make that safe because the agent can't touch the sources. Every later source we've read tests one piece: WikiSkill measured the compounding, gbrain asked what git doesn't record, obsidian-wiki and OpenWiki mark provenance differently, and Anthropic's automations show what running it unattended would take.

**Likely follow-ups:**

- **Is compounding actually measured?** Once, in WikiSkill, on benchmark agents rather than documents; everything else is practice and testimony.
- **Where does this KB differ from the comparators?** On the gate: it keeps a human at ingest where WikiSkill, obsidian-wiki and OpenWiki run batch or CI.
- **Which pages have no evidence?** [[Fractal Federation]] and [[Subtractive Onboarding]]; they describe the template, not the sources.
