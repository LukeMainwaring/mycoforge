# AGENTS.md — the schema

This file is the **schema** of this knowledge base: the contract that tells an AI
agent (Claude Code, Codex, etc.) how the wiki is structured, what the conventions
are, and which workflow to run when. It is the canonical instruction file —
`CLAUDE.md` is a symlink to it; always edit this file.

MycoForge is a Karpathy-pattern **LLM wiki**: a persistent, compounding markdown
knowledge base that you (the agent) build and maintain, sitting between the user
and their raw sources. Knowledge is compiled once at ingest time and kept current —
not re-derived on every question. This instance's domain is the LLM-wiki pattern
itself (see `kb.toml` for identity and all per-instance configuration).

## The three layers

1. **`raw/`** — immutable curated sources (`papers/`, `articles/`, `podcasts/`,
   `assets/`). You read these; you **never modify or delete** them. They are the
   user's source of truth.
2. **The wiki** — `wiki/` (and its `index.md` catalog, append-only `log.md`, and
   `overview.md`). You own this layer entirely: you create pages, update them when
   new sources arrive, maintain cross-references, and keep everything consistent.
3. **The schema** — this file. You and the user co-evolve it; log every schema
   change (see Log conventions).

## Division of labor

The user curates sources, directs the analysis, and asks questions. You do
everything else: summarizing, cross-referencing, filing, indexing, logging, and
linting. The user reads the wiki (usually in Obsidian) but rarely edits it — if
you find hand-made edits, respect them and fold them in.

## File naming

- **Wiki pages**: Title Case, e.g. `Three-Layer Architecture.md`. The filename is
  the page title and the wikilink target.
- **Raw files**: `YYYY-MM-DD <Title>.<ext>` — publication date if known, otherwise
  capture date, e.g. `2026-04-04 LLM Wiki (Karpathy).md`.
- **Never** use these characters in a filename (they break Obsidian links or file
  systems): `[ ] # ^ | : / \`. Parentheses, hyphens, apostrophes, and spaces are fine.

## Frontmatter

Every wiki page starts with YAML frontmatter. **Wikilinks in YAML must be quoted**
(`"[[Page]]"`) or Obsidian's parser chokes.

```yaml
---
type: concept            # this instance: concept | person | synthesis | decision
created: 2026-07-10      # date the page was created (never changes)
updated: 2026-07-10      # bump on every substantive edit
sources:                 # wikilinks to the raw sources behind this page
  - "[[2026-04-04 LLM Wiki (Karpathy)]]"
raw:                     # repo-relative paths to those raw files (lint verifies these)
  - raw/articles/2026-04-04 LLM Wiki (Karpathy).md
related:                 # wikilinks to sibling wiki pages
  - "[[Ingest Workflow]]"
confidence: high         # high | medium | low — how settled the page's content is
tags: [architecture]
---
```

`type: decision` pages (ADRs) additionally carry `status: proposed | accepted |
superseded | rejected`. Omit fields that genuinely don't apply (e.g. a person page
may have no `raw:`), but `type`, `created`, and `updated` are mandatory.

## Claims

Contestable assertions — anything a future source could contradict — go in a
`[!claim]` callout so they're findable and auditable:

```markdown
> [!claim] LLM wikis compound knowledge; RAG re-derives it per query
> confidence: high · status: supported
> evidence: "the wiki is a persistent, compounding artifact" — [[2026-04-04 LLM Wiki (Karpathy)]]
```

When a new source contradicts an existing claim, don't silently rewrite it: update
the callout's status (`supported | contested | superseded`), cite both sources, and
note the conflict in the ingest's log entry.

## Workflows

| The user says… | Run |
|---|---|
| "ingest this", "process \<file\>", drops a file in `raw/` | **Ingest** |
| any question about the domain | **Query** |
| "lint", "health check", "clean up the wiki" | **Lint** |
| "grab this podcast/video", `/transcript <url>` | **Transcript** — fetch into `raw/podcasts/` | <!-- sf:keep-if(media-capture) -->
| "carve the highlights", `/snippet <file>` | **Snippet** — carve `==highlights==` into a clip | <!-- sf:keep-if(media-capture) -->
| "research \<topic\>", "find sources on…", `/research` | **Research** — source discovery into `raw/` | <!-- sf:keep-if(insight) -->
| "what connects…", "find novel links", `/connect` | **Connect** — bridge weakly-linked pages | <!-- sf:keep-if(insight) -->
| "we decided…", "new ADR", "update the roadmap" | **Product ops** | <!-- sf:keep-if(product) -->
| a question belonging to a child KB | **Routing** | <!-- sf:keep-if(orchestrator) -->

### Ingest

One source per session — ingestion is judgment-heavy and the user stays involved.

1. Read the raw source in full. Discuss key takeaways with the user.
2. Create or update wiki pages: new concepts/entities get pages; existing pages get
   updated content and provenance (`sources`/`raw` frontmatter, claim callouts).
   A single source may touch many pages — that's the point.
3. Update `wiki/index.md` (every page has exactly one entry).
4. Append an `ingest |` entry to `wiki/log.md`.

Never modify anything under `raw/` during ingest.

### Query

Read `wiki/index.md` first to find relevant pages, drill into them, and answer **in
conversation** with wikilink citations. File the answer back into the wiki as a
`syntheses/` page **only when the user asks** — good answers are worth keeping, but
the user decides which ones. If you do file one, index it and log a `query |` entry.

### Lint

1. Run `python3 scripts/lint.py` and fix every hard issue it reports.
2. Then do the judgment pass the script can't: contradictions between pages, claims
   a newer source supersedes, missing cross-references, concepts worth promoting to
   pages, data gaps worth a new source.
3. Log a `lint |` entry summarizing what changed.

<!-- sf:begin(media-capture) -->
### Transcript and Snippet

Two capture skills that populate `raw/` and **never** touch the wiki (capture is
mechanical; ingestion stays a separate, deliberate step):

- **`/transcript`** (`.agents/skills/transcript/`) — pulls a YouTube/podcast
  transcript into `raw/podcasts/` with dated naming, source frontmatter, and
  `[MM:SS]` anchors.
- **`/snippet`** (`.agents/skills/snippet/`) — carves the passages the user marked
  with `==highlight==` out of a transcript into a structured clip file, applying
  the ASR-correction glossary from `kb.toml` `[snippet]`.
<!-- sf:end(media-capture) -->

<!-- sf:begin(insight) -->
### Research and Connect

Two knowledge-work skills that bracket the ingest pipeline:

- **`/research`** (`.agents/skills/research/`) — the sourcing arm: web-search a
  question, vet candidates with the user, and land approved sources in `raw/`
  with full provenance frontmatter. Capture-only — it ends by *offering* Ingest,
  never running it.
- **`/connect`** (`.agents/skills/connect/`) — the compounding arm: find pages
  that should reference each other but don't, propose at most three candidate
  bridges, and file only user-approved ones as `syntheses/` pages whose claims
  are marked `status: speculative` with confirm/refute lines. Logs a
  `discovered |` entry.
<!-- sf:end(insight) -->

<!-- sf:begin(product) -->
### Product ops

This KB carries its product layer as **spec pages, never application code**. Real
software lives in separate repos (grown from the sporeforge template) that read
this KB over MCP.

- **Decisions lifecycle**: significant decisions become ADR pages in `decisions/`
  (Context / Decision / Consequences / Alternatives, `type: decision` frontmatter
  with `status:`). Supersede rather than rewrite: new decision page, old one gets
  `status: superseded` and a link. Log a `decision |` entry.
- **Roadmap upkeep**: `roadmap.md` holds Next / Later only — no Done section.
  Remove items when they ship (the log and git history are the record); promote
  Later items to Next as they become active. `Home.md` is the dashboard — keep
  its links current.
- **Embedded-prompt convention**: each external software artifact gets one page in
  `product/software/` containing the full build prompt (a fenced block ready to
  paste into a coding agent) plus a link to the resulting repo. The prompt *is*
  the spec; keep it current as decisions change. See the example page in
  `product/software/`.
<!-- sf:end(product) -->

<!-- sf:begin(orchestrator) -->
### Routing (orchestrator)

When this KB is a parent: consult the `[[orchestrator.children]]` entries in
`kb.toml` and descend into the child whose `scope` matches the question. Read the
child's `index.md` and `overview.md` first. **Never edit a child's files from the
parent session** — children are independent git repos; open a session there
instead. Cross-KB wikilinks resolve in Obsidian (vault-wide) but are warn-only in
lint, so every KB stays portable as a standalone folder.
<!-- sf:end(orchestrator) -->

<!-- sf:begin(mcp-server) -->
## MCP server

`mcp/server.py` exposes this KB read-only over MCP: `search_kb`, `read_page`,
`get_index`. `.mcp.json` registers it for sessions opened in this repo; product
repos attach it with one config line (see README). It is deliberately read-only —
ingestion stays an interactive workflow here, never an API call.
<!-- sf:end(mcp-server) -->

## Log conventions

`wiki/log.md` is **append-only**, most recent at the bottom. Every entry:

```markdown
## [YYYY-MM-DD] <prefix> | <Title>
One or two lines on what happened and which pages were touched.
```

Prefixes (greppable — `grep "^## \[" wiki/log.md | tail -5` shows recent activity):
`ingest | query | lint | decision | schema | discovered`. Use `schema` for changes
to this file, `discovered` for connections or gaps worth recording outside a
formal workflow.

## Style

- **Anti-padding rule**: a 5-line stub with good links beats a 50-line page with
  filler. Never pad a page to look complete; density of linked facts is the goal.
- Every page cites its provenance (frontmatter `sources`/`raw`, claim evidence).
- **Self-contained portability**: links resolve within this repo. The KB must work
  as a standalone folder — cloned alone, everything still connects.
- Obsidian-compatible everywhere: wikilinks (`[[Page]]`, `[[Page|shown]]`,
  `[[Page#Heading]]`), callouts, no HTML that pollutes reading view.

## Template contract

This repo is a MycoForge-template instance. The template machinery lives in
`.template/` (deleted once onboarding is done) and the vendored tooling in
`scripts/` and `.agents/skills/`.

- Feature-specific code and prose are wrapped in the template's `sf:` markers —
  see `.template/README.md` for the exact syntax. **Preserve the markers** when
  editing marked content; if the feature is later cut, your unmarked additions
  would wrongly survive.
- If you add content that belongs to a single feature, mark it and update
  `.template/features.toml`.
- After touching any feature seam, re-run `bash .template/verify_matrix.sh`.
- All per-instance data (lint terms, link allowlists, glossaries, children) lives
  in `kb.toml`, **never hard-coded in Python** — that's what keeps the vendored
  code byte-identical across instances and lets `/sync-upstream` port template
  updates.
