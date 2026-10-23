---
type: person
created: 2026-07-10
updated: 2026-10-23
sources:
  - "[[2026-04-04 LLM Wiki (Karpathy)]]"
  - "[[2026-08-27 WikiSkill - Compiling Agent Experience into Persistent Knowledge for Skill Evolution]]"
  - "[[2026-10-22 ar9av obsidian-wiki (repo)]]"
raw:
  - raw/articles/2026-04-04 LLM Wiki (Karpathy).md
  - raw/papers/2026-08-27 WikiSkill - Compiling Agent Experience into Persistent Knowledge for Skill Evolution.md
  - raw/articles/2026-10-22 ar9av obsidian-wiki (repo).md
related:
  - "[[Provenance Tags]]"
  - "[[Skill Evolution]]"
  - "[[Three-Layer Architecture]]"
confidence: high
tags: [person]
---

# Andrej Karpathy

AI researcher and educator (formerly OpenAI founding member and Director of AI at
Tesla; founder of Eureka Labs). Author of the **LLM Wiki** gist (2026-04-04), the
pattern this knowledge base — and the MycoForge template itself — implements.

His formulation supplies the load-bearing ideas here: the
[[Three-Layer Architecture]] with immutable sources, the wiki as "a persistent,
compounding artifact" maintained entirely by the LLM, the schema file as the
discipline mechanism, and the working setup of Obsidian-as-IDE beside an agent
session. He traces the lineage to Vannevar Bush's Memex (1945) — a private,
curated knowledge store whose unsolved problem was *who does the maintenance*;
the LLM is his answer.

First academic uptake in `raw/`: WikiSkill ([[2026-08-27 WikiSkill - Compiling Agent Experience into Persistent Knowledge for Skill Evolution]]) cites the gist as the
inspiration for putting a persistent wiki between agent execution traces and
evolved skills, and reports controlled gains from doing so; see
[[Skill Evolution]].

First open-source implementation at scale in `raw/`: obsidian-wiki
([[2026-10-22 ar9av obsidian-wiki (repo)]], 3,609 stars at capture) names
the gist as its origin and ships the pattern as 39 markdown skills with an
optional CLI; its additions over the gist are per-sentence
[[Provenance Tags]], a session memory surface and a locked bookkeeping
writer ([[Three-Layer Architecture]]).
