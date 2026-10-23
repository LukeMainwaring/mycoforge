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
  - "[[ADR-006 Two Clocks in Frontmatter]]"
tags: [adr, schema, trust]
---

# ADR-009 Hand Edits Are the Unmanaged Writer

## Context

gbrain certifies coverage only on sources where every write passes a
coordinated path, because an unmanaged writer breaks interval completeness
(source sections 5.1 and 7). Its trust tiers record **who wrote**
(`user_confirmed`, `operator_curated`, `agent_written`), and a lower-tier
write that would supersede a higher-tier belief is held for the owner, never
applied or refused (section 6.2).

The ingest asked whether `raw/` sources should carry a trust tier by genre.
Both reviews say that misreads gbrain: genre is visible from folder, `type:`
and `author:`; reliability is per claim, not per source; deriving
`confidence` from a tier would be false precision. Both reject a source tier
and a derived confidence. Opus carries the real idea over: this KB's unmanaged
writer is the user editing in Obsidian between sessions. Those edits are
swept into the next agent commit with that run's time and prefix, so both
the recorded clock and the authorship are wrong, and AGENTS.md says to
"respect and fold in" hand edits but nothing about a later source
contradicting a claim the user wrote.

## Decision

Two sentences, no fields, no lint.

- **Version control**: at session start, if `git status` shows uncommitted
  changes under `wiki/`, tell the user and commit them on their own as
  `hand-edit: <pages>` before the workflow run.
- **Claims**: a claim the user wrote or edited by hand is never superseded by
  the agent. Set `status: contested`, cite both, and ask. Identifying such a
  claim is what the `hand-edit:` commits are for.

Nothing changes for `/connect`: its `status: speculative` already follows
gbrain's cap rule that an agent-derived claim is never promoted without a
source.

## Consequences

- One `git status` per session and an occasional extra commit.
- Recorded time stays honest for agent writes, which is what makes the
  "commit time is recorded time" line in [[Three-Layer Architecture]] true as
  narrowed.
- `contested` stays a convention, not a gate: GPT-6's point that it "neither
  enforces a write gate nor establishes an owner decision" is accepted; the
  ask-the-user step is the owner decision.

## Alternatives

- **Trust tier on raw sources, confidence derived from it**: rejected by both
  reviews for the reasons above.
- **A `tier:` or `author:` field on claims**: rejected; the commit prefix
  already carries authorship, and a field would be stale the first time the
  agent touched a hand-written claim.
- **Do nothing**: rejected because the clock problem is real and the fix is
  one git command.
