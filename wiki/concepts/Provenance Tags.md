---
type: concept
created: 2026-10-23
updated: 2026-10-23
sources:
  - "[[2026-10-22 ar9av obsidian-wiki (repo)]]"
raw:
  - raw/articles/2026-10-22 ar9av obsidian-wiki (repo).md
related:
  - "[[ADR-011 Speculative Drift Lint]]"
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
in a page as `extracted`, `^[inferred]` or `^[ambiguous]`, and its lint
"flags pages drifting into speculation". The README does not say how drift is
computed or what a claim's boundaries are; `extracted` is written bare and
the other two as footnote marks, so extracted prose may carry no visible mark
at all. The capturer's repo notes add an `undated_claims` lint rule, not
described in the README; the repo's `docs/` were not captured. The README's
own gloss is "you can tell knowledge from guessing" and "Not an oracle. Pages
are as good as their sources."

## Three ways to mark the same thing

Two implementations in `raw/` and this KB carry provenance at the claim
level, and they split the work differently:

| | obsidian-wiki | this KB (`[!claim]`) | gbrain ([[Belief Ledger]]) |
|---|---|---|---|
| Unit | every claim (granularity unspecified) | contestable assertions only | every fact, take and link |
| Marks | origin: extracted / inferred / ambiguous | `confidence` + `status` + an evidence wikilink | trust tier of the writer, plus status over time |
| Lint | page-level drift into speculation; undated claims | callout shape and a resolving evidence link ([[ADR-010 Lint the Claim Contract]]) | coverage and completeness, in the database |

The tags answer *origin*; the callouts answer *standing*. This KB's nearest
equivalent to `^[inferred]` is `status: speculative`, which in practice only
`/connect` has used (0 of 48 callouts at the time of writing), and the nearest
equivalent to `^[ambiguous]` is an evidence line that says the source is
unclear. Prose outside callouts carries no origin mark here, and lint checks
callout shape only ([[ADR-010 Lint the Claim Contract]]: "does not try to
find contestable prose that should have been a claim").

> [!claim] obsidian-wiki marks the origin of every claim and lints pages for drift into speculation
> confidence: medium · status: supported
> evidence: "Every claim is tagged `extracted`, `^[inferred]`, or
> `^[ambiguous]`, and lint flags pages drifting into speculation" —
> [[2026-10-22 ar9av obsidian-wiki (repo)]]. A README description of a
> shipped feature: no algorithm, no threshold, no measurement of how often it
> fires or what tagging costs at write time.

> [!claim] A lint over origin marks can only count inference the agent already admitted to; the failure this KB has, a contestable inference written as bare prose, is invisible to it
> confidence: medium · status: speculative
> evidence: the KB's own reasoning, checked by two independent reviews
> (`staging/schema-review-obsidian-wiki-*.md`) that sampled three pages and
> found one to three such sentences each, e.g. "strictly worse than RAG" in
> [[Why LLM Wikis Beat RAG]]. Confirm: a source that measures tag coverage
> against an audit. Refute: obsidian-wiki's `docs/` describing a drift check
> that does not depend on the agent's own marks.

## What transfers

Not the lint. The gap here is narrow: an inference that skips the callout at
the moment it is written, on a page one person reads before it is committed.
Tagging every sentence would add footnote noise in Obsidian for a check that
cannot see the untagged sentence anyway. The decision is
[[ADR-011 Speculative Drift Lint]]: widen `speculative` to the agent's own
inferences during ingest, add the check to the lint judgment pass, no new
field and no Python.
