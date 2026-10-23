---
type: concept
created: 2026-10-23
updated: 2026-10-23
sources:
  - "[[2026-10-16 gbrain Belief Ledger Design (Garry Tan)]]"
raw:
  - raw/articles/2026-10-16 gbrain Belief Ledger Design (Garry Tan).md
related:
  - "[[Three-Layer Architecture]]"
  - "[[Company Brain]]"
  - "[[Organizational Legibility]]"
  - "[[Ingest Workflow]]"
  - "[[Garry Tan]]"
confidence: medium
tags: [architecture, memory, provenance]
---

# Belief Ledger

gbrain's answer to a question this KB's `log.md` only half answers: **what did
this brain believe, and when did it come to believe it?** The ledger
([[2026-10-16 gbrain Belief Ledger Design (Garry Tan)]]) is one append-only
table of *canonical transitions*: a page published, a fact asserted or
retracted, a take resolved, a link added. Each row is written in the same
transaction as the change it records, so on managed sources the record cannot
drift from the store. It is "canonical audit state, not a projection": one of
the few stores gbrain declares database-only, beside its withdrawal ledger and
mutation journal, because it cannot be rebuilt from the markdown.

The design is a database design, but four of its rules apply to any
agent-maintained knowledge base, including a markdown one.

## 1. Diff beliefs, not storage

> [!claim] A record of what a knowledge base believed must diff canonical state, not the rows or bytes that store it
> confidence: medium · status: supported
> evidence: measured on gbrain's write path: a prose-only edit to a typical
> page rewrites 27 rows and changes 0 beliefs; on a large page, 258 rows and
> 0 beliefs; one changed fact is 1 belief against 26 rows — [[2026-10-16 gbrain Belief Ledger Design (Garry Tan)]], section 9.
> Row triggers or a post-commit diff would record projection churn as belief
> change, miss renames and cascades, and never see a contested write. The
> stronger support is the code reading in section 2; the numbers come from
> "a free local bench (scratch test, not committed)", hence medium.

The event taxonomy follows: a projection refresh emits **nothing**; a real
assertion emits one event per changed logical key; a visibility change (page
deleted, restored, made private) is **one page-level event**, never one per
fact; row reuse is retract-old plus assert-new linked by `replaces`; an
identity change is one `page.renamed`. For a markdown wiki the analogue is
that a `git diff` of a page is storage churn, and the thing worth recording
is which `[!claim]` callouts changed: proposition, status, confidence or
evidence, not only status.

## 2. Slugs are labels; lifetimes are identity

Every event names its subject by a **logical key** with no row id in it: a
page by a `page_lifetime` UUID minted at creation and kept across renames and
soft deletes; a fact by a content fingerprint under its page's lifetime; a
take by claim hash plus ordinal. A rename therefore changes no key in any
stream. A reused slug never inherits an older page's history, because the
lifetime ended. This is what lets the ledger survive engine copies, fallback
renames and row reuse: "keys are derived, never stored as foreign keys."

The markdown equivalent does not exist here: a wiki page's identity *is* its
filename, and a claim's identity is its position in a file. Git keeps the old
text and path through a rename or reword, so history is recoverable by a
human; what is missing is a machine-readable join. Decided not to add one in
[[ADR-007 No Stable Claim Identity]]; context in
[[Three-Layer Architecture#What the wiki layer does not record]].

## 3. Two clocks, and disclose what you do not know

Every event keeps `recorded_at` (when the brain recorded it) apart from
`source_time` (the time the evidence claims for itself: git commit time, a
frontmatter date, `valid_from`). Imported timestamps never populate
`recorded_at`. Reads expose the two clocks as two parameters: `as_of` for
valid time ("what was true on this date") and `known_as_of` for recorded time
("what did the brain know at this instant"), and a bare date passed where an
instant is required is refused as `clock_mismatch` rather than read as
midnight.

Coverage is honest about its own gaps. Enabling the ledger runs a **baseline**
(one snapshot per live page, each page's coverage starting at its own cut);
when every page has a cut, that time is the source's **watermark**. A read
for a time before a page's cut gets a coded refusal, not a guess. History
backfilled from page versions or git is marked `origin = 'backfill'`, keeps
the backfill run's time as recorded time and the historical time only as
source time, and never answers a recorded-time read. Only sources where every write passes a coordinated path
are *certified*; the rest get recorded but uncertified history, answered
"with a disclosure, never as fact." The design separates **timestamp
accuracy** (an event's time is right) from **interval completeness** (nothing
unrecorded happened between two events), and notes that only instrumentation
gives the second: a matching hash cannot, since two real transitions can
return a subject to the same hash.

## 4. Trust travels with the event; a blocked write is contested, not refused

Fact, take and page events carry a `trust_tier` read from the stored row
*after* the tier-clamping trigger ran; held events and backfill carry writer
attribution or `unknown` instead. Destructive events keep two tiers (the subject's
tier before deletion and the writer's). In the common case a lower-trust write that
would supersede a higher-trust assertion is not rejected: the new row is
inserted active, the higher-trust row stays, and a proposal is filed for the
owner to accept, as a `trust.contested` event emitted before projection
(other cases hold the new row or refuse a remote request). Refreshed or
derived text inherits the **lowest** tier of its evidence; a lowering
propagates to dependents, a raise never promotes them automatically, and
historical event tiers stay as recorded. Links have no tier column, so a link
event's tier is actor attribution only, never evidence quality, and backfill
records `unknown` rather than the scanner's own tier.

The shape matches this KB's claim `status: contested`: keep both assertions
visible, cite both, let the human decide. The trigger differs: gbrain
contests between *writer* tiers on one subject, this KB between *sources*,
and `contested` here is a convention with no gate. The writer-tier idea does
carry over, as the user's hand edits: [[ADR-009 Hand Edits Are the Unmanaged Writer]].

## Withdrawal is not erasure

`forget` is a recorded event that removes a fact from active memory and erases
nothing. Purge removes content from the live stores and refuses its return,
but "never promises physical erasure": history, source material and backups
may remain, and git history is explicitly outside purge's reach. The ledger
stores claim text, so it is itself a purge target, swept field by field.

## What it buys

> [!claim] A change report that cites each claim's old value, new value and evidence costs about the same as a plain list of changed pages
> confidence: medium · status: supported
> evidence: on four seeded synthetic weeks (37 gold changes) the cited diff
> costs 258, 233, 215 and 273 tokens against 227, 182, 307 and 281 for the
> uncited list, with set-F1 1.0 on both engines — [[2026-10-16 gbrain Belief Ledger Design (Garry Tan)]], section 15.
> Synthetic data, the authors' own probe, one brain. The mechanism is the
> point: because events net per subject (an edit and its revert report
> nothing), the weekly diff is a list of *beliefs that ended the window
> different*, which is what a reader wants from "what changed" anyway.

The weekly diff also shows the honest-disclosure rule in use: a subject with
no earlier event has its `before` read from the page body as recorded at the
window start, and when no body answers, `before` is null with
`before_known: false`. An inferred end (the nightly contradiction check closed
a relationship) renders as "ended by \<date\>", an upper bound, and an
explicit end replaces it.

## Relation to this KB

A MycoForge instance records *that* something changed (`log.md`, one commit
per workflow run) and *what the current belief is* (claim callouts with
`status` and evidence). It does not record a claim's history under a stable
identity, and it has no notion of coverage: a page written before the KB
adopted callouts has no "unknown" marker on its earlier beliefs. Whether
either gap is worth closing in markdown was put to two independent reviews;
the outcome is [[ADR-006 Two Clocks in Frontmatter]] through
[[ADR-010 Lint the Claim Contract]], summarized in
[[Three-Layer Architecture#What the wiki layer does not record]]. [[Company Brain]] is the
organizational frame: gbrain is a company brain that has decided time is a
first-class axis of the brain, not a property of the sources.
