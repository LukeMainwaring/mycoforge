---
type: concept
created: 2026-10-23
updated: 2026-10-23
sources:
  - "[[2026-10-22 ar9av obsidian-wiki (repo)]]"
raw:
  - raw/articles/2026-10-22 ar9av obsidian-wiki (repo).md
related:
  - "[[Belief Ledger]]"
  - "[[Three-Layer Architecture]]"
  - "[[Ingest Workflow]]"
  - "[[Progressive Disclosure]]"
  - "[[ADR-010 Lint the Claim Contract]]"
confidence: medium
tags: [provenance, claims, lint]
---

# Provenance Tags

obsidian-wiki ([[2026-10-22 ar9av obsidian-wiki (repo)]]) marks **every claim**
in a page with one of three tags, `extracted`, `^[inferred]` or
`^[ambiguous]`, and its lint flags pages "drifting into speculation" from the
tag mix, with an `undated_claims` rule beside it. The tag answers one
question per sentence: did a source say this, did the agent work it out, or
is the source itself unclear? The README's own gloss is "you can tell
knowledge from guessing" and "Not an oracle. Pages are as good as their
sources."

## Three ways to mark the same thing

Three implementations in `raw/` now carry provenance at the claim level,
and they split the work differently:

| | obsidian-wiki | this KB (`[!claim]`) | gbrain ([[Belief Ledger]]) |
|---|---|---|---|
| Unit | every claim-shaped sentence | contestable assertions only | every fact, take and link |
| Marks | origin: extracted / inferred / ambiguous | `confidence` + `status` + an evidence wikilink | trust tier of the writer, plus status over time |
| Lint | page-level drift into speculation; undated claims | callout shape and a resolving evidence link ([[ADR-010 Lint the Claim Contract]]) | coverage and completeness, in the database |

The tags answer *origin*; the callouts answer *standing*. This KB's nearest
equivalent to `^[inferred]` is `status: speculative`, which only `/connect`
files, and the nearest equivalent to `^[ambiguous]` is an evidence line that
says the source is unclear. Neither is enforced on ordinary prose: a sentence
the agent inferred while writing a page carries no mark here unless it was
promoted to a callout.

> [!claim] Marking the origin of every claim lets lint catch a page drifting into speculation; marking only contestable claims cannot
> confidence: medium · status: supported
> evidence: "Every claim is tagged `extracted`, `^[inferred]`, or
> `^[ambiguous]`, and lint flags pages drifting into speculation"; repo notes
> add an `undated_claims` rule — [[2026-10-22 ar9av obsidian-wiki (repo)]].
> A README description of a shipped feature, no measurement of how often the
> lint fires or how much tagging costs at write time. The second half is this
> KB's own position by construction: `check_claims` validates callouts and
> "does not try to find contestable prose that should have been a claim".

## What transfers

The drift lint is the part that solves a problem this KB has: a page's
share of inferred prose can rise over several ingests and nothing here would
notice. The cost is tagging every sentence, which the anti-padding rule and
the callout convention were chosen to avoid. A middle form is possible: a
page-level `inferred:` count or a `^[inferred]` footnote on prose sentences
only, counted by lint. That is a schema question, filed in the ingest log
for the Decision workflow, not decided here.
