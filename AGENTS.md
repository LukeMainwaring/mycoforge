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
  capture date, e.g. `2026-04-04 LLM Wiki (Karpathy).md`. Raw frontmatter keeps
  source time (`published:`) apart from capture time (`retrieved:`; older
  clipper files say `created:`); the filename date is one of those two, and
  neither is ever copied into a wiki page's `created`/`updated`, which are
  maintenance time (lint warns on a mismatch; the user fixes raw files).
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
the callout's status, cite both sources, and note the conflict in the ingest's
log entry. Statuses (vocabulary in `kb.toml` `[lint].claim_statuses`, lint
checks the shape of every callout): `supported | contested | superseded |
speculative`, where `speculative` is an inference you drew rather than a
source stated, whether filed by `/connect` or written during ingest or query
filing: its evidence line names the premises and what would confirm or refute
it, and a later source promotes or refutes it. A contestable sentence no
source states goes in a `speculative` callout or is cut; cross-links and
statements about this KB itself stay as prose. When a claim is superseded, keep the old proposition in
its callout and point at the successor by page and claim title; never
overwrite it in place. When you reword, move or split a claim, name the old
and new title in the log entry. A claim the user wrote or edited by hand is
never superseded by you: set `status: contested`, cite both, and ask.

## Workflows

| The user says… | Run |
|---|---|
| "ingest this", "process \<file\>", drops a file in `raw/` | **Ingest** |
| any question about the domain | **Query** |
| "lint", "health check", "clean up the wiki" | **Lint** |
| `/transcript <url>` | **Transcript** — fetch into `raw/podcasts/` | <!-- sf:keep-if(media-capture) -->
| `/snippet <file>` | **Snippet** — carve `==highlights==` into a clip | <!-- sf:keep-if(media-capture) -->
| `/research <topic>` | **Research** — source discovery into `raw/` | <!-- sf:keep-if(insight) -->
| `/scout [Nd]` | **Scout** — standing watch for fresh sources, staged in `staging/scout.md` | <!-- sf:keep-if(insight) -->
| `/connect` | **Connect** — bridge weakly-linked pages | <!-- sf:keep-if(insight) -->
| "we decided…", "new ADR", a schema implication worth deciding | **Decision** |
| "update the roadmap", a new software spec | **Product ops** | <!-- sf:keep-if(product) -->
| a question belonging to a child KB | **Routing** | <!-- sf:keep-if(orchestrator) -->
| `/sync-skills` | **Sync skills** — port upstream changes to the vendored Pocock skills |

The slash-only rows are user-invoked: the agent never fires them on its own, the
user types the command. Utility skills outside the KB workflows: `/grill-me` (stress-
test a plan), `/handoff` (compact a session for the next agent), `/teach` (learn a
concept in `learning/<topic>/`), `/pr` (PR body template).

### Ingest

One source per session — ingestion is judgment-heavy and the user stays involved.

1. Read the raw source in full. Discuss key takeaways with the user.
2. Create or update wiki pages: new concepts/entities get pages; existing pages get
   updated content and provenance (`sources`/`raw` frontmatter, claim callouts).
   A single source may touch many pages — that's the point.
3. Update `wiki/index.md` (every page has exactly one entry).
4. Append an `ingest |` entry to `wiki/log.md`.
5. If the source bears on how *this KB* works — its schema, claim conventions,
   lint rules, or skills — do not change them in the ingest session. Record the
   implication as a line in the ingest's log entry, then make the change on its
   own branch (see Version control), with the PR citing the source. Knowledge
   lands on `main` now; structure changes with review and provenance.

Never modify anything under `raw/` during ingest.

<!-- sf:begin(insight) -->
Pending sources, in recommended order with per-source watch-outs, live in
`staging/ingest.md`; tick a row once its ingest is logged.
<!-- sf:end(insight) -->

### Query

Read `wiki/index.md` first to find relevant pages, drill into them, and answer **in
conversation** with wikilink citations. File the answer back into the wiki as a
`syntheses/` page **only when the user asks** — good answers are worth keeping, but
the user decides which ones. If you do file one, index it and log a `query |` entry.
A "what did this KB say at time T" answer cites the commit it read and says
"the page stated X" rather than "the KB recorded X" unless a claim callout
carried it; an earlier state that git does not hold is reported as unknown,
never reconstructed.

### Lint

1. Run `python3 scripts/lint.py` and fix every hard issue it reports.
2. Then do the judgment pass the script can't: contradictions between pages, claims
   a newer source supersedes, contestable inference in bare prose and claims whose
   conclusion is stronger than the evidence cited, missing cross-references,
   concepts worth promoting to pages, data gaps worth a new source.
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
### Research, Scout, and Connect

Three knowledge-work skills that bracket the ingest pipeline:

- **`/research`** (`.agents/skills/research/`) — the sourcing arm: web-search a
  question, vet candidates with the user, and land approved sources in `raw/`
  with full provenance frontmatter. Capture-only — it ends by *offering* Ingest,
  never running it.
- **`/scout`** (`.agents/skills/scout/`) — the standing watch: searches the
  `topics` and `watch` list in `kb.toml` `[scout]` for sources fresher than
  `max_age_days` / `repo_active_days`, stages at most five candidates in
  `staging/scout.md` (the **ledger**: review stage, skip list, and "since when"
  in one file, plus `unreachable:` entries whose window stays open and
  `proposed watch` rows the user pastes into `kb.toml`), and captures only
  approved rows. It reads `kb.toml` and never writes it. Capture-only, same
  hand-off as `/research`. The capture rules both skills follow live in
  `.agents/skills/research/capture.md`.
- **`/connect`** (`.agents/skills/connect/`) — the compounding arm: find pages
  that should reference each other but don't, propose at most three candidate
  bridges, and file only user-approved ones as `syntheses/` pages whose claims
  are marked `status: speculative` with confirm/refute lines. Logs a
  `discovered |` entry.
<!-- sf:end(insight) -->

### Decision

Significant decisions about this KB, its schema, or (where the product layer is
kept) its product become ADR pages in `decisions/`: Context / Decision /
Consequences / Alternatives, `type: decision` frontmatter with `status:`.
Supersede rather than rewrite: new decision page, old one gets
`status: superseded` and a link. Log a `decision |` entry.

Schema implications recorded by Ingest (step 5) enter here: each becomes a
`status: proposed` ADR on a branch, stating the question, the source that
raised it, and the smallest change that would close it. Accept, reject, or
leave proposed; later ingests add evidence to the ADR instead of to the log.
A `proposed` ADR is a question on record, not a commitment.

<!-- sf:begin(product) -->
### Product ops

This KB carries its product layer as **spec pages, never application code**. Real
software lives in separate repos (grown from the sporeforge template) that read
this KB over MCP.

- **Roadmap upkeep**: `roadmap.md` holds Next / Later only — no Done section.
  Remove items when they ship (the log and git history are the record); promote
  Later items to Next as they become active. `Home.md` is the dashboard — keep
  its links current.
- **Embedded-prompt convention**: each external software artifact gets one page in
  `product/software/` containing the full build prompt (a fenced block ready to
  paste into a coding agent) plus a link to the resulting repo. The prompt *is*
  the spec; keep it current as decisions change. See the example page in
  `product/software/`. Product decisions use the Decision workflow above.
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

## Version control

Content work (`ingest | query | lint | decision | discovered`) commits straight to
`main`, one commit per workflow run, with the log prefix as the commit prefix
(`ingest: <source>`). At session start, if `git status` shows uncommitted changes
under `wiki/`, tell the user and commit them on their own as `hand-edit: <pages>`
before the workflow run, so the user's edits keep their own time and author. Schema, tooling, and skill changes go on a branch and open a
draft PR whose body comes from the `pr` skill; Evidence is the `scripts/lint.py` output,
plus `.template/verify_matrix.sh` output while `.template/` still exists (onboarding
deletes it). Merge only on the user's explicit approval.

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
- Skills copied from mattpocock/skills are listed in `.agents/skills/VENDORED.md`
  with the pinned upstream commit; `/sync-skills` owns them, `/sync-upstream` owns
  everything else vendored from the template.
- All per-instance data (lint terms, link allowlists, glossaries, children) lives
  in `kb.toml`, **never hard-coded in Python** — that's what keeps the vendored
  code byte-identical across instances and lets `/sync-upstream` port template
  updates.
