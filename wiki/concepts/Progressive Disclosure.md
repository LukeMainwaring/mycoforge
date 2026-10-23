---
type: concept
created: 2026-09-06
updated: 2026-10-23
sources:
  - "[[2026-09-06 The AI Daily Brief - How to Build an AI-Native Company Today]]"
  - "[[2026-08-27 WikiSkill - Compiling Agent Experience into Persistent Knowledge for Skill Evolution]]"
  - "[[2026-10-22 ar9av obsidian-wiki (repo)]]"
raw:
  - raw/podcasts/2026-09-06 The AI Daily Brief - How to Build an AI-Native Company Today.md
  - raw/papers/2026-08-27 WikiSkill - Compiling Agent Experience into Persistent Knowledge for Skill Evolution.md
  - raw/articles/2026-10-22 ar9av obsidian-wiki (repo).md
related:
  - "[[Provenance Tags]]"
  - "[[Skill Evolution]]"
  - "[[Token Efficiency]]"
  - "[[Company Brain]]"
  - "[[Three-Layer Architecture]]"
  - "[[Why LLM Wikis Beat RAG]]"
  - "[[Organizational Legibility]]"
  - "[[AI-Native SDLC]]"
confidence: medium
tags: [ai-native, knowledge-capture, architecture]
---

# Progressive Disclosure

Organize a company's knowledge so an agent loads only the slice it needs.
[[Alex Lieberman]]'s feature 12: "use CLI tools to parse metadata in markdown
files and traverse dependency relationships, allowing agents to be precise
about input token usage." The host names the pattern: an
information-architecture idea "where complexity is unpacked gradually and in
sequence in order to not create too much context overhead when an agent is
working" — [[2026-09-06 The AI Daily Brief - How to Build an AI-Native Company Today]].

> [!claim] Knowledge files need machine-readable metadata at the top so an agent can judge relevance without reading the body
> confidence: medium · status: supported
> evidence: "making sure that the metadata that an agent can reference to
> understand whether something is useful is right there at the top of
> knowledge files that it has access to so that it doesn't waste context
> window on things it doesn't need" — [[2026-09-06 The AI Daily Brief - How to Build an AI-Native Company Today]].
> The host singles this out as the one feature on the list granular enough to
> "actually do things differently." Same reasoning as the under-a-page rule
> for `CLAUDE.md` in the [[AI-Native SDLC]] playbook ("anything stale is
> taking up context for no benefit"), from the loading side rather than the
> writing side. Prescription, no cases.
> First non-practitioner source: WikiSkill's maintainer prompt requires each
> `index.md` entry to give "PROBLEM + ROOT CAUSE + FIX in one or two
> sentence[s]… specific enough that an agent can judge relevance without
> reading the full page", and its skill proposer is given the index, not the
> wiki — [[2026-08-27 WikiSkill - Compiling Agent Experience into Persistent Knowledge for Skill Evolution]]. The paper also cites progressive disclosure as a property
> of the skill format itself. Asserted in a prompt and a citation, not
> ablated, so confidence stays medium.

It is the [[Token Efficiency]] mechanism that touches the [[Company Brain]]
directly: the brain has to be shaped for partial reads, not just accumulated.
The diarization rule in [[Organizational Legibility]] (synthesize recordings
down because a context window can't hold an org's history) is the same
constraint applied at capture time.

## This KB is one

MycoForge is built on exactly this pattern, and the source was not describing
it. Every page opens with frontmatter (`type`, `sources`, `related`,
`confidence`, `tags`) that an agent reads before the body; `index.md` is one
line per page and is read first on every query, so drilling into a page is a
choice; wikilinks and `related:` are the dependency graph the agent traverses;
the MCP server's `search_kb` / `read_page` / `get_index` split is the
CLI-tools half. The [[Three-Layer Architecture]] gives the metadata a place to
live that the source's flat "markdown files" does not. See
[[Why LLM Wikis Beat RAG]] for the compile-at-ingest argument the routing
rests on.

## The index is for routing, not for reasoning

obsidian-wiki's one measurement ([[2026-10-22 ar9av obsidian-wiki (repo)]])
asks structural questions of a 38-page vault ("how is X connected to Y",
"which pages hold my vault together") with and without its CLI. The CLI
answered in 19 seconds against 81, with 83% correct against 44%, at the same
API cost. The accuracy gap had one cause the authors name: the plain agent
"routed through `index.md` — which links to *every* page, so it 'found' a
short path that means nothing", and named `index` as a most-important page.

> [!claim] Bookkeeping files must be excluded from the link graph: an index that links every page makes every path two hops long and every centrality score meaningless
> confidence: medium · status: supported
> evidence: the misrouting above, repeated in both plain-agent runs; "the
> graph the skills query excludes bookkeeping files, so that answer isn't
> reachable" — [[2026-10-22 ar9av obsidian-wiki (repo)]]. Ground truth from
> networkx. Small study: n=2 per cell, one vault, one model (Claude Sonnet),
> and one "with" run failed because the model ignored the CLI. The wall-clock
> gap is well outside the run-to-run spread; the accuracy figures rest on
> fewer samples.

For this KB the rule is already half true: `index.md` and `log.md` are read
first and never counted as `related:`. Anything that walks wikilinks here,
`/connect` above all, should skip them, and the MCP server's `get_index`
exists so a reader never has to.

## The payoff, measured once

[[Skill Evolution]] gives the first number. Because WikiSkill's proposer
reads the index first and opens pages and traces only as needed, its
optimizer cost per iteration is one maintainer call plus 10–20 ReAct turns,
independent of how many training traces exist; the three baselines it beats
all scale linearly with the training set because they read every trace or
every minibatch ([[2026-08-27 WikiSkill - Compiling Agent Experience into Persistent Knowledge for Skill Evolution]]). That is the [[Token Efficiency]] argument for
metadata-first reading with a cost model attached, though at wiki sizes of
4–10 pages.
