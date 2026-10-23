---
type: decision
status: proposed
created: 2026-10-23
updated: 2026-10-23
sources:
  - "[[2026-10-16 gbrain Belief Ledger Design (Garry Tan)]]"
raw:
  - raw/articles/2026-10-16 gbrain Belief Ledger Design (Garry Tan).md
related:
  - "[[Belief Ledger]]"
  - "[[Three-Layer Architecture]]"
  - "[[ADR-007 No Stable Claim Identity]]"
tags: [adr, schema, provenance]
---

# ADR-006 Two Clocks in Frontmatter

## Context

gbrain keeps `recorded_at` (when the brain recorded something) apart from
`source_time` (the time the evidence claims for itself) and never lets one
populate the other ([[Belief Ledger]], source section 5.4). This KB already
does the same without saying so: a raw file's name and `published:` are source
time; `retrieved:` is capture time; a wiki page's `created`/`updated` and the
workflow commit are recorded time.

Both external reviews (`staging/schema-review-gbrain-opus-5.5.md`,
`staging/schema-review-gbrain-gpt-6.md`) say: real, cheap, name it in
AGENTS.md, add no wiki fields, never backdate `created`/`updated` to a source
date. They split on lint. Checked in this session, the drift Opus found is real:

- `raw/articles/2026-08-21 The AI-Native SDLC Playbook (Anthropic).md` has
  `published: 2001-08-21` (clipper error; the filename says 2026).
- The gbrain file is named by its `updated:` date (2026-10-16); `published:`
  is 2026-10-15. File naming says publication date.
- Capture date is `retrieved:` in files from the capture skills and `created:`
  in clipper and transcript files; the two PDFs have no frontmatter.

## Decision

1. One sentence under **File naming** in AGENTS.md: raw frontmatter keeps
   source time (`published:`) apart from capture time (`retrieved:`); the
   filename date is `published`, else `retrieved`; neither is ever copied into
   a wiki page's `created`/`updated`, which are maintenance time. One sentence
   under **Query**: a "what did the KB say at T" answer cites the commit it
   read, and says "the page stated X" rather than "the KB recorded X" unless a
   callout carried it.
2. A **warn-only** lint check, `check_raw_dates`: a raw `.md` whose filename
   date matches none of `published`, `retrieved`, `created` gets a warning.
   Warn, not error, because `raw/` is immutable to the agent and the user
   fixes it. `created:` is accepted as a stand-in for `retrieved:`; no
   migration of old files. PDFs are skipped.
3. The user corrects the SDLC frontmatter and may rename the gbrain file to
   `2026-10-15`; the agent does neither.

## Consequences

- No new fields, no page noise, nothing per ingest: the capture skills already
  write both dates.
- One warning to clear now, and a check that catches the next clipper error.
- The wording "commit time is recorded time" in [[Three-Layer Architecture]]
  is narrowed to agent writes; see [[ADR-009 Hand Edits Are the Unmanaged Writer]].

## Alternatives

- **No lint, convention only** (GPT-6): rejected because the drift already
  exists and nothing else would find it.
- **Per-claim `recorded_at`**: rejected by both reviews; it duplicates the
  workflow commit.
- **Rename raw files to a bitemporal scheme**: rejected; raw is immutable and
  the frontmatter already carries both dates.
