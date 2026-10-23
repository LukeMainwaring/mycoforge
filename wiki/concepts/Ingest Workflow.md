---
type: concept
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
tags: [workflow]
---

# Ingest Workflow

The core write path of an LLM wiki: a new source arrives in `raw/`, and the LLM
**integrates** it rather than merely indexing it — reading it in full, extracting
what matters, and updating every wiki page it touches. A single source might touch
10–15 pages: entity pages gain facts, syntheses get strengthened or challenged,
contradictions with older claims get flagged instead of papered over.

The MycoForge house style, following Karpathy's own practice: **one source per
session**, with the user in the loop. Ingestion is judgment-heavy — what to
emphasize, what to contest, what to promote to its own page — so it stays
interactive. (This is also why the MCP server is read-only: capture and search
can be mechanical; integration can't.)

Every ingest ends with bookkeeping: an `index.md` entry per new page and an
`ingest |` line in `log.md`. Companion workflows: [[Query Workflow]] (the read
path) and [[Lint Workflow]] (the health check) — see `AGENTS.md` until those
pages are written.

## Ingest without a human: the Wiki Maintainer

WikiSkill ([[2026-08-27 WikiSkill - Compiling Agent Experience into Persistent Knowledge for Skill Evolution]]) runs this workflow unattended once per optimization
iteration ([[Skill Evolution]]), and its rules converge on the same
bookkeeping: read the current wiki and the new material; create or
patch-edit pages (append, replace, insert-after against exact substrings,
"keep each edit minimal"); never duplicate, extend the existing page with
new evidence; rewrite `index.md` in full and append one entry to `logs.md`
every pass, even when nothing changed. Two differences are worth noting
rather than adopting. The sources are machine-generated and plentiful, so
the maintainer *samples* its raw layer (at most 8 traces per pass,
stratified 5 failing / 3 passing, each capped at 15k characters) instead of
reading one source in full. And no human judges the consolidation; a
validation score downstream catches a bad one indirectly. One source per
session is the right rule when the source is a document and the gate is the
user; the paper shows what the rule becomes when neither holds. Its authors
also name the gap this KB covers with Lint: "WikiSkill currently lacks an
automated mechanism to prune the wiki."

## Batch ingest: the manifest and the locked writer

obsidian-wiki ([[2026-10-22 ar9av obsidian-wiki (repo)]]) takes the other
side of the one-source rule. `/wiki-ingest ~/research` processes a folder;
"a manifest tracks every source ingested, so the second run processes the
delta — not your whole library again"; `/wiki-capture` files the current
conversation straight into the wiki; `/wiki-dedup` and `/cross-linker` run
afterwards as separate skills. The manifest solves a problem batch ingest
creates. This KB's equivalent is `staging/ingest.md` plus the `ingest |`
log entries, which is enough when one session handles one source and the
user ticks the row.

Its second convention is a concurrency rule: `index.md`, `log.md`, `hot.md`
and the `_meta/` files "all go through one writer that takes a lock and
writes atomically, so parallel agents can't drop each other's updates."
That matters only when more than one agent writes the wiki at once. This KB
runs one session at a time, so the lock buys nothing here; the writer it
does not coordinate is the user editing in Obsidian, which is the case
[[ADR-009 Hand Edits Are the Unmanaged Writer]] covers with `hand-edit:`
commits. If this KB ever runs parallel ingest sessions, the bookkeeping
files are the first thing that needs a lock, and `log.md` being append-only
is what makes that cheap.
