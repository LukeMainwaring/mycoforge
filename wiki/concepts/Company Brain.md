---
type: concept
created: 2026-07-23
updated: 2026-10-23
sources:
  - "[[2026-05-21 Y Combinator - How to Build a Self-Improving Company with AI]]"
  - "[[2026-05-06 The Founders Playbook (Anthropic)]]"
  - "[[2026-08-20 The Claude Code Guide For Startups]]"
  - "[[2026-08-21 The AI-Native SDLC Playbook (Anthropic)]]"
  - "[[2026-09-06 The AI Daily Brief - How to Build an AI-Native Company Today]]"
  - "[[2026-10-15 gbrain Belief Ledger Design (Garry Tan)]]"
raw:
  - raw/podcasts/2026-05-21 Y Combinator - How to Build a Self-Improving Company with AI.md
  - raw/articles/2026-05-06 The Founders Playbook (Anthropic).pdf
  - raw/articles/2026-08-20 The Claude Code Guide For Startups.pdf
  - raw/articles/2026-08-21 The AI-Native SDLC Playbook (Anthropic).md
  - raw/podcasts/2026-09-06 The AI Daily Brief - How to Build an AI-Native Company Today.md
  - raw/articles/2026-10-15 gbrain Belief Ledger Design (Garry Tan).md
related:
  - "[[AI-Native Company]]"
  - "[[Organizational Legibility]]"
  - "[[Three-Layer Architecture]]"
  - "[[Build for Rebuilding]]"
  - "[[Everyone Ships]]"
  - "[[AI-Native SDLC]]"
  - "[[Advisory and Deterministic Controls]]"
  - "[[Progressive Disclosure]]"
  - "[[Token Efficiency]]"
  - "[[Belief Ledger]]"
confidence: medium
tags: [ai-native, knowledge-capture]
---

# Company Brain

[[Tom Blomfield]]'s name for the durable center of an [[AI-Native Company]]: all
the data, emails, DMs, skills, and know-how — the extracted domain knowledge
that defines how the company works — with humans arranged **around the edge**,
where the intelligence makes contact with reality.

> [!claim] Business context and skills are the durable asset; software on top is ephemeral
> confidence: medium · status: supported
> evidence: "very preciously store all the data… treat the software as ephemeral.
> The models get smarter in a month or two — throw the software away, give it
> your original set of instructions, and regenerate it" — [[2026-05-21 Y Combinator - How to Build a Self-Improving Company with AI]].
> Internal dashboards and workflow tools become on-demand, one-shot,
> regenerable; the instructions that produce them are what you keep. See
> [[AI Software Factory]] for the same inversion applied to product code.
> Practitioner corroboration: Clay's "build it four times" and Harvey's
> per-model-wave re-architecture — [[Build for Rebuilding]].

## From efficiency asset to moat

[[2026-05-06 The Founders Playbook (Anthropic)]] corroborates the pattern from
the vendor side and extends it: "investing in persistent context from day one
is what keeps AI a force multiplier instead of a source of entropy."

> [!claim] Accumulated AI context compounds into a defensible moat
> confidence: medium · status: supported
> evidence: domain expertise externalized into structured context and skills
> becomes "a proprietary knowledge substrate that no generalist AI can match";
> compounding user-behavior data is "time-locked, context-specific, and
> impossible for a copycat to recreate" — [[2026-05-06 The Founders Playbook (Anthropic)]].
> Vendor prescription, no independent case data yet — but note it inverts the
> usual moat story: the durable asset is the context layer, not the software
> (Blomfield's ephemeral-software point, above, from the other direction).
> Practitioner echoes in [[2026-08-20 The Claude Code Guide For Startups]]:
> "the moat for any company right now is that it needs to be self-improving…
> the more you use this, the more we know who your best customers are"
> ([[Kareem Amin]], Clay); "structure your codebase, knowledge base, and team
> the right way, and every contribution compounds" (Dan Shiebler, Artemis
> Security). Still vendor-collected; held at medium.

## One layer or a mesh

> [!claim] Large organizations get a mesh of sources of truth that agents traverse and reconcile, not one intelligence layer
> confidence: low · status: contested
> evidence: [[Alex Lieberman]]'s feature 3, which commenters called
> load-bearing for the rest of his list: "build one intelligence layer to
> aggregate structured and unstructured data, documents, and business logic
> into a single source of truth that is queryable and that agentic work can
> be built on top of." The host's dissent: "I kind of like the metaphor of a
> mesh or lattice rather than a single layer… sources of truth that can
> interface with one another and that agents can traverse, perhaps even
> uncovering and trying to reconcile with human support differences in
> sources of truth" — [[2026-09-06 The AI Daily Brief - How to Build an AI-Native Company Today]].
> Both agree on the substance (organizing context for agents is "a major
> discipline"); the disagreement is topology at scale. The
> [[AI-Native SDLC]] playbook's "for every artifact, name one source of
> truth" with linkage as the minimum bar is the mesh position stated as
> policy. Two opinions, no cases; low.

Lieberman's feature 5 restates the durable-asset claim above as a mindset,
**context as code**: keep architecture documents and conventions updated and
make "diligent upfront planning part of the operating discipline," treating
context "not just as the background info that is required, but as the actual
foundations upon which agents are building." Feature 7 is the distribution
half: "organizations will distribute skills, not just prompts," a skills
distribution system that manages agent behavior org-wide, which the host
reads as "the discipline of agent management coming to the fore." Both are
the enterprise skills play below, said by a non-Anthropic source. The brain
also has to be *shaped* for agents, not just filled: metadata at the top of
every file so an agent loads only what it needs ([[Progressive Disclosure]],
the [[Token Efficiency]] side of the brain).

## What a practitioner's brain looks like

The startup guide shows the substrate: markdown in a repo. Emergent keeps "a
GitHub repo of Claude Code skills which works as a shared knowledge base to
quickly bootstrap a Claude Code session" — database and warehouse locations,
schema, company context — and a new hire's day-one setup doc that Claude
updates when it finds something broken. Its tolerance rule: "it is ok to live
with slightly outdated context files as long as the agent can quickly verify
and course correct." Translucent runs an internal marketplace of agents
organized by role; Anthropic keeps Claude Tag's standing on-call instructions
as skills in a repo "so multiple teammates can iterate on them." All of these
are the shared-skills mechanism in [[Everyone Ships]], and the same substrate
as this KB.

The enterprise prescription in [[2026-08-21 The AI-Native SDLC Playbook (Anthropic)]]
is the same substrate with owners attached. `CLAUDE.md` is what "used to
sit in people's heads and on wikis" turned into a file read at the start of
every session, with a working rule — "When Claude makes a mistake twice, the
correction goes into `CLAUDE.md`" — and a size rule: under a page, because
"anything stale is taking up context for no benefit." Skills are "how an
organization makes its institutional knowledge operational": one policy,
one named owner, one written source of truth, distributed org-wide through
plugins, with the rule of thumb to write a skill for knowledge that must be
applied consistently and leave the rest to `CLAUDE.md` or the prompt.
Incident post-mortems go to "a version-controlled lessons file that future
investigations can read." Note the tension with Zingage's 567-line
`CLAUDE.md` ([[Verification Bottleneck]]): the playbook would push most of
that into skills. How much of the brain the agent is *forced* to obey is
the subject of [[Advisory and Deterministic Controls]]; the full artifact
chain is in [[AI-Native SDLC]].

## A brain that knows when it knew

The first implementation on this KB's shelf that is not markdown:
[[Garry Tan]]'s gbrain, an agent memory layer built as a database with
facts, takes, typed links, trust tiers and purge. Its [[Belief Ledger]]
([[2026-10-15 gbrain Belief Ledger Design (Garry Tan)]]) adds what none of the
brains above have: a certified record of *when the brain came to believe
each thing*, kept apart from when the thing was true, with a weekly diff of
beliefs that changed, each cited to its evidence. Two rules carry back to any
brain. Trust is a property of each write, and a low-trust write that would
overwrite a high-trust belief is held for the owner rather than refused or
applied. And the brain discloses its own coverage: a question about a time
it was not recording gets a coded refusal, not a reconstruction. Blomfield's
"software is ephemeral" holds here too, in a stricter form: the ledger is one
of the few stores gbrain declares non-recomputable, and it gets a backup
contract for that reason.

## Where humans still matter

Humans reach where models can't: novel situations, ethical considerations,
high-stakes and high-emotion moments (the co-founder-breakup conversation),
in-person contexts like conferences — and sales, which Blomfield puts at "a
human being in the room for the next 20 years."

The structural rhyme with this KB: the brain/edge split mirrors the
[[Three-Layer Architecture]] — durable curated knowledge at the center
(`raw/` + wiki), regenerable consumers at the edge (product repos reading over
MCP). A MycoForge instance is a candidate implementation of a company brain;
noted here as an observation, not yet a filed synthesis.
The center/edge seam is decided in [[ADR-001 Separate Repo with Product as Seam]].
