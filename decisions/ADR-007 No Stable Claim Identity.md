---
type: decision
status: accepted
created: 2026-10-23
updated: 2026-10-23
sources:
  - "[[2026-10-16 gbrain Belief Ledger Design (Garry Tan)]]"
raw:
  - raw/articles/2026-10-16 gbrain Belief Ledger Design (Garry Tan).md
related:
  - "[[Belief Ledger]]"
  - "[[Three-Layer Architecture]]"
  - "[[ADR-010 Lint the Claim Contract]]"
tags: [adr, schema, claims]
---

# ADR-007 No Stable Claim Identity

## Context

gbrain keys every belief on a logical identity that survives renames and row
churn ([[Belief Ledger]], section 2). The gbrain ingest logged the gap that a
`[!claim]` callout is identified only by its position and title in a file, so
a rename or reword "severs" its history.

Both reviews say that overstates it. Git keeps the old path and text; a
reworded title is a `-`/`+` pair in one commit, and `git log --follow`
survives a page rename. What is missing is a machine-readable join across
moves, splits and rewordings, and today nothing consumes one: lint does not
parse callouts and no page links to a claim. gbrain itself does not keep one
key through rewording; a changed fingerprint is a new assertion linked to its
predecessor by `replaces` (source sections 3 and 4). A universal id would mean
rewriting 45 callouts on 23 pages for zero belief change, which is exactly the
projection churn the source warns against.

## Decision

No claim ids, no lint. Two sentences in **Claims**:

- When you reword, move or split a claim, name the old and new title in the
  log entry.
- When a claim is superseded, keep the old proposition in the callout (status
  `superseded`, pointing at the successor by page and claim title); never
  overwrite it in place.

If a page ever needs to link to one claim on another page, give that claim an
Obsidian block id (`^short-slug`) and link `[[Page#^short-slug]]`. Ids are
added when a link needs them, never to every claim.

## Consequences

- One clause in a log line, a few times a month.
- Claim history stays recoverable by a human with git and the log; it is not
  queryable by machine, and that is accepted until something needs to query it.
- The [[Three-Layer Architecture]] claim title is softened from "severs" to
  "has no stable join"; done in the same PR as this ADR.

## Alternatives

- **`id: claim-<uuid>` in every callout with uniqueness lint** (GPT-6's
  fallback form): deferred, not rejected. Revisit when there is a consumer,
  such as a weekly belief diff over the wiki.
- **Fingerprint claims by content** as gbrain does: rejected; the proposition
  text changes on most substantive edits, so the fingerprint buys nothing a
  diff does not.
