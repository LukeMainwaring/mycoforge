---
type: concept
created: 2026-07-10
updated: 2026-10-23
sources:
  - "[[2026-04-04 LLM Wiki (Karpathy)]]"
  - "[[2026-08-27 WikiSkill - Compiling Agent Experience into Persistent Knowledge for Skill Evolution]]"
  - "[[2026-10-22 ar9av obsidian-wiki (repo)]]"
  - "[[2026-10-22 langchain-ai openwiki (repo)]]"
raw:
  - raw/articles/2026-04-04 LLM Wiki (Karpathy).md
  - raw/papers/2026-08-27 WikiSkill - Compiling Agent Experience into Persistent Knowledge for Skill Evolution.md
  - raw/articles/2026-10-22 ar9av obsidian-wiki (repo).md
  - raw/articles/2026-10-22 langchain-ai openwiki (repo).md
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

## Continuous ingest: the gate moves to the pull request

OpenWiki ([[2026-10-22 langchain-ai openwiki (repo)]]), LangChain's repository-to-wiki
tool (17,335 stars and seventy commits in the thirty days before capture),
drops the session altogether. In code mode a scheduled CI job runs
`openwiki --update`, which "checks repository changes and the evidence behind
existing Claims to decide what needs updating", and opens a docs-only pull
request when the wiki changed; "clean updates skip model work and leave the
wiki content untouched". An auto-merge variant is offered as "repository
infrastructure rather than an OpenWiki runtime feature", gated by the
branch's required checks, and the README leaves the repo to "decide whether
OpenWiki PRs still require human review". In personal mode `openwiki ingest
all` runs every configured connector (Gmail, Notion, Slack, X, web search,
Hacker News, local git, custom MCP); connector tools write raw data and
manifests, then a per-source agent run synthesizes the wiki from them.

Two things make the unattended run schedulable, and neither is scale. The
model's work is narrowed before it starts: a page is reopened only for
changed source or a stale claim, and the page worker "receives only Claims
requiring attention; current issue-free Claims are retained
deterministically" ([[Provenance Tags]] has the claim mechanics). And the
judgment this KB spends at ingest time is spent at review time instead, on a
PR diff, or waived by auto-merge behind the repo's own checks. The user's
standing instructions survive in `openwiki/INSTRUCTIONS.md`, "a user-authored
file OpenWiki reads for scope and priorities but never rewrites". The source
is also different in kind: a codebase changes under its wiki, so the update
is driven by the diff and the stale evidence, where this KB's raw layer is
immutable and nothing in it ever goes stale ([[Three-Layer Architecture]]).

> [!claim] One source per session is a choice of gate, not of scale: each unattended ingest in `raw/` replaces the user's judgment at ingest time with a different gate, never with none
> confidence: medium · status: speculative
> evidence: this KB's inference across three sources. WikiSkill gates on a
> downstream validation score with no human — [[2026-08-27 WikiSkill - Compiling Agent Experience into Persistent Knowledge for Skill Evolution]];
> obsidian-wiki's batch ingest keeps the human as the one who runs the skill
> and reviews the manifest — [[2026-10-22 ar9av obsidian-wiki (repo)]]; OpenWiki
> gates on PR review and required branch checks, and its auto-merge path
> drops review only where those checks stand in — [[2026-10-22 langchain-ai openwiki (repo)]].
> Confirm: an auto-merged OpenWiki whose docs drift in ways review would have
> caught, which would show the gate doing the work. Refute: a maintainer that
> runs with no gate at all and is shown to hold quality.
