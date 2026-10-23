---
type: concept
created: 2026-09-06
updated: 2026-10-23
sources:
  - "[[2026-09-06 The AI Daily Brief - How to Build an AI-Native Company Today]]"
  - "[[2026-08-27 WikiSkill - Compiling Agent Experience into Persistent Knowledge for Skill Evolution]]"
raw:
  - raw/podcasts/2026-09-06 The AI Daily Brief - How to Build an AI-Native Company Today.md
  - raw/papers/2026-08-27 WikiSkill - Compiling Agent Experience into Persistent Knowledge for Skill Evolution.md
related:
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
[[Why LLM Wikis Beat RAG]] for why compiling at ingest is what makes the
metadata trustworthy enough to route on.

## The payoff, measured once

[[Skill Evolution]] gives the first number. Because WikiSkill's proposer
reads the index first and opens pages and traces only as needed, its
optimizer cost per iteration is one maintainer call plus 10–20 ReAct turns,
independent of how many training traces exist; the three baselines it beats
all scale linearly with the training set because they read every trace or
every minibatch ([[2026-08-27 WikiSkill - Compiling Agent Experience into Persistent Knowledge for Skill Evolution]]). That is the [[Token Efficiency]] argument for
metadata-first reading with a cost model attached, though at wiki sizes of
4–10 pages.
