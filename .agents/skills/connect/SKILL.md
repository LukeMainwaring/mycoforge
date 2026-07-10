---
name: connect
description: Find novel connections between weakly-linked pages in the wiki and file the good ones as speculative synthesis pages. Use when the user says "what connects", "find novel links", "draw connections", "muse on the wiki", or "/connect". The one skill that exploits compounding — use sparingly and file only what survives discussion.
---

# Draw novel connections across the wiki

You are looking for bridges the wiki doesn't know it has: pages (or clusters)
that rarely reference each other but share an underlying idea, tension, or
mechanism. This is the compounding payoff of a maintained wiki — the
cross-references already exist, so *missing* cross-references are findable.
It is also the easiest skill to produce slop with, so the guardrails below are
the skill.

## Steps

1. **Pick the scope.** The user may name a topic or pages; otherwise work from
   the whole wiki. Read `wiki/index.md`, then map the link structure — grep the
   wiki for `[[...]]` wikilinks (skills and scripts aside, `scripts/lint.py`'s
   source shows the parsing conventions) and look for pages or clusters with few
   or no links between them despite living in the same domain.
2. **Generate candidate bridges — at most three.** For each candidate, work it
   out honestly before presenting:
   - the two (or more) anchor pages, by wikilink
   - the proposed connection, stated in one falsifiable sentence
   - what in the KB already supports it (quote or cite the pages/raw sources)
   - what would **confirm or refute** it — a source to find, a question to ask
3. **Discuss in conversation.** Present the candidates and let the user poke at
   them. Expect most to die here; that's the skill working, not failing.
4. **File only what survives — at most one or two pages per run.** An approved
   bridge becomes a `wiki/syntheses/` page obeying the full schema: frontmatter
   with `related:` pointing at the anchors, `confidence: low` (or `medium` if
   the KB's own evidence is strong), and every contestable assertion in a
   `[!claim]` callout with `status: speculative` and its confirm/refute line as
   evidence. Add the index entry and a `discovered |` log entry naming the
   anchors.
5. **Report.** What was proposed, what was filed, what was discarded and why.

<!-- sf:begin(orchestrator) -->
## Cross-KB mode (parent KBs)

When this KB is a parent, connections can span children: consult the children
manifest in `kb.toml`, read each relevant child's `index.md` and `overview.md`
(and drill into pages per the routing workflow), and look for bridges *between*
children's domains. The bridge page is filed **in this parent's own wiki** —
never write into a child. Link the anchors with ordinary wikilinks; Obsidian
resolves them vault-wide, and lint treats cross-KB links as warnings by design.
<!-- sf:end(orchestrator) -->

## Guardrails

- **Never file without explicit approval**, and never more than two pages per
  run — a wiki that grows speculative pages faster than evidence is worse than
  one with none.
- Every filed claim carries `status: speculative` and names what would confirm
  or refute it. When later ingests touch a speculative claim, update its status
  — that's how these pages earn their keep or get deleted.
- The anti-padding rule applies double here: a 5-line bridge with two good
  anchors and one sharp claim beats a 50-line essay.
- Connections must be grounded in what the KB actually says — cite pages and raw
  sources, don't free-associate from general knowledge. If the idea needs
  outside evidence, say so and suggest `/research` instead of filing.
