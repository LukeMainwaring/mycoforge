# Schema review: what the gbrain belief ledger implies for a markdown KB

You are reviewing a proposal set for an agent-maintained markdown knowledge
base. Run this prompt verbatim; two independent reviewers receive the same
text. Do not coordinate with the other reviewer. Do not read `wiki/log.md`,
`staging/ingest.md` or any `decisions/` page: they contain the ingesting
agent's own ranking of these questions, and the point of this review is an
unanchored read.

## Read, in this order

1. `AGENTS.md` — the schema of this KB. Note the Frontmatter, Claims, Ingest,
   Lint and Version control sections.
2. `scripts/lint.py` — what the linter enforces today.
3. `raw/articles/2026-10-15 gbrain Belief Ledger Design (Garry Tan).md` — the
   source. Sections 1–4, 5.4, 6, 7 and 13–15 carry the argument; 5.1–5.3 and
   8–12 are database mechanics you may skim.
4. `wiki/concepts/Belief Ledger.md` and the section "What the wiki layer does
   not record" in `wiki/concepts/Three-Layer Architecture.md` — how the KB
   filed the source. Treat these as one reader's summary, not as ground truth;
   where you think they misread the source, say so.
5. Two or three pages with `[!claim]` callouts, e.g.
   `wiki/syntheses/Why LLM Wikis Beat RAG.md`, to see the convention in use.

## The questions

The source argues that a markdown-plus-git wiki cannot answer "what did this
knowledge base believe at time T". The ingest raised four possible schema
changes in response. For each one, answer three things:

- **Real or local?** Is this a real gap for a markdown KB whose agent commits
  once per workflow run and marks contestable assertions in `[!claim]`
  callouts with `status` and `evidence`? Or does the gap only exist in
  gbrain's database model (many writers, synced sources, row-level storage)?
- **Smallest change.** If real, the smallest change to `AGENTS.md` and
  `scripts/lint.py` that closes it. Name the fields, the lint check, and what
  an existing page would have to change. If you think the right answer is a
  convention with no lint, say so.
- **Cost.** What it costs on every future ingest, in agent effort and in page
  noise for the human reading in Obsidian.

The four:

1. **Claim identity.** A `[!claim]` callout is identified by its position and
   title text in a file. Renaming a page or rewording the claim title severs
   its history. Should claims carry a stable id?
2. **Coverage marker.** Pages written before the claim convention existed
   carry no marker saying "beliefs on this page before date D were not
   recorded as claims." Should they, and should the marker be on the page,
   in the log, or nowhere?
3. **Two clocks.** The KB already separates source time (the date in a raw
   file's name and frontmatter) from recorded time (page `created`/`updated`,
   commit time) without saying so. Is naming this in `AGENTS.md` worth a
   paragraph, and does anything need to change in practice?
4. **Trust on sources.** gbrain stamps every write with a trust tier and holds
   a lower-tier write that would supersede a higher-tier belief for the owner
   instead of applying or refusing it. This KB's claim `status: contested` is
   the convention form of the same move, but `raw/` sources carry no tier
   (paper, practitioner, vendor, secondhand). Should they, and would a claim's
   `confidence` field then be derived rather than hand-set?

Then two open questions:

5. **Missed.** Anything in the source that bears on this KB's schema and that
   the four questions above do not cover.
6. **Misread.** Anywhere the two wiki pages in step 4 state the source
   wrongly or overreach.

## Output

Write one file and touch nothing else:
`staging/schema-review-gbrain-<your model name>.md`. Keep it under 150 lines.
Use this shape:

```
# Schema review (gbrain belief ledger) — <model>, <date>

## Summary
Three to five lines. Which of the four you would adopt, which you would not,
and the one thing you would do first.

## 1. Claim identity
Real or local: ...
Smallest change: ...
Cost: ...

## 2. Coverage marker
...

## 3. Two clocks
...

## 4. Trust on sources
...

## 5. Missed
...

## 6. Misread
...
```

Be specific and be willing to say "no change". A reviewer who recommends all
four has not done the cost column.
