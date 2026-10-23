---
type: concept
created: 2026-07-10
updated: 2026-10-23
sources:
  - "[[2026-04-04 LLM Wiki (Karpathy)]]"
  - "[[2026-08-27 WikiSkill - Compiling Agent Experience into Persistent Knowledge for Skill Evolution]]"
  - "[[2026-10-15 gbrain Belief Ledger Design (Garry Tan)]]"
  - "[[2026-10-22 ar9av obsidian-wiki (repo)]]"
raw:
  - raw/articles/2026-04-04 LLM Wiki (Karpathy).md
  - raw/papers/2026-08-27 WikiSkill - Compiling Agent Experience into Persistent Knowledge for Skill Evolution.md
  - raw/articles/2026-10-15 gbrain Belief Ledger Design (Garry Tan).md
  - raw/articles/2026-10-22 ar9av obsidian-wiki (repo).md
related:
  - "[[Provenance Tags]]"
  - "[[Skill Evolution]]"
  - "[[Belief Ledger]]"
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
> A third raw type from practice: obsidian-wiki feeds the same wiki layer
> from documents, saved conversations (`/wiki-capture`) and mined agent
> session histories (`/wiki-history-ingest` for Claude, Codex, Copilot and
> others), with `_raw/` as the staging folder — [[2026-10-22 ar9av obsidian-wiki (repo)]].
> Its "Not a transcript recorder" rule keeps the layer curated: "nothing is
> saved unless you or a skill decides it's worth keeping".

Two details carry back. Who may read the wiki is a design variable: WikiSkill
denies the executing agent wiki access during rollouts and lets only the
maintainer and proposer in, because an executor that reads the wiki leaves
less informative traces (63.7% to 60.9%). And the ownership boundary holds
with no human in the loop at all, provided the raw layer stays immutable and
the wiki is only ever patched, never reset.

## What the wiki layer does not record

gbrain's [[Belief Ledger]] design ([[2026-10-15 gbrain Belief Ledger Design (Garry Tan)]])
argues that, for its own synced sources, markdown plus git cannot answer
"what did this brain believe at time T": "a fence carries what is true now,
git carries file history without observation time, and a fence format change
produces held files." gbrain is a database, so it adds an append-only ledger
of belief transitions keyed on logical identity. The third failure is
specific to its fence parser; the first two are the ones to test here.

> [!claim] Markdown plus git records file history, not belief history: it has no stable join for a claim across renames and rewordings, and commit time is recorded time only for agent writes
> confidence: medium · status: supported
> evidence: the failure cases named above, plus the measurement that a prose
> edit rewrites 27 to 258 storage rows for 0 belief changes — [[2026-10-15 gbrain Belief Ledger Design (Garry Tan)]].
> Holds only in part for this KB. Time: this KB commits once per workflow
> run, so commit time is recorded time *for agent writes*; the user's hand
> edits in Obsidian are swept into the next run's commit with the wrong time
> and author. Identity: a `[!claim]` callout has no id; git keeps the old
> text through a rename or reword, so a human can recover the history, but
> nothing can join it by machine. No page here predates the claim
> convention, so the coverage gap gbrain closes with a watermark is absent
> in this instance. gbrain's argument is aimed at synced sources, where git
> time is the author's clock, not the brain's.

Put to two independent reviews and decided as five proposals:
[[ADR-006 Two Clocks in Frontmatter]] (name the two clocks; warn-only lint
on raw dates), [[ADR-007 No Stable Claim Identity]] (no ids; log reword and
move), [[ADR-008 No Coverage Marker]] (none; an onboarding log line for
imported vaults), [[ADR-009 Hand Edits Are the Unmanaged Writer]]
(`hand-edit:` commits; never supersede a user-written claim) and
[[ADR-010 Lint the Claim Contract]] (lint callout shape; align the status
vocabulary). The layering survives: the ledger is a property of the wiki
layer, not a fourth layer.

obsidian-wiki ([[2026-10-22 ar9av obsidian-wiki (repo)]]) keeps the same
three layers in markdown and adds a fourth kind of file the Karpathy gist does
not name: a **memory surface** (`hot.md`, an owner profile and todo index
under `_meta/`) injected at session start by a hook, with `index.md` and
`log.md`, written through one locked atomic writer. It also moves provenance
down a level, from the contestable claim to every claim ([[Provenance Tags]]). Both are
properties of the wiki layer; the schema layer is spread across 39 skill
files rather than one `AGENTS.md`.
