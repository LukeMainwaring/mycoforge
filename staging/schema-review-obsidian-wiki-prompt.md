# Schema review: should this KB lint for speculative drift?

You are reviewing one proposed schema change for an agent-maintained
markdown knowledge base. Run this prompt verbatim. Do not read `wiki/log.md`,
`staging/ingest.md`, `staging/schema-review-gbrain-*.md` or any `decisions/`
page: they contain the ingesting agent's own view, and the point is an
unanchored read.

## Read, in this order

1. `AGENTS.md` — the schema. Note the Claims, Lint and Style sections.
2. `scripts/lint.py` — what the linter enforces today, `check_claims` above all.
3. `raw/articles/2026-10-22 ar9av obsidian-wiki (repo).md` — the source. The
   "Why this and not a notes folder" list and the "Repo notes" at the end carry
   the relevant material. Only the README was captured, not the repo's docs.
4. `wiki/concepts/Provenance Tags.md` — how the KB filed the source. One
   reader's summary, not ground truth; say where it misreads or overreaches.
5. Three pages with `[!claim]` callouts and ordinary prose around them, e.g.
   `wiki/syntheses/Why LLM Wikis Beat RAG.md`,
   `wiki/concepts/Progressive Disclosure.md`,
   `wiki/concepts/Three-Layer Architecture.md`. For each, estimate roughly what
   share of the prose outside callouts is the agent's inference rather than a
   restatement of a source. This is the measurement the question turns on.

## The question

obsidian-wiki tags every claim `extracted`, `^[inferred]` or `^[ambiguous]`
and lints pages that drift into speculation. This KB marks only contestable
assertions, in `[!claim]` callouts with `confidence`, `status` and an evidence
link; prose outside callouts carries no origin mark, and lint checks callout
shape only. Answer:

- **Real or local?** Is unmarked inferred prose a real gap for this KB, given
  what you found in step 5? Or does the drift lint only pay off in
  obsidian-wiki's setting (batch ingest of many sources, conversation capture,
  no human reading each page as it is written)?
- **Smallest change.** If real, the smallest change to `AGENTS.md` and
  `scripts/lint.py` that closes it. Candidates you may accept, reject or
  replace: (a) no change, promote inferred prose to `status: speculative`
  callouts when it matters; (b) a footnote-style `^[inferred]` mark on inferred
  sentences only, counted per page by lint with a threshold in `kb.toml`;
  (c) a hand-maintained `inferred:` count in frontmatter. Name the fields, the
  check, and what an existing page would have to change.
- **Cost.** On every future ingest, in agent effort and in page noise for a
  human reading in Obsidian. The KB's Style section says "a 5-line stub with
  good links beats a 50-line page with filler"; weigh against that.

Then two open questions:

- **Missed.** Anything else in the source that bears on this KB's schema:
  the `undated_claims` rule, the locked writer for `index.md` and `log.md`,
  the ingest manifest, the session hooks.
- **Misread.** Anywhere `Provenance Tags.md` states the source wrongly.

## Output

Write one file and touch nothing else:
`staging/schema-review-obsidian-wiki-<your model name>.md`. Under 100 lines.

```
# Schema review (obsidian-wiki drift lint) — <model>, <date>

## Summary
Three lines: adopt or not, which form, what you would do first.

## Measurement
Per page from step 5: rough share of inferred prose, one line each.

## Real or local
## Smallest change
## Cost
## Missed
## Misread
```

Be willing to say "no change". A reviewer who adopts without doing the cost
column has not answered.
