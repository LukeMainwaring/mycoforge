---
type: decision
status: accepted
created: 2026-10-28
updated: 2026-10-28
related:
  - "[[Three-Layer Architecture]]"
  - "[[Ingest Workflow]]"
  - "[[ADR-013 Evidence Stays at File Level]]"
  - "[[ADR-014 The Wiki Does Not Edit Skills]]"
tags: [adr, schema, skills, architecture]
---

# ADR-016 Architecture Guide for Machinery and Content

## Context

Two code repos grown from the sporeforge template carry an
`architecture-guide` skill: an overview plus one page per topic under
`docs/architecture/`, each page a Summary, a Mermaid diagram, how it works,
why it is built that way, a short spoken explanation, and a footer naming the
commit and source paths it was written from. A `check` run diffs each page's
commit to `HEAD` over its paths and reports stale pages. Archify renders a
topic as standalone HTML, committed beside the page with its spec; the
Mermaid diagram stays the statement of the topic's claims. Upstart's ADR
0004 fixed those committed-output rules.

This KB has no diagram anywhere. A developer who clones it meets `AGENTS.md`
and a wiki, and has to reconstruct the loop (sources in, pages compiled,
questions answered, lint feeding back) from prose. The wiki's content has
the same gap: twenty-seven concept pages in three clusters with no map of
how they relate.

A wiki differs from a codebase in two ways that matter. Its "source code"
is `AGENTS.md`, `scripts/lint.py`, `kb.toml` and the skills, small enough
that one page can hold the machinery. And it has a second subject, the
knowledge itself, whose sources are wiki pages and raw files rather than
modules.

## Decision

Port the skill as a native skill, `/architecture-guide`,
forked from Upstart's copy. Sporeforge and Upstart keep the code-repo
flavor; this KB owns the wiki flavor, and children receive it through
`/sync-upstream`. The two flavors drift independently.

- **Two kinds of topic, one folder.** Pages live in `architecture/` at the
  repo root, beside `decisions/` and `product/`, with full frontmatter
  (`type: architecture`), an `index.md` entry each, and wikilinks. Each page
  carries `kind: machinery | content`. The staleness mechanism is shared:
  frontmatter `commit:` (the commit the page was written at) and
  `watches:` (repo paths the page rests on), diffed by the skill's `check`
  run. A machinery page watches tooling paths; a content page watches wiki
  pages and raw files.
- **Two overviews, no hub.** `The Machinery` is one page: the loop as one
  Mermaid diagram, then one focus per section (why compile rather than
  retrieve; the three layers and who writes where; the write path; the read
  path; keeping it honest), promoted to its own page only when a focus
  outgrows a screen or needs its own diagram. `The Knowledge Map` is the
  content overview, with one topic page per concept cluster. Each overview
  holds its kind's topic list and watched directories.
- **Template per kind.** Machinery pages keep "Why it's built this way",
  with reasons from ADRs and `AGENTS.md`. Content pages replace it with
  "Where the tensions are": which claims are contested or speculative and
  what would settle them. The explain section is a few sentences in a
  colleague register plus at most three follow-ups.
- **Archify unchanged.** Mermaid in the page is the source of truth for a
  topic's pieces, relationships and boundaries. A render is committed as
  spec plus HTML under `architecture/diagrams/<slug>/`, linked from the
  page, never embedded; no PNGs, no receipts. The layout rules that passed
  Upstart's tallies port as written, with repo-specific phrasing removed.
  Evidence points at file paths of whatever kind, which
  [[ADR-013 Evidence Stays at File Level]] already requires.
- **A cuttable feature.** `[features.architecture]` in
  `.template/features.toml`, owning the skill and the `architecture/`
  folder, with `sf:` markers around its prose in `AGENTS.md`.
- **One PR.** Skill, this ADR, the schema row, and the first run land
  together: the two overviews rendered, the cluster pages drawn in Mermaid
  only. Cluster renders follow one per `render <topic>` run, each its own
  PR.

## Consequences

- Lint is untouched. It already checks frontmatter, index entries, links
  and orphans for any root folder, so the new pages are held to the wiki's
  rules at no cost; the new `commit:` and `watches:` fields are the skill's
  to read. A warn-only staleness check in lint is a later option, not taken
  here.
- Staleness is measured against committed state, as in the code repos: a
  page edited in the working tree is current only once committed.
- A page about the knowledge is itself a wiki artifact and can go stale
  when an ingest changes a cluster; the `check` run reports it with the
  changed pages, and the ingest log entry is where that is noticed first.
- The reader of the machinery page is a developer who clones the template:
  technical, new to LLM wikis, interested in closed-loop systems. Internals
  (branching, ADR mechanics, template seams, federation) get a sentence in
  the overview at most.
- Parked: whether machinery pages travel to children as template content or
  are regenerated per instance. Nothing here forecloses either.

## Alternatives

- **Pages under `docs/architecture/` as in the code repos**: rejected. The
  user reads this repo in Obsidian, and a sidecar outside the frontmatter,
  index and lint rules would be the one unlinted folder.
- **One topic page per machinery focus**: rejected for now. Six pages of
  six sections about a loop one diagram holds is padding; the archify render
  carries the focuses as regions and cards, and the promotion rule covers
  growth.
- **Separate skills or configs for machinery and content**: rejected. The
  mechanism is identical once sources are repo paths; only the watched paths
  and one template section differ.
- **Knowledge maps via `/connect`**: rejected. `/connect` proposes bridges
  the wiki lacks; the map shows the links it has.

## Implemented

2026-10-28, same PR, accepted by the user: the skill, the five pages, the two overview renders, and `[features.architecture]`. `verify_matrix.sh` caught three prune hazards on the way (the ADR citing the skill path, unmarked index and Home links, a render citing a cuttable skill as evidence), all fixed in-branch. Cluster renders follow one per PR.
