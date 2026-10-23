---
type: decision
status: accepted
created: 2026-10-23
updated: 2026-10-23
sources:
  - "[[2026-10-15 gbrain Belief Ledger Design (Garry Tan)]]"
  - "[[2026-10-22 ar9av obsidian-wiki (repo)]]"
raw:
  - raw/articles/2026-10-15 gbrain Belief Ledger Design (Garry Tan).md
  - raw/articles/2026-10-22 ar9av obsidian-wiki (repo).md
related:
  - "[[Provenance Tags]]"
  - "[[Belief Ledger]]"
  - "[[ADR-007 No Stable Claim Identity]]"
  - "[[ADR-003 Copy-and-Own with Config-Code Split]]"
tags: [adr, schema, lint, claims]
---

# ADR-010 Lint the Claim Contract

## Context

Raised by the GPT-6 review alone, confirmed in this session: `scripts/lint.py`
checks links, raw paths, index presence and dates, and never parses a
`[!claim]` callout. The Claims section lists `supported | contested |
superseded`, while `/connect` files claims as `status: speculative`; the
vocabulary disagrees and nothing notices. gbrain's point that a belief
record is only as good as the writes it captures (section 7) applies here in
the smallest form: the convention that carries every contestable assertion in
this KB has no check at all, so a malformed callout is invisible until a human
reads it. The present count is 45 callouts on 23 pages; a quick grep shows
every one has a status, but that is luck, not a rule.

## Decision

A bounded `check_claims` in lint, hard error:

- Outside code fences, every `> [!claim]` block has exactly one
  `confidence:` from `high | medium | low` and exactly one `status:` from the
  configured vocabulary, and a nonempty `evidence:` line that contains at
  least one resolving wikilink.
- The status vocabulary moves to `kb.toml` under `[lint]`
  (`claim_statuses = ["supported", "contested", "superseded", "speculative"]`)
  per [[ADR-003 Copy-and-Own with Config-Code Split]], and the Claims section
  in AGENTS.md lists all four, with `speculative` described as what `/connect`
  files and what a later source promotes or refutes.

The check validates shape, not truth. It does not try to find contestable
prose that should have been a claim.

## Consequences

- Existing callouts need repair only where a field is missing or invalid;
  expected to be none or few.
- Any later claim metadata ([[ADR-007 No Stable Claim Identity]]'s block ids,
  if ever) has a parser to hook into.
- About 40 lines of Python, byte-identical across instances since the
  vocabulary is in `kb.toml`.

## Alternatives

- **Warn only**: rejected; a claim without evidence is the one thing this KB
  says never happens, and the fix is always local to one callout.
- **Also require `status: superseded` claims to link their successor**:
  deferred to when [[ADR-007 No Stable Claim Identity]]'s convention has been
  in use long enough to have examples.

## Later evidence

- 2026-10-23, [[2026-10-22 ar9av obsidian-wiki (repo)]]: a lint that goes
  past shape. obsidian-wiki tags every claim `extracted`, `^[inferred]` or
  `^[ambiguous]` and "lint flags pages drifting into speculation", with an
  `undated_claims` rule. That is the check this ADR declined ("does not try
  to find contestable prose that should have been a claim"), made possible by
  tagging all prose rather than only callouts. Whether a lighter form fits
  here is the open question on [[Provenance Tags]]; logged for the Decision
  workflow.
