---
type: decision
status: proposed
created: 2026-10-23
updated: 2026-10-23
sources:
  - "[[2026-10-22 langchain-ai openwiki (repo)]]"
raw:
  - raw/articles/2026-10-22 langchain-ai openwiki (repo).md
related:
  - "[[Provenance Tags]]"
  - "[[ADR-007 No Stable Claim Identity]]"
  - "[[ADR-010 Lint the Claim Contract]]"
  - "[[Three-Layer Architecture]]"
tags: [adr, schema, claims, provenance]
---

# ADR-013 Evidence Stays at File Level

## Context

OpenWiki pins every Grounded Claim to versioned evidence, a file plus line
range plus version, and rechecks each pin before deciding a run is a no-op
([[2026-10-22 langchain-ai openwiki (repo)]], [[Provenance Tags]]). Here a
claim's evidence line names the raw file by wikilink and quotes the passage;
it never points inside the file. The openwiki ingest asked whether
`[[raw file#heading]]` is worth adding for reader auditability, since `raw/`
is immutable and a pin could never go stale.

## Question

Should claim evidence carry an in-file anchor, for new claims or as a
backfill, and should lint resolve it?

Two independent reviews (`staging/schema-review-open-implications-*.md`,
diff in `-diff.md`; removed from the tree on 2026-10-23, in git history at `0ddc41b`). Both: no mandatory anchor, no backfill, no lint now.
Both checked that `WIKILINK_RE` discards the fragment, so any anchor passes
lint today, and Opus: "an anchor that lint does not check is worse than no
anchor." Opus measured (throwaway script, not committed) 51 of 52 claims
citing a raw file, 0 anchored, and 58 of 131 quoted spans matching the raw
file verbatim after normalising whitespace and quote marks, with 33 of the 73
misses in transcripts and PDFs; so a mechanical quote check would also be
too noisy for Python. Anchors would need three syntaxes (markdown heading,
PDF page, transcript timestamp) and block ids would mean writing into
`raw/`. GPT-6 would allow an optional heading link "when it materially
narrows the evidence." Both reframed the real question: raw files do not
change, but three of them are dated snapshots of repos that do, so what
OpenWiki calls currency applies here to the snapshot, not the pin.

## Decision (proposed)

Evidence stays a wikilink to the raw file. The verbatim quote is the
locator; Obsidian search on it lands in the passage. No anchor rule, no
backfill, no lint change.

One convention added under Claims, from the reframing: when a new dated
snapshot of an already-captured repo or rolling page is ingested, the ingest
greps the claims whose evidence cites the earlier snapshot and rechecks each,
logging any status change. That is the one place "is the evidence still the
evidence" arises in an immutable raw layer, and it costs one grep per
re-capture.

## Consequences

- Zero cost on ordinary ingests. One grep and a few rechecks on a re-capture
  ingest, which is where the cost belongs.
- Quote fidelity stays in the Lint judgment pass, sampled, as
  [[ADR-010 Lint the Claim Contract]] already places it.
- Reopenable if vendored `lint.py` ever gains an anchor resolver upstream;
  then the question is new claims in long markdown sources only.

## Alternatives

- **Optional heading anchors for new claims (GPT-6)**: rejected for now. Two
  writers would read "optional" differently, lint cannot tell a resolving
  anchor from a broken one, and the quote already does the work on every
  source type.
- **Block ids in raw files**: rejected. `raw/` is the user's and immutable.
- **Mechanical quote check in lint**: rejected. 73 of 131 misses on the
  current corpus, most of them transcripts and PDFs where the text is
  reflowed.

## Noted, not decided

Lint gaps GPT-6 found and this review checked, all upstream since `lint.py`
is vendored: `check_claims` accepts any resolving wikilink as evidence, not
necessarily a raw file (a `speculative` claim legitimately cites wiki pages,
so a raw-only check would need a carve-out); `check_raw_refs` checks that a
path exists, not that it is under `raw/`; wiki-to-wiki `#Heading` links are
never resolved. Opus's circular-evidence line, that a source written by an
agent which read this KB over MCP cannot raise a claim's confidence, is its
own question when such a source arrives.
