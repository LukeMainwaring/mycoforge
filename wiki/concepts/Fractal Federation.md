---
type: concept
created: 2026-07-10
updated: 2026-07-10
related:
  - "[[Subtractive Onboarding]]"
  - "[[Three-Layer Architecture]]"
confidence: high
tags: [architecture, template]
---

# Fractal Federation

How MycoForge KBs nest: **there is one template, and "parent" is a feature, not a
different kind of repo.** An orchestrator KB is just a normal KB that kept the
`orchestrator` feature — a children manifest in `kb.toml`, a routing workflow in
its schema, and child-aware lint checks.

The federation rules:

- **Children are independent git repos**, physically nested inside the parent's
  folder tree (so Obsidian sees one vault) but gitignored by the parent (so each
  repo stays self-contained).
- **Routing, not reaching.** The parent session consults its children manifest and
  descends into the matching child — reading its `index.md` and `overview.md`
  first — but never edits a child's files. Writes happen in a session opened in
  the child.
- **Cross-KB wikilinks are warn-only.** Obsidian resolves them vault-wide, so they
  work for the reader; lint warns rather than errors so every KB remains portable
  as a standalone folder. Portability is the invariant federation must not break.

Because the pattern is fractal, a child can itself keep the orchestrator feature
and have children — the structure recurses without any new machinery.
