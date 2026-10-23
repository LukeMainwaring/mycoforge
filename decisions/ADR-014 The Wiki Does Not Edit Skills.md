---
type: decision
status: proposed
created: 2026-10-23
updated: 2026-10-23
sources:
  - "[[2026-08-27 WikiSkill - Compiling Agent Experience into Persistent Knowledge for Skill Evolution]]"
raw:
  - raw/papers/2026-08-27 WikiSkill - Compiling Agent Experience into Persistent Knowledge for Skill Evolution.md
related:
  - "[[Skill Evolution]]"
  - "[[Advisory and Deterministic Controls]]"
  - "[[ADR-003 Copy-and-Own with Config-Code Split]]"
  - "[[ADR-004 Read-Only MCP in v1]]"
tags: [adr, schema, skills]
---

# ADR-014 The Wiki Does Not Edit Skills

## Context

WikiSkill's third layer is executable skills: a proposer reads the wiki and
rewrites skills, each skill carries a `PURPOSE.md` pointing back at the wiki
pages it came from, and a validation score with rollback gates every change
([[2026-08-27 WikiSkill - Compiling Agent Experience into Persistent Knowledge for Skill Evolution]], [[Skill Evolution]]). The
WikiSkill ingest asked whether `wiki/` should feed `.agents/skills/` here,
what would gate it with no score, and whether the paper's executor/maintainer
read split says who the MCP server's readers should be.

## Question

May anything in `wiki/` change `.agents/skills/`, and what is the gate?

Two independent reviews (`staging/schema-review-open-implications-*.md`,
diff in `-diff.md`; removed from the tree on 2026-10-23, in git history at `0ddc41b`) agree: no change. The path exists already. A wiki page
motivates a `proposed` ADR (Ingest step 5), the change goes on a branch as a
draft PR with lint and the verify matrix as evidence, and merges on the
user's say-so. "That human merge is the gate." Lint and the matrix check
shape, not quality, so they cannot stand in for WikiSkill's score, and
neither review wants an automated acceptance without one. Both reject a
`PURPOSE.md` per skill: it breaks the upstream diff `/sync-skills` relies on,
lives in a dot-folder Obsidian hides, and the trail already exists (the ADR
links the page, the PR cites the source, `git log --follow` finds the PR).
Both reject reading an MCP reader policy out of section 5.1: the split
protects a training signal, the paper calls its mechanism a hypothesis, and
product repos reading over MCP produce code, not traces that feed this wiki.

## Decision (proposed)

No schema change. Recorded so the question is closed on record:

- Skills are vendored tooling. The wiki describes them and may motivate a
  change to them; it never writes them. The gate is the human merge of a
  draft PR whose ADR names the motivating page and source.
- No per-skill provenance file. Provenance for a skill change lives in its
  ADR and PR.
- No MCP reader policy follows from WikiSkill. [[ADR-004 Read-Only MCP in v1]]
  stands as written.

## Consequences

- Nothing per ingest. A skill change pays for its evidence once, in the PR.
- A rejected skill ADR stays on record, which is what WikiSkill's
  `skill-impact.md` does for rejected proposals.
- The one thing the paper's split does imply here is circular evidence, not
  reader access: a source produced by an agent that read this KB is not
  independent support for what it repeats. Noted in
  [[ADR-013 Evidence Stays at File Level]].

## Alternatives

- **Wiki-driven skill proposals gated by lint and the matrix**: rejected.
  Shape checks are not a quality score; the paper's result depends on the
  score and on rollback.
- **`PURPOSE.md` per skill with no automation**: rejected. Cost on every
  upstream sync, invisible to the reader, duplicates the ADR trail.
- **Restrict MCP readers to maintainers**: rejected. No evidence it helps a
  wiki that trains nothing, and it would defeat the product seam.

## Noted, not decided

Opus: WikiSkill names "no automated pruning" as its own gap, and this KB's
Lint step 2 has "concepts worth promoting" but no "pages worth merging or
retiring". A one-line addition to Lint when a lint pass first needs it.
