# Schema review: three open implications (WikiSkill, OpenWiki, agent automations)

You are reviewing three proposed schema questions for an agent-maintained
markdown knowledge base. Run this prompt verbatim; two independent reviewers
receive the same text. Do not coordinate. Do not read `wiki/log.md`,
`staging/ingest.md`, `staging/scout.md`, any `staging/schema-review-*` file
other than this one, or any `ADR-*` page: they hold the ingesting agent's own
ranking, and the point is an unanchored read. Where you need a prior
decision, it is stated below.

## Read, in this order

1. `AGENTS.md` — the schema. Note Claims, Ingest, the Research/Scout/Connect
   paragraph, Version control, and Template contract.
2. `scripts/lint.py` — what is enforced today; `check_claims` and the raw-path
   checks above all.
3. `.agents/skills/scout/SKILL.md` and `.agents/skills/research/capture.md` —
   the only capture path that could plausibly run unattended.
4. `mcp/server.py` — the read-only MCP surface.
5. The three sources, the relevant parts only:
   - `raw/papers/2026-08-27 WikiSkill - Compiling Agent Experience into Persistent Knowledge for Skill Evolution.md`:
     sections 3.1, 3.2 (all four subsections) and 5.1.
   - `raw/articles/2026-10-22 langchain-ai openwiki (repo).md`: the
     "Grounded Claims" section and the paragraphs around lines 230 and 334.
   - `raw/articles/2026-10-08 Building Effective Agent Automations (Anthropic).md`:
     Sources, Memory, Guardrails, and the six rules under Getting started.
6. How the KB filed them: `wiki/concepts/Skill Evolution.md`,
   `wiki/concepts/Provenance Tags.md`, `wiki/concepts/Unattended Agent State.md`,
   and the "Continuous ingest" section of `wiki/concepts/Ingest Workflow.md`.
   One reader's summaries, not ground truth; say where they misread or
   overreach.

## Prior decisions you may rely on without reading them

- Claims have no stable id. A reword, move or split is named in the log entry.
  Evidence in a `[!claim]` callout is a wikilink to a raw file, never a
  location inside it.
- `speculative` is the status for the agent's own inference, with premises
  and a confirm/refute line in the evidence.
- The MCP server is read-only; writes stay interactive.
- Skills are kept small and portable; anything instance-specific lives in
  `kb.toml`, lint, or AGENTS.md, never in a skill.
- `raw/` is immutable. The user owns it; the agent never writes there except
  through the capture skills, and never edits a captured file.

## The questions

For each, answer: **Real or local?** (a gap for this KB, or one that exists
only in the source's setting), **Smallest change** (to `AGENTS.md`,
`scripts/lint.py`, `kb.toml`, or a skill; or "a convention, no tooling"; or
"no change"), and **Cost** on every future ingest and for the human reading in
Obsidian.

1. **Wiki feeding skills.** WikiSkill's third layer is executable skills, with
   a skill proposer that reads the wiki and a `PURPOSE.md` per skill pointing
   back at the wiki pages it came from, gated by a validation score with
   rollback. This KB's skills are vendored tooling that the wiki describes but
   never feeds. Should anything in `wiki/` be allowed to change
   `.agents/skills/`, what would gate it given there is no score, and is
   per-skill provenance back to wiki pages worth having even with no
   automation? Also: WikiSkill keeps the wiki away from the inference agent
   and gives it only to the maintainer (5.1). Does that split say anything
   about who the MCP server's readers should be?

2. **Evidence anchors.** OpenWiki pins each Grounded Claim to versioned
   source evidence (file plus line range plus version) and rechecks every
   pin before deciding a run is a no-op. Here, raw files never change, so a
   pin cannot go stale, and claim evidence names the file only. Is
   `[[raw file#heading]]` (or a block id) in the evidence line worth the write
   cost for reader auditability alone? If yes, as a rule for new claims only,
   or a backfill, and should lint check that the anchor resolves?

3. **Scheduled capture.** The automations source describes an agent that runs
   on a schedule with two stores (reader-owned read-only preferences,
   agent-owned read-write state), per-source bookmarks, an append-only ledger,
   a failed-read rule, and verify-then-confirm-then-record. `/scout` now has
   most of that (read `SKILL.md` as it stands). `AGENTS.md` says ingest is one
   source per session with the user present, and says nothing about capture
   running unattended. If `/scout` were ever put on a timer, what must
   `AGENTS.md` say first: where the human gate sits (the ledger row? a PR?),
   what the scheduled run may write, and what it must never do? Or is the
   right answer that scheduling is out of scope for this schema and the
   sentence to add is a prohibition?

Then:

4. **Missed.** Anything in the three sources bearing on this KB's schema
   that the questions above do not cover.
5. **Misread.** Where the four wiki pages in step 6 state a source wrongly
   or overreach, quoting the sentence.

## Output

Write one file and touch nothing else:
`staging/schema-review-open-implications-<your model name>.md`. Under 150
lines. Shape:

```
# Schema review (open implications) — <model>, <date>

## Summary
Three to five lines: which of the three you would adopt, which not, and the
one thing you would do first.

## 1. Wiki feeding skills
Real or local: ...
Smallest change: ...
Cost: ...

## 2. Evidence anchors
...

## 3. Scheduled capture
...

## 4. Missed
...

## 5. Misread
...
```

Be specific and willing to say "no change". A reviewer who adopts all three
has not done the cost column.
