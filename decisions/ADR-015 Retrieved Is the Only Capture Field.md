---
type: decision
status: accepted
created: 2026-10-25
updated: 2026-10-25
related:
  - "[[ADR-006 Two Clocks in Frontmatter]]"
tags: [adr, schema, provenance]
---

# ADR-015 Retrieved Is the Only Capture Field

## Context

[[ADR-006 Two Clocks in Frontmatter]] accepted `created:` as a stand-in for
`retrieved:` in raw files and ruled out migrating old ones. In practice the
stand-in reads as a third clock: a wiki page's `created` is maintenance time,
so a raw `created:` invites the reading "when the source was made", which is
`published:`. On 2026-10-25 four raw files still said `created:` (three
`/transcript` captures and one Web Clipper clip), and `/transcript` wrote it
until that day's refresh.

## Decision

1. Raw capture time is `retrieved:` only. `created:` means wiki-page creation
   and nothing else.
2. `check_raw_dates` warns on any raw `.md` carrying `created:`. Still warn,
   not error: the user fixes `raw/`.
3. The user renames the field in the four files and sets the Obsidian Web
   Clipper template's capture-date property to `retrieved`.

## Consequences

- One word per clock across the KB: `published` (source), `retrieved`
  (capture), `created`/`updated` (wiki maintenance).
- A clipper template left on its default shows up as a lint warning on the
  next clip, not as silent drift.
- Narrows ADR-006 point 2; the rest of ADR-006 stands.

## Alternatives

- **Keep the stand-in** (ADR-006 as written): rejected; it is the source of
  the confusion this ADR fixes.
- **Error, not warn**: rejected for the same reason as ADR-006; the agent
  never edits `raw/`.
