---
type: concept
created: 2026-07-10
updated: 2026-07-10
sources:
  - "[[2026-04-04 LLM Wiki (Karpathy)]]"
raw:
  - raw/articles/2026-04-04 LLM Wiki (Karpathy).md
related:
  - "[[Ingest Workflow]]"
  - "[[Why LLM Wikis Beat RAG]]"
confidence: high
tags: [architecture]
---

# Three-Layer Architecture

An LLM wiki has exactly three layers, with a strict ownership boundary between them:

1. **Raw sources** (`raw/`) — the user's curated collection: papers, articles,
   transcripts, images. **Immutable.** The LLM reads them but never modifies them;
   they are the source of truth every wiki claim traces back to.
2. **The wiki** (`wiki/`) — LLM-generated markdown: concept pages, entity pages,
   syntheses, plus the `index.md` catalog and append-only `log.md`. The LLM owns
   this layer entirely; the user reads it (typically in Obsidian) but rarely edits.
3. **The schema** (`AGENTS.md`) — the contract that disciplines the LLM: structure,
   conventions, and workflows. Karpathy calls it "what makes the LLM a disciplined
   wiki maintainer rather than a generic chatbot." User and LLM co-evolve it.

The analogy from the source: *Obsidian is the IDE; the LLM is the programmer; the
wiki is the codebase.* The ownership boundary is what makes the pattern safe — the
LLM can rewrite fifteen wiki pages in one [[Ingest Workflow|ingest]] pass precisely
because it can never damage the sources underneath.
