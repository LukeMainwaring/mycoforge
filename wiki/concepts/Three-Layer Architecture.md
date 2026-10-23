---
type: concept
created: 2026-07-10
updated: 2026-10-23
sources:
  - "[[2026-04-04 LLM Wiki (Karpathy)]]"
  - "[[2026-08-27 WikiSkill - Compiling Agent Experience into Persistent Knowledge for Skill Evolution]]"
raw:
  - raw/articles/2026-04-04 LLM Wiki (Karpathy).md
  - raw/papers/2026-08-27 WikiSkill - Compiling Agent Experience into Persistent Knowledge for Skill Evolution.md
related:
  - "[[Skill Evolution]]"
  - "[[Ingest Workflow]]"
  - "[[Why LLM Wikis Beat RAG]]"
  - "[[Progressive Disclosure]]"
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

The read side of the layering, frontmatter and `index.md` as metadata an agent
routes on before opening a page, is [[Progressive Disclosure]].

## The same split with machine-generated sources

WikiSkill ([[2026-08-27 WikiSkill - Compiling Agent Experience into Persistent Knowledge for Skill Evolution]]) rebuilds the architecture for [[Skill Evolution]], citing
Karpathy's gist directly, and swaps the top layer: `raw/` holds immutable
execution traces instead of documents; `wiki/` holds pattern pages plus
`index.md`, `logs.md` and a `skill-impact.md` audit trail; and the third
layer is executable skills (`SKILL.md` plus a `PURPOSE.md` that maps each
skill back to the wiki patterns behind it) rather than the schema. The
schema's job, disciplining the maintainer, lives in fixed agent prompts and
a harness the paper holds constant.

> [!claim] The three layers generalize beyond curated documents: raw can be any immutable record, and the wiki is the layer that persists while the layer above it is rolled back
> confidence: medium · status: supported
> evidence: "While skill updates can be rolled back, the wiki persists so that
> future updates can build on accumulated knowledge"; removing the wiki layer
> drops average accuracy from 63.7% to 48.7% — [[2026-08-27 WikiSkill - Compiling Agent Experience into Persistent Knowledge for Skill Evolution]].
> One paper, one domain (benchmark agents); the asymmetry is a design choice
> the authors do not ablate on its own.

Two details carry back. Who may read the wiki is a design variable: WikiSkill
denies the executing agent wiki access during rollouts and lets only the
maintainer and proposer in, because an executor that reads the wiki leaves
less informative traces (63.7% to 60.9%). And the ownership boundary holds
with no human in the loop at all, provided the raw layer stays immutable and
the wiki is only ever patched, never reset.
