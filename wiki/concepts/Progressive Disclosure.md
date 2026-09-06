---
type: concept
created: 2026-09-06
updated: 2026-09-06
sources:
  - "[[2026-09-06 The AI Daily Brief - How to Build an AI-Native Company Today]]"
raw:
  - raw/podcasts/2026-09-06 The AI Daily Brief - How to Build an AI-Native Company Today.md
related:
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
