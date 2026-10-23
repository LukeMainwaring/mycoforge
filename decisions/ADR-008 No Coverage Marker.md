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
  - "[[Subtractive Onboarding]]"
  - "[[ADR-006 Two Clocks in Frontmatter]]"
tags: [adr, schema, provenance]
---

# ADR-008 No Coverage Marker

## Context

gbrain certifies its history only from a per-page baseline cut, and a read for
an earlier time gets a coded refusal rather than a reconstruction
([[Belief Ledger]], section 3). The ingest asked whether pages written before
the claim convention should carry a "beliefs before D unrecorded" marker.

Checked in this session: the Claims section was in AGENTS.md from the scaffold
commit (`2833df0`, 2026-07-10), the same day as the first wiki page, so no page
in this instance predates the convention. Both reviews reject a page marker:
it would be permanent Obsidian noise, would imply more assurance than it
gives, and prose that never became a callout is by design, since only
contestable assertions are claims. The gap is real for one case Opus names:
an instance that imports an existing vault.

## Decision

No page field, no lint. Two small things:

- The `/onboard` skill, when it imports existing pages, writes one log line:
  `discovered | imported N pages; beliefs before <date> not recorded as claims`.
  The marker lives in the log, never on pages.
- The Query sentence from [[ADR-006 Two Clocks in Frontmatter]] covers the
  rest: historical answers cite the commit and separate "the page stated X"
  from "a callout marked X supported"; a missing earlier state is reported as
  unknown, never reconstructed.

## Consequences

- Zero cost per ingest.
- Template-only change, deleted with `.template/` once onboarding is done.

## Alternatives

- **`claims_since:` on each page**: rejected; it would not certify the edits
  between then and now, which is the only thing a coverage marker is for.
- **A repo-wide watermark in `kb.toml`**: rejected for this instance, where the
  first commit already is the watermark; folded into the onboarding log line
  for imports.
