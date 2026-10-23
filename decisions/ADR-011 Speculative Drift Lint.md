---
type: decision
status: accepted
created: 2026-10-23
updated: 2026-10-23
sources:
  - "[[2026-10-22 ar9av obsidian-wiki (repo)]]"
raw:
  - raw/articles/2026-10-22 ar9av obsidian-wiki (repo).md
related:
  - "[[Provenance Tags]]"
  - "[[ADR-010 Lint the Claim Contract]]"
  - "[[ADR-007 No Stable Claim Identity]]"
tags: [adr, schema, claims, lint]
---

# ADR-011 Speculative Drift Lint

## Context

obsidian-wiki ([[2026-10-22 ar9av obsidian-wiki (repo)]]) tags every claim in
a page `extracted`, `^[inferred]` or `^[ambiguous]`, and its lint "flags pages
drifting into speculation", with an `undated_claims` rule beside it. Filed
here as [[Provenance Tags]]: the tags mark *origin* on every sentence, where
this KB's `[!claim]` callouts mark *standing* on contestable assertions only.

The gap that leaves: a sentence the agent infers while writing a page (a
comparison, a "this transfers because", a reading of what a source implies)
carries no mark unless it is promoted to a callout. Over several ingests a
page's share of inferred prose can rise and nothing here would notice.
[[ADR-010 Lint the Claim Contract]] chose shape-only lint and said so: it
"does not try to find contestable prose that should have been a claim".

Against closing it: the anti-padding rule and the callout convention exist
so pages read as prose in Obsidian, not as annotated transcripts. Tagging
every sentence is the cost obsidian-wiki pays for its lint.

## Question

Is unmarked inferred prose a real gap for this KB, and if so what is the
smallest marking that lets lint see drift without tagging every sentence?

Two independent reviews ran `staging/schema-review-obsidian-wiki-prompt.md`
(Opus 5.5, GPT-6; diff in `staging/schema-review-obsidian-wiki-diff.md`; all
three removed from the tree on 2026-10-23, in git history at `0ddc41b`).
Both sampled three pages and found 25 to 55 percent of prose outside callouts
to be inference, nearly all of it cross-linking, framing or statements about
this KB that git can check. The gap is one to three contestable sentences per
page that skipped a callout when written ("strictly worse than RAG" in
[[Why LLM Wikis Beat RAG]] is both reviews' example). Both reject a drift
lint for the same reason: a count of `^[inferred]` marks "measures declared
annotations, not missed inferences"; the untagged sentence looks exactly like
extracted prose. Both reject a hand-kept count as a number lint cannot check.
Opus also found that 0 of 48 callouts use `speculative`: the agent's own
inferences land as `supported` or as bare prose.

## Decision

Option (a), widened. No lint, no field.

- **Claims** in AGENTS.md: `speculative` covers an inference the agent drew
  rather than a source stated, whether filed by `/connect` or written during
  ingest or query filing; its evidence line names the premises and what would
  confirm or refute it. A contestable sentence no source states goes in a
  `speculative` callout or is cut. Cross-links and statements about this KB
  itself stay as prose.
- **Lint step 2** in AGENTS.md: add to the judgment pass "contestable
  inference in bare prose, and claims whose conclusion is stronger than the
  evidence cited".
- **Existing pages**: no sweep. Fix on touch; the first fixes are the
  sentences the reviews named, done in the PR that accepts this ADR, with
  the claim split in [[Provenance Tags]] named in the log.

The two reviews split on one point: whether origin (inferred) and standing
(unsupported) should share the one status. GPT-6 keeps them apart: an
inference whose premises establish the conclusion can be `supported` with the
premises in its evidence line. This ADR takes that reading. `speculative` is
for the inference the evidence does not carry, which is what `/connect`
already means by it.

## Consequences

- One more judgment per touched page per ingest, and zero to two extra
  callouts. The "or cut it" clause guards against callout inflation.
- `check_claims` is unchanged; `speculative` is already in the vocabulary.
- Drift detection stays a human and agent judgment, named as such in Lint.
  No deterministic check finds a missed callout, and this ADR says so rather
  than implying coverage.

## Alternatives

- **`^[inferred]` marks on inferred sentences, counted per page by lint with
  a threshold in `kb.toml`**: rejected. It counts admitted inference only; a
  threshold would have to vary by `type`, since syntheses are inferred by
  design; in Obsidian reading view every mark is a superscript and a
  "Footnotes" list repeating "inferred".
- **A hand-maintained `inferred:` count in frontmatter**: rejected. Lint
  cannot verify it and it goes stale on the first edit.
- **Do nothing**: rejected narrowly. The convention already says contestable
  assertions go in callouts; what was missing is that the agent's own
  inferences count as contestable and have a status to land in.

## Implemented

2026-10-23, same PR: Claims and Lint step 2 in AGENTS.md as above; "strictly
worse than RAG" in [[Why LLM Wikis Beat RAG]] and "not a fourth layer" in
[[Three-Layer Architecture]] became `speculative` callouts; "precisely because
it can never damage" and "no human in the loop at all" on the same page were
narrowed in prose; the causal "trustworthy enough to route on" in
[[Progressive Disclosure]] softened. First `speculative` callouts outside
`/connect`.

## Noted, not decided

From the reviews' "Missed" sections, each its own question if ever raised:
a warn-only lint for a `raw/` file no wiki page cites ("captured, never
ingested"); capture obsidian-wiki's `docs/` before reading anything into its
`undated_claims` rule; a locked writer only when concurrent sessions exist.
